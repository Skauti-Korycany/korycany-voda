# -*- coding: utf-8 -*-
"""04_vyuziti_pudy.py - využití půdy (ZABAGED polohopis přes WFS ČÚZK) -> rastr tříd 5 m + součty.

Použití (z libovolné složky):
    python tools/04_vyuziti_pudy.py [--bez-stahovani] [--buffer 200]

Krok 1 - stažení: WFS ZABAGED polohopis (https://ags.cuzk.gov.cz/arcgis/services/ZABAGED_POLOHOPIS/MapServer/WFSServer,
    WFS 2.0, GeoJSON, EPSG:5514, max 1000 prvků na dotaz; startIndex server ignoruje -> dělení bboxu na čtvrtiny). Bbox = území modelu + buffer.
    Soubory do data/zabaged/<vrstva>.geojson (mimo git; při dalším běhu se nestahují znovu, smaž složku pro obnovu).
    Licence ČÚZK: CC BY 4.0, uvádět "ČÚZK - on-line".
Krok 2 - rastr: polygony se vypálí do mřížky DEM (5 m, EPSG:5514) v pořadí od obecného ke konkrétnímu,
    pak linie komunikací (1 buňka = 5 m, zjednodušení), nakonec budovy (INSPIRE BU z kroku 03 + kůlny ZABAGED).
Krok 3 - součty: plocha tříd v území modelu a v dílčích povodích; legenda s kódy pro CN (fáze 3).

Výstupy:
    data/dmr/vyuziti_kod.tif       uint8 kódy tříd (0 = nic/NoData), stejná mřížka jako dmr5g_5m.tif
    data/vyuziti_pudy.json         legenda (kód -> název, zdrojová vrstva), plochy v ha v území modelu a po dílčích povodích
    data/vyuziti_pudy.geojson      vektor tříd v území modelu (z rastru, WGS84, zjednodušený) pro mapu
    data/povodi_chp.geojson        hranice povodí IV. řádu ČHP (ZABAGED, vrstva Rozvodnice) v bboxu - ke kontrole rozvodnic
    data/vyuziti_nahled.png        náhled (kopie do docs/img po kontrole)

Závislosti: numpy, rasterio, pyproj, matplotlib (stdlib: urllib, json). Bez geopandas/shapely.
"""
import argparse, json, os, sys, time, urllib.request, urllib.parse
import numpy as np

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

WFS = "https://ags.cuzk.gov.cz/arcgis/services/ZABAGED_POLOHOPIS/MapServer/WFSServer"

# (vrstva WFS, kód, název, atribut pro dělení, {hodnota atributu: (kód, název)})
# Pořadí = pořadí vypalování (pozdější přepisuje dřívější).
VRSTVY = [
    ("Orná_půda_a_ostatní_dále_nespecifikované_plochy", 2, "ostatní nespecifikovaná plocha", "TYP_PUDY_K", {"OR": (1, "orná půda")}),
    ("Trvalý_travní_porost", 3, "trvalý travní porost", None, {}),
    ("Lesní_půda_se_stromy", 4, "les (druh neurčen)", None, {}),
    ("Lesní_půda_se_stromy_kategorizovaná__plocha_", 4, "les (druh neurčen)", "druh_k", {"J": (41, "les jehličnatý"), "L": (42, "les listnatý"), "S": (43, "les smíšený")}),
    ("Lesní_půda_s_křovinatým_porostem", 5, "křoviny", None, {}),
    ("Ovocný_sad__zahrada", 7, "zahrada", "TYP_PUDY_K", {"OS": (6, "ovocný sad"), "OTK": (8, "ostatní trvalá kultura")}),
    ("Vinice", 8, "ostatní trvalá kultura", None, {}),
    ("Udržovaná_zeleň", 9, "udržovaná zeleň, park", None, {}),
    ("Ostatní_plocha_v_sídlech", 10, "ostatní plocha v sídle", None, {}),
    ("Areál_účelové_zástavby", 11, "areál účelové zástavby", None, {}),
    ("Hřbitov", 12, "hřbitov", None, {}),
    ("Skládka", 13, "skládka, úložiště", None, {}),
    ("Povrchová_těžba__lom", 13, "skládka, úložiště", None, {}),
    ("Parkoviště__odpočívka", 14, "parkoviště", None, {}),
    ("Kolejiště", 15, "kolejiště", None, {}),
    ("Areál_železniční_stanice__zastávky", 15, "kolejiště", None, {}),
    ("Bažina__močál", 17, "bažina, močál", None, {}),
    ("Vodní_plocha", 16, "vodní plocha", None, {}),
]
LINIE = [  # linie: kód, filtr (atribut, povolené hodnoty) nebo None
    ("Cesta", 22, "cesta zpevněná", ("povrch_k", {"Z", "P"})),
    ("Ulice", 21, "ulice", None),
    ("Silnice__dálnice", 20, "silnice", None),
]
KOD_BUDOVA = 30; KOD_KULNA = 31
LEGENDA = {1: "orná půda", 2: "ostatní nespecifikovaná plocha", 3: "trvalý travní porost", 4: "les (druh neurčen)",
           41: "les jehličnatý", 42: "les listnatý", 43: "les smíšený", 5: "křoviny", 6: "ovocný sad", 7: "zahrada",
           8: "ostatní trvalá kultura", 9: "udržovaná zeleň, park", 10: "ostatní plocha v sídle", 11: "areál účelové zástavby",
           12: "hřbitov", 13: "skládka, úložiště", 14: "parkoviště", 15: "kolejiště", 16: "vodní plocha", 17: "bažina, močál",
           20: "silnice", 21: "ulice", 22: "cesta zpevněná", 30: "budova", 31: "kůlna, skleník, přístřešek"}
