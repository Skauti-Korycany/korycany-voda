# -*- coding: utf-8 -*-
"""05_hsp.py - hydrologické skupiny půd (HSP A-D) pro území modelu -> data/dmr/hsp.tif

NÁHRADNÍ CESTA (dokud nepřijdou data VÚMOP): BPEJ z otevřeného WFS SPÚ -> HPJ (2. a 3. číslice kódu BPEJ)
-> HSP podle Janeček a kol. 2012, tab. 2.2 (orientační přiřazení). Plochy bez BPEJ (lesy, intravilán, voda)
se doplní hodnotou NEJBLIŽŠÍ bonitované plochy (stejný geologický podklad) a označí jako odhad.

Data VÚMOP (od 27. 10. 2026): vektor HSP 2026 (data/vumop/HSP_Korycany.gpkg, vrstva HSP_2026, atribut HSP A-D,
EPSG:5514, území obce + 500 m; licence CC BY-NC, uvádět „VÚMOP, v.v.i.“; v gitu NENÍ). Když soubor existuje,
použije se automaticky (nebo --vumop <soubor>, --bez-vumop pro starou cestu). VÚMOP má přednost před BPEJ,
do hsp_zdroj.tif jde kód 3. Dvojí skupina „B/D“ (odvodněno / neodvodněno, TR-55) = D, protože odvodnění neznáme.
Plochy bez hodnoty dostanou BPEJ, jinak nejbližší hodnotu (odhad). Navazující 06_cn.py nic nepozná - čte jen hsp.tif.

Použití:  python tools/05_hsp.py [--bez-stahovani] [--vumop cesta | --bez-vumop]

Vstup:  WFS SPÚ https://geoportal.spucr.cz/api/open-data/wfs/wfs_bpej (WFS 1.0.0, GML2, EPSG:5514, Fees none,
        AccessConstraints none; ověřeno 19. 10. 2026), vrstva ft_pudniJednotka, atribut at_pudniJednotka_kodBpej.
Výstupy: data/dmr/hsp.tif         uint8 1=A 2=B 3=C 4=D, 0=NoData (stejná mřížka jako DEM)
         data/dmr/hsp_zdroj.tif   uint8 1=BPEJ přímo, 2=doplněno nejbližší BPEJ (odhad), 3=VÚMOP, 0=nic
         data/dmr/hpj.tif         uint8 HPJ 1-78 (0 = bez BPEJ) - pro K faktor USLE později
         data/hsp_info.json       plochy A-D v území modelu, podíl odhadu, četnost HPJ, zdroje
         data/bpej.geojson        polygony BPEJ v bboxu (WGS84; kód BPEJ, HPJ, HSP, třída ochrany) pro mapu
         data/hsp_nahled.png
Závislosti: numpy, scipy, rasterio, pyproj, matplotlib (stdlib: urllib, re, json).
"""
import argparse, json, os, re, sys, time, urllib.request
import numpy as np

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

WFS = "https://geoportal.spucr.cz/api/open-data/wfs/wfs_bpej"
# Janeček a kol. 2012, tab. 2.2 "Hydrologické skupiny zemědělských půd podle BPEJ, resp. HPJ" (ověřeno 19. 10. 2026)
HPJ_HSP = {}
for h in (4, 5, 17, 21, 31, 32, 55): HPJ_HSP[h] = 1
for h in (1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 22, 24, 25, 26, 27, 28, 29, 30, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 56, 60): HPJ_HSP[h] = 2
for h in (3, 6, 23, 39, 44, 45, 46, 47, 48, 50, 51, 52, 57, 58, 62, 64, 65, 75, 77, 78): HPJ_HSP[h] = 3
for h in (7, 20, 49, 53, 54, 59, 61, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76): HPJ_HSP[h] = 4
assert len(HPJ_HSP) == 78
HSP_PISM = {1: "A", 2: "B", 3: "C", 4: "D"}

