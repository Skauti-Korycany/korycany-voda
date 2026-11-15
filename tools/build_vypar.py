# -*- coding: utf-8 -*-
"""build_vypar.py - možný výpar (ET0) přesnější metodou a kontrola měřením. Vstup data/vypar/*.csv (16_vypar_data.py).

Metody (Allen a kol. 1998, FAO Irrigation and Drainage Paper 56):
- HS: Hargreaves-Samani, rov. 52 (jen teploty) - dosavadní výpočet aplikace.
- PM: Penman-Monteith, rov. 6: teplota, vlhkost (ea z RHmean, rov. 19), vítr z 10 m přepočtený na 2 m (rov. 47),
  záření ze slunečního svitu (Angström, rov. 35, a_s 0,25, b_s 0,50; ověřeno proti měřenému záření), Rnl rov. 39, G = 0.
Výstup data/vypar_rocni.json: roční řady, srovnání metod, kontrola proti měřenému záření a výparoměru, trendy.
"""
import csv, json, math, os, statistics as st
from datetime import date
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); V = os.path.join(ROOT, "data", "vypar")
ST = {"nemochovice": (49.20, 283), "stare_mesto": (49.09, 221), "kromeriz": (49.28, 233), "holesov": (49.32, 222), "straznice": (48.90, 176), "brno_turany": (49.15, 241)}
LAT_K, Z_K = 49.11, 300   # Koryčany


def nacti(n):
    d = {}
    for r in csv.DictReader(open(os.path.join(V, n + ".csv"), encoding="utf-8")):
        d[r["datum"]] = {k: float(v) for k, v in r.items() if k != "datum" and v != ""}
    return d


def ra_n(den, lat):
    J = den.timetuple().tm_yday; fi = math.radians(lat)
    dr = 1 + 0.033 * math.cos(2 * math.pi * J / 365); de = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    ws = math.acos(-math.tan(fi) * math.tan(de))
    Ra = 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(fi) * math.sin(de) + math.cos(fi) * math.cos(de) * math.sin(ws))
    return Ra, 24 / math.pi * ws


def es(t):
    return 0.6108 * math.exp(17.27 * t / (t + 237.3))


def hs(den, t, tn, tx, lat):
    Ra, _ = ra_n(den, lat)
    return max(0.0, 0.0023 * (t + 17.8) * math.sqrt(max(0.0, tx - tn)) * Ra * 0.408)


def pm(den, t, tn, tx, rh, u10, lat, z, n=None, rs=None, a=0.25, b=0.50):
    Ra, N = ra_n(den, lat)
    if rs is None:
        rs = (a + b * min(1.0, max(0.0, n / N))) * Ra
    rso = (0.75 + 2e-5 * z) * Ra
    esm = (es(tx) + es(tn)) / 2; ea = rh / 100 * esm
    rns = 0.77 * rs
    rnl = 4.903e-9 * ((tx + 273.16) ** 4 + (tn + 273.16) ** 4) / 2 * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * min(1.0, rs / rso) - 0.35)
    rn = rns - rnl
    u2 = u10 * 4.87 / math.log(67.8 * 10 - 5.42)
    P = 101.3 * ((293 - 0.0065 * z) / 293) ** 5.26; g = 0.000665 * P
    D = 4098 * es(t) / (t + 237.3) ** 2
    return max(0.0, (0.408 * D * rn + g * 900 / (t + 273) * u2 * (esm - ea)) / (D + g * (1 + 0.34 * u2)))


def rocni(d, minimum=360):
    y = {}
    for k, v in d.items():
        y.setdefault(int(k[:4]), []).append(v)
    return {r: sum(v) * (366 if r % 4 == 0 else 365) / len(v) for r, v in sorted(y.items()) if len(v) >= minimum}


def f(x, n=3):
    return round(float(x), n)


def trend(r, od=None, do=None):
    ys = [y for y in sorted(r) if (od is None or y >= od) and (do is None or y <= do)]; v = [r[y] for y in ys]
    L = stats.linregress(ys, v); K = stats.kendalltau(ys, v)
    return {"od": ys[0], "do": ys[-1], "n": len(ys), "prumer": round(st.mean(v), 1), "prvnich_10": [ys[0], ys[9], round(st.mean(v[:10]), 1)], "poslednich_10": [ys[-10], ys[-1], round(st.mean(v[-10:]), 1)], "za_10_let": f(L.slope * 10, 2), "p": f(L.pvalue, 4), "tau": f(K.statistic, 2), "p_tau": f(K.pvalue, 4)}


D = {k: nacti(k) for k in ST}
OM = nacti("open_meteo")
out = {"vytvoreno": date.today().isoformat(), "metoda": __doc__.split("Metody")[1].split("Výstup")[0].strip(), "kontroly": {}, "rady": {}, "trendy": {}}
dd = lambda s: date.fromisoformat(s)
ma = ("T", "TMI", "TMA", "H", "F")