EXTRA = ["Rozvodnice"]  # jen uložit, nevypalovat

def wfs_get(layer, bbox, count=1000):
    q = {"service": "WFS", "version": "2.0.0", "request": "GetFeature", "outputFormat": "GEOJSON",
         "srsName": "urn:ogc:def:crs:EPSG::5514", "count": count,
         "typeNames": "ZABAGED_POLOHOPIS:" + layer,
         "bbox": "{},{},{},{},urn:ogc:def:crs:EPSG::5514".format(*bbox)}
    url = WFS + "?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)
    req = urllib.request.Request(url, headers={"User-Agent": "korycany-voda/1.0 (skauti; nekomercni)"})
    for pokus in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                txt = r.read().decode("utf-8")
            break
        except Exception as e:
            if pokus == 2:
                raise
            log(f"   {layer}: chyba {e}, zkouším znovu"); time.sleep(3)
    try:
        return json.loads(txt).get("features", [])
    except Exception:
        sys.exit(f"WFS nevrátil JSON pro {layer}: {txt[:300]}")

def wfs_fetch(layer, bbox, out_path, count=1000, depth=0):
    """Stáhne vrstvu v bboxu. Server ignoruje startIndex (ověřeno 19. 10. 2026), proto když vrátí plných 1000 prvků,
    bbox se rozdělí na čtvrtiny a stáhne se znovu (rekurzivně); prvky se slučují podle GmlID."""
    feats = {}
    def grab(bb, d):
        f = wfs_get(layer, bb, count)
        if len(f) >= count and d < 6:
            x0, y0, x1, y1 = bb; xm = (x0 + x1) / 2; ym = (y0 + y1) / 2
            for sub in ((x0, y0, xm, ym), (xm, y0, x1, ym), (x0, ym, xm, y1), (xm, ym, x1, y1)):
                grab(sub, d + 1)
        else:
            for ft in f:
                feats[ft["properties"].get("GmlID") or ft.get("id") or len(feats)] = ft
    grab(tuple(bbox), depth)
    feats = list(feats.values())
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "EPSG:5514"}},
                   "zdroj": "ČÚZK ZABAGED polohopis, WFS, CC BY 4.0, staženo " + time.strftime("%Y-%m-%d"),
                   "vrstva": layer, "features": feats}, fh, ensure_ascii=False)
    return len(feats)

def polys_of(geom):
    """GeoJSON Polygon/MultiPolygon -> list polygonů [[ring, ...]]"""
    if geom is None: return []
    if geom["type"] == "Polygon": return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon": return geom["coordinates"]
    return []