def fetch_bpej(bbox, out_path):
    url = WFS + "?service=WFS&version=1.0.0&request=GetFeature&typeName=ft_pudniJednotka&outputFormat=GML2&bbox={},{},{},{}".format(*bbox)
    req = urllib.request.Request(url, headers={"User-Agent": "korycany-voda/1.0 (skauti; nekomercni)"})
    for pokus in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                txt = r.read().decode("utf-8")
            break
        except Exception as e:
            if pokus == 2: raise
            log(f"   chyba {e}, zkouším znovu"); time.sleep(3)
    if "ServiceException" in txt[:500]:
        sys.exit("WFS SPÚ vrátil chybu: " + txt[:300])
    with open(out_path, "w", encoding="utf-8") as f: f.write(txt)
    return txt

def parse_gml2(txt):
    """Vrací list prvků: {kod, hpj, trida, vymera, polys: [[outer, [inner...]]]} v EPSG:5514."""
    feats = []
    for m in re.finditer(r"<ber:ft_pudniJednotka\b.*?</ber:ft_pudniJednotka>", txt, re.S):
        f = m.group(0)
        kod = re.search(r"kodBpej>(\d+)<", f); kodt = re.search(r"kodText>([^<]+)<", f)
        tr = re.search(r"tridaOchrany>([^<]*)<", f); vym = re.search(r"vymera>([^<]*)<", f)
        if not kod: continue
        k = kod.group(1).zfill(5)
        hpj = int(k[1:3])
        polys = []
        for pm in re.finditer(r"<gml:Polygon>(.*?)</gml:Polygon>", f, re.S):
            p = pm.group(1)
            def ring(s):
                pts = [tuple(map(float, c.split(","))) for c in s.strip().split()]
                if pts and pts[0] != pts[-1]: pts.append(pts[0])
                return pts
            outer = re.search(r"<gml:outerBoundaryIs>.*?<gml:coordinates>(.*?)</gml:coordinates>", p, re.S)
            inners = re.findall(r"<gml:innerBoundaryIs>.*?<gml:coordinates>(.*?)</gml:coordinates>", p, re.S)
            if outer:
                polys.append([ring(outer.group(1))] + [ring(i) for i in inners])
        feats.append({"kod": k, "kod_text": kodt.group(1) if kodt else k, "hpj": hpj, "hsp": HPJ_HSP.get(hpj, 0),
                      "trida_ochrany": tr.group(1) if tr else "", "vymera_m2": float(vym.group(1)) if vym and vym.group(1) else None,
                      "polys": polys})
    return feats

# ---- čtení GeoPackage bez GDAL (sqlite3 + WKB), stačí pro polygony VÚMOP
import sqlite3, struct

def _wkb(b, o=0):
    end = '<' if b[o] == 1 else '>'; o += 1
    t, = struct.unpack(end + 'I', b[o:o+4]); o += 4
    has_z = (t & 0x80000000) or (1000 <= t % 10000 < 2000) or (3000 <= t % 10000 < 4000)
    has_m = (t & 0x40000000) or (2000 <= t % 10000 < 4000)
    base = (t & 0x0FFFFFFF) % 1000
    dim = 2 + (1 if has_z else 0) + (1 if has_m else 0)
    def ring(o):
        n, = struct.unpack(end + 'I', b[o:o+4]); o += 4
        pts = []
        for _ in range(n):
            v = struct.unpack(end + 'd' * dim, b[o:o+8*dim]); o += 8 * dim
            pts.append((v[0], v[1]))
        return pts, o
    if base == 3:
        nr, = struct.unpack(end + 'I', b[o:o+4]); o += 4
        poly = []
        for _ in range(nr):
            r, o = ring(o); poly.append(r)
        return [poly], o
    if base == 6:
        np_, = struct.unpack(end + 'I', b[o:o+4]); o += 4
        out = []
        for _ in range(np_):
            p, o = _wkb(b, o); out += p
        return out, o
    raise ValueError(f"nepodporovaný typ geometrie {t}")