# 1) Angström: sluneční svit -> záření, proti měřenému globálnímu záření (Holešov, Brno-Tuřany)
print("1) záření ze svitu proti měřenému záření")
for s in ("holesov", "brno_turany"):
    x, y, mer, odh = [], [], [], []
    for k, v in D[s].items():
        if "SSV" in v and "RGLB_D" in v:
            Ra, N = ra_n(dd(k), ST[s][0]); x.append(min(1, v["SSV"] / N)); y.append(v["RGLB_D"] / 1000 / Ra)
            mer.append(v["RGLB_D"] / 1000); odh.append((0.25 + 0.5 * min(1, v["SSV"] / N)) * Ra)
    L = stats.linregress(x, y)
    rm = math.sqrt(st.mean([(a - b) ** 2 for a, b in zip(mer, odh)]))
    out["kontroly"]["zareni_" + s] = {"dni": len(x), "a": f(L.intercept), "b": f(L.slope), "r": f(L.rvalue),
                                      "mereno_MJ_den": round(st.mean(mer), 2), "odhad_025_050_MJ_den": round(st.mean(odh), 2), "rmse_MJ_den": round(rm, 2)}
    print("  ", s, out["kontroly"]["zareni_" + s])

# 2) PM se svitem proti PM s měřeným zářením (jak moc vadí odhad záření)
print("2) výpar: svit proti měřenému záření, HS proti PM")
for s in ("holesov", "brno_turany"):
    a, b, c = {}, {}, {}
    for k, v in D[s].items():
        if all(e in v for e in ma + ("SSV", "RGLB_D")):
            den = dd(k); lat, z = ST[s]
            a[k] = pm(den, v["T"], v["TMI"], v["TMA"], v["H"], v["F"], lat, z, n=v["SSV"])
            b[k] = pm(den, v["T"], v["TMI"], v["TMA"], v["H"], v["F"], lat, z, rs=v["RGLB_D"] / 1000)
            c[k] = hs(den, v["T"], v["TMI"], v["TMA"], lat)
    ra_, rb, rc = rocni(a), rocni(b), rocni(c); roky = sorted(set(ra_) & set(rb))
    out["kontroly"]["pm_" + s] = {"roky": [roky[0], roky[-1]], "pm_svit_mm": round(st.mean(ra_[y] for y in roky)), "pm_zareni_mm": round(st.mean(rb[y] for y in roky)),
                                 "hs_mm": round(st.mean(rc[y] for y in roky)), "r_denni_svit_zareni": f(stats.pearsonr([a[k] for k in a], [b[k] for k in a])[0], 3)}
    print("  ", s, out["kontroly"]["pm_" + s])

# 3) výparoměr (volná hladina, květen-září) proti PM a HS: Kroměříž, Holešov, Brno
print("3) výparoměr proti výpočtu (měsíční úhrny, jen měsíce s >= 25 dny)")
for s in ("kromeriz", "holesov", "brno_turany"):
    m = {}
    for k, v in D[s].items():
        if "VY" in v and all(e in v for e in ma + ("SSV",)):
            den = dd(k); lat, z = ST[s]
            m.setdefault(k[:7], []).append((v["VY"], pm(den, v["T"], v["TMI"], v["TMA"], v["H"], v["F"], lat, z, n=v["SSV"]), hs(den, v["T"], v["TMI"], v["TMA"], lat)))
    mm = [(sum(x[0] for x in v), sum(x[1] for x in v), sum(x[2] for x in v)) for k, v in sorted(m.items()) if len(v) >= 25]
    if len(mm) > 10:
        vy, p_, h_ = zip(*mm)
        out["kontroly"]["vyparomer_" + s] = {"mesicu": len(mm), "obdobi": [min(m)[:4], max(m)[:4]], "vyparomer_mm_mes": round(st.mean(vy), 1), "pm_mm_mes": round(st.mean(p_), 1), "hs_mm_mes": round(st.mean(h_), 1),
                                             "r_pm": f(stats.pearsonr(vy, p_)[0], 3), "r_hs": f(stats.pearsonr(vy, h_)[0], 3)}
        print("  ", s, out["kontroly"]["vyparomer_" + s])

# 4) Koryčany: teplota, vlhkost, vítr Nemochovice + svit Staré Město (od 2007), jinak Kroměříž
print("4) Koryčany 2001-2025")
k_pm, k_hs, k_om, zdroj = {}, {}, {}, {}
for k, v in D["nemochovice"].items():
    if not all(e in v for e in ma):
        continue
    den = dd(k)
    k_hs[k] = hs(den, v["T"], v["TMI"], v["TMA"], LAT_K)
    n, z_ = None, None
    for z_ in ("stare_mesto", "kromeriz", "straznice", "holesov"):     # sluneční svit: nejbližší stanice, která ten den měřila
        n = D[z_].get(k, {}).get("SSV")
        if n is not None:
            break
    if n is not None:
        k_pm[k] = pm(den, v["T"], v["TMI"], v["TMA"], v["H"], v["F"], LAT_K, Z_K, n=n); zdroj[z_] = zdroj.get(z_, 0) + 1
for k, v in OM.items():
    if "et0_fao_evapotranspiration" in v:
        k_om[k] = v["et0_fao_evapotranspiration"]
