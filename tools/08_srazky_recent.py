#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
08_srazky_recent.py - srazky CHMU za rok 2026 z adresare /recent/ (opendata.chmi.cz).

Historical_csv konci 31. 12. 2025. Letosni rok je v /recent/data/ jako JSON po mesicich:
 - denni:    dly-{WSI}-{YYYYMM}.json  (manualni i automaticke stanice)
 - hodinove: 1h-{WSI}-{YYYYMM}.json, 10min: 10m-{WSI}-{YYYYMM}.json (jen automaticke stanice)
Presne umisteni (mesicni podadresare /01/../12/ vs. primo v /daily/) popis CHMU neuvadi jednoznacne,
skript zkousi obe varianty. Format JSON neni popsan - parser hleda zaznamy s klici ELEMENT/DT/VALUE
(seznam slovniku nebo header+values); prvni stazeny soubor se zapise do logu, aby slo format zkontrolovat.

Vstup: data/srazky_stanice.json (z 07_srazky_chmi.py). Vystup: data/srazky_2026.json, data/chmi/recent/*.json (mimo git).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, timedelta

R = "https://opendata.chmi.cz/meteorology/climate/recent/data"
ROK = 2026
MESICE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
MESICE_HOD = [6, 7, 8, 9, 10]
STANIC_DENNI = 6          # nejblizsich stanic s dennimi daty (podle 07)
HLEDAT_AUTOMAT = 2        # kolik nejblizsich automatickych stanic najit
EPIZODY = ["2026-07-15", "2026-07-23", "2026-08-01", "2026-08-02", "2026-09-08", "2026-09-11", "2026-09-17"]

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
RAW = os.path.join(REPO, "data", "chmi", "recent")
os.makedirs(RAW, exist_ok=True)
OUT = os.path.join(REPO, "data", "srazky_2026.json")
LOG = []
UKAZKA = {}


def log(m):
    print(m)
    LOG.append(m)


def stahni(url, cil):
    if os.path.exists(cil) and os.path.getsize(cil) > 0:
        return cil
    for i in range(2):
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
            log(f"  HTTP {e.code} {url}")
        except Exception as e:  # noqa
            log(f"  chyba {e} {url}")
        time.sleep(2)
    return None


def stahni_variantu(prefix, wsi, m, druh):
    """Zkusi obe umisteni souboru. druh = daily / 1hour / 10min."""
    nazev = f"{prefix}-{wsi}-{ROK}{m:02d}.json"
    cil = os.path.join(RAW, nazev)
    for url in (f"{R}/{druh}/{m:02d}/{nazev}", f"{R}/{druh}/{nazev}"):
        c = stahni(url, cil)
        if c:
            return c
    return None


def zaznamy(cesta):
    """Vrati seznam dict se sjednocenymi klici (velka pismena). Hleda header+values nebo seznam dictu."""
    with open(cesta, "r", encoding="utf-8-sig") as f:
        j = json.load(f)
    if "prvni" not in UKAZKA:
        UKAZKA["prvni"] = os.path.basename(cesta)
        UKAZKA["struktura"] = json.dumps(j, ensure_ascii=False)[:1500]
    out = []

    def projdi(x):
        if isinstance(x, dict):
            if "header" in x and "values" in x and isinstance(x["values"], list):
                h = x["header"]
                h = h.split(",") if isinstance(h, str) else list(h)
                # recent JSON (overeno 19. 10. 2026): STATION,ELEMENT,VTYPE,DT,VAL,FLAG,QUALITY
                h = [{"VAL": "VALUE", "VTYPE": "TIMEFUNC"}.get(str(c).strip().upper(), str(c).strip().upper()) for c in h]
                for row in x["values"]:
                    if isinstance(row, (list, tuple)):
                        out.append(dict(zip(h, row)))
                return
            keys = {k.upper() for k in x}
            if "ELEMENT" in keys and "DT" in keys and ("VALUE" in keys or "VAL" in keys):
                out.append({{"VAL": "VALUE", "VTYPE": "TIMEFUNC"}.get(k.upper(), k.upper()): v for k, v in x.items()})
                return
            for v in x.values():
                projdi(v)
        elif isinstance(x, list):
            for v in x:
                projdi(v)
    projdi(j)
    return out


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def serie(cesty, element, timefunc_pref=None):
    """Slouci soubory -> {DT: value} pro dany prvek (VALUE, vyrazeny QUALITY >= 4)."""
    s = {}
    for c in cesty:
        rows = [r for r in zaznamy(c) if str(r.get("ELEMENT", "")).upper() == element]
        tfs = {str(r.get("TIMEFUNC", "")) for r in rows}
        for r in rows:
            if timefunc_pref and timefunc_pref in tfs and str(r.get("TIMEFUNC", "")) != timefunc_pref:
                continue
            v, q = fl(r.get("VALUE")), fl(r.get("QUALITY"))
            if v is None or (q is not None and q >= 4):
                continue
            s[str(r.get("DT", ""))[:16]] = v
    return s


# ---------------------------------------------------------------- stanice
with open(os.path.join(REPO, "data", "srazky_stanice.json"), "r", encoding="utf-8") as f:
    stanice = json.load(f)["stanice"]
aktivni = [s for s in stanice if s.get("aktivni")]
log(f"aktivnich stanic do 30 km: {len(aktivni)}")

# ---------------------------------------------------------------- denni 2026
log("1) Denni uhrny 2026")
denni_out = {}
for s in [x for x in aktivni if x.get("denni_data")][:STANIC_DENNI]:
    wsi = s["wsi"]
    cesty = [c for m in MESICE if (c := stahni_variantu("dly", wsi, m, "daily"))]
    if not cesty:
        log(f"   {s['nazev']}: nic (404 v obou umistenich)")
        continue
    d = {k[:10]: v for k, v in serie(cesty, "SRA", "06:00").items()}
    if not d:
        log(f"   {s['nazev']}: soubory stazeny, ale parser nenasel SRA - viz ukazka struktury v JSON")
        continue
    mes = defaultdict(float)
    for k, v in d.items():
        mes[int(k[5:7])] += v
    dny_ep = sorted(set(EPIZODY + [(date.fromisoformat(e) + timedelta(days=1)).isoformat() for e in EPIZODY]))
    denni_out[wsi] = {"nazev": s["nazev"], "km_od_stredu": s["km_od_stredu"], "obdobi": [min(d), max(d)], "dni": len(d),
                      "mesicni_mm": {str(m): round(mes[m], 1) for m in sorted(mes)},
                      "epizody_mm": {e: d.get(e) for e in dny_ep},
                      "dni_nad_10mm": sorted((k, v) for k, v in d.items() if v >= 10),
                      "denni": dict(sorted(d.items()))}
    log(f"   {s['nazev']}: {min(d)}..{max(d)} ({len(d)} dni), cerven-zari: " +
        ", ".join(f"{m}: {mes[m]:.0f}" for m in (6, 7, 8, 9) if m in mes))

# ---------------------------------------------------------------- automaticke stanice: hodinove + 10min
log("2) Hledam nejblizsi automaticke stanice (hodinovy soubor 1h za zari 2026)")
hod_out = {}
nalezeno = 0
for s in aktivni:
    if nalezeno >= HLEDAT_AUTOMAT:
        break
    wsi = s["wsi"]
    test = stahni_variantu("1h", wsi, 9, "1hour")
    if not test:
        continue
    nalezeno += 1
    cesty = [c for m in MESICE_HOD if (c := stahni_variantu("1h", wsi, m, "1hour"))]
    h = serie(cesty, "SRA1H")
    cesty10 = [c for m in MESICE_HOD if (c := stahni_variantu("10m", wsi, m, "10min"))]
    d10 = serie(cesty10, "SRA10M")
    if not h:
        log(f"   {s['nazev']} ({s['km_od_stredu']} km): soubor je, ale SRA1H nenalezen - stanice asi nemeri srazky automaticky")
        hod_out[wsi] = {"nazev": s["nazev"], "km_od_stredu": s["km_od_stredu"], "pozn": "1h soubor bez SRA1H", "prvky": sorted({str(r.get('ELEMENT')) for c in cesty for r in zaznamy(c)})}
        continue
    ep = {}
    for e in EPIZODY:
        for den in (e, (date.fromisoformat(e) + timedelta(days=1)).isoformat()):
            hh = {k: v for k, v in h.items() if k.startswith(den)}
            dd = sorted((k, v) for k, v in d10.items() if k.startswith(den))
            m30 = max((dd[i][1] + dd[i + 1][1] + dd[i + 2][1] for i in range(len(dd) - 2)), default=None) if dd else None
            ep[den] = {"uhrn_mm": round(sum(hh.values()), 1) if hh else None, "max_1h_mm": round(max(hh.values()), 1) if hh else None,
                       "max_1h_utc": max(hh, key=hh.get)[11:16] if hh else None,
                       "max_10min_mm": round(max(v for _, v in dd), 1) if dd else None, "max_30min_mm": round(m30, 1) if m30 is not None else None}
    hod_out[wsi] = {"nazev": s["nazev"], "km_od_stredu": s["km_od_stredu"], "vyska_m": s["vyska_m"], "hodin": len(h), "desetiminut": len(d10),
                    "max_1h_leto_mm": round(max(h.values()), 1), "max_1h_leto_utc": max(h, key=h.get),
                    "hodiny_nad_10mm": sorted((k, v) for k, v in h.items() if v >= 10), "epizody": ep}
    log(f"   {s['nazev']} ({s['km_od_stredu']} km): {len(h)} hodin, {len(d10)} desetiminut, max 1h {max(h.values()):.1f} mm {max(h, key=h.get)} UTC")
if nalezeno == 0:
    log("   zadna automaticka stanice do 30 km nenalezena (nebo jine umisteni souboru) - viz log")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"zdroj": "CHMU opendata.chmi.cz, recent/data (denni SRA, hodinove SRA1H, 10min SRA10M), rok 2026",
               "stazeno": date.today().isoformat(), "pozn": "data recent jsou predbezna (po kontrole CHMU se prepisuji), denni uhrn = klimatologicky den k 06 UTC",
               "epizody_kachnik": EPIZODY, "denni_2026": denni_out, "automaticke_stanice_2026": hod_out, "ukazka_formatu": UKAZKA, "log": LOG},
              f, ensure_ascii=False, indent=1)
log(f"Zapsano {OUT}")
print("\nHOTOVO.")
