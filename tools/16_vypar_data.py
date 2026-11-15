# -*- coding: utf-8 -*-
"""16_vypar_data.py - podklady pro přesnější výpar (FAO-56 Penman-Monteith) a jeho kontrolu měřením.

Stáhne z ČHMÚ denní řady teploty, vlhkosti, větru, slunečního svitu, globálního záření a výparu z výparoměru
pro Nemochovice a nejbližší stanice se slunečním svitem, a z Open-Meteo (reanalýza ERA5) srovnávací řadu.
Uloží kompaktní tabulky <out>/<stanice>.csv (datum + prvky). Běží ve workflow vypar.yml (z Claude blokováno).
Výpočet a srovnání dělá tools/build_vypar.py.
"""
import csv, io, json, os, sys, time, urllib.request, urllib.error

OUT = sys.argv[1] if len(sys.argv) > 1 else "data/vypar"
os.makedirs(OUT, exist_ok=True)
B = "https://opendata.chmi.cz/meteorology/climate/historical_csv/"
SLOZKA = {"T": "temperature", "TMA": "temperature", "TMI": "temperature", "H": "humidity", "F": "wind",
          "SSV": "sunshine", "RGLB_D": "radiation", "VY": "evaporation"}
JEN = {"straznice": ("SSV",)}   # Strážnice jen jako záloha slunečního svitu
STANICE = {"nemochovice": "0-203-0-41503035001", "stare_mesto": "0-203-0-11754", "kromeriz": "0-203-0-11751",
           "holesov": "0-20000-0-11774", "straznice": "0-203-0-11755", "brno_turany": "0-20000-0-11723"}
PREF = ["AVG", "SUM", "00:00", "24:00", "20:00", "06:00", "07:00"]
UA = {"User-Agent": "korycany-voda/0.1"}


def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception as e:  # noqa
            print("  chyba", repr(e)[:100], url, flush=True)
        time.sleep(2)
    return None


for nazev, wsi in STANICE.items():
    tab, sl = {}, []
    for el, slozka in SLOZKA.items():
        if nazev in JEN and el not in JEN[nazev]:
            continue
        b = get(f"{B}data/daily/{slozka}/dly-{wsi}-{el}.csv")
        if not b:
            continue
        rad = list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"))))
        tf = {}
        for r in rad:
            tf[r["TIMEFUNC"]] = tf.get(r["TIMEFUNC"], 0) + 1
        vyber = next((p for p in PREF if p in tf), max(tf, key=tf.get))
        n = 0
        for r in rad:
            if r["TIMEFUNC"] != vyber or r["VALUE"] in ("", None):
                continue
            try:
                q = float(r["QUALITY"]) if r.get("QUALITY") not in ("", None) else None
                v = float(r["VALUE"])
            except ValueError:
                continue
            if q is not None and q >= 4:
                continue
            tab.setdefault(r["DT"][:10], {})[el] = v; n += 1
        sl.append(el)
        print(f"  {nazev:12} {el:7} TIMEFUNC {tf} -> {vyber}: {n} hodnot", flush=True)
    with open(os.path.join(OUT, nazev + ".csv"), "w", encoding="utf-8") as f:
        f.write("datum," + ",".join(sl) + "\n")
        for d in sorted(tab):
            f.write(d + "," + ",".join("" if tab[d].get(e) is None else f"{tab[d][e]:g}" for e in sl) + "\n")

# výšky čidel a období z metadat (vítr: výška měření pro přepočet na 2 m)
m2 = get(B + "metadata/meta2.csv")
if m2:
    with open(os.path.join(OUT, "meta2_stanice.csv"), "w", encoding="utf-8") as f:
        for i, radek in enumerate(m2.decode("utf-8-sig").splitlines()):
            if i == 0 or (radek.startswith("DLY,") and any(f",{w}," in radek for w in STANICE.values())
                          and any(f",{e}," in radek for e in ("F", "SSV", "RGLB_D", "VY", "H", "T"))):
                f.write(radek + "\n")
m1 = get(B + "metadata/meta1.csv")
if m1:
    with open(os.path.join(OUT, "meta1_stanice.csv"), "w", encoding="utf-8") as f:
        for i, radek in enumerate(m1.decode("utf-8-sig").splitlines()):
            if i == 0 or any(w in radek for w in STANICE.values()):
                f.write(radek + "\n")

# Open-Meteo: reanalýza pro buňku Koryčan (model, jen pro srovnání)
DV = "et0_fao_evapotranspiration,shortwave_radiation_sum"
radky, hl = [], None
for a, b_ in ((1940, 1969), (1970, 1999), (2000, 2025)):
    b = get(f"https://archive-api.open-meteo.com/v1/archive?latitude=49.11&longitude=17.17&start_date={a}-01-01&end_date={b_}-12-31&daily={DV}&timezone=Europe%2FBerlin&wind_speed_unit=ms")
    if not b:
        continue
    j = json.loads(b); d = j["daily"]; hl = ["datum"] + DV.split(",")
    print("  open-meteo", a, b_, len(d["time"]), "dní, buňka", j.get("latitude"), j.get("longitude"), j.get("elevation"), j.get("daily_units"), flush=True)
    for i, t in enumerate(d["time"]):
        radky.append([t] + ["" if d[k][i] is None else f"{d[k][i]:g}" for k in DV.split(",")])
    time.sleep(5)
if radky:
    with open(os.path.join(OUT, "open_meteo.csv"), "w", encoding="utf-8") as f:
        f.write(",".join(hl) + "\n")
        for r in radky:
            f.write(",".join(r) + "\n")
print("hotovo", flush=True)