def gpkg_geom(blob):
    if blob is None: return []
    assert blob[:2] == b'GP', "není GPKG geometrie"
    flags = blob[3]; env = (flags >> 1) & 7
    off = 8 + {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[env]
    polys, _ = _wkb(blob, off)
    return polys

def cti_gpkg(path, vrstva=None):
    c = sqlite3.connect(path)
    if vrstva is None:
        vrstva = c.execute("select table_name from gpkg_contents where data_type='features'").fetchone()[0]
    gcol, srs = c.execute("select column_name, srs_id from gpkg_geometry_columns where table_name=?", (vrstva,)).fetchone()
    cols = [r[1] for r in c.execute(f"pragma table_info('{vrstva}')")]
    out = []
    for row in c.execute(f"select * from '{vrstva}'"):
        d = dict(zip(cols, row)); g = d.pop(gcol)
        out.append((d, gpkg_geom(g)))
    c.close()
    return out, srs, vrstva

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bez-stahovani", action="store_true")
    ap.add_argument("--vumop", default=None, help="cesta k datům VÚMOP (GPKG nebo GeoJSON s atributem HSP, nebo GeoTIFF 1-4); výchozí data/vumop/HSP_Korycany.gpkg, když existuje")
    ap.add_argument("--bez-vumop", action="store_true", help="nepoužít data VÚMOP ani když existují (stará cesta jen z BPEJ)")
    ap.add_argument("--buffer", type=float, default=300.0)
    a = ap.parse_args()
    import rasterio
    from rasterio.features import rasterize
    from scipy.ndimage import distance_transform_edt
    from pyproj import Transformer
    from matplotlib.path import Path

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data"); raw = os.path.join(data, "bpej"); os.makedirs(raw, exist_ok=True)
    dem_path = os.path.join(data, "dmr", "dmr5g_5m.tif"); pov_path = os.path.join(data, "povodi.geojson")
    for p in (dem_path, pov_path):
        if not os.path.exists(p): sys.exit(f"Chybí {p}")
    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    to_wgs = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
    gj = json.load(open(pov_path, encoding="utf-8"))
    model = next(f for f in gj["features"] if f["properties"].get("typ") == "uzemi_modelu")
    ring = np.array([to5514.transform(x, y) for x, y in model["geometry"]["coordinates"][0]])
    xmin, ymin = ring.min(axis=0); xmax, ymax = ring.max(axis=0); b = a.buffer
    bbox = (round(xmin - b), round(ymin - b), round(xmax + b), round(ymax + b))

    with rasterio.open(dem_path) as src:
        prof = src.profile; transform = src.transform; H, W = src.height, src.width; res = transform.a
        valid = src.read(1) != src.nodata
    gx = transform.c + (np.arange(W) + 0.5) * res; gy = transform.f - (np.arange(H) + 0.5) * res
    GX, GY = np.meshgrid(gx, gy)
    mask = Path(ring).contains_points(np.column_stack([GX.ravel(), GY.ravel()])).reshape(H, W)
    ha = res * res / 1e4

    # ---- 1. BPEJ
    gml = os.path.join(raw, "bpej_wfs.gml")
    if os.path.exists(gml) and os.path.getsize(gml) > 1000:
        txt = open(gml, encoding="utf-8").read(); log("1/4 BPEJ ze souboru data/bpej/bpej_wfs.gml (smaž ho pro nové stažení)")
    elif a.bez_stahovani:
        sys.exit("Chybí data/bpej/bpej_wfs.gml a stahování je vypnuté")
    else:
        log(f"1/4 stahuji BPEJ z WFS SPÚ, bbox {bbox} ..."); txt = fetch_bpej(bbox, gml)
    feats = parse_gml2(txt)
    log(f"   polygonů BPEJ: {len(feats)}; bez HSP (HPJ mimo tabulku): {sum(1 for f in feats if f['hsp'] == 0)}")

    log("2/4 vypaluji ...")
    def shapes(key):
        out = []
        for f in feats:
            v = f[key]
            if not v: continue
            for poly in f["polys"]:
                out.append(({"type": "Polygon", "coordinates": poly}, v))
        return out
    hsp = rasterize(shapes("hsp"), out_shape=(H, W), transform=transform, fill=0, dtype="uint8")
    hpj = rasterize(shapes("hpj"), out_shape=(H, W), transform=transform, fill=0, dtype="uint8")
    zdroj = np.where(hsp > 0, 1, 0).astype(np.uint8)

    # ---- 2. VÚMOP (když je)
    vychozi = os.path.join(data, "vumop", "HSP_Korycany.gpkg")
    if not a.vumop and not a.bez_vumop and os.path.exists(vychozi): a.vumop = vychozi
    if a.bez_vumop: a.vumop = None
    if a.vumop:
        vp = a.vumop
        if vp.lower().endswith((".tif", ".tiff")):
            from rasterio.warp import reproject, Resampling
            with rasterio.open(vp) as vs:
                arr = np.zeros((H, W), np.uint8)
                reproject(vs.read(1), arr, src_transform=vs.transform, src_crs=vs.crs, dst_transform=transform,
                          dst_crs=prof["crs"], resampling=Resampling.nearest)
            # dovol i písmena v kódu rastru: 1-4 beru jako je
            arr = np.where((arr >= 1) & (arr <= 4), arr, 0).astype(np.uint8)
        else:
            if vp.lower().endswith(".gpkg"):
                prvky, srs, vrstva = cti_gpkg(vp)
                if srs != 5514: sys.exit(f"GPKG {vp}: čekám EPSG:5514, je {srs}")
                vstup = [(d, polys) for d, polys in prvky]
            else:
                vj = json.load(open(vp, encoding="utf-8")); vstup = []
                for f in vj["features"]:
                    g = f["geometry"]; vstup.append((f["properties"], [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]))
            shp = []; dvoji = 0
            for props, polys in vstup:
                val = props.get("HSP") or props.get("hsp") or props.get("HSP_K")
                if val is None: continue
                t = str(val).strip().upper()
                if "/" in t: t = t.split("/")[-1]; dvoji += 1   # B/D: neodvodněný stav (D), odvodnění v území neznáme
                val = {"A": 1, "B": 2, "C": 3, "D": 4}.get(t, 0)
                if not val: continue
                for poly in polys: shp.append(({"type": "Polygon", "coordinates": poly}, val))
            arr = rasterize(shp, out_shape=(H, W), transform=transform, fill=0, dtype="uint8")
            if dvoji: log(f"   dvojí skupina (např. B/D) u {dvoji} prvků -> druhé písmeno (neodvodněno)")
        hsp = np.where(arr > 0, arr, hsp); zdroj = np.where(arr > 0, 3, zdroj).astype(np.uint8)
        log(f"   VÚMOP: {int((arr > 0).sum() * ha)} ha převzato z {vp}")

    # ---- 3. doplnění mezer nejbližší hodnotou
    log("3/4 doplňuji plochy bez HSP nejbližší hodnotou (odhad) ...")
    chybi = (hsp == 0) & valid
    if (hsp > 0).any():
        idx = distance_transform_edt(hsp == 0, return_distances=False, return_indices=True)
        fill = hsp[idx[0], idx[1]]
        hsp = np.where(chybi, fill, hsp).astype(np.uint8)
        zdroj = np.where(chybi, 2, zdroj).astype(np.uint8)
    hsp[~valid] = 0; zdroj[~valid] = 0

    log("4/4 zapisuji ...")
    prof.update(dtype="uint8", nodata=0, compress="lzw", count=1)
    for name, arr in (("hsp.tif", hsp), ("hsp_zdroj.tif", zdroj), ("hpj.tif", hpj)):
        with rasterio.open(os.path.join(data, "dmr", name), "w", **prof) as dst: dst.write(arr, 1)
    plochy = {HSP_PISM[k]: round(float(((hsp == k) & mask).sum() * ha), 1) for k in (1, 2, 3, 4)}
    zdr = {"BPEJ primo_ha": round(float(((zdroj == 1) & mask).sum() * ha), 1),
           "doplneno_nejblizsi_ha": round(float(((zdroj == 2) & mask).sum() * ha), 1),
           "vumop_ha": round(float(((zdroj == 3) & mask).sum() * ha), 1)}
    hpj_cet = {}
    for f in feats: hpj_cet[str(f["hpj"]).zfill(2)] = hpj_cet.get(str(f["hpj"]).zfill(2), 0) + 1
    info = {"datum": time.strftime("%Y-%m-%d"),
            "zdroj_bpej": "SPÚ, otevřená data, WFS wfs_bpej (WFS 1.0.0, GML2, EPSG:5514), Fees none, AccessConstraints none",
            "prirazeni_hsp": "Janeček a kol. 2012, Ochrana zemědělské půdy před erozí, tab. 2.2 (HPJ -> HSP, orientační)",
            "zdroj_vumop": ("VÚMOP, v.v.i., vektor HSP 2026 (" + os.path.basename(a.vumop) + "), CC BY-NC, poskytnuto 27. 10. 2026; B/D = D") if a.vumop else None,
            "metoda_doplneni": "pořadí: VÚMOP HSP 2026 (když je) > BPEJ (Janeček 2012 tab. 2.2) > nejbližší hodnota (euklidovsky) - ODHAD",
            "uzemi_modelu_celkem_ha": round(float(mask.sum() * ha), 1), "plochy_hsp_ha": plochy, "zdroj_hsp_ha": zdr,
            "podil_odhadu_pct": round(100 * zdr["doplneno_nejblizsi_ha"] / max(1e-9, mask.sum() * ha), 1),
            "cetnost_hpj_polygony": dict(sorted(hpj_cet.items())),
            "kody": {"hsp": {"1": "A", "2": "B", "3": "C", "4": "D"}, "hsp_zdroj": {"1": "BPEJ přímo", "2": "doplněno nejbližší BPEJ (odhad)", "3": "VÚMOP"}}}
    with open(os.path.join(data, "hsp_info.json"), "w", encoding="utf-8") as f: json.dump(info, f, ensure_ascii=False, indent=1)
    for k, v in plochy.items(): log(f"   HSP {k}: {v} ha")
    log(f"   z toho odhad (bez dat, doplněno nejbližší): {zdr['doplneno_nejblizsi_ha']} ha = {info['podil_odhadu_pct']} %")

    # GeoJSON BPEJ pro mapu (jen bbox, WGS84)
    gf = []
    for f in feats:
        for poly in f["polys"]:
            gf.append({"type": "Feature", "properties": {"bpej": f["kod_text"], "hpj": f["hpj"], "hsp": HSP_PISM.get(f["hsp"], "?"),
                                                           "trida_ochrany": f["trida_ochrany"]},
                       "geometry": {"type": "Polygon", "coordinates": [[[round(a_, 6), round(b_, 6)] for a_, b_ in
                                    (to_wgs.transform(x, y) for x, y in r)] for r in poly]}})
    with open(os.path.join(data, "bpej.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "name": "bpej", "zdroj": info["zdroj_bpej"] + "; HSP podle Janeček 2012 tab. 2.2", "features": gf}, f, ensure_ascii=False)
    log(f"   zapsáno data/bpej.geojson ({len(gf)} polygonů), data/hsp_info.json, data/dmr/hsp.tif, hsp_zdroj.tif, hpj.tif")

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap; from matplotlib.patches import Patch
    cm = ListedColormap(["#f6e8c3", "#80cdc1", "#35978f", "#01665e"])
    show = np.where(mask & (hsp > 0), hsp, np.nan)
    fig, ax = plt.subplots(figsize=(10, 10 * H / W))
    ax.imshow(show, cmap=cm, vmin=1, vmax=4, extent=[transform.c, transform.c + W * res, transform.f - H * res, transform.f], interpolation="nearest")
    od = np.where(mask & (zdroj == 2), 1.0, np.nan)
    ax.imshow(od, cmap=ListedColormap(["#ffffff"]), alpha=0.35, extent=[transform.c, transform.c + W * res, transform.f - H * res, transform.f], interpolation="nearest")
    ax.plot(ring[:, 0], ring[:, 1], color="k", lw=1)
    ax.set_xlim(xmin - 300, xmax + 300); ax.set_ylim(ymin - 300, ymax + 300)
    ax.legend(handles=[Patch(color=c, label=f"HSP {l}") for c, l in zip(cm.colors, "ABCD")] + [Patch(facecolor="#ffffff", edgecolor="#888", label="zesvětleno = bez dat, doplněno nejbližší (odhad)")],
              loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    ax.set_title("Hydrologické skupiny půd (VÚMOP HSP 2026, CC BY-NC; jinde BPEJ SPÚ -> Janeček 2012)" if a.vumop else "Hydrologické skupiny půd (BPEJ SPÚ -> HPJ -> HSP, Janeček 2012 tab. 2.2)")
    fig.savefig(os.path.join(data, "hsp_nahled.png"), dpi=150, bbox_inches="tight"); plt.close(fig)
    log("hotovo.")

if __name__ == "__main__":
    main()
