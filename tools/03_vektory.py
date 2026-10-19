# -*- coding: utf-8 -*-
"""03_vektory.py - budovy (INSPIRE BU, ČÚZK) a vodní toky (INSPIRE HY-NET, ČÚZK) ořezané na území modelu.

Použití (z libovolné složky):
    python tools/03_vektory.py [--budovy data/588601/588601.xml] [--toky data/HY-NET/HY-NET/HY-NET.gpkg]
                               [--povodi data/povodi.geojson] [--typ uzemi_modelu]

Vstupy (stahuje uživatel z atom.cuzk.gov.cz, CC BY 4.0):
    data/588601/588601.xml        INSPIRE Budovy, obec Koryčany [588601], GML 3.2.1, EPSG:5514
    data/HY-NET/**/HY-NET.gpkg    INSPIRE Vodstvo - hydrografická síť, celá ČR, GeoPackage, EPSG:3045 (ETRS89/TM33)
    data/povodi.geojson           z kroku 02 (polygon typ = uzemi_modelu)
    data/dmr/povodi_id.tif        z kroku 02 (id dílčích povodí)

Výstupy (WGS84, do gitu):
    data/budovy.geojson           půdorysy budov v území modelu; vlastnosti: ucel, cast_obce, plocha_m2, povodi_id.
                                  ZÁMĚRNĚ BEZ č.p., adres a identifikátorů (pravidlo projektu: žádné osobní údaje).
    data/budovy_info.json         součty: počet budov a plocha střech podle části obce, účelu a dílčího povodí
    data/toky_cuzk.geojson        linie vodních toků HY-NET v území modelu (+ 200 m), vlastnosti: nazev, typ
    data/vektory_nahled.png       kontrolní náhled (do docs/img po kontrole)

Metoda: čistý Python (xml.etree, sqlite3, numpy, pyproj, rasterio, matplotlib) - bez geopandas/shapely,
aby se na Windows nic nemuselo kompilovat. Ořez: budova patří do území, když její těžiště leží v polygonu
(matplotlib.path); tok se bere, když má aspoň jeden vrchol v polygonu rozšířeném o 200 m (bbox).
"""
import argparse, json, os, re, sqlite3, struct, sys, time
import xml.etree.ElementTree as ET
import numpy as np

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "bu-base": "http://inspire.ec.europa.eu/schemas/bu-base/4.0",
    "bu-core2d": "http://inspire.ec.europa.eu/schemas/bu-core2d/4.0",
    "bu-ext2d": "http://inspire.ec.europa.eu/schemas/bu-ext2d/4.0",
    "bu-ext": "http://inspire.ec.europa.eu/schemas/bu-ext/4.0",
    "ad": "http://inspire.ec.europa.eu/schemas/ad/4.0",
    "gn": "http://inspire.ec.europa.eu/schemas/gn/4.0",
    "xlink": "http://www.w3.org/1999/xlink",
}
UCEL = {  # INSPIRE CurrentUseValue -> česky
    "individualResidence": "rodinný dům", "collectiveResidence": "bytový dům", "residential": "bydlení",
    "agriculture": "zemědělství", "industrial": "průmysl", "commerceAndServices": "obchod a služby",
    "publicServices": "veřejná služba", "ancillary": "vedlejší stavba (garáž, kůlna)", "trade": "obchod",
    "office": "kancelář", "transport": "doprava", "utilities": "technická infrastruktura",
}

def ring_area_centroid(xy):
    x = xy[:, 0]; y = xy[:, 1]
    cross = x * np.roll(y, -1) - np.roll(x, -1) * y
    a = 0.5 * cross.sum()
    if abs(a) < 1e-9:
        return 0.0, xy.mean(axis=0)
    cx = ((x + np.roll(x, -1)) * cross).sum() / (6 * a)
    cy = ((y + np.roll(y, -1)) * cross).sum() / (6 * a)
    return abs(a), np.array([cx, cy])

