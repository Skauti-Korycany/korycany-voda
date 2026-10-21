# -*- coding: utf-8 -*-
"""10_parcely.py - katastrální parcely (INSPIRE CP, ČÚZK, CC BY 4.0) pro území modelu.

Co dělá:
 1. stáhne Atom feed https://atom.cuzk.gov.cz/CP/CP.xml a najde kódy katastrálních území podle názvu,
 2. stáhne GML každého k.ú. (services.cuzk.gov.cz/gml/inspire/cp/epsg-5514/{kod}.zip), rozbalí, naparsuje
    (xml.etree, bez geopandas): obrys, výměra, parcelní číslo (label), k.ú.,
 3. ořízne na území modelu (data/povodi.geojson, typ uzemi_modelu) - parcela zůstane, když má těžiště
    nebo aspoň jeden vrchol uvnitř,
 4. ke každé parcele spočítá budovy z data/budovy.geojson (těžiště budovy v parcele): počet a plocha půdorysů,
 5. zapíše data/parcely.geojson (WGS84, 6 des. míst), data/parcely_info.json, docs/img/parcely_nahled.png.

Vlastnosti parcely: ku (název k.ú.), ku_kod, cislo (parcelní číslo, veřejný identifikátor pozemku),
vymera_m2 (z katastru), plocha_m2 (z obrysu), strechy_m2, budov, povodi_id.
ZÁMĚRNĚ BEZ vlastníků, LV a adres (pravidlo projektu). Parcelní číslo není osobní údaj - osobním se stává
až spojením s vlastníkem, které tu neděláme.

Vstupy stažené skriptem zůstávají v data/cp/ (mimo git).
"""
import io, json, os, re, sys, time, zipfile
import urllib.request
import xml.etree.ElementTree as ET
import numpy as np

KU_NAZVY = ["Koryčany", "Jestřabice", "Blišice", "Lískovec", "Mouchnice"]   # ve feedu CUZK je k.u. Liskovce u Korycan jen "Lískovec" [684881] (overeno 20. 10. 2026); orez na uzemi modelu vyradi pripadne cizi
ATOM = "https://atom.cuzk.gov.cz/CP/CP.xml"
GML_URL = "https://services.cuzk.gov.cz/gml/inspire/cp/epsg-5514/{kod}.zip"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RAW = os.path.join(DATA, "cp")
os.makedirs(RAW, exist_ok=True)
os.makedirs(os.path.join(ROOT, "docs", "img"), exist_ok=True)


def log(*a):
    print(*a, flush=True)


def stahni(url, cil):
    if os.path.exists(cil) and os.path.getsize(cil) > 0:
        return cil
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "korycany-voda/0.1 (skautsky oddil Korycany)"})
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
            with open(cil, "wb") as f:
                f.write(data)
            return cil
        except Exception as e:  # noqa
            log(f"  chyba {e} u {url}, pokus {i + 1}")
            time.sleep(3)
    return None


def local(tag):
    return tag.split("}", 1)[1] if "}" in tag else tag


def ring_area_centroid(xy):
    x = xy[:, 0]; y = xy[:, 1]
    cross = x * np.roll(y, -1) - np.roll(x, -1) * y
    a = 0.5 * cross.sum()
    if abs(a) < 1e-9:
        return 0.0, xy.mean(axis=0)
    cx = ((x + np.roll(x, -1)) * cross).sum() / (6 * a)
    cy = ((y + np.roll(y, -1)) * cross).sum() / (6 * a)
    return abs(a), np.array([cx, cy])


def poslist(el):
    v = np.array(el.text.split(), float)
    return v.reshape(-1, 2) if len(v) >= 8 else None


