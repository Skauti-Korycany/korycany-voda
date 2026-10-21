#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
13_normaly_pocasi.py - jednorazove: referencni hodnoty a rocniky pro zalozku "Jak bylo".

Vstup (historical_csv CHMU, overeno 21. 10. 2026; z Claude nejde stahovat, stahne GitHub Actions nebo PC):
  https://opendata.chmi.cz/meteorology/climate/historical_csv/data/daily/precipitation/dly-0-203-0-41701068002-SRA.csv  (Korycany 1920-2025)
  .../daily/temperature/dly-0-203-0-41503035001-{T,TMA,TMI}.csv, .../humidity/...-H.csv, .../wind/...-F.csv       (Nemochovice 2000-12 az 2025)
  Format: STATION,ELEMENT,TIMEFUNC,DT,VALUE,FLAG,QUALITY ; vyradit QUALITY >= 4 nebo prazdne VALUE.
  Nemochovice ma uplne roky 2001-2025 = 25 let (ne 30): referencni obdobi pro T a ET0 je 2001-2025, srazky 1991-2020.

Vystup: data/pocasi/normaly.json
  - mesic: {1..12: {P_norm (1991-2020), T, Tmin, Tmax, ET0, bil (2001-2025)}}
  - den_v_roce: 366 hodnot klouzaveho prumeru (okno 15 dni) T a ET0 pro "proti prumeru" v prubehu mesice
  - rocniky: {rok: {P (mesice 1-12 + rok, Korycany 1921-2025), T, ET0, bil (Nemochovice 2001-2025)}}
  - rekordy: nejvyssi / nejnizsi mesicni P, T a nejvyssi denni P pro kazdy mesic