r_pm, r_hs, r_om = rocni(k_pm), rocni(k_hs), rocni(k_om)
print("   svit ze stanic (dní):", zdroj); out["kontroly"]["svit_pro_korycany_dni"] = zdroj
# 5) Kroměříž: dlouhá řada PM (vše měřeno na jedné stanici)
km_pm, km_hs = {}, {}
for k, v in D["kromeriz"].items():
    n = v.get("SSV", D["holesov"].get(k, {}).get("SSV"))     # mezery ve svitu Kroměříže z Holešova (17 km)
    if all(e in v for e in ma) and n is not None:
        den = dd(k); lat, z = ST["kromeriz"]
        km_pm[k] = pm(den, v["T"], v["TMI"], v["TMA"], v["H"], v["F"], lat, z, n=n); km_hs[k] = hs(den, v["T"], v["TMI"], v["TMA"], lat)
r_km, r_kmh = rocni(km_pm), rocni(km_hs)
ho_pm = {k: pm(dd(k), v["T"], v["TMI"], v["TMA"], v["H"], v["F"], *ST["holesov"], n=v["SSV"]) for k, v in D["holesov"].items() if all(e in v for e in ma + ("SSV",))}
r_ho = rocni(ho_pm)
for nazev, r in (("korycany_pm", r_pm), ("korycany_hs", r_hs), ("open_meteo_et0", r_om), ("kromeriz_pm", r_km), ("kromeriz_hs", r_kmh), ("holesov_pm", r_ho)):
    out["rady"][nazev] = {str(y): round(v) for y, v in r.items()}
out["trendy"] = {"korycany_pm": trend(r_pm), "korycany_hs": trend(r_hs, 2001), "open_meteo_2001": trend(r_om, 2001), "open_meteo_1940": trend(r_om), "open_meteo_1961": trend(r_om, 1961),
                 "kromeriz_pm": trend(r_km), "kromeriz_pm_1961": trend(r_km, 1961), "kromeriz_pm_2001": trend(r_km, 2001), "kromeriz_hs_1961": trend(r_kmh, 1961), "holesov_pm_1961": trend(r_ho, 1961), "holesov_pm_2001": trend(r_ho, 2001)}
# složky: vítr, vlhkost, svit - roční průměry a trendy (Nemochovice 2001+, Kroměříž 1961+)
for s, od in (("nemochovice", 2001), ("kromeriz", 1961), ("holesov", 1961)):
    for e in ("F", "H", "SSV", "T"):
        y = {}
        for k, v in D[s].items():
            if e in v:
                y.setdefault(int(k[:4]), []).append(v[e])
        r = {a: (sum(b) if e == "SSV" else st.mean(b)) for a, b in y.items() if len(b) >= 350 and a >= od}
        if len(r) > 15:
            out["trendy"][f"{s}_{e}"] = trend(r)
# bilance srážky minus výpar pro Koryčany oběma metodami (srážky: roční úhrny z normaly.json)
NR = json.load(open(os.path.join(ROOT, "data", "pocasi", "normaly.json"), encoding="utf-8"))["rocniky"]
Pr = {int(r): z["P"]["rok"] for r, z in NR.items() if z.get("P") and z["P"].get("rok") is not None}
by = sorted(set(r_pm) & set(r_hs) & set(Pr))
out["kontroly"]["bilance_korycany"] = {"roky": [by[0], by[-1]], "n": len(by), "srazky_mm": round(st.mean(Pr[y] for y in by)),
    "pm_bilance_mm": round(st.mean(Pr[y] - r_pm[y] for y in by)), "pm_let_v_minusu": sum(1 for y in by if Pr[y] < r_pm[y]),
    "hs_bilance_mm": round(st.mean(Pr[y] - r_hs[y] for y in by)), "hs_let_v_minusu": sum(1 for y in by if Pr[y] < r_hs[y]),
    "pm_bilance_trend": trend({y: Pr[y] - r_pm[y] for y in by})}
print("  ", out["kontroly"]["bilance_korycany"])
# vegetační období duben-září (PM)
veg = {}
for k, v in k_pm.items():
    if 4 <= int(k[5:7]) <= 9:
        veg.setdefault(int(k[:4]), []).append(v)
out["rady"]["korycany_pm_duben_zari"] = {str(y): round(sum(v)) for y, v in sorted(veg.items()) if len(v) >= 180}
spol = sorted(set(r_pm) & set(r_hs) & set(r_om))
out["kontroly"]["korycany_metody"] = {"roky": [spol[0], spol[-1]], "n": len(spol), "pm_mm": round(st.mean(r_pm[y] for y in spol)), "hs_mm": round(st.mean(r_hs[y] for y in spol)), "open_meteo_mm": round(st.mean(r_om[y] for y in spol)),
                                      "r_pm_hs": f(stats.pearsonr([r_pm[y] for y in spol], [r_hs[y] for y in spol])[0], 2), "r_pm_om": f(stats.pearsonr([r_pm[y] for y in spol], [r_om[y] for y in spol])[0], 2)}
print("  ", out["kontroly"]["korycany_metody"])
for k, t in out["trendy"].items():
    print(f"   {k:22} {t}")
json.dump(out, open(os.path.join(ROOT, "data", "vypar_rocni.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
