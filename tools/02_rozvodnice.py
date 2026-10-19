# -*- coding: utf-8 -*-
"""02_rozvodnice.py - z rastru terénu (dmr5g_5m.tif) odvodí odtok vody a rozvodnice.

Použití (z libovolné složky):
    python tools/02_rozvodnice.py [--dem data/dmr/dmr5g_5m.tif] [--out data/dmr] [--body data/rozvodnice_body.json]
                                  [--tok-km2 0.25]

    --dem      vstupní rastr výšek (výchozí data/dmr/dmr5g_5m.tif z kroku 01)
    --out      složka pro rastry a náhledy (výchozí data/dmr, je v .gitignore)
    --body     JSON s uzávěrovými body (výchozí data/rozvodnice_body.json; když chybí, použijí se
               body vestavěné níže a soubor se vytvoří - pak ho stačí upravit a skript pustit znovu)
    --tok-km2  od jaké plochy povodí (km²) kreslit vodní tok; výchozí 0,25 km²

Výstupy (rastry, EPSG:5514, 5 m, stejná mřížka jako DEM):
    data/dmr/smer_odtoku.tif      D8 směr odtoku, uint8: 1=V 2=JV 4=J 8=JZ 16=Z 32=SZ 64=S 128=SV, 0=nikam (okraj, NoData)
    data/dmr/akumulace.tif        kolik buněk odtéká přes buňku (float32; × 25 m² = plocha povodí)
    data/dmr/sklon_deg.tif        sklon ve stupních (Horn 3×3) z původního terénu
    data/dmr/expozice_deg.tif     expozice ve stupních od severu po směru hodin, -1 = rovina
    data/dmr/deprese.tif          hloubka vyplněných prohlubní v m (kde voda stojí, než přeteče)
    data/dmr/povodi_id.tif        id dílčího povodí (uint8, 0 = mimo), kódy v rozvodnice_info.json
Výstupy lehké (do gitu, WGS84):
    data/povodi.geojson           polygony: celé povodí k hlavnímu profilu + dílčí povodí sídel
    data/toky_dmr.geojson         údolnice (vodní toky odvozené z terénu, plocha >= --tok-km2)
    data/rozvodnice_body.json     uzávěrové body (vstup, upravitelný)
    data/rozvodnice_info.json     plochy, souřadnice přichycených bodů, kontroly
Náhledy (data/dmr, kopie do docs/img po kontrole):
    rozvodnice_nahled.png         reliéf + toky + hranice povodí + body
    sklon_nahled.png              sklon

Metoda:
  1. Vyplnění prohlubní "priority-flood" s malým spádem (Barnes et al. 2014), aby každá buňka
     měla kam odtéct. Hloubka vyplnění = vrstva deprese.tif.
  2. D8: každá buňka teče do nejstrmějšího z 8 sousedů (O'Callaghan & Mark 1984).
  3. Akumulace: součet buněk proti proudu (zpracováno od nejvyšší buňky k nejnižší).
  4. Uzávěrový bod se přichytí k buňce s největší akumulací v okruhu `polomer_m` (jinak by
     trefil svah vedle toku). Povodí = všechny buňky, které přes něj protečou.
  5. Toky = buňky s akumulací nad prahem, vedené po směru odtoku do linií.
Žádné externí hydrologické knihovny (whitebox, pysheds): jen numpy, scipy, rasterio, pyproj, matplotlib.
Čistý Python je u vyplňování pomalejší (minuty), ale nic se nestahuje a nic nepadá.

Závislosti: pip install numpy scipy rasterio matplotlib pyproj
"""
import argparse, heapq, json, os, sys, time
import numpy as np

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