def read_buildings(path):
    """Vrací list dict: ring (N,2) v EPSG:5514, ucel, cast_obce, plocha_m2."""
    out = []
    tree = ET.parse(path)
    for b in tree.getroot().iter("{%s}Building" % NS["bu-ext2d"]):
        pos = b.find(".//bu-core2d:geometry2D//gml:exterior//gml:posList", NS)
        if pos is None or not pos.text:
            continue
        v = np.array(pos.text.split(), float).reshape(-1, 2)
        if len(v) < 4:
            continue
        holes = []
        for h in b.findall(".//bu-core2d:geometry2D//gml:interior//gml:posList", NS):
            holes.append(np.array(h.text.split(), float).reshape(-1, 2))
        u = b.find(".//bu-base:currentUse/bu-base:CurrentUse/bu-base:currentUse", NS)
        ucel_raw = ""
        if u is not None:
            href = u.get("{%s}href" % NS["xlink"], "")
            m = re.search(r"CurrentUseValue/([^/]+)/", href)
            ucel_raw = m.group(1) if m else (u.get("{%s}title" % NS["xlink"], "") or "")
        cast = b.find(".//bu-ext:address//ad:addressArea//gn:text", NS)
        cast_obce = cast.text.strip() if cast is not None and cast.text else ""
        floors = b.find(".//bu-base:numberOfFloorsAboveGround", NS)
        podlazi = None
        if floors is not None and floors.text and floors.text.strip().isdigit():
            podlazi = int(floors.text)
        area, c = ring_area_centroid(v)
        for h in holes:
            area -= ring_area_centroid(h)[0]
        out.append({"ring": v, "holes": holes, "ucel": UCEL.get(ucel_raw, ucel_raw or "neuvedeno"),
                    "cast_obce": cast_obce, "plocha_m2": round(float(area), 1), "podlazi": podlazi, "c": c})
    return out

def gpkg_lines(path, bbox3045, layer_hint=("WatercourseLink", "Watercourse")):
    """Čte linie z GeoPackage (sqlite3 + ruční WKB), jen uvnitř bbox (přes RTree, když existuje)."""
    con = sqlite3.connect(path)
    cur = con.cursor()
    tabs = [r for r in cur.execute("SELECT table_name, geometry_column, srs_id FROM gpkg_geometry_columns")]
    if not tabs:
        sys.exit("V GPKG nejsou geometrické vrstvy")
    log("   vrstvy v GPKG: " + ", ".join(t[0] for t in tabs))
    tab = next((t for t in tabs for h in layer_hint if h.lower() in t[0].lower()), tabs[0])
    tname, gcol, srs = tab
    cols = [r[1] for r in cur.execute(f'PRAGMA table_info("{tname}")')]
    name_col = next((c for c in cols if c.lower() in ("name", "geographicalname", "nazev", "geographicalname_text")), None)
    for c in cols:
        if "name" in c.lower() and name_col is None:
            name_col = c
    pk = next((r[1] for r in cur.execute(f'PRAGMA table_info("{tname}")') if r[5] == 1), "fid")
    xmin, ymin, xmax, ymax = bbox3045
    rt = f"rtree_{tname}_{gcol}"
    has_rt = cur.execute("SELECT name FROM sqlite_master WHERE name=?", (rt,)).fetchone() is not None
    sel = ", ".join(['"%s"' % gcol] + (['"%s"' % name_col] if name_col else []) + ['"%s"' % c for c in cols if c != gcol and c != name_col and c != pk])
    if has_rt:
        q = f'SELECT {sel} FROM "{tname}" WHERE "{pk}" IN (SELECT id FROM "{rt}" WHERE minx<=? AND maxx>=? AND miny<=? AND maxy>=?)'
        rows = cur.execute(q, (xmax, xmin, ymax, ymin)).fetchall()
    else:
        log("   RTree chybí, čtu celou tabulku (pomalé)")
        rows = cur.execute(f'SELECT {sel} FROM "{tname}"').fetchall()
    other_cols = [c for c in cols if c != gcol and c != name_col and c != pk]
    feats = []
    for r in rows:
        blob = r[0]
        if blob is None:
            continue
        for line in wkb_lines(gpkg_geom(blob)):
            feats.append({"pts": line, "nazev": (r[1] if name_col else None),
                          "attr": dict(zip(other_cols, r[(2 if name_col else 1):]))})
    con.close()
    return feats, tname, srs

