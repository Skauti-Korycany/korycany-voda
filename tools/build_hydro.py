# -*- coding: utf-8 -*-
"""build_hydro.py - roční řady měření ČHMÚ pro záložku Jak bylo: vydatnost pramenů u Koryčan a průtok Kyjovky.

Vstup: data/hydro/*.csv (stahuje tools/15_pramen_kyjovka.py ve workflow hydro.yml). Výstup: data/hydro_rocni.json.
Roční průměr se počítá jen z úplných let: týdenní měření aspoň 40 hodnot, denní aspoň 300 (prameny) nebo 360 (průtok).
Trend = lineární regrese ročních průměrů, p-hodnota a Kendallovo tau (scipy). Potom spustit build_dummy.py.
"""
import collections, csv, json, os, statistics as st
from datetime import date
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "data", "hydro")
PRAMENY = {"PB0425": ("Koryčany", 2.3, 450), "PB0433": ("Čeložnice", 4.3, 400), "PB0411": ("Lovčice", 9.0, 370), "PB0415": ("Staré Hutě", 9.5, 440)}
STANICE = {"483100": ("Kyjovka, Koryčany nad nádrží", 19.42), "484000": ("Kyjovka, pod přehradou", 27.54)}


def rada(soubor):
    d = {}
    p = os.path.join(H, soubor)
    if os.path.exists(p):
        for r in csv.reader(open(p, encoding="utf-8")):
            if r and r[0] != "datum":
                d[r[0][:10]] = float(r[1])
    return d


def rocni(d, minimum):
    y = collections.defaultdict(list)
    for k, v in d.items():
        y[int(k[:4])].append(v)
    return {r: st.mean(v) for r, v in sorted(y.items()) if len(v) >= minimum}


def trend(r):
    ys = sorted(r); v = [r[y] for y in ys]
    L = stats.linregress(ys, v); K = stats.kendalltau(ys, v)
    return {"za_10_let": round(L.slope * 10, 4), "p": round(L.pvalue, 4), "tau": round(K.statistic, 2), "p_tau": round(K.pvalue, 4),
            "prvnich_10": [ys[0], ys[9], round(st.mean(v[:10]), 4)], "poslednich_10": [ys[-10], ys[-1], round(st.mean(v[-10:]), 4)]}


out = {"zdroj": "ČHMÚ, otevřená data hydrologie (opendata.chmi.cz/hydrology): prameny groundwater/historical + recent, průtoky historical/data/daily",
       "vytvoreno": date.today().isoformat(),
       "metoda": "roční průměr z úplných let (týdenní měření >= 40 hodnot, denní >= 300, průtok >= 360 dní); trend lineární regresí ročních průměrů",
       "prameny": {}, "prutoky": {}}
for k, (nazev, km, vyska) in PRAMENY.items():
    w, d = rocni(rada(k + "_YT.csv"), 40), rocni(rada(k + "_YD.csv"), 300)
    r = {**w, **d}
    out["prameny"][k] = {"nazev": nazev, "km": km, "vyska_m": vyska, "jednotka": "l/s", "denne_od": min(d) if d else None,
                         "roky": {str(y): round(v, 3) for y, v in sorted(r.items())}, "trend": trend(r)}
for k, (nazev, plocha) in STANICE.items():
    q = rada(k + "_QD.csv"); r = {y: v * 1000 for y, v in rocni(q, 360).items()}
    out["prutoky"][k] = {"nazev": nazev, "plocha_km2": plocha, "jednotka": "l/s", "roky": {str(y): round(v, 1) for y, v in sorted(r.items())}, "trend": trend(r)}
json.dump(out, open(os.path.join(ROOT, "data", "hydro_rocni.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
for sk in ("prameny", "prutoky"):
    for k, z in out[sk].items():
        t = z["trend"]; print(f"{z['nazev']:32} {min(z['roky'])}-{max(z['roky'])} n={len(z['roky'])}  {t['prvnich_10'][2]} -> {t['poslednich_10'][2]} l/s, trend {t['za_10_let']} / 10 let, p={t['p']}")