# ---------------------------------------------------------------------------
# Vestavěné uzávěrové body (WGS84 lon, lat). Jsou to ODHADY z mapy, ne měření.
# Po prvním běhu se zapíší do data/rozvodnice_body.json; opravy dělej tam.
# "polomer_m": v jakém okruhu smí skript hledat buňku s největší akumulací (= koryto).
# "min_km2": když přichycená buňka má menší povodí, je bod vedle toku -> skript to ohlásí.
# ---------------------------------------------------------------------------
VYCHOZI_BODY = {
  "pozn": "Bod má buď 'lonlat' (WGS84 [lon, lat]) nebo 'xy5514' (S-JTSK [X, Y]). Přichytí se ke korytu "
          "(buňka s největší akumulací) v okruhu polomer_m. Uprav a spusť skript znovu.",
  "hlavni": {"nazev": "Kyjovka pod Koryčany (pod soutokem se Stříbrníkem)", "pod_soutokem_id": 2, "min_km2": 15,
             "pozn": "bod se najde automaticky: od profilu Stříbrník (id 2) po proudu až k soutoku s Kyjovkou, "
                     "první buňka za soutokem. Chceš-li jiný profil, nahraď 'pod_soutokem_id' klíčem 'xy5514' nebo 'lonlat'."},
  "sidla": [
    {"id": 1, "nazev": "Koryčany (Kyjovka, ř. km 75,69)", "xy5514": [-558794.48, -1173991.39], "polomer_m": 60, "min_km2": 10,
     "zdroj": "edpp.cz, hlásné profily ORP Kroměříž (kat. C, město Koryčany); souřadnice z odkazu na mapu"},
    {"id": 2, "nazev": "Koryčany (Stříbrník, ř. km 1,07)", "xy5514": [-559180.53, -1174691.52], "polomer_m": 150, "min_km2": 2,
     "zdroj": "edpp.cz, hlásný profil kat. C"},
    {"id": 3, "nazev": "VN Koryčany (Kyjovka pod přehradou, ř. km 77,76)", "xy5514": [-556751.96, -1173879.95], "polomer_m": 80,
     "min_km2": 5, "zdroj": "edpp.cz, hlásný profil kat. A (Povodí Moravy)"},
    {"id": 4, "nazev": "Lískovec", "lonlat": [17.1808, 49.1236], "polomer_m": 300, "min_km2": 0.3,
     "zdroj": "střed obce cs.wikipedia; bod = tok procházející obcí"},
    {"id": 5, "nazev": "Blišice", "lonlat": [17.1656, 49.1228], "polomer_m": 300, "min_km2": 0.3,
     "zdroj": "střed obce cs.wikipedia; bod = tok procházející obcí"},
    {"id": 6, "nazev": "Jestřabice", "lonlat": [17.1297, 49.0919], "polomer_m": 300, "min_km2": 0.3,
     "zdroj": "střed obce cs.wikipedia (soutok Jestřabického potoka a Kratinky); mimo povodí Kyjovky nad Koryčany"},
  ]
}

# D8 sousedé: (dřádek, dsloupec, kód, vzdálenost)
D8 = [(0, 1, 1, 1.0), (1, 1, 2, 2**0.5), (1, 0, 4, 1.0), (1, -1, 8, 2**0.5),
      (0, -1, 16, 1.0), (-1, -1, 32, 2**0.5), (-1, 0, 64, 1.0), (-1, 1, 128, 2**0.5)]

def priority_flood(dem, valid, eps=1e-4):
    """Vyplní prohlubně tak, aby z každé platné buňky vedla cesta dolů k okraji (Barnes 2014, s epsilonem).
    Vrací vyplněný terén (float64). Čistý Python + heapq: ~1-2 min na 2,4 M buněk."""
    nrow, ncol = dem.shape
    filled = np.full(dem.shape, np.inf)
    closed = ~valid              # NoData bereme jako "hotové" (voda do nich může odtéct)
    heap = []
    # semena: platné buňky na okraji rastru nebo sousedící s NoData
    from scipy.ndimage import binary_dilation
    edge = np.zeros(dem.shape, bool)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    edge |= binary_dilation(~valid, structure=np.ones((3, 3), bool))
    seeds = np.argwhere(edge & valid)
    for r, c in seeds:
        filled[r, c] = dem[r, c]
        closed[r, c] = True
        heapq.heappush(heap, (dem[r, c], int(r), int(c)))
    demf = dem  # lokální aliasy kvůli rychlosti
    push, pop = heapq.heappush, heapq.heappop
    n_done = 0; total = int(valid.sum())
    while heap:
        z, r, c = pop(heap)
        n_done += 1
        if n_done % 500000 == 0:
            log(f"  vyplňování {n_done/total*100:.0f} %")
        for dr, dc, _, _ in D8:
            rr, cc = r + dr, c + dc
            if rr < 0 or rr >= nrow or cc < 0 or cc >= ncol or closed[rr, cc]:
                continue
            closed[rr, cc] = True
            zz = demf[rr, cc]
            if zz < z + eps:
                zz = z + eps
            filled[rr, cc] = zz
            push(heap, (zz, rr, cc))
    return filled