def cti_parcely(gml_path, ku_nazev, ku_kod):
    """Namespace-agnostický parser INSPIRE CP: hledá prvky CadastralParcel, v nich exterior/interior posList,
    areaValue, label, nationalCadastralReference."""
    out = []
    prvni = None
    for ev, el in ET.iterparse(gml_path, events=("end",)):
        if local(el.tag) != "CadastralParcel":
            continue
        if prvni is None:
            prvni = sorted({local(x.tag) for x in el.iter()})
        ext, holes, area_v, label, ref = None, [], None, None, None
        stack_mode = None
        for x in el.iter():
            t = local(x.tag)
            if t == "exterior":
                stack_mode = "ext"
            elif t == "interior":
                stack_mode = "int"
            elif t == "posList" and x.text:
                v = poslist(x)
                if v is None:
                    continue
                if stack_mode == "int":
                    holes.append(v)
                elif ext is None:
                    ext = v
            elif t == "areaValue" and x.text:
                try:
                    area_v = float(x.text)
                except ValueError:
                    pass
            elif t == "label" and x.text and label is None:
                label = x.text.strip()
            elif t == "nationalCadastralReference" and x.text:
                ref = x.text.strip()
        if ext is not None:
            a, c = ring_area_centroid(ext)
            for h in holes:
                a -= ring_area_centroid(h)[0]
            out.append({"ring": ext, "holes": holes, "plocha_m2": float(a), "vymera_m2": area_v, "cislo": label or ref or "",
                        "ref": ref, "ku": ku_nazev, "ku_kod": ku_kod, "c": c})
        el.clear()
    if not out:
        log(f"  !!! v {gml_path} žádný CadastralParcel; první prvek obsahoval: {prvni}")
    return out


