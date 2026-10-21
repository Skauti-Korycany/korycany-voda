# -*- coding: utf-8 -*-
"""14_toky_vypaleni.py - vypálí vodní toky ČÚZK (HY-NET) do terénu a připraví toky pro jádro (nádrže).

Proč: DMR 5G má 5 m buňky a koryta malých potoků jsou užší a v interpolaci TIN zahlazená.
Odtok odvozený jen z terénu (D8) se pak od skutečného potoka místy odchyluje (hlavně v intravilánu,
kde je potok zatrubněný nebo v zídkách). Vypálením (stream burning, Hutchinson 1989 / AGREE,
zjednodušeně: snížení buněk pod linií toku o pevnou hodnotu) se odtok přinutí jít po linii toku.

Použití:
    python tools/14_toky_vypaleni.py [--dem data/dmr/dmr5g_5m.tif] [--hloubka 2.0]

Vstupy:  data/dmr/dmr5g_5m.tif (01), data/toky_cuzk.geojson (03, WGS84), data/povodi.geojson (02)
Výstupy:
    data/dmr/dmr_vypaleny.tif       terén se sníženými buňkami toků (jen pro odtok, NE pro objemy)
    data/dmr/smer_vypaleny.tif      D8 z vypáleného terénu (kódy jako smer_odtoku.tif)
    data/dmr/akumulace_vypalena.tif akumulace z vypáleného terénu (buňky)
    data/web/toky.json              toky v území modelu v mřížce S-JTSK pro jádro: body po 5 m od pramene
                                    po proudu, u každého plocha povodí (km², z vypálené akumulace) a kóta dna
                                    (m, minimum PŮVODNÍHO terénu v okolí 3x3 buněk = nejnižší místo údolí)
    data/toky_vypaleni_info.json    kontrola: odchylka toků od D8 před a po vypálení
    docs/img/toky_vypaleni_nahled.png
Metoda a omezení: docs/JADRO.md, kap. Nádrže.
"""
import argparse, importlib.util, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# funkce z 02_rozvodnice.py (stejný algoritmus, ať se výsledky dají porovnat)
spec = importlib.util.spec_from_file_location("rozv", os.path.join(HERE, "02_rozvodnice.py"))
rozv = importlib.util.module_from_spec(spec); spec.loader.exec_module(rozv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dem", default=os.path.join(REPO, "data", "dmr", "dmr5g_5m.tif"))
    ap.add_argument("--hloubka", type=float, default=2.0, help="o kolik m snížit buňky toku (jen pro odtok)")
    ap.add_argument("--krok", type=float, default=5.0, help="vzdálenost bodů v toky.json (m)")
    a = ap.parse_args()

    import rasterio
    from pyproj import Transformer
    from scipy.ndimage import distance_transform_edt, minimum_filter

    if not os.path.exists(a.dem):
        sys.exit(f"Chybí terén {a.dem}. Nejdřív vyrob_teren.bat.")
    with rasterio.open(a.dem) as s:
        dem = s.read(1).astype(np.float64); nd = s.nodata; T = s.transform; prof = s.profile
    valid = np.isfinite(dem) & (dem != nd) if nd is not None else np.isfinite(dem)
    nrow, ncol = dem.shape; res = T.a
    x0, y1 = T.c, T.f
    to_xy = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)

    # ------------------------------------------------ toky -> S-JTSK, jen ty, co zasahují do území modelu
    g = json.load(open(os.path.join(REPO, "data", "toky_cuzk.geojson"), encoding="utf-8"))
    linie = []
    for ft in g["features"]:
        geom = ft["geometry"]
        parts = [geom["coordinates"]] if geom["type"] == "LineString" else geom["coordinates"]
        for co in parts:
            xs, ys = to_xy.transform([c[0] for c in co], [c[1] for c in co])
            linie.append({"xy": np.c_[xs, ys], "uzemi": bool(ft["properties"].get("v_uzemi_modelu")),
                          "od": ft["properties"].get("startnode"), "do": ft["properties"].get("endnode")})
    log(f"toků {len(linie)}, v území modelu {sum(l['uzemi'] for l in linie)}")

    def zhustit(xy, krok):
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
        if d[-1] == 0:
            return xy[:1], d[:1]
        s = np.r_[np.arange(0, d[-1], krok), d[-1]]
        return np.c_[np.interp(s, d, xy[:, 0]), np.interp(s, d, xy[:, 1])], s

    def bunky(xy):
        r = ((y1 - xy[:, 1]) / res).astype(int); c = ((xy[:, 0] - x0) / res).astype(int)
        ok = (r >= 0) & (r < nrow) & (c >= 0) & (c < ncol)
        return r[ok], c[ok]

    # ------------------------------------------------ vypálení (všechny toky v rastru, hustě po 1 m = žádná buňka nevynechána)
    tok = np.zeros(dem.shape, bool)
    for l in linie:
        r, c = bunky(zhustit(l["xy"], 1.0)[0])
        tok[r, c] = True
    tok &= valid
    demb = np.where(tok, dem - a.hloubka, dem)
    log(f"vypáleno {tok.sum():,} buněk o {a.hloubka} m")

    log("D8 původní terén (pro srovnání) ...")
    f0 = rozv.priority_flood(dem, valid); _, rc0 = rozv.d8_direction(f0, valid); acc0 = rozv.accumulate(f0, rc0, valid)
    log("D8 vypálený terén ...")
    fb = rozv.priority_flood(demb, valid); codeb, rcb = rozv.d8_direction(fb, valid); accb = rozv.accumulate(fb, rcb, valid)
    km2 = res * res / 1e6

    # ------------------------------------------------ kontrola: odchylka vrcholů toků v území od D8 toku (>= 0,02 km²)
    def odchylka(acc):
        dist = distance_transform_edt(~(acc * km2 >= 0.02)) * res
        v = []
        for l in linie:
            if l["uzemi"]:
                r, c = bunky(zhustit(l["xy"], res)[0]); v.append(dist[r, c])
        v = np.concatenate(v)
        return {"median_m": float(np.median(v)), "p90_m": float(np.percentile(v, 90)), "podil_nad_15m": float((v > 15).mean())}
    kontrola = {"pred": odchylka(acc0), "po": odchylka(accb)}
    log(f"odchylka toků od D8: před {kontrola['pred']}, po {kontrola['po']}")

    # povodí hlavních profilů před/po (kontrola, že se rozvodnice nezměnily)
    body = json.load(open(os.path.join(REPO, "data", "rozvodnice_info.json"), encoding="utf-8"))
    profily = []
    for b in body.get("uzaverove_body", []):
        if "prichyceno_5514" not in b:
            continue
        X, Y = b["prichyceno_5514"]; r = int((y1 - Y) / res); c = int((X - x0) / res)
        win = (slice(max(0, r - 2), r + 3), slice(max(0, c - 2), c + 3))
        profily.append({"nazev": b.get("nazev"), "km2_pred": round(float(acc0[win].max() * km2), 3), "km2_po": round(float(accb[win].max() * km2), 3)})
    kontrola["profily"] = profily
    for p in profily:
        log(f"   {p['nazev']}: {p['km2_pred']} -> {p['km2_po']} km²")

    # ------------------------------------------------ zápis rastrů
    out = os.path.join(REPO, "data", "dmr")
    p = prof.copy(); p.update(dtype="float32", nodata=-9999.0, compress="deflate")
    with rasterio.open(os.path.join(out, "dmr_vypaleny.tif"), "w", **p) as d:
        d.write(np.where(valid, demb, -9999).astype(np.float32), 1)
    with rasterio.open(os.path.join(out, "akumulace_vypalena.tif"), "w", **p) as d:
        d.write(np.where(valid, accb, -9999).astype(np.float32), 1)
    p8 = prof.copy(); p8.update(dtype="uint8", nodata=0, compress="deflate")
    with rasterio.open(os.path.join(out, "smer_vypaleny.tif"), "w", **p8) as d:
        d.write(codeb, 1)

    # ------------------------------------------------ toky.json pro jádro
    dno = minimum_filter(np.where(valid, dem, np.inf), size=3)   # nejnižší místo v okolí 3x3 = dno zahlazeného údolí
    tj = []
    for k, l in enumerate(linie):
        if not l["uzemi"]:
            continue
        xy, s = zhustit(l["xy"], a.krok)
        r = np.clip(((y1 - xy[:, 1]) / res).astype(int), 0, nrow - 1); c = np.clip(((xy[:, 0] - x0) / res).astype(int), 0, ncol - 1)
        # plocha: akumulace přímo v buňce bodu (buňky linie jsou vypálené, takže leží na dráze odtoku)
        A = accb[r, c] * km2
        z = dno[r, c]
        od, do = l["od"], l["do"]
        # orientace: HY-NET je digitalizovaný po proudu (flowdirection inDirection); ověřeno 21. 10. 2026 na všech 44 liniích proti výšce dna
        A = np.maximum.accumulate(A)            # po proudu neklesá (šum na soutocích)
        tj.append({"id": len(tj), "od": od, "do": do, "delka_m": round(float(s[-1]), 1),
                   "x": [round(float(v), 1) for v in xy[:, 0]], "y": [round(float(v), 1) for v in xy[:, 1]],
                   "A_km2": [round(float(v), 4) for v in A], "z_dno": [round(float(v), 2) if np.isfinite(v) else None for v in z]})
    # návaznosti: které linie přitékají do začátku linie (podle uzlů HY-NET)
    podle_do = {}
    for t in tj:
        podle_do.setdefault(t["do"], []).append(t["id"])
    for t in tj:
        t["pritoky"] = podle_do.get(t["od"], [])
        nav = [u["id"] for u in tj if u["od"] == t["do"]]
        t["dal"] = nav[0] if nav else None
    # plocha na začátku linie = plocha v uzlu soutoku (konec přítoku už zahrnuje celý uzel, proto max, ne součet)
    for _ in range(3):
        for t in tj:
            if t["pritoky"]:
                a0 = max(tj[i]["A_km2"][-1] for i in t["pritoky"])
                t["A_km2"] = [round(float(v), 4) for v in np.maximum.accumulate(np.maximum(t["A_km2"], [a0] + [0] * (len(t["A_km2"]) - 1)))]
    # konec přítoku leží v buňce soutoku, kde už je plocha hlavního toku -> konec přítoku dostane plochu před soutokem
    for t in tj:
        A = t["A_km2"]; an = A[-1]; k = len(A) - 1
        while k > 0 and A[k] >= 0.98 * an:
            k -= 1
        if t["dal"] is not None and k < len(A) - 1 and A[k] < 0.9 * an:
            t["A_km2"] = A[:k + 1] + [A[k]] * (len(A) - 1 - k)
    for t in tj:
        t.pop("od"); t.pop("do")
    meta = {"verze": 1, "datum": time.strftime("%Y-%m-%d"), "epsg": 5514, "krok_m": a.krok,
            "pozn": "body od pramene po proudu; A_km2 = plocha povodí z D8 po vypálení toků; z_dno = min. terénu DMR 5G v okolí 3x3 buněk (m n. m.); "
                    "pritoky = id linií končících na začátku linie, dal = linie pokračující po proudu",
            "zdroj": "ČÚZK INSPIRE HY-NET (WatercourseLink, CC BY 4.0), DMR 5G (CC BY 4.0); tools/14_toky_vypaleni.py",
            "vypaleni_m": a.hloubka, "linie": tj}
    with open(os.path.join(REPO, "data", "web", "toky.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, separators=(",", ":"))
    kontrola.update({"linii": len(tj), "delka_km": round(sum(t["delka_m"] for t in tj) / 1000, 2), "vypaleno_bunek": int(tok.sum()), "hloubka_m": a.hloubka})
    with open(os.path.join(REPO, "data", "toky_vypaleni_info.json"), "w", encoding="utf-8") as f:
        json.dump(kontrola, f, ensure_ascii=False, indent=1)
    log(f"toky.json: {len(tj)} linií, {kontrola['delka_km']} km, {os.path.getsize(os.path.join(REPO, 'data', 'web', 'toky.json')) / 1024:.0f} kB")

    # ------------------------------------------------ náhled: kde se D8 po vypálení změnil (výřez centra)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        r0, r1, c0, c1 = 600, 1150, 450, 1100
        fig, ax = plt.subplots(1, 2, figsize=(14, 6.5))
        for k, (acc, nazev) in enumerate([(acc0, "D8 z terénu"), (accb, "D8 po vypálení toků ČÚZK")]):
            ax[k].imshow(dem[r0:r1, c0:c1], cmap="gray", alpha=0.6)
            m = np.ma.masked_less(acc[r0:r1, c0:c1] * km2, 0.02)
            ax[k].imshow(np.log10(m), cmap="Blues", vmin=-2, vmax=1.5)
            for l in linie:
                ax[k].plot((l["xy"][:, 0] - x0) / res - c0, (y1 - l["xy"][:, 1]) / res - r0, "r-", lw=0.7)
            ax[k].set_xlim(0, c1 - c0); ax[k].set_ylim(r1 - r0, 0); ax[k].set_title(nazev + " (modře >= 0,02 km²), červeně toky ČÚZK")
        plt.tight_layout(); plt.savefig(os.path.join(REPO, "docs", "img", "toky_vypaleni_nahled.png"), dpi=70)
    except Exception as e:
        log("náhled se nepovedl:", e)


if __name__ == "__main__":
    main()