def d8_direction(filled, valid):
    """Směr do nejstrmějšího nižšího souseda. Vrací (kód uint8, index příjemce int64 nebo -1)."""
    nrow, ncol = filled.shape
    best_drop = np.full(filled.shape, 0.0)
    code = np.zeros(filled.shape, np.uint8)
    recv = np.full(filled.shape, -1, np.int64)
    idx = np.arange(nrow * ncol).reshape(nrow, ncol)
    big = np.full(filled.shape, np.inf)  # okraj = nekonečně vysoký
    for dr, dc, k, dist in D8:
        nb = big.copy()
        nb[max(0, -dr):nrow - max(0, dr), max(0, -dc):ncol - max(0, dc)] = \
            filled[max(0, dr):nrow - max(0, -dr), max(0, dc):ncol - max(0, -dc)]
        nidx = np.full(filled.shape, -1, np.int64)
        nidx[max(0, -dr):nrow - max(0, dr), max(0, -dc):ncol - max(0, dc)] = \
            idx[max(0, dr):nrow - max(0, -dr), max(0, dc):ncol - max(0, -dc)]
        with np.errstate(invalid="ignore"):
            drop = (filled - nb) / dist
        better = (drop > best_drop) & valid & np.isfinite(nb)
        best_drop[better] = drop[better]
        code[better] = k
        recv[better] = nidx[better]
    # buňky, které tečou do NoData, berou kód 0 (odtok ven)
    rflat = recv.ravel(); vflat = valid.ravel()
    out = (rflat >= 0) & ~vflat[np.clip(rflat, 0, None)]
    rflat[out] = -1
    code.ravel()[out] = 0
    return code, recv

def accumulate(filled, recv, valid):
    """Počet buněk, které protečou každou buňkou (včetně jí samé)."""
    order = np.argsort(filled.ravel(), kind="stable")[::-1]   # od nejvyšší
    order = order[valid.ravel()[order]]
    acc = np.where(valid, 1.0, 0.0).ravel()
    r = recv.ravel()
    for i in order.tolist():
        j = r[i]
        if j >= 0:
            acc[j] += acc[i]
    return acc.reshape(filled.shape)

def label_basins(filled, recv, valid, outlets):
    """outlets: {id: flat_index}. Vrací rastr id (uint8). Zpracování od nejnižší buňky nahoru:
    buňka dědí id svého příjemce, uzávěrová buňka má id pevně."""
    lab = np.zeros(filled.size, np.uint8)
    fixed = np.zeros(filled.size, bool)
    for k, i in outlets.items():
        lab[i] = k; fixed[i] = True
    order = np.argsort(filled.ravel(), kind="stable")
    order = order[valid.ravel()[order]]
    r = recv.ravel()
    for i in order.tolist():
        if fixed[i]:
            continue
        j = r[i]
        if j >= 0:
            lab[i] = lab[j]
    return lab.reshape(filled.shape)

def snap(acc, transform, x, y, radius_m, res):
    """Najde buňku s největší akumulací v okruhu radius_m kolem (x, y) v EPSG:5514."""
    col = int((x - transform.c) / res); row = int((transform.f - y) / res)
    n = int(np.ceil(radius_m / res))
    r0, r1 = max(0, row - n), min(acc.shape[0], row + n + 1)
    c0, c1 = max(0, col - n), min(acc.shape[1], col + n + 1)
    if r1 <= r0 or c1 <= c0:
        return None
    win = acc[r0:r1, c0:c1].copy()
    rr, cc = np.mgrid[r0:r1, c0:c1]
    dist = np.hypot((rr - row) * res, (cc - col) * res)
    win[dist > radius_m] = -1
    k = np.unravel_index(np.argmax(win), win.shape)
    return int(rr[k]), int(cc[k]), float(dist[k])