def lines_of(geom):
    if geom is None: return []
    if geom["type"] == "LineString": return [geom["coordinates"]]
    if geom["type"] == "MultiLineString": return geom["coordinates"]
    return []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bez-stahovani", action="store_true")
    ap.add_argument("--buffer", type=float, default=200.0)
    a = ap.parse_args()
    import rasterio
    from rasterio.features import rasterize, shapes
    from pyproj import Transformer
    from matplotlib.path import Path

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = os.path.join(root, "data"); raw = os.path.join(data, "zabaged"); os.makedirs(raw, exist_ok=True)
    dem_path = os.path.join(data, "dmr", "dmr5g_5m.tif")
    pov_path = os.path.join(data, "povodi.geojson")
    for p in (dem_path, pov_path):
        if not os.path.exists(p):
            sys.exit(f"Chybí {p} - nejdřív spusť vyrob_teren.bat a vyrob_rozvodnice.bat")
    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    to_wgs = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)

    gj = json.load(open(pov_path, encoding="utf-8"))
    model = next(f for f in gj["features"] if f["properties"].get("typ") == "uzemi_modelu")
    ring = np.array([to5514.transform(x, y) for x, y in model["geometry"]["coordinates"][0]])
    xmin, ymin = ring.min(axis=0); xmax, ymax = ring.max(axis=0)
    b = a.buffer
    bbox = (round(xmin - b), round(ymin - b), round(xmax + b), round(ymax + b))
    log(f"území modelu {model['properties'].get('plocha_vlastni_km2')} km², bbox {bbox}")

    # ---- 1. stažení
    vrstvy = [v[0] for v in VRSTVY] + [l[0] for l in LINIE] + ["Kůlna__skleník__fóliovník__přístřešek"] + EXTRA
    if not a.bez_stahovani:
        log("1/3 stahuji ZABAGED přes WFS ČÚZK ...")
        for L in vrstvy:
            p = os.path.join(raw, L + ".geojson")
            if os.path.exists(p):
                try:
                    n_old = len(json.load(open(p, encoding="utf-8"))["features"])
                except Exception:
                    n_old = -1
                if n_old != 1000:        # přesně 1000 = oříznuto limitem serveru (stará verze skriptu) -> stáhnout znovu
                    continue
                log(f"   {L}: soubor má přesně 1000 prvků (oříznuto), stahuji znovu po dlaždicích")
            n = wfs_fetch(L, bbox, p)
            log(f"   {L}: {n} prvků")
    else:
        log("1/3 stahování přeskočeno")

    # ---- 2. rastr
    log("2/3 vypaluji do mřížky DEM ...")
    with rasterio.open(dem_path) as src:
        prof = src.profile; transform = src.transform; H, W = src.height, src.width; res = transform.a
        dem = src.read(1); valid = dem != src.nodata
    kod = np.zeros((H, W), np.uint8)
    pocty = {}
    def burn(shapes_list, k):
        if not shapes_list: return
        r = rasterize(shapes_list, out_shape=(H, W), transform=transform, fill=0, dtype="uint8", all_touched=False)
        kod[r > 0] = r[r > 0]
    for L, k0, _, attr, mapa in VRSTVY:
        p = os.path.join(raw, L + ".geojson")
        if not os.path.exists(p): continue
        feats = json.load(open(p, encoding="utf-8"))["features"]
        shp = []
        for f in feats:
            k = k0
            if attr and f["properties"].get(attr) in mapa:
                k = mapa[f["properties"][attr]][0]
            for poly in polys_of(f["geometry"]):
                shp.append(({"type": "Polygon", "coordinates": poly}, k))
        burn(shp, k0); pocty[L] = len(feats)
    for L, k, _, filt in LINIE:
        p = os.path.join(raw, L + ".geojson")
        if not os.path.exists(p): continue
        feats = json.load(open(p, encoding="utf-8"))["features"]
        shp = []
        for f in feats:
            if filt and f["properties"].get(filt[0]) not in filt[1]:
                continue
            for ln in lines_of(f["geometry"]):
                shp.append(({"type": "LineString", "coordinates": ln}, k))
        if shp:
            r = rasterize(shp, out_shape=(H, W), transform=transform, fill=0, dtype="uint8", all_touched=True)
            kod[r > 0] = r[r > 0]
        pocty[L] = len(shp)
    # kůlny ZABAGED, pak budovy INSPIRE (z kroku 03, WGS84 -> 5514)
    p = os.path.join(raw, "Kůlna__skleník__fóliovník__přístřešek.geojson")
    if os.path.exists(p):
        shp = [({"type": "Polygon", "coordinates": poly}, KOD_KULNA) for f in json.load(open(p, encoding="utf-8"))["features"] for poly in polys_of(f["geometry"])]
        burn(shp, KOD_KULNA); pocty["Kůlna"] = len(shp)
    bp = os.path.join(data, "budovy.geojson")
    if os.path.exists(bp):
        shp = []
        for f in json.load(open(bp, encoding="utf-8"))["features"]:
            rings = [[list(to5514.transform(x, y)) for x, y in r] for r in f["geometry"]["coordinates"]]
            shp.append(({"type": "Polygon", "coordinates": rings}, KOD_BUDOVA))
        # all_touched=False: buňka je budova, když její střed leží v půdorysu -> plocha bez nadsazení (malé kůlny mohou vypadnout)
        r = rasterize(shp, out_shape=(H, W), transform=transform, fill=0, dtype="uint8", all_touched=False)
        kod[r > 0] = KOD_BUDOVA; pocty["budovy (INSPIRE BU)"] = len(shp)
    kod[~valid] = 0
    prof.update(dtype="uint8", nodata=0, compress="lzw", count=1)
    with rasterio.open(os.path.join(data, "dmr", "vyuziti_kod.tif"), "w", **prof) as dst:
        dst.write(kod, 1)
    log("   zapsáno data/dmr/vyuziti_kod.tif")

    # ---- 3. součty v území modelu a po dílčích povodích
    log("3/3 součty a výstupy ...")
    gx = transform.c + (np.arange(W) + 0.5) * res; gy = transform.f - (np.arange(H) + 0.5) * res
    GX, GY = np.meshgrid(gx, gy)
    mask = Path(ring).contains_points(np.column_stack([GX.ravel(), GY.ravel()])).reshape(H, W)
    ha = res * res / 1e4
    def soucty(m):
        vals, cnt = np.unique(kod[m], return_counts=True)
        d = {LEGENDA.get(int(v), f"kód {v}"): round(float(c * ha), 2) for v, c in zip(vals, cnt) if v > 0}
        d["nezařazeno"] = round(float((kod[m] == 0).sum() * ha), 2)
        return dict(sorted(d.items(), key=lambda kv: -kv[1]))
    out = {"zdroj": "ČÚZK ZABAGED polohopis (WFS, CC BY 4.0); budovy INSPIRE BU; vypáleno do mřížky DMR 5 m",
           "datum": time.strftime("%Y-%m-%d"), "legenda": {str(k): v for k, v in LEGENDA.items()},
           "pozn": "Komunikace vypáleny jako linie šířky 1 buňky (5 m) - zjednodušení. Les podle druhu jen tam, kde má ZABAGED "
                   "kategorizaci (jinak 'les (druh neurčen)'). 'nezařazeno' = buňky bez plošného objektu ZABAGED (mezery, okraj).",
           "pocty_prvku_stazeno": pocty,
           "uzemi_modelu_ha": soucty(mask), "uzemi_modelu_celkem_ha": round(float(mask.sum() * ha), 1)}
    pid_path = os.path.join(data, "dmr", "povodi_id.tif")
    if os.path.exists(pid_path):
        with rasterio.open(pid_path) as s: pid = s.read(1)
        kody = json.load(open(os.path.join(data, "rozvodnice_info.json"), encoding="utf-8")).get("povodi_id_kody", {})
        out["dilci_povodi_ha"] = {kody.get(str(int(v)), str(v)): soucty((pid == v) & mask) for v in np.unique(pid) if v > 0}
    with open(os.path.join(data, "vyuziti_pudy.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    for k, v in out["uzemi_modelu_ha"].items():
        log(f"   {k}: {v} ha")

    # vektor tříd pro mapu (jen území modelu, zjednodušeno)
    km = np.where(mask, kod, 0).astype(np.int32)
    feats = []
    for geom, val in shapes(km, mask=km > 0, transform=transform):
        val = int(val)
        rings = []
        for rg in geom["coordinates"]:
            pts = rg[::2] if len(rg) > 8 else rg      # hrubé zjednodušení schodů 5 m
            if pts[0] != pts[-1]: pts = list(pts) + [pts[0]]
            rings.append([[round(a_, 6), round(b_, 6)] for a_, b_ in (to_wgs.transform(x, y) for x, y in pts)])
        feats.append({"type": "Feature", "properties": {"kod": val, "trida": LEGENDA.get(val, "")},
                      "geometry": {"type": "Polygon", "coordinates": rings}})
    with open(os.path.join(data, "vyuziti_pudy.geojson"), "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "name": "vyuziti_pudy", "zdroj": out["zdroj"], "features": feats}, fh, ensure_ascii=False)
    log(f"   zapsáno data/vyuziti_pudy.geojson ({len(feats)} polygonů)")

    # rozvodnice ČHP ke kontrole (WGS84)
    p = os.path.join(raw, "Rozvodnice.geojson")
    if os.path.exists(p):
        ff = []
        for f in json.load(open(p, encoding="utf-8"))["features"]:
            for ln in lines_of(f["geometry"]):
                ff.append({"type": "Feature", "properties": {"chp1": f["properties"].get("chp1"), "chp2": f["properties"].get("chp2")},
                           "geometry": {"type": "LineString", "coordinates": [[round(a_, 6), round(b_, 6)] for a_, b_ in (to_wgs.transform(x, y) for x, y in ln)]}})
        with open(os.path.join(data, "povodi_chp.geojson"), "w", encoding="utf-8") as fh:
            json.dump({"type": "FeatureCollection", "name": "povodi_chp", "zdroj": "ČÚZK ZABAGED polohopis - Rozvodnice (ČHP), CC BY 4.0", "features": ff}, fh, ensure_ascii=False)
        log(f"   zapsáno data/povodi_chp.geojson ({len(ff)} linií)")

    # náhled
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from matplotlib.patches import Patch
    barvy = {1: "#e6c86e", 2: "#d9d2b8", 3: "#b6df8a", 4: "#3f8f3f", 41: "#1f6b2a", 42: "#5fae4a", 43: "#3c8f3c", 5: "#8fbf6f",
             6: "#c9a0dc", 7: "#d6b4e8", 8: "#c9a0dc", 9: "#9fd89f", 10: "#cfcfcf", 11: "#b08968", 12: "#a0a0a0", 13: "#7a7a7a",
             14: "#9a9a9a", 15: "#6b6b6b", 16: "#4c9ed9", 17: "#7fc3d8", 20: "#333333", 21: "#555555", 22: "#8a7a5a", 30: "#c0392b", 31: "#e08a7a"}
    ks = sorted(barvy); cmap = ListedColormap([barvy[k] for k in ks]); norm = BoundaryNorm([k - 0.5 for k in ks] + [ks[-1] + 0.5], len(ks))
    show = np.where(mask & (kod > 0), kod, np.nan).astype(float)
    # kódy, které nejsou v ks, by rozbily normu -> mapuj na nejbližší
    fig, ax = plt.subplots(figsize=(11, 11 * H / W))
    ax.imshow(show, cmap=cmap, norm=norm, extent=[transform.c, transform.c + W * res, transform.f - H * res, transform.f], interpolation="nearest")
    ax.plot(ring[:, 0], ring[:, 1], color="k", lw=1)
    ax.set_xlim(xmin - 300, xmax + 300); ax.set_ylim(ymin - 300, ymax + 300)
    pres = [k for k in ks if (kod[mask] == k).any()]
    ax.legend(handles=[Patch(color=barvy[k], label=LEGENDA[k]) for k in pres], loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8, framealpha=.9)
    ax.set_title("Využití půdy v území modelu (ZABAGED, 5 m)"); ax.set_xlabel("X [m] EPSG:5514"); ax.set_ylabel("Y [m]")
    png = os.path.join(data, "vyuziti_nahled.png")
    fig.savefig(png, dpi=150, bbox_inches="tight"); plt.close(fig)
    log(f"   zapsáno {png}"); log("hotovo.")

if __name__ == "__main__":
    main()
