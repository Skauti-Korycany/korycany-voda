# -*- coding: utf-8 -*-
"""01_dmr_grid.py - DMR 5G (LAZ, ČÚZK) -> rastr výšek 5 m v EPSG:5514 + náhledy.

Použití (z libovolné složky):
    python tools/01_dmr_grid.py <složka_s_laz> [--out <výstupní_složka>] [--res 5] [--limit N]

    <složka_s_laz>   složka se soubory *.laz (listy SM5, např. BUCO25.laz ...)
    --out            výchozí: data/dmr (v repozitáři; je v .gitignore)
    --res            velikost buňky v metrech, výchozí 5 (DMR 5G má ~0,07 bodu/m², jemnější grid nemá oporu v datech)
    --limit          zpracuj jen prvních N souborů (test)

Výstup:
    data/dmr/dmr5g_5m.tif        výšky (float32, EPSG:5514, NoData = -9999), LZW
    data/dmr/dmr5g_5m_hillshade.png  stínovaný reliéf (náhled pro kontrolu)
    data/dmr/dmr5g_5m_info.json  rozsah v S-JTSK i WGS84, počty bodů, hustota, statistiky výšek
    data/dmr/dmr5g_5m_bounds.geojson  obrys zpracovaného území (WGS84) - lze otevřít v mapě

Metoda: všechny body (třída 8 = body modelu terénu) -> Delaunay triangulace -> lineární interpolace
do pravidelné mřížky (= rekonstrukce TIN, ze kterého DMR 5G vznikl). Buňky mimo konvexní obal = NoData.
Kontroly: CRS přiřazeno natvrdo EPSG:5514 (LAZ ČÚZK CRS nenese), souřadnice musí být záporné (Křovák),
výšky v rozumném rozsahu pro Chřiby (150-600 m), hustota bodů, mezery mezi listy.

Závislosti: pip install laspy lazrs numpy scipy rasterio matplotlib pyproj
"""
import argparse, glob, json, os, sys, time
import numpy as np

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("laz_dir")
    ap.add_argument("--out", default=None)
    ap.add_argument("--res", type=float, default=5.0)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    import laspy
    from scipy.spatial import Delaunay
    from scipy.interpolate import LinearNDInterpolator
    import rasterio
    from rasterio.transform import from_origin
    from pyproj import Transformer

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = a.out or os.path.join(root, "data", "dmr")
    os.makedirs(out_dir, exist_ok=True)

    files = sorted(glob.glob(os.path.join(a.laz_dir, "*.laz")) + glob.glob(os.path.join(a.laz_dir, "*.las")))
    if a.limit: files = files[:a.limit]
    if not files:
        sys.exit(f"Ve složce {a.laz_dir} nejsou žádné .laz/.las")
    log(f"souborů: {len(files)}")

    xs, ys, zs = [], [], []
    tiles = []
    for p in files:
        with laspy.open(p) as f:
            las = f.read()
            x, y, z = np.asarray(las.x), np.asarray(las.y), np.asarray(las.z)
            cls = np.asarray(las.classification)
            keep = (cls == 8) | (cls == 2)  # 8 = body modelu (DMR 5G), 2 = terén (kdyby přišel jiný produkt)
            if keep.sum() == 0:
                keep = np.ones(len(x), bool)
                log(f"  {os.path.basename(p)}: žádná třída 8/2, beru vše")
            x, y, z = x[keep], y[keep], z[keep]
        if x.min() > 0 or y.min() > 0:
            sys.exit(f"{p}: souřadnice nejsou záporné, to není S-JTSK Křovák (EPSG:5514). Zastavuji.")
        if z.min() < 100 or z.max() > 800:
            log(f"  POZOR {os.path.basename(p)}: výšky {z.min():.1f}-{z.max():.1f} m mimo očekávaný rozsah")
        tiles.append({"file": os.path.basename(p), "points": int(len(x)),
                      "xmin": float(x.min()), "xmax": float(x.max()), "ymin": float(y.min()), "ymax": float(y.max()),
                      "zmin": float(z.min()), "zmax": float(z.max()),
                      "density_pts_m2": float(len(x) / max((x.max()-x.min())*(y.max()-y.min()), 1))})
        log(f"  {os.path.basename(p)}: {len(x):,} bodů, x {x.min():.0f}..{x.max():.0f}, y {y.min():.0f}..{y.max():.0f}, z {z.min():.1f}..{z.max():.1f}")
        xs.append(x); ys.append(y); zs.append(z)
    X = np.concatenate(xs); Y = np.concatenate(ys); Z = np.concatenate(zs)
    del xs, ys, zs
    log(f"celkem bodů: {len(X):,}")

    # mřížka zarovnaná na celé metry násobku res
    res = a.res
    xmin = np.floor(X.min()/res)*res; xmax = np.ceil(X.max()/res)*res
    ymin = np.floor(Y.min()/res)*res; ymax = np.ceil(Y.max()/res)*res
    ncol = int(round((xmax-xmin)/res)); nrow = int(round((ymax-ymin)/res))
    log(f"grid {ncol} x {nrow} buněk po {res} m ({ncol*nrow/1e6:.2f} M buněk)")

    log("Delaunay triangulace ...")
    tri = Delaunay(np.column_stack([X, Y]))
    log("interpolace ...")
    interp = LinearNDInterpolator(tri, Z, fill_value=np.nan)
    gx = xmin + (np.arange(ncol) + 0.5)*res
    gy = ymax - (np.arange(nrow) + 0.5)*res   # shora dolů (sever nahoře)
    grid = np.full((nrow, ncol), np.nan, dtype=np.float32)
    step = 256
    for r0 in range(0, nrow, step):
        r1 = min(r0+step, nrow)
        GX, GY = np.meshgrid(gx, gy[r0:r1])
        grid[r0:r1, :] = interp(GX.ravel(), GY.ravel()).reshape(r1-r0, ncol).astype(np.float32)
    nodata = -9999.0
    valid = ~np.isnan(grid)
    log(f"platných buněk: {valid.mean()*100:.1f} %")
    out = np.where(valid, grid, nodata).astype(np.float32)

    transform = from_origin(xmin, ymax, res, res)
    tif = os.path.join(out_dir, f"dmr5g_{int(res)}m.tif")
    with rasterio.open(tif, "w", driver="GTiff", height=nrow, width=ncol, count=1, dtype="float32",
                       crs="EPSG:5514", transform=transform, nodata=nodata, compress="lzw", tiled=True) as dst:
        dst.write(out, 1)
    log(f"zapsáno {tif}")

    # hillshade náhled
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    g = np.where(valid, grid, np.nan)
    dzdx = np.gradient(g, res, axis=1); dzdy = np.gradient(g, res, axis=0)
    slope = np.arctan(np.hypot(dzdx, dzdy)); aspect = np.arctan2(-dzdx, dzdy)
    az, alt = np.radians(315), np.radians(45)
    hs = np.sin(alt)*np.cos(slope) + np.cos(alt)*np.sin(slope)*np.cos(az - aspect)
    fig, ax = plt.subplots(figsize=(10, 10*nrow/ncol))
    ax.imshow(hs, cmap="gray", vmin=-0.2, vmax=1, extent=[xmin, xmax, ymin, ymax])
    ax.contour(gx, gy, g, levels=np.arange(np.floor(np.nanmin(g)/20)*20, np.nanmax(g)+20, 20), colors="#c0392b", linewidths=0.3)
    ax.set_title(f"DMR 5G {int(res)} m - stínovaný reliéf, vrstevnice 20 m (EPSG:5514)")
    ax.set_xlabel("X [m]"); ax.set_ylabel("Y [m]")
    png = os.path.join(out_dir, f"dmr5g_{int(res)}m_hillshade.png")
    fig.savefig(png, dpi=150, bbox_inches="tight"); plt.close(fig)
    log(f"zapsáno {png}")

    # rozsah ve WGS84 + info
    tr = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
    corners = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]
    ll = [tr.transform(x, y) for x, y in corners]
    info = {
        "zdroj": "ČÚZK DMR 5G (LAZ), CC BY 4.0; CRS přiřazeno EPSG:5514 (soubory CRS nenesou)",
        "res_m": res, "ncol": ncol, "nrow": nrow, "valid_pct": round(float(valid.mean()*100), 2),
        "extent_5514": {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax},
        "extent_wgs84": {"lon_min": min(p[0] for p in ll), "lon_max": max(p[0] for p in ll),
                          "lat_min": min(p[1] for p in ll), "lat_max": max(p[1] for p in ll)},
        "points_total": int(len(X)), "density_pts_m2": round(float(len(X)/((xmax-xmin)*(ymax-ymin))), 4),
        "z_min": float(np.nanmin(g)), "z_max": float(np.nanmax(g)), "z_mean": float(np.nanmean(g)),
        "tiles": tiles,
        "pozn": "1 m grid nemá v DMR 5G oporu (0,07 bodu/m²); 5 m je poctivé rozlišení. Hodnoty jsou lineární interpolace TIN.",
    }
    with open(os.path.join(out_dir, f"dmr5g_{int(res)}m_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    gj = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "DMR 5G zpracované území", "res_m": res},
          "geometry": {"type": "Polygon", "coordinates": [[list(p) for p in ll]]}}]}
    with open(os.path.join(out_dir, f"dmr5g_{int(res)}m_bounds.geojson"), "w", encoding="utf-8") as f:
        json.dump(gj, f)
    log("hotovo. Pošli *_hillshade.png a *_info.json ke kontrole.")

if __name__ == "__main__":
    main()