def slope_aspect(dem, valid, res):
    """Horn (1981) 3×3. Sklon ve stupních, expozice 0-360 od severu po směru hodin, -1 rovina."""
    from scipy.ndimage import convolve
    g = np.where(valid, dem, np.nan)
    # okraje: doplníme nejbližší hodnotou, aby konvoluce nedělala NaN
    gf = np.where(np.isnan(g), np.nanmean(g), g)
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float) / (8 * res)
    ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], float) / (8 * res)   # řádky jdou shora (sever) dolů
    dzdx = convolve(gf, kx, mode="nearest"); dzdy = convolve(gf, ky, mode="nearest")
    slope = np.degrees(np.arctan(np.hypot(dzdx, dzdy)))
    # expozice = azimut, kam svah klesá: vektor (-dzdx, -dzdy) = (východ, sever)
    aspect = np.degrees(np.arctan2(-dzdx, -dzdy)) % 360
    aspect[np.hypot(dzdx, dzdy) < 1e-6] = -1
    # buňky s NaN sousedy raději vynulovat
    from scipy.ndimage import binary_dilation
    bad = binary_dilation(~valid, structure=np.ones((3, 3), bool))
    slope[bad] = np.nan; aspect[bad] = np.nan
    return slope.astype(np.float32), aspect.astype(np.float32)

def douglas_peucker(pts, tol):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    P = np.array(pts[1:-1])
    ab = b - a; L = np.hypot(*ab)
    if L == 0:
        d = np.hypot(*(P - a).T)
    else:
        d = np.abs(ab[0] * (P[:, 1] - a[1]) - ab[1] * (P[:, 0] - a[0])) / L
    k = int(np.argmax(d))
    if d[k] > tol:
        left = douglas_peucker(pts[:k + 2], tol); right = douglas_peucker(pts[k + 1:], tol)
        return left[:-1] + right
    return [pts[0], pts[-1]]