def main():
    from pyproj import Transformer
    from matplotlib.path import Path
    import rasterio

    # 1. kódy k.ú. z Atom feedu
    log("1) Atom feed CP - kódy k.ú.")
    atom = stahni(ATOM, os.path.join(RAW, "CP.xml"))
    if not atom:
        sys.exit("Atom feed se nepodařilo stáhnout (atom.cuzk.gov.cz) - zkontroluj připojení")
    txt = open(atom, encoding="utf-8", errors="replace").read()
    kody = {}
    for n in KU_NAZVY:
        m = re.search(r"katastrální území:\s*" + re.escape(n) + r"\s*\[(\d+)\]", txt)
        if m:
            kody[n] = m.group(1)
            log(f"   {n} [{m.group(1)}]")
        else:
            log(f"   {n}: ve feedu nenalezeno (zkontroluj název)")
    if not kody:
        sys.exit("Žádné k.ú. nenalezeno")

    # 2. GML
    log("2) Stahuji a parsuji GML")
    parcely = []
    for n, kod in kody.items():
        z = stahni(GML_URL.format(kod=kod), os.path.join(RAW, f"{kod}.zip"))
        if not z:
            log(f"   {n}: zip se nepodařilo stáhnout")
            continue
        with zipfile.ZipFile(z) as zf:
            names = [x for x in zf.namelist() if x.lower().endswith((".xml", ".gml"))]
            if not names:
                log(f"   {n}: v zipu není XML/GML: {zf.namelist()}")
                continue
            gml = os.path.join(RAW, f"{kod}.xml")
            if not os.path.exists(gml):
                with open(gml, "wb") as f:
                    f.write(zf.read(names[0]))
        p = cti_parcely(gml, n, kod)
        log(f"   {n}: {len(p)} parcel")
        parcely.extend(p)

    # 3. ořez
    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    to_wgs = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
    gj = json.load(open(os.path.join(DATA, "povodi.geojson"), encoding="utf-8"))
    feat = next(f for f in gj["features"] if f["properties"].get("typ") == "uzemi_modelu")
    uz = Path(np.array([to5514.transform(x, y) for x, y in feat["geometry"]["coordinates"][0]]))
    keep = []
    for p in parcely:
        if uz.contains_point(p["c"]) or uz.contains_points(p["ring"]).any():
            keep.append(p)
    log(f"3) v území modelu: {len(keep)} z {len(parcely)} parcel")

    # povodí id
    pid = rasterio.open(os.path.join(DATA, "dmr", "povodi_id.tif")) if os.path.exists(os.path.join(DATA, "dmr", "povodi_id.tif")) else None
    if pid:
        vals = list(pid.sample([(p["c"][0], p["c"][1]) for p in keep]))
        for p, v in zip(keep, vals):
            p["povodi_id"] = int(v[0]) if v[0] != pid.nodata else 0

    # 4. budovy v parcele
    log("4) budovy v parcelách")
    bud = json.load(open(os.path.join(DATA, "budovy.geojson"), encoding="utf-8"))
    bc = []
    for f in bud["features"]:
        ring = np.array([to5514.transform(x, y) for x, y in f["geometry"]["coordinates"][0]])
        bc.append((ring_area_centroid(ring)[1], float(f["properties"].get("plocha_m2") or ring_area_centroid(ring)[0]), f["properties"].get("ucel", "")))
    bxy = np.array([c for c, _, _ in bc])
    for p in keep:
        p["budov"] = 0; p["strechy_m2"] = 0.0; p["rd"] = 0
        xmin, ymin = p["ring"].min(axis=0); xmax, ymax = p["ring"].max(axis=0)
        cand = np.where((bxy[:, 0] >= xmin) & (bxy[:, 0] <= xmax) & (bxy[:, 1] >= ymin) & (bxy[:, 1] <= ymax))[0]
        if not len(cand):
            continue
        path = Path(p["ring"])
        inside = path.contains_points(bxy[cand])
        for k, ok in zip(cand, inside):
            if ok:
                p["budov"] += 1; p["strechy_m2"] += bc[k][1]
                if bc[k][2] == "rodinný dům":
                    p["rd"] += 1

    # 5. zápis
    feats = []
    for p in keep:
        rings = [p["ring"]] + p["holes"]
        coords = []
        for r in rings:
            lon, lat = to_wgs.transform(r[:, 0], r[:, 1])
            cc = [[round(float(a), 6), round(float(b), 6)] for a, b in zip(lon, lat)]
            if cc[0] != cc[-1]:
                cc.append(cc[0])
            coords.append(cc)
        feats.append({"type": "Feature", "properties": {
            "ku": p["ku"], "ku_kod": p["ku_kod"], "cislo": p["cislo"], "vymera_m2": p["vymera_m2"], "plocha_m2": round(p["plocha_m2"], 1),
            "budov": p["budov"], "rd": p["rd"], "strechy_m2": round(p["strechy_m2"], 1), "povodi_id": p.get("povodi_id", 0)},
            "geometry": {"type": "Polygon", "coordinates": coords}})
    out = {"type": "FeatureCollection", "name": "parcely",
           "zdroj": "ČÚZK, INSPIRE Katastrální parcely (CP), CC BY 4.0; stav podle Atom feedu v den stažení; skript tools/10_parcely.py",
           "stazeno": time.strftime("%Y-%m-%d"), "pozn": "bez vlastníků, LV a adres; budovy = INSPIRE BU (těžiště v parcele)",
           "features": feats}
    with open(os.path.join(DATA, "parcely.geojson"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    s_ku = {}
    for p in keep:
        d = s_ku.setdefault(p["ku"], {"kod": p["ku_kod"], "parcel": 0, "plocha_ha": 0.0, "s_budovou": 0, "s_rd": 0})
        d["parcel"] += 1; d["plocha_ha"] += p["plocha_m2"] / 1e4; d["s_budovou"] += p["budov"] > 0; d["s_rd"] += p["rd"] > 0
    for d in s_ku.values():
        d["plocha_ha"] = round(d["plocha_ha"], 1)
    rd_parc = [p for p in keep if p["rd"] > 0]
    info = {"zdroj": out["zdroj"], "stazeno": out["stazeno"], "ku": s_ku, "parcel_celkem": len(keep),
            "parcel_s_rd": len(rd_parc),
            "parcela_s_rd_median_m2": float(np.median([p["plocha_m2"] for p in rd_parc])) if rd_parc else None,
            "strechy_na_parcele_s_rd_median_m2": float(np.median([p["strechy_m2"] for p in rd_parc])) if rd_parc else None,
            "velikost_souboru_MB": round(os.path.getsize(os.path.join(DATA, "parcely.geojson")) / 1e6, 2)}
    with open(os.path.join(DATA, "parcely_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    log("5) zapsáno data/parcely.geojson, data/parcely_info.json:", json.dumps(info, ensure_ascii=False))

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.collections import PolyCollection
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.add_collection(PolyCollection([p["ring"] for p in keep], facecolors="none", edgecolors="#777", linewidths=0.2))
        ax.add_collection(PolyCollection([p["ring"] for p in rd_parc], facecolors="#f4c27a", edgecolors="none"))
        ax.plot(*uz.vertices.T, color="#1f6f8b", lw=1)
        ax.set_aspect("equal"); ax.autoscale(); ax.set_title(f"Parcely v území modelu: {len(keep)} (oranžově s rodinným domem: {len(rd_parc)})")
        fig.tight_layout(); fig.savefig(os.path.join(ROOT, "docs", "img", "parcely_nahled.png"), dpi=130)
        log("   náhled docs/img/parcely_nahled.png")
    except Exception as e:  # noqa
        log("   náhled se nepovedl:", e)


if __name__ == "__main__":
    main()
    print("\nHOTOVO.")
