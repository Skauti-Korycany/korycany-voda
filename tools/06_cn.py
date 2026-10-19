# -*- coding: utf-8 -*-
"""06_cn.py - rastr CN a přímý odtok z návrhového deště (SCS-CN) pro území modelu.

Vstupy: data/dmr/vyuziti_kod.tif (04), data/dmr/hsp.tif (05), data/cn_tabulka.json (build_cn.py),
        data/povodi.geojson + data/dmr/povodi_id.tif (02). Použití: python tools/06_cn.py [--dest 20,40,60]
Výstupy:
    data/dmr/cn.tif            uint8 CN (IPS II), 0 = NoData
    data/dmr/odtok_P<mm>.tif   float32 přímý odtok Q [mm] pro každý návrhový úhrn P
    data/cn_info.json          vážené CN a objemy odtoku (m³) pro území modelu a dílčí povodí, podíl odhadu HSP
    data/cn_nahled.png
Vzorce (Janeček 2012 kap. 2; TR-55): S = 25400/CN - 254 [mm]; Ia = 0,2 S; Q = (P - Ia)^2 / (P - Ia + S) pro P > Ia.
Návrhové úhrny výchozí 20/40/60 mm = ilustrace (přívaly 1 h); skutečné N-leté úhrny pro Koryčany doplnit z ČHMÚ /
metodiky "Krátkodobé srážky pro hydrologické modelování" (ČVUT 2023) - zatím 🤔.
"""
import argparse, json, os, sys, time
import numpy as np

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="20,40,60", help="návrhové úhrny v mm, oddělené čárkou")
    a = ap.parse_args()
    import rasterio
    from pyproj import Transformer
    from matplotlib.path import Path
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); data = os.path.join(root, "data"); dmr = os.path.join(data, "dmr")
    need = ["vyuziti_kod.tif", "hsp.tif", "hsp_zdroj.tif", "povodi_id.tif", "dmr5g_5m.tif"]
    for n in need:
        if not os.path.exists(os.path.join(dmr, n)): sys.exit(f"Chybí data/dmr/{n} - spusť předchozí .bat")
    tab = json.load(open(os.path.join(data, "cn_tabulka.json"), encoding="utf-8"))
    with rasterio.open(os.path.join(dmr, "vyuziti_kod.tif")) as s:
        kod = s.read(1); prof = s.profile; transform = s.transform; H, W = s.height, s.width; res = transform.a
    with rasterio.open(os.path.join(dmr, "hsp.tif")) as s: hsp = s.read(1)
    with rasterio.open(os.path.join(dmr, "hsp_zdroj.tif")) as s: zdroj = s.read(1)
    with rasterio.open(os.path.join(dmr, "povodi_id.tif")) as s: pid = s.read(1)

    # tabulka CN: lut[kod, hsp] -> CN (výchozí varianta)
    lut = np.zeros((256, 5), np.uint8)
    for k, t in tab["tridy"].items():
        cn = t["varianty"][t["vychozi"]]["cn"]
        for i, L in enumerate("ABCD", start=1): lut[int(k), i] = cn[L]
    cn = lut[kod, hsp]
    valid = (kod > 0) & (hsp > 0)
    cn[~valid] = 0
    log(f"CN spočítáno: buněk s CN {int(valid.sum()):,}, bez CN (chybí využití nebo HSP) {int(((kod > 0) | (hsp > 0)).sum() - valid.sum()):,}")

    # území modelu
    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    gj = json.load(open(os.path.join(data, "povodi.geojson"), encoding="utf-8"))
    model = next(f for f in gj["features"] if f["properties"].get("typ") == "uzemi_modelu")
    ring = np.array([to5514.transform(x, y) for x, y in model["geometry"]["coordinates"][0]])
    gx = transform.c + (np.arange(W) + 0.5) * res; gy = transform.f - (np.arange(H) + 0.5) * res
    GX, GY = np.meshgrid(gx, gy)
    mask = Path(ring).contains_points(np.column_stack([GX.ravel(), GY.ravel()])).reshape(H, W) & valid
    cell_m2 = res * res

    prof.update(dtype="uint8", nodata=0, compress="lzw", count=1)
    with rasterio.open(os.path.join(dmr, "cn.tif"), "w", **prof) as dst: dst.write(cn, 1)

    S = np.where(valid, 25400.0 / np.maximum(cn, 1) - 254.0, np.nan); Ia = 0.2 * S
    dests = [float(x) for x in a.dest.split(",")]
    Q = {}
    for P in dests:
        q = np.where(P > Ia, (P - Ia) ** 2 / (P - Ia + S), 0.0); q = np.where(valid, q, np.nan).astype(np.float32)
        Q[P] = q
        p2 = prof.copy(); p2.update(dtype="float32", nodata=-9999)
        with rasterio.open(os.path.join(dmr, f"odtok_P{int(P)}.tif"), "w", **p2) as dst: dst.write(np.where(np.isnan(q), -9999, q).astype(np.float32), 1)

    def souhrn(m):
        n = int(m.sum())
        if n == 0: return None
        d = {"plocha_ha": round(n * cell_m2 / 1e4, 1), "cn_vazene": round(float(cn[m].mean()), 1),
             "podil_hsp_odhad_pct": round(float((zdroj[m] == 2).mean() * 100), 1),
             "hsp_podil_pct": {L: round(float((hsp[m] == i).mean() * 100), 1) for i, L in enumerate("ABCD", start=1)},
             "odtok": {}}
        for P in dests:
            qm = float(np.nanmean(Q[P][m]))
            d["odtok"][f"P{int(P)}mm"] = {"Q_mm": round(qm, 1), "objem_m3": round(qm / 1000 * n * cell_m2), "koef_odtoku": round(qm / P, 2)}
        return d
    kody = json.load(open(os.path.join(data, "rozvodnice_info.json"), encoding="utf-8")).get("povodi_id_kody", {})
    info = {"datum": time.strftime("%Y-%m-%d"), "metoda": "SCS-CN, IPS II, Ia = 0,2 S; CN = cn_tabulka.json (výchozí varianty) × vyuziti_kod × hsp",
            "navrhove_uhrny_mm": dests, "pozn_uhrny": "ilustrační úhrny; N-leté hodnoty pro Koryčany doplnit (ČHMÚ / ČVUT 2023)",
            "uzemi_modelu": souhrn(mask),
            "dilci_povodi": {kody.get(str(int(v)), str(v)): souhrn((pid == v) & mask) for v in np.unique(pid) if v > 0},
            "pozn": "Objem = Q × plocha; nepočítá se transformace vlny ani soustředění odtoku. Podíl odhadu HSP = plochy bez BPEJ doplněné nejbližší hodnotou."}
    with open(os.path.join(data, "cn_info.json"), "w", encoding="utf-8") as f: json.dump(info, f, ensure_ascii=False, indent=1)
    u = info["uzemi_modelu"]
    log(f"území modelu: CN vážené {u['cn_vazene']}, HSP {u['hsp_podil_pct']}, odhad HSP {u['podil_hsp_odhad_pct']} %")
    for k, v in u["odtok"].items(): log(f"   {k}: Q = {v['Q_mm']} mm, objem {v['objem_m3']:,} m³, koeficient {v['koef_odtoku']}")

    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 10 * H / W))
    im = ax.imshow(np.where(mask, cn, np.nan), cmap="RdYlGn_r", vmin=30, vmax=100, extent=[transform.c, transform.c + W * res, transform.f - H * res, transform.f], interpolation="nearest")
    fig.colorbar(im, ax=ax, label="CN (IPS II)", shrink=0.7)
    ax.plot(ring[:, 0], ring[:, 1], color="k", lw=1)
    xmin, ymin = ring.min(axis=0); xmax, ymax = ring.max(axis=0)
    ax.set_xlim(xmin - 300, xmax + 300); ax.set_ylim(ymin - 300, ymax + 300)
    ax.set_title(f"Číslo odtokové křivky CN - území modelu (vážené {u['cn_vazene']})")
    fig.savefig(os.path.join(data, "cn_nahled.png"), dpi=150, bbox_inches="tight"); plt.close(fig)
    log("hotovo.")

if __name__ == "__main__":
    main()