Spusteni: python tools/13_normaly_pocasi.py [adresar s CSV, vychozi data/pocasi/vzorek]
"""
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else os.path.join(REPO, "data", "pocasi", "vzorek")
OUT = os.path.join(REPO, "data", "pocasi", "normaly.json")
WSI_KOR, WSI_NEM = "0-203-0-41701068002", "0-203-0-41503035001"
P_OBDOBI = (1991, 2020)
T_OBDOBI = (2001, 2025)

sys.path.insert(0, HERE)
import importlib.util  # noqa: E402
_sp = importlib.util.spec_from_file_location("p12", os.path.join(HERE, "12_pocasi.py"))
p12 = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(p12)
et0_hs = p12.et0_hs


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def nacti(nazev, timefunc):
    """{date: value} z historical CSV."""
    s = {}
    with open(os.path.join(SRC, nazev), "r", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if r["TIMEFUNC"] != timefunc:
                continue
            v, q = fl(r["VALUE"]), fl(r["QUALITY"])
            if v is None or (q is not None and q >= 4):
                continue
            s[date.fromisoformat(r["DT"][:10])] = v
    return s


def r1(x):
    return None if x is None else round(x, 1)


def prumer(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


# ---------------------------------------------------------------- nacteni
P = nacti(f"dly-{WSI_KOR}-SRA.csv", "06:00")
T = nacti(f"dly-{WSI_NEM}-T.csv", "AVG")
TMA = nacti(f"dly-{WSI_NEM}-TMA.csv", "20:00")
TMI = nacti(f"dly-{WSI_NEM}-TMI.csv", "20:00")
H = nacti(f"dly-{WSI_NEM}-H.csv", "AVG")
F = nacti(f"dly-{WSI_NEM}-F.csv", "AVG")
ET0 = {d: et0_hs(d, T.get(d), TMI.get(d), TMA.get(d)) for d in T}
ET0 = {d: v for d, v in ET0.items() if v is not None}
print(f"P Korycany {min(P)}..{max(P)} ({len(P)} dni); T Nemochovice {min(T)}..{max(T)} ({len(T)} dni); ET0 {len(ET0)} dni")

# ---------------------------------------------------------------- rocniky (mesicni a rocni hodnoty po letech)
def mesicni(serie, agg):
    """{rok: {mesic: hodnota}} jen pro mesice s >= 25 dny (P: 28)."""
    m = defaultdict(lambda: defaultdict(list))
    for d, v in serie.items():
        m[d.year][d.month].append(v)
    out = {}
    for rok, mm in m.items():
        out[rok] = {}
        for mes, xs in mm.items():
            dni = (date(rok + (mes == 12), mes % 12 + 1, 1) - date(rok, mes, 1)).days
            if len(xs) >= dni - 3:
                out[rok][mes] = round(sum(xs) if agg == "sum" else sum(xs) / len(xs), 1)
    return out


P_m, T_m, ET0_m = mesicni(P, "sum"), mesicni(T, "mean"), mesicni(ET0, "sum")
TMA_m, TMI_m = mesicni(TMA, "mean"), mesicni(TMI, "mean")
rocniky = {}
for rok in sorted(set(P_m) | set(T_m)):
    z = {}
    pm = P_m.get(rok, {})
    if pm:
        z["P"] = {str(k): pm[k] for k in sorted(pm)}
        if len(pm) == 12:
            z["P"]["rok"] = round(sum(pm.values()), 1)
            z["P"]["max_den"] = max((v, d.isoformat()) for d, v in P.items() if d.year == rok)[::-1]
    tm, em = T_m.get(rok, {}), ET0_m.get(rok, {})
    if tm:
        z["T"] = {str(k): tm[k] for k in sorted(tm)}
        if len(tm) == 12:
            z["T"]["rok"] = round(sum(tm.values()) / 12, 1)
            z["T"]["max_den"] = max((v, d.isoformat()) for d, v in TMA.items() if d.year == rok)[::-1]
            z["T"]["min_den"] = min((v, d.isoformat()) for d, v in TMI.items() if d.year == rok)[::-1]
            z["T"]["dni_nad_30"] = sum(1 for d, v in TMA.items() if d.year == rok and v >= 30)
            z["T"]["dni_pod_0"] = sum(1 for d, v in TMI.items() if d.year == rok and v < 0)
    if em:
        z["ET0"] = {str(k): em[k] for k in sorted(em)}
        if len(em) == 12:
            z["ET0"]["rok"] = round(sum(em.values()), 1)
    if pm and em and len(pm) == 12 and len(em) == 12:
        z["bil"] = {str(k): round(pm[k] - em[k], 1) for k in range(1, 13)}
        z["bil"]["rok"] = round(sum(pm.values()) - sum(em.values()), 1)
    rocniky[str(rok)] = z

# ---------------------------------------------------------------- mesicni normaly
def norm(mes_dict, obdobi, agg="mean"):
    out = {}
    for mes in range(1, 13):
        xs = [mes_dict[r][mes] for r in range(obdobi[0], obdobi[1] + 1) if r in mes_dict and mes in mes_dict[r]]
        out[str(mes)] = {"hodnota": r1(prumer(xs)), "roku": len(xs)}
    return out


mesic = {}
Pn, Tn, Tmin_n, Tmax_n, En = norm(P_m, P_OBDOBI), norm(T_m, T_OBDOBI), norm(TMI_m, T_OBDOBI), norm(TMA_m, T_OBDOBI), norm(ET0_m, T_OBDOBI)
for mes in range(1, 13):
    k = str(mes)
    mesic[k] = {"P": Pn[k]["hodnota"], "P_roku": Pn[k]["roku"], "T": Tn[k]["hodnota"], "Tmin": Tmin_n[k]["hodnota"], "Tmax": Tmax_n[k]["hodnota"],
                "ET0": En[k]["hodnota"], "T_roku": Tn[k]["roku"],
                "bil": r1(Pn[k]["hodnota"] - En[k]["hodnota"]) if Pn[k]["hodnota"] is not None and En[k]["hodnota"] is not None else None}
P_rok = r1(sum(mesic[str(m)]["P"] for m in range(1, 13)))
ET0_rok = r1(sum(mesic[str(m)]["ET0"] for m in range(1, 13)))

# ---------------------------------------------------------------- denni krivka (den v roce, klouzave okno 15 dni)
def den_v_roce(serie, obdobi):
    akum = defaultdict(list)
    for d, v in serie.items():
        if obdobi[0] <= d.year <= obdobi[1]:
            akum[d.replace(year=2000).timetuple().tm_yday].append(v)   # 2000 = prestupny, 366 dni
    hod = [prumer(akum.get(i, [])) for i in range(1, 367)]
    out = []
    for i in range(366):
        okno = [hod[(i + j) % 366] for j in range(-7, 8)]
        out.append(r1(prumer(okno)))
    return out


# ---------------------------------------------------------------- rekordy po mesicich
rekordy = {}
for mes in range(1, 13):
    k = str(mes)
    pm = [(P_m[r][mes], r) for r in P_m if mes in P_m[r]]
    tm = [(T_m[r][mes], r) for r in T_m if mes in T_m[r]]
    pd = [(v, d.isoformat()) for d, v in P.items() if d.month == mes]
    rekordy[k] = {"P_max": max(pm)[::-1], "P_min": min(pm)[::-1], "P_den_max": max(pd)[::-1],
                  "T_max": max(tm)[::-1] if tm else None, "T_min": min(tm)[::-1] if tm else None,
                  "TMA_max": max((v, d.isoformat()) for d, v in TMA.items() if d.month == mes)[::-1],
                  "TMI_min": min((v, d.isoformat()) for d, v in TMI.items() if d.month == mes)[::-1]}

out = {
    "vytvoreno": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
    "zdroj": "ČHMÚ otevřená data, historical_csv (denní): srážky Koryčany 0-203-0-41701068002 (1920-11 až 2025-12), "
             "teplota/vlhkost/vítr Nemochovice 0-203-0-41503035001 (2000-12 až 2025-12); ET0 Hargreaves-Samani FAO-56 rov. 52 (viz 12_pocasi.py)",
    "obdobi": {"P": list(P_OBDOBI), "T_ET0": list(T_OBDOBI),
               "pozn": "Nemochovice měří od 12/2000, proto referenční období T a ET0 = 2001-2025 (25 let), ne standardní normál 1991-2020; srážky Koryčany normál 1991-2020"},
    "rok": {"P": P_rok, "ET0": ET0_rok, "bil": r1(P_rok - ET0_rok),
            "T": r1(prumer([mesic[str(m)]["T"] for m in range(1, 13)]))},
    "mesic": mesic,
    "den_v_roce": {"pozn": "index 0 = 1. leden (rok 2000, 366 dní), klouzavý průměr 15 dní, období T_ET0",
                   "T": den_v_roce(T, T_OBDOBI), "ET0": den_v_roce(ET0, T_OBDOBI)},
    "rocniky": rocniky,
    "rekordy": rekordy,
    "pocty": {"P_dni": len(P), "T_dni": len(T), "ET0_dni": len(ET0), "rocniky_P_uplne": sum(1 for z in rocniky.values() if "rok" in z.get("P", {})),
              "rocniky_T_uplne": sum(1 for z in rocniky.values() if "rok" in z.get("T", {}))},
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print(f"rok: P {P_rok} mm, ET0 {ET0_rok} mm, bil {out['rok']['bil']} mm, T {out['rok']['T']} C")
print("mesic:", {k: (v["P"], v["T"], v["ET0"]) for k, v in mesic.items()})
print("uplnych rocniku P:", out["pocty"]["rocniky_P_uplne"], "T:", out["pocty"]["rocniky_T_uplne"], "->", OUT, os.path.getsize(OUT), "B")