def trace_streams(acc, recv, thresh_cells, transform, res):
    """Vede linie toků: start = buňka toku bez přítoku toku, konec = soutok nebo odtok."""
    stream = acc >= thresh_cells
    sidx = np.flatnonzero(stream.ravel())
    r = recv.ravel()
    donors = np.zeros(acc.size, np.int32)
    tgt = r[sidx]; tgt = tgt[tgt >= 0]
    np.add.at(donors, tgt, 1)
    heads = sidx[donors[sidx] == 0]
    ncol = acc.shape[1]
    def xy(i):
        rr, cc = divmod(int(i), ncol)
        return (transform.c + (cc + 0.5) * res, transform.f - (rr + 0.5) * res)
    lines = []
    visited = np.zeros(acc.size, bool)
    for h in heads.tolist():
        pts = [xy(h)]; i = h; visited[h] = True
        while True:
            j = r[i]
            if j < 0:
                break
            pts.append(xy(j))
            if donors[j] >= 2 or visited[j]:
                # soutok: linie končí, pokračování vede jen jednou
                if not visited[j]:
                    visited[j] = True
                    lines.append(pts); pts = [xy(j)]; i = j
                    continue
                break
            visited[j] = True
            i = j
        if len(pts) > 1:
            lines.append(pts)
    # přepočet: každá linie dostane plochu povodí na konci (km²) a stupeň
    out = []
    for pts in lines:
        out.append({"pts": douglas_peucker(pts, res * 0.8), "km2_konec": None})
    return out, stream

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dem", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--body", default=None)
    ap.add_argument("--tok-km2", type=float, default=0.25)
    a = ap.parse_args()

    import rasterio
    from rasterio.features import shapes
    from pyproj import Transformer

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dem_path = a.dem or os.path.join(root, "data", "dmr", "dmr5g_5m.tif")
    out_dir = a.out or os.path.join(root, "data", "dmr")
    data_dir = os.path.join(root, "data")
    body_path = a.body or os.path.join(data_dir, "rozvodnice_body.json")
    os.makedirs(out_dir, exist_ok=True)
    if not os.path.exists(dem_path):
        sys.exit(f"Chybí terén {dem_path}. Nejdřív spusť vyrob_teren.bat.")

    if os.path.exists(body_path):
        with open(body_path, encoding="utf-8") as f:
            body = json.load(f)
        log(f"uzávěrové body z {body_path}")
    else:
        body = VYCHOZI_BODY
        with open(body_path, "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=1)
        log(f"uzávěrové body vestavěné, zapsány do {body_path} (uprav a spusť znovu)")

    with rasterio.open(dem_path) as src:
        dem = src.read(1).astype(np.float64)
        nodata = src.nodata
        transform = src.transform
        res = transform.a
        crs = src.crs
        profile = src.profile
    valid = np.isfinite(dem) & (dem != nodata) if nodata is not None else np.isfinite(dem)
    nrow, ncol = dem.shape
    log(f"DEM {ncol} x {nrow}, res {res} m, platných {valid.mean()*100:.1f} %")

    to_wgs = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    to_sjtsk = Transformer.from_crs("EPSG:4326", crs, always_xy=True)

    log("1/6 vyplňování prohlubní ...")
    filled = priority_flood(dem, valid)
    deprese = np.where(valid, filled - dem, np.nan).astype(np.float32)
    log(f"   max. hloubka vyplnění {np.nanmax(deprese):.2f} m, buněk s vyplněním > 0,2 m: {(deprese > 0.2).sum():,}")

    log("2/6 směr odtoku (D8) ...")
    code, recv = d8_direction(filled, valid)
    log("3/6 akumulace ...")
    acc = accumulate(filled, recv, valid)
    cell_km2 = res * res / 1e6
    log(f"   max. akumulace {acc.max():,.0f} buněk = {acc.max()*cell_km2:.2f} km²")

    log("4/6 sklon a expozice ...")
    slope, aspect = slope_aspect(dem, valid, res)

    log("5/6 uzávěrové body a povodí ...")
    thresh = int(round(a.tok_km2 / cell_km2))
    info_pts = []
    outlets = {}
    def resolve(p, pid):
        if "pod_soutokem_id" in p:
            start = outlets.get(int(p["pod_soutokem_id"]))
            rec = {"id": pid, "nazev": p["nazev"], "pozn": p.get("pozn", "")}
            if start is None:
                rec["stav"] = "CHYBA: bod s id pod_soutokem_id se nenašel"; info_pts.append(rec); return None
            a0 = acc.ravel()[start]; i = start; r = recv.ravel(); steps = 0
            while r[i] >= 0 and acc.ravel()[r[i]] < 3 * a0 and steps < 100000:
                i = r[i]; steps += 1
            if r[i] < 0:
                rec["stav"] = "CHYBA: soutok nenalezen (tok opustil rastr dřív)"; info_pts.append(rec); return None
            i = r[i]                       # první buňka za soutokem
            rr, cc = divmod(int(i), ncol)
            X = transform.c + (cc + 0.5) * res; Y = transform.f - (rr + 0.5) * res
            LON, LAT = to_wgs.transform(X, Y); km2 = float(acc[rr, cc] * cell_km2)
            rec.update({"prichyceno_lonlat": [round(LON, 6), round(LAT, 6)], "prichyceno_5514": [round(X, 1), round(Y, 1)],
                        "posun_m": 0, "plocha_km2": round(km2, 3), "vyska_m": round(float(dem[rr, cc]), 1),
                        "stav": "ok" if km2 >= p.get("min_km2", 0) else "POZOR: malé povodí"})
            info_pts.append(rec)
            return int(i)
        if "xy5514" in p:
            x, y = p["xy5514"]; lon, lat = to_wgs.transform(x, y)
        else:
            lon, lat = p["lonlat"]; x, y = to_sjtsk.transform(lon, lat)
        s = snap(acc, transform, x, y, p.get("polomer_m", 150), res)
        rec = {"id": pid, "nazev": p["nazev"], "zadano_lonlat": [round(lon, 6), round(lat, 6)],
               "zadano_5514": [round(x, 1), round(y, 1)], "zdroj": p.get("zdroj", ""), "pozn": p.get("pozn", "")}
        if s is None:
            rec["stav"] = "MIMO RASTR"; info_pts.append(rec); return None
        rr, cc, dist = s
        km2 = float(acc[rr, cc] * cell_km2)
        X = transform.c + (cc + 0.5) * res; Y = transform.f - (rr + 0.5) * res
        LON, LAT = to_wgs.transform(X, Y)
        rec.update({"prichyceno_lonlat": [round(LON, 6), round(LAT, 6)], "prichyceno_5514": [round(X, 1), round(Y, 1)],
                    "posun_m": round(dist, 1), "plocha_km2": round(km2, 3), "vyska_m": round(float(dem[rr, cc]), 1),
                    "stav": "ok" if km2 >= p.get("min_km2", 0) else "POZOR: malé povodí, bod je asi vedle toku"})
        info_pts.append(rec)
        return rr * ncol + cc
    for p in body["sidla"]:
        i = resolve(p, int(p["id"]))
        if i is not None:
            outlets[int(p["id"])] = i
    main_idx = resolve(body["hlavni"], 0)
    # hlavní povodí zvlášť (dílčí povodí jsou v něm vnořená)
    main_lab = label_basins(filled, recv, valid, {1: main_idx}) if main_idx is not None else np.zeros(dem.shape, np.uint8)
    sidla_lab = label_basins(filled, recv, valid, outlets) if outlets else np.zeros(dem.shape, np.uint8)
    # odtok z celého rastru: buňka s největší akumulací vůbec (kde hlavní tok opouští území)
    imax = int(np.argmax(acc)); rmax, cmax = divmod(imax, ncol)
    lonm, latm = to_wgs.transform(transform.c + (cmax + 0.5) * res, transform.f - (rmax + 0.5) * res)

    log("6/6 toky a zápis ...")
    lines, stream = trace_streams(acc, recv, thresh, transform, res)

    # --- rastry
    def write(name, arr, dtype, nodata_val):
        prof = profile.copy()
        prof.update(dtype=dtype, nodata=nodata_val, compress="lzw", tiled=True, count=1)
        p = os.path.join(out_dir, name)
        with rasterio.open(p, "w", **prof) as dst:
            dst.write(arr.astype(dtype), 1)
        log(f"   zapsáno {p}")
    write("smer_odtoku.tif", code, "uint8", 255)
    write("akumulace.tif", np.where(valid, acc, -1).astype(np.float32), "float32", -1)
    write("sklon_deg.tif", np.where(np.isnan(slope), -9999, slope), "float32", -9999)
    write("expozice_deg.tif", np.where(np.isnan(aspect), -9999, aspect), "float32", -9999)
    write("deprese.tif", np.where(np.isnan(deprese), -9999, deprese), "float32", -9999)
    write("povodi_id.tif", sidla_lab, "uint8", 0)

    # --- GeoJSON polygony (WGS84)
    def poly_features(lab, names):
        feats = []
        for geom, val in shapes(lab.astype(np.int32), mask=lab > 0, transform=transform):
            # vezmeme jen největší polygon na id (drobné ostrůvky vynecháme); plocha se počítá z rastru
            feats.append((int(val), geom))
        out = []
        for val, nm in names.items():
            cand = [g for v, g in feats if v == val]
            if not cand:
                continue
            def area(g):
                x, y = zip(*g["coordinates"][0]); x = np.array(x); y = np.array(y)
                return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
            g = max(cand, key=area)
            rings = []
            for ring in g["coordinates"]:
                ring = douglas_peucker([tuple(p) for p in ring], res * 0.6)
                if ring[0] != ring[-1]:
                    ring.append(ring[0])
                rings.append([list(to_wgs.transform(x, y)) for x, y in ring])
            km2 = float((lab == val).sum() * cell_km2)
            tot = total_km2.get(val, km2)
            out.append({"type": "Feature", "properties": {"id": val, "nazev": nm,
                        "plocha_vlastni_km2": round(km2, 3), "plocha_celkem_km2": round(tot, 3),
                        "pozn": "vlastní = bez vnořených dílčích povodí; celkem = vše nad bodem",
                        "ostruvku_vynechano": len(cand) - 1},
                        "geometry": {"type": "Polygon", "coordinates": [[[round(a, 6), round(b, 6)] for a, b in r] for r in rings]}})
        return out
    total_km2 = {int(p["id"]): p["plocha_km2"] for p in info_pts if "plocha_km2" in p}
    feats = []
    if main_idx is not None:
        total_km2[1] = total_km2.get(0, 0)
        feats += poly_features(main_lab, {1: body["hlavni"]["nazev"]})
        for f in feats: f["properties"]["typ"] = "hlavni"
    total_km2 = {int(p["id"]): p["plocha_km2"] for p in info_pts if "plocha_km2" in p and p["id"] > 0}
    sub = poly_features(sidla_lab, {int(p["id"]): p["nazev"] for p in body["sidla"]})
    for f in sub: f["properties"]["typ"] = "sidlo"
    feats += sub
    # celé území odvodňované přes buňku s největší akumulací (kde hlavní tok opouští rastr)
    cele_lab = label_basins(filled, recv, valid, {1: imax})
    total_km2 = {1: float(acc.max() * cell_km2)}
    cele = poly_features(cele_lab, {1: "celé povodí k výstupu z rastru"})
    for f in cele: f["properties"]["typ"] = "cele_uzemi"
    feats += cele
    gj = {"type": "FeatureCollection", "name": "povodi",
          "zdroj": "odvozeno z ČÚZK DMR 5G (CC BY 4.0), skript tools/02_rozvodnice.py", "features": feats}
    with open(os.path.join(data_dir, "povodi.geojson"), "w", encoding="utf-8") as f:
        json.dump(gj, f, ensure_ascii=False)
    log(f"   zapsáno data/povodi.geojson ({len(feats)} polygonů)")

    # --- GeoJSON toky
    tf = []
    for ln in lines:
        pts = ln["pts"]
        # plocha povodí na konci linie
        cc = int((pts[-1][0] - transform.c) / res); rr = int((transform.f - pts[-1][1]) / res)
        km2 = float(acc[min(rr, nrow-1), min(cc, ncol-1)] * cell_km2)
        tf.append({"type": "Feature", "properties": {"km2_na_konci": round(km2, 3)},
                   "geometry": {"type": "LineString", "coordinates": [[round(a, 6), round(b, 6)] for a, b in
                                (to_wgs.transform(x, y) for x, y in pts)]}})
    with open(os.path.join(data_dir, "toky_dmr.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "name": "toky_dmr", "prah_km2": a.tok_km2,
                   "zdroj": "údolnice z DMR 5G (CC BY 4.0), ne DIBAVOD; skript tools/02_rozvodnice.py",
                   "features": tf}, f, ensure_ascii=False)
    log(f"   zapsáno data/toky_dmr.geojson ({len(tf)} linií)")

    # --- info
    info = {
        "zdroj_dem": os.path.relpath(dem_path, root), "res_m": res, "ncol": ncol, "nrow": nrow,
        "metoda": "priority-flood fill (eps 1e-4 m) -> D8 -> akumulace; sklon Horn 3x3; toky >= prah",
        "prah_toku_km2": a.tok_km2,
        "uzaverove_body": info_pts,
        "povodi_id_kody": {str(int(p["id"])): p["nazev"] for p in body["sidla"]},
        "odtok_z_rastru": {"lonlat": [round(lonm, 6), round(latm, 6)], "plocha_km2": round(float(acc.max() * cell_km2), 2),
                           "pozn": "buňka s největší akumulací = kde hlavní tok opouští rastr"},
        "deprese": {"max_hloubka_m": round(float(np.nanmax(deprese)), 2),
                    "plocha_nad_0_2m_ha": round(float((deprese > 0.2).sum() * res * res / 1e4), 1),
                    "pozn": "obsahuje i hladinu VN Koryčany a umělé prohlubně (silniční zářezy, lomy)"},
        "sklon": {"prumer_deg": round(float(np.nanmean(slope)), 2), "podil_nad_12deg_pct": round(float(np.nanmean(slope > 12) * 100), 1)},
        "kontrola": "Zkontroluj rozvodnice_nahled.png: toky mají ležet v údolích, body na tocích, hranice po hřebenech.",
    }
    with open(os.path.join(data_dir, "rozvodnice_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    for p in info_pts:
        log(f"   {p['nazev']}: {p['stav']}, povodí {p.get('plocha_km2','?')} km², posun {p.get('posun_m','?')} m")

    # --- náhled
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    g = np.where(valid, dem, np.nan)
    dzdx = np.gradient(g, res, axis=1); dzdy = np.gradient(g, res, axis=0)
    sl = np.arctan(np.hypot(dzdx, dzdy)); asp = np.arctan2(-dzdx, dzdy)
    az, alt = np.radians(315), np.radians(45)
    hs = np.sin(alt)*np.cos(sl) + np.cos(alt)*np.sin(sl)*np.cos(az - asp)
    xmin, xmax = transform.c, transform.c + ncol * res
    ymin, ymax = transform.f - nrow * res, transform.f
    ext = [xmin, xmax, ymin, ymax]
    fig, ax = plt.subplots(figsize=(11, 11 * nrow / ncol))
    ax.imshow(hs, cmap="gray", vmin=-0.2, vmax=1, extent=ext)
    cols = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
    if outlets:
        over = np.where(sidla_lab > 0, sidla_lab, np.nan)
        ax.imshow(over, cmap=ListedColormap(cols[:max(outlets)]), vmin=1, vmax=max(outlets), alpha=0.25, extent=ext, interpolation="nearest")
        ax.contour(np.where(sidla_lab > 0, sidla_lab, 0), levels=np.arange(0.5, max(outlets) + 1), colors="k", linewidths=0.6,
                   extent=ext, origin="upper")
    if main_idx is not None:
        ax.contour(main_lab, levels=[0.5], colors="#d62728", linewidths=1.8, extent=ext, origin="upper")
    for ln in lines:
        x, y = zip(*ln["pts"])
        ax.plot(x, y, color="#0b3d91", linewidth=0.6)
    for p in info_pts:
        if "prichyceno_5514" in p:
            X, Y = p["prichyceno_5514"]
            ax.plot(X, Y, "o", color="yellow", markeredgecolor="k", markersize=7)
            ax.annotate(f"{p['nazev']} {p['plocha_km2']:.1f} km²", (X, Y), xytext=(6, 6), textcoords="offset points",
                        fontsize=8, bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8))
    ax.set_title(f"Rozvodnice z DMR 5G {int(res)} m - toky (>= {a.tok_km2} km²), hlavní povodí (červeně), dílčí povodí sídel")
    ax.set_xlabel("X [m] EPSG:5514"); ax.set_ylabel("Y [m]")
    png = os.path.join(out_dir, "rozvodnice_nahled.png")
    fig.savefig(png, dpi=150, bbox_inches="tight"); plt.close(fig)
    log(f"   zapsáno {png}")
    fig, ax = plt.subplots(figsize=(10, 10 * nrow / ncol))
    im = ax.imshow(slope, cmap="YlOrRd", vmin=0, vmax=30, extent=ext)
    fig.colorbar(im, ax=ax, label="sklon [°]", shrink=0.7)
    for ln in lines:
        x, y = zip(*ln["pts"]); ax.plot(x, y, color="#0b3d91", linewidth=0.4)
    ax.set_title("Sklon terénu (Horn 3×3, DMR 5G 5 m)")
    png2 = os.path.join(out_dir, "sklon_nahled.png")
    fig.savefig(png2, dpi=150, bbox_inches="tight"); plt.close(fig)
    log(f"   zapsáno {png2}")
    log("hotovo.")

if __name__ == "__main__":
    main()