def gpkg_geom(blob):
    # GeoPackageBinary header: magic 'GP', version, flags, srs_id, envelope -> pak WKB
    flags = blob[3]
    env = (flags >> 1) & 0x7
    env_len = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}.get(env, 0)
    return blob[8 + env_len:]

def wkb_lines(wkb):
    """Vrací list polylinií (N,2) z WKB LineString / MultiLineString (2D i 3D/M)."""
    out = []
    def parse(off):
        bo = "<" if wkb[off] == 1 else ">"
        t = struct.unpack(bo + "I", wkb[off + 1:off + 5])[0]
        base = t & 0xFF; dims = 2 + (1 if t & 0x80000000 or 1000 <= (t % 10000) < 2000 else 0) + (1 if t & 0x40000000 or 2000 <= (t % 10000) < 4000 else 0)
        if (t % 10000) >= 3000: dims = 4
        off += 5
        if base in (2,):  # LineString
            n = struct.unpack(bo + "I", wkb[off:off + 4])[0]; off += 4
            arr = np.frombuffer(wkb[off:off + n * dims * 8], dtype=bo + "f8").reshape(n, dims)[:, :2]
            out.append(np.array(arr)); return off + n * dims * 8
        if base in (5, 7):  # Multi / collection
            n = struct.unpack(bo + "I", wkb[off:off + 4])[0]; off += 4
            for _ in range(n):
                off = parse(off)
            return off
        if base == 1:
            return off + dims * 8
        raise ValueError(f"WKB typ {t} neumím")
    parse(0)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budovy", default=None)
    ap.add_argument("--toky", default=None)
    ap.add_argument("--povodi", default=None)
    ap.add_argument("--typ", default="uzemi_modelu")
    a = ap.parse_args()
    import rasterio
    from pyproj import Transformer
    from matplotlib.path import Path
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data")
    bud = a.budovy or os.path.join(data, "588601", "588601.xml")
    toky = a.toky
    if toky is None:
        for dp, dn, fn in os.walk(os.path.join(data, "HY-NET")):
            for f in fn:
                if f.lower().endswith(".gpkg"):
                    toky = os.path.join(dp, f)
    pov = a.povodi or os.path.join(data, "povodi.geojson")
    if not os.path.exists(pov):
        sys.exit("Chybí data/povodi.geojson - nejdřív spusť vyrob_rozvodnice.bat")

    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    to_wgs = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
    gj = json.load(open(pov, encoding="utf-8"))
    feat = next((f for f in gj["features"] if f["properties"].get("typ") == a.typ), None)
    if feat is None:
        sys.exit(f"V povodi.geojson není polygon typ={a.typ}")
    ring = np.array([to5514.transform(x, y) for x, y in feat["geometry"]["coordinates"][0]])
    path = Path(ring)
    xmin, ymin = ring.min(axis=0); xmax, ymax = ring.max(axis=0)
    log(f"území '{feat['properties']['nazev']}' {feat['properties'].get('plocha_vlastni_km2')} km², bbox {xmin:.0f}..{xmax:.0f} / {ymin:.0f}..{ymax:.0f}")

    # id dílčích povodí
    pid_path = os.path.join(data, "dmr", "povodi_id.tif")
    pid = None
    if os.path.exists(pid_path):
        pid = rasterio.open(pid_path)
    kody = {}
    ip = os.path.join(data, "rozvodnice_info.json")
    if os.path.exists(ip):
        kody = {int(k): v for k, v in json.load(open(ip, encoding="utf-8")).get("povodi_id_kody", {}).items()}

    # ---------------- budovy
    feats_b = []; info = {}
    if os.path.exists(bud):
        log("budovy: čtu GML ...")
        B = read_buildings(bud)
        inside = path.contains_points(np.array([b["c"] for b in B]))
        log(f"   budov v souboru {len(B)}, v území modelu {int(inside.sum())}")
        sums = {"podle_casti_obce": {}, "podle_ucelu": {}, "podle_povodi": {}}
        def add(d, k, area):
            e = d.setdefault(k, {"pocet": 0, "plocha_strech_m2": 0.0}); e["pocet"] += 1; e["plocha_strech_m2"] += area
        for b, ok in zip(B, inside):
            if not ok:
                continue
            p_id = 0
            if pid is not None:
                try:
                    p_id = int(next(pid.sample([(float(b["c"][0]), float(b["c"][1]))]))[0])
                except Exception:
                    p_id = 0
            props = {"ucel": b["ucel"], "cast_obce": b["cast_obce"] or "neuvedeno", "plocha_m2": b["plocha_m2"],
                     "podlazi": b["podlazi"], "povodi_id": p_id, "povodi": kody.get(p_id, "mimo dílčí povodí")}
            rings = [[list(map(lambda v: round(v, 6), to_wgs.transform(x, y))) for x, y in b["ring"]]]
            for h in b["holes"]:
                rings.append([list(map(lambda v: round(v, 6), to_wgs.transform(x, y))) for x, y in h])
            feats_b.append({"type": "Feature", "properties": props, "geometry": {"type": "Polygon", "coordinates": rings}})
            add(sums["podle_casti_obce"], props["cast_obce"], b["plocha_m2"])
            add(sums["podle_ucelu"], props["ucel"], b["plocha_m2"])
            add(sums["podle_povodi"], props["povodi"], b["plocha_m2"])
        for d in sums.values():
            for e in d.values():
                e["plocha_strech_m2"] = round(e["plocha_strech_m2"])
        info = {"zdroj": "ČÚZK, INSPIRE Budovy (BU), obec Koryčany [588601], CC BY 4.0; půdorysy z RÚIAN/ISKN, přesnost ~1,5 m",
                "stazeno": time.strftime("%Y-%m-%d"), "pozn": "Bez č.p., adres a identifikátorů budov (pravidlo projektu). "
                "Plocha = půdorys, ne plocha střechy se sklonem. Účel podle RÚIAN, u mnoha budov 'neuvedeno'.",
                "budov_celkem_v_obci": len(B), "budov_v_uzemi_modelu": len(feats_b),
                "plocha_pudorysu_v_uzemi_m2": round(sum(f["properties"]["plocha_m2"] for f in feats_b)), **sums}
        with open(os.path.join(data, "budovy.geojson"), "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "name": "budovy", "zdroj": info["zdroj"], "features": feats_b}, f, ensure_ascii=False)
        with open(os.path.join(data, "budovy_info.json"), "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=1)
        log(f"   zapsáno data/budovy.geojson a budovy_info.json; půdorysy celkem {info['plocha_pudorysu_v_uzemi_m2']:,} m²")
    else:
        log(f"budovy: soubor {bud} chybí, přeskakuji")

    # ---------------- toky
    feats_t = []
    if toky and os.path.exists(toky):
        log(f"toky: čtu {toky} ...")
        buf = 200.0
        to3045 = Transformer.from_crs("EPSG:5514", "EPSG:3045", always_xy=True)
        from3045 = Transformer.from_crs("EPSG:3045", "EPSG:5514", always_xy=True)
        cx = [xmin - buf, xmax + buf, xmax + buf, xmin - buf]; cy = [ymin - buf, ymin - buf, ymax + buf, ymax + buf]
        bx, by = to3045.transform(cx, cy)
        lines, tname, srs = gpkg_lines(toky, (min(bx), min(by), max(bx), max(by)))
        log(f"   vrstva {tname}, srs {srs}, linií v bboxu {len(lines)}")
        big = Path(np.array([[xmin - buf, ymin - buf], [xmax + buf, ymin - buf], [xmax + buf, ymax + buf], [xmin - buf, ymax + buf]]))
        for ln in lines:
            X, Y = from3045.transform(ln["pts"][:, 0], ln["pts"][:, 1])
            P = np.column_stack([X, Y])
            if not big.contains_points(P).any():
                continue
            v_uzemi = bool(path.contains_points(P).any())
            attr = {k: (v if isinstance(v, (int, float, str)) or v is None else str(v)) for k, v in ln["attr"].items()}
            attr = {k: v for k, v in attr.items() if v not in (None, "") and len(str(v)) < 120}
            feats_t.append({"type": "Feature", "properties": {"nazev": ln["nazev"], "v_uzemi_modelu": v_uzemi, **attr},
                            "geometry": {"type": "LineString", "coordinates": [[round(a_, 6), round(b_, 6)] for a_, b_ in
                                        zip(*to_wgs.transform(X, Y))]}})
        with open(os.path.join(data, "toky_cuzk.geojson"), "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "name": "toky_cuzk",
                       "zdroj": "ČÚZK, INSPIRE Vodstvo - hydrografická síť (HY-NET), CC BY 4.0; výřez území modelu + 200 m",
                       "features": feats_t}, f, ensure_ascii=False)
        names = sorted({f["properties"]["nazev"] for f in feats_t if f["properties"]["nazev"]})
        log(f"   zapsáno data/toky_cuzk.geojson ({len(feats_t)} linií); názvy: {', '.join(names)[:300]}")
    else:
        log("toky: HY-NET.gpkg nenalezen v data/HY-NET, přeskakuji")

    # ---------------- náhled
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection, LineCollection
    fig, ax = plt.subplots(figsize=(11, 11 * (ymax - ymin) / (xmax - xmin)))
    hs = os.path.join(data, "dmr", "dmr5g_5m.tif")
    if os.path.exists(hs):
        with rasterio.open(hs) as src:
            g = src.read(1).astype(float); g[g == src.nodata] = np.nan; t = src.transform
            dzdx = np.gradient(g, 5, axis=1); dzdy = np.gradient(g, 5, axis=0)
            sl = np.arctan(np.hypot(dzdx, dzdy)); asp = np.arctan2(-dzdx, dzdy)
            h = np.sin(np.radians(45)) * np.cos(sl) + np.cos(np.radians(45)) * np.sin(sl) * np.cos(np.radians(315) - asp)
            ax.imshow(h, cmap="gray", vmin=-0.2, vmax=1, extent=[t.c, t.c + src.width * 5, t.f - src.height * 5, t.f])
    ax.plot(ring[:, 0], ring[:, 1], color="#d62728", lw=1.5, label="území modelu")
    if feats_t:
        segs = []
        for f in feats_t:
            X, Y = to5514.transform([p[0] for p in f["geometry"]["coordinates"]], [p[1] for p in f["geometry"]["coordinates"]])
            segs.append(np.column_stack([X, Y]))
        ax.add_collection(LineCollection(segs, colors="#0b3d91", linewidths=0.9))
    if feats_b:
        polys = []
        for f in feats_b:
            X, Y = to5514.transform([p[0] for p in f["geometry"]["coordinates"][0]], [p[1] for p in f["geometry"]["coordinates"][0]])
            polys.append(np.column_stack([X, Y]))
        ax.add_collection(PolyCollection(polys, facecolors="#e07b00", edgecolors="none"))
    ax.set_xlim(xmin - 300, xmax + 300); ax.set_ylim(ymin - 300, ymax + 300)
    ax.set_title(f"Budovy (oranžově, {len(feats_b)}) a toky ČÚZK (modře, {len(feats_t)}) v území modelu")
    ax.set_xlabel("X [m] EPSG:5514"); ax.set_ylabel("Y [m]")
    png = os.path.join(data, "vektory_nahled.png")
    fig.savefig(png, dpi=150, bbox_inches="tight"); plt.close(fig)
    log(f"zapsáno {png}"); log("hotovo.")

if __name__ == "__main__":
    main()
