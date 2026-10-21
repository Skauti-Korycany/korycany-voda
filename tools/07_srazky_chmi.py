#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_srazky_chmi.py - srazkova data CHMU (opendata.chmi.cz) pro okoli Korycan.

Co dela:
 1. stahne seznam stanic (meta1.csv), vybere stanice do RADIUS_KM od stredu uzemi modelu,
 2. pro nejblizsi stanice stahne denni uhrny (dly-{WSI}-SRA.csv) za cele obdobi mereni,
 3. pro automaticke stanice stahne hodinove uhrny (1h-{WSI}-SRA1H-{YYYYMM}.csv) za leto 2026
    (porovnani s epizodami cidla Kachnik) a zkusi i 10min (SRA10M),
 4. spocita: rocni uhrny, mesicni normal 1991-2020, rocni maxima denniho uhrnu,
    orientacni N-lete denni uhrny (Gumbel), pocty dnu nad 10/20/30/50 mm,
    denni a hodinove uhrny kolem epizod z Kachniku,
 5. zapise lehke vystupy do data/ (JSON) a nahled do docs/img/.

Surova data zustavaji v repo\\data\\chmi\\ (mimo git). Cista standardni knihovna + matplotlib (nahled).
Zdroj: CHMU, opendata.chmi.cz (popis: meteorology/climate/Klimatologicka_data_popis.pdf).
Format souboru overen podle knihovny wetterdienst (provider/chmi/observation/api.py), 19. 10. 2026.
"""
import csv
import io
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

BASE = "https://opendata.chmi.cz/meteorology/climate/historical_csv"
# stred uzemi modelu (WGS84) - z dmr5g_5m_bounds (17.108-17.221 E, 49.074-49.153 N)
STRED_LON, STRED_LAT = 17.165, 49.113
RADIUS_KM = 30.0          # stanice, ktere se vypisou do seznamu
MAX_STANIC_DENNI = 10     # kolik nejblizsich stanic stahnout (denni data)
ROK_OD_HODINOVE = 2026    # hodinova data jen pro tento rok (leto 2026)
MESICE_HODINOVE = [6, 7, 8, 9, 10]
# epizody z cidla Kachnik (STAV.md, 16. 10. 2026)
EPIZODY = ["2026-07-15", "2026-07-23", "2026-08-01", "2026-08-02", "2026-09-08", "2026-09-11", "2026-09-17"]

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RAW = os.path.join(REPO, "data", "chmi")
OUT_JSON = os.path.join(REPO, "data", "srazky_chmi.json")
OUT_STANICE = os.path.join(REPO, "data", "srazky_stanice.json")
OUT_PNG = os.path.join(REPO, "docs", "img", "srazky_nahled.png")
os.makedirs(RAW, exist_ok=True)
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)

LOG = []


def log(msg):
    print(msg)
    LOG.append(msg)


def stahni(url, cil, pokusy=3):
    """Stahne URL do souboru cil (pokud uz existuje, nestahuje). Vraci cestu nebo None (404)."""
    if os.path.exists(cil) and os.path.getsize(cil) > 0:
        return cil
    for i in range(pokusy):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "korycany-voda/0.1 (skautsky oddil Korycany)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            with open(cil, "wb") as f:
                f.write(data)
            return cil
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            log(f"  HTTP {e.code} u {url}, pokus {i + 1}")
        except Exception as e:  # noqa
            log(f"  chyba {e} u {url}, pokus {i + 1}")
        time.sleep(2)
    return None


def cti_csv(cesta):
    with open(cesta, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def km(lon1, lat1, lon2, lat2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- 1. stanice
log("1) Seznam stanic CHMU")
meta_path = stahni(f"{BASE}/metadata/meta1.csv", os.path.join(RAW, "meta1.csv"))
if not meta_path:
    sys.exit("meta1.csv se nepodarilo stahnout - zkontroluj pripojeni, pripadne otevri opendata.chmi.cz v prohlizeci")
radky = cti_csv(meta_path)
stanice = {}
for r in radky:
    wsi = (r.get("WSI") or "").strip()
    lon, lat = fl(r.get("GEOGR1")), fl(r.get("GEOGR2"))
    if not wsi or lon is None or lat is None:
        continue
    d = km(STRED_LON, STRED_LAT, lon, lat)
    if d > RADIUS_KM:
        continue
    s = stanice.setdefault(wsi, {"wsi": wsi, "gh_id": (r.get("GH_ID") or "").strip(), "nazev": "",
                                 "lon": lon, "lat": lat, "vyska_m": fl(r.get("ELEVATION")),
                                 "od": None, "do": None, "km_od_stredu": round(d, 1)})
    od, do = (r.get("BEGIN_DATE") or "")[:10], (r.get("END_DATE") or "")[:10]
    s["od"] = min(s["od"], od) if s["od"] else od
    if not s["do"] or do > s["do"]:
        s["do"], s["nazev"], s["lon"], s["lat"], s["vyska_m"] = do, (r.get("FULL_NAME") or "").strip(), lon, lat, fl(r.get("ELEVATION"))
        s["km_od_stredu"] = round(d, 1)
for s in stanice.values():
    s["aktivni"] = s["do"].startswith("3999") if s["do"] else False
serazene = sorted(stanice.values(), key=lambda s: s["km_od_stredu"])
log(f"   stanic do {RADIUS_KM:.0f} km: {len(serazene)}")
for s in serazene[:MAX_STANIC_DENNI]:
    log(f"   {s['km_od_stredu']:5.1f} km  {s['nazev']:<32} {s['wsi']}  {s['od']}..{s['do'][:4]}  {s['vyska_m']} m")

# ---------------------------------------------------------------- 2. denni data
log("2) Denni uhrny (dly-WSI-SRA.csv)")
vysledky = {}
for s in serazene[:MAX_STANIC_DENNI]:
    wsi = s["wsi"]
    cesta = stahni(f"{BASE}/data/daily/precipitation/dly-{wsi}-SRA.csv", os.path.join(RAW, f"dly-{wsi}-SRA.csv"))
    if not cesta:
        log(f"   {s['nazev']}: denni SRA neni (404)")
        s["denni_data"] = False
        continue
    radky = cti_csv(cesta)
    timefuncs = sorted(set((r.get("TIMEFUNC") or "") for r in radky))
    denni = {}
    for r in radky:
        if "06:00" in timefuncs and (r.get("TIMEFUNC") or "") != "06:00":
            continue
        dt = (r.get("DT") or "")[:10]
        v = fl(r.get("VALUE"))
        q = fl(r.get("QUALITY"))
        if v is None or (q is not None and q >= 4):   # 4 = chybi
            continue
        denni[dt] = v
    if not denni:
        log(f"   {s['nazev']}: soubor bez pouzitelnych hodnot (TIMEFUNC {timefuncs})")
        s["denni_data"] = False
        continue
    s["denni_data"] = True
    roky = defaultdict(list)
    for dt, v in denni.items():
        roky[int(dt[:4])].append((dt, v))
    rocni = {}
    for rok, polozky in roky.items():
        dni_v_roce = 366 if (rok % 4 == 0 and (rok % 100 != 0 or rok % 400 == 0)) else 365
        uplny = len(polozky) >= dni_v_roce - 5
        rocni[rok] = {"uhrn_mm": round(sum(v for _, v in polozky), 1), "dni": len(polozky), "uplny": uplny,
                      "max_denni_mm": round(max(v for _, v in polozky), 1),
                      "max_denni_datum": max(polozky, key=lambda p: p[1])[0]}
    uplne_roky = sorted(r for r, x in rocni.items() if x["uplny"])
    # mesicni normal 1991-2020 (jen uplne mesice)
    mes = defaultdict(list)
    for dt, v in denni.items():
        y, m = int(dt[:4]), int(dt[5:7])
        if 1991 <= y <= 2020:
            mes[(y, m)].append(v)
    normal = {}
    for m in range(1, 13):
        hod = [sum(v) for (y, mm), v in mes.items() if mm == m and len(v) >= 26]
        normal[m] = round(sum(hod) / len(hod), 1) if hod else None
    normal_rok = round(sum(x for x in normal.values() if x is not None), 1) if all(normal.values()) else None
    # N-lete denni uhrny - Gumbel z rocnich maxim (jen uplne roky, min. 15)
    maxima = [rocni[r]["max_denni_mm"] for r in uplne_roky]
    nlete = None
    if len(maxima) >= 15:
        n = len(maxima)
        mu_ = sum(maxima) / n
        sd = math.sqrt(sum((x - mu_) ** 2 for x in maxima) / (n - 1))
        beta = sd * math.sqrt(6) / math.pi
        mu = mu_ - 0.5772 * beta
        nlete = {f"N{T}": round(mu - beta * math.log(-math.log(1 - 1 / T)), 1) for T in (2, 5, 10, 20, 50, 100)}
    prahy = {f"dni_nad_{p}mm_za_rok": round(sum(1 for dt, v in denni.items() if v >= p and int(dt[:4]) in uplne_roky) / max(1, len(uplne_roky)), 2)
             for p in (10, 20, 30, 50)}
    # histogram dennich uhrnu 1991-2020 (prumerny pocet dni za rok v 1mm binech) - pro rocni bilanci SCS-CN v aplikaci
    hist_roky = [r for r in uplne_roky if 1991 <= r <= 2020]
    histogram = None
    if hist_roky:
        biny = defaultdict(float)
        for dt, v in denni.items():
            if int(dt[:4]) in hist_roky and v >= 0.1:
                biny[int(math.ceil(v))] += 1
        kl = sorted(biny)
        histogram = {"obdobi": [hist_roky[0], hist_roky[-1]], "roku": len(hist_roky),
                     "pozn": "bin = horni mez 1mm intervalu (1 = 0,1-1,0 mm); dni_za_rok = prumer za uplne roky 1991-2020; dny < 0,1 mm vynechany",
                     "bin_mm": kl, "dni_za_rok": [round(biny[k] / len(hist_roky), 3) for k in kl]}
    posledni = max(denni)
    vysledky[wsi] = {
        "nazev": s["nazev"], "km_od_stredu": s["km_od_stredu"], "vyska_m": s["vyska_m"],
        "obdobi": [min(denni), posledni], "dni_celkem": len(denni), "uplne_roky": len(uplne_roky),
        "uplne_roky_rozsah": [uplne_roky[0], uplne_roky[-1]] if uplne_roky else None,
        "normal_1991_2020_mm": normal_rok, "normal_mesicni_mm": {str(m): normal[m] for m in range(1, 13)},
        "prumer_uplnych_roku_mm": round(sum(rocni[r]["uhrn_mm"] for r in uplne_roky) / len(uplne_roky), 1) if uplne_roky else None,
        "rocni": {str(r): rocni[r] for r in sorted(rocni)},
        "n_lete_denni_mm_gumbel": nlete, "pocet_rocnich_maxim": len(maxima),
        "histogram_denni_1991_2020": histogram,
        **prahy,
        # den epizody i den po ni: denni uhrn CHMU je k 06 UTC a muze patrit k predchozimu dni (overit v meta3/popisu)
        "epizody_2026_denni_mm": {d: denni.get(d) for d in sorted(set(EPIZODY + [(date.fromisoformat(d) + timedelta(days=1)).isoformat() for d in EPIZODY]))},
        "leto_2026_mm": {m: round(sum(v for dt, v in denni.items() if dt.startswith(f"2026-{m:02d}")), 1) for m in MESICE_HODINOVE},
    }
    log(f"   {s['nazev']}: {min(denni)}..{posledni}, uplnych roku {len(uplne_roky)}, normal 91-20 {normal_rok} mm, "
        f"N10 denni {nlete['N10'] if nlete else '-'} mm")

# ---------------------------------------------------------------- 3. hodinova a 10min data (leto 2026)
log("3) Hodinove (SRA1H) a 10min (SRA10M) uhrny, leto 2026")
hodinove = {}
for s in serazene[:MAX_STANIC_DENNI]:
    wsi = s["wsi"]
    rady = {}
    for m in MESICE_HODINOVE:
        cesta = stahni(f"{BASE}/data/1hour/precipitation/{ROK_OD_HODINOVE}/1h-{wsi}-SRA1H-{ROK_OD_HODINOVE}{m:02d}.csv",
                       os.path.join(RAW, f"1h-{wsi}-SRA1H-{ROK_OD_HODINOVE}{m:02d}.csv"))
        if not cesta:
            continue
        for r in cti_csv(cesta):
            v = fl(r.get("VALUE"))
            if v is not None:
                rady[(r.get("DT") or "")[:16]] = v
    s["hodinova_data"] = bool(rady)
    if not rady:
        continue
    # 10min - zkusime, format neni v dokumentaci potvrzen pro SRA10M
    des = {}
    for m in MESICE_HODINOVE:
        cesta = stahni(f"{BASE}/data/10min/precipitation/{ROK_OD_HODINOVE}/10m-{wsi}-SRA10M-{ROK_OD_HODINOVE}{m:02d}.csv",
                       os.path.join(RAW, f"10m-{wsi}-SRA10M-{ROK_OD_HODINOVE}{m:02d}.csv"))
        if cesta:
            for r in cti_csv(cesta):
                v = fl(r.get("VALUE"))
                if v is not None:
                    des[(r.get("DT") or "")[:16]] = v
    s["desetiminutova_data"] = bool(des)
    ep = {}
    for d in EPIZODY:
        hod = {k: v for k, v in rady.items() if k.startswith(d)}
        d10 = sorted((k, v) for k, v in des.items() if k.startswith(d))
        max30 = max((d10[i][1] + d10[i + 1][1] + d10[i + 2][1] for i in range(len(d10) - 2)), default=None) if d10 else None
        ep[d] = {"uhrn_den_mm": round(sum(hod.values()), 1) if hod else None,
                 "max_1h_mm": round(max(hod.values()), 1) if hod else None,
                 "max_1h_cas_utc": max(hod, key=hod.get)[11:16] if hod else None,
                 "max_10min_mm": round(max(v for _, v in d10), 1) if d10 else None,
                 "max_30min_mm": round(max30, 1) if max30 is not None else None}
    hodinove[wsi] = {"nazev": s["nazev"], "km_od_stredu": s["km_od_stredu"], "hodin": len(rady), "desetiminut": len(des),
                     "max_1h_leto_mm": round(max(rady.values()), 1), "max_1h_leto_cas_utc": max(rady, key=rady.get),
                     "epizody_kachnik": ep}
    log(f"   {s['nazev']}: {len(rady)} hodin, {len(des)} desetiminut, max 1h {max(rady.values()):.1f} mm ({max(rady, key=rady.get)} UTC)")
if not hodinove:
    log("   zadna stanice v okruhu nema hodinova data (automaticke stanice jsou dal) - rozsir RADIUS_KM nebo MAX_STANIC_DENNI")

# ---------------------------------------------------------------- 4. vystupy
with open(OUT_STANICE, "w", encoding="utf-8") as f:
    json.dump({"zdroj": "CHMU opendata.chmi.cz, historical_csv/metadata/meta1.csv", "stazeno": date.today().isoformat(),
               "stred_lon": STRED_LON, "stred_lat": STRED_LAT, "radius_km": RADIUS_KM, "stanice": serazene}, f, ensure_ascii=False, indent=1)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"zdroj": "CHMU, opendata.chmi.cz (historical_csv, denni SRA, hodinove SRA1H, 10min SRA10M)",
               "licence": "overit na opendata.chmi.cz - podminky uziti otevrenych dat CHMU",
               "stazeno": date.today().isoformat(),
               "metoda": {"rok_uplny": "chybi max. 5 dnu", "normal": "prumer mesicnich uhrnu 1991-2020 z mesicu s >= 26 dny",
                          "n_lete": "Gumbel (momentova metoda) z rocnich maxim denniho uhrnu, jen uplne roky, min. 15 let; orientacni, ne nahrada za CHMU/CSN 75 9010",
                          "denni_uhrn": "klimatologicky den 06-06 UTC (TIMEFUNC 06:00)", "kvalita": "vyrazeny hodnoty QUALITY >= 4"},
               "epizody_kachnik": EPIZODY, "denni": vysledky, "hodinove_leto_2026": hodinove, "log": LOG}, f, ensure_ascii=False, indent=1)
log(f"4) Zapsano: {OUT_JSON}, {OUT_STANICE}")

# nahled
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 1, figsize=(11, 8))
    for wsi, v in vysledky.items():
        roky = [int(r) for r, x in v["rocni"].items() if x["uplny"]]
        if not roky:
            continue
        ax[0].plot(roky, [v["rocni"][str(r)]["uhrn_mm"] for r in roky], label=f"{v['nazev']} ({v['km_od_stredu']} km)", lw=1)
        if all(v["normal_mesicni_mm"].values()):
            ax[1].plot(range(1, 13), [v["normal_mesicni_mm"][str(m)] for m in range(1, 13)], marker="o", label=v["nazev"], lw=1)
    ax[0].set_title("Rocni uhrn srazek (uplne roky), stanice CHMU v okoli Korycan")
    ax[0].set_ylabel("mm"); ax[0].grid(alpha=.3); ax[0].legend(fontsize=7)
    ax[1].set_title("Mesicni normal 1991-2020"); ax[1].set_ylabel("mm"); ax[1].set_xticks(range(1, 13)); ax[1].grid(alpha=.3); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT_PNG, dpi=110)
    log(f"   nahled: {OUT_PNG}")
except Exception as e:  # noqa
    log(f"   nahled se nepovedl ({e}) - data jsou v JSON")

print("\nHOTOVO. Posli Claudovi obsah okna (nebo soubor data/srazky_chmi.json).")
