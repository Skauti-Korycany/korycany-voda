# -*- coding: utf-8 -*-
"""15_pramen_kyjovka.py - měřené řady ČHMÚ v území: prameny (vydatnost) a vodoměrné stanice Kyjovky (stav, průtok).

Stáhne z opendata.chmi.cz/hydrology všechny soubory daných objektů (historical + recent), sloučí je po typu řady
a uloží jako CSV do <out>/ (jeden soubor na objekt a typ). Spouští workflow .github/workflows/hydro.yml
(z prostředí Claude je server blokovaný). Formát JSON ČHMÚ: tabulky {"header": "A,B,..", "values": [[..],..]}.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

OUT = sys.argv[1] if len(sys.argv) > 1 else "data/hydro"
os.makedirs(OUT, exist_ok=True)
CH = "https://opendata.chmi.cz/hydrology/"
PRAMENY = {"PB0425": "Koryčany", "PB0433": "Čeložnice", "PB0411": "Lovčice", "PB0415": "Staré Hutě"}
STANICE = {"483100": "Koryčany nad nádrží (Kyjovka)", "484000": "Koryčany pod přehradou (Kyjovka)"}
UA = {"User-Agent": "korycany-voda/0.1"}


def get(url, pokusy=3):
    for i in range(pokusy):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception as e:  # noqa
            if i == pokusy - 1:
                print("  CHYBA", repr(e)[:120], url, flush=True)
        time.sleep(2)
    return None


def seznam(url):
    b = get(url)
    return re.findall(r'href="([^"?#/]+\.json)"', b.decode("utf-8", "replace")) if b else []


def tabulky(o, out):
    if isinstance(o, dict):
        if "header" in o and "values" in o:
            out.append(o)
        for v in o.values():
            tabulky(v, out)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, (dict, list)):
                tabulky(v, out)
    return out


def vse_json(t):
    """soubor může být jeden JSON, nebo několik JSON dokumentů za sebou"""
    dec, i, out = json.JSONDecoder(), 0, []
    while i < len(t):
        while i < len(t) and t[i] in " \r\n\t,":
            i += 1
        if i >= len(t):
            break
        try:
            o, i = dec.raw_decode(t, i)
            out.append(o)
        except json.JSONDecodeError:
            i += 1
    return out


def rady(o, out):
    """najde všechny řady {tsConID, unit, tsData}; tsData je tabulka header/values nebo seznam {dt, value}"""
    if isinstance(o, dict):
        if "tsConID" in o and "tsData" in o:
            d = o["tsData"]
            if isinstance(d, dict):
                for t in tabulky(d, []):
                    out.append((o["tsConID"], o.get("unit"), [(r[0], r[1]) for r in t["values"]]))
            elif isinstance(d, list):
                out.append((o["tsConID"], o.get("unit"), [(r.get("dt"), r.get("value")) for r in d if isinstance(r, dict)]))
        else:
            for v in o.values():
                rady(v, out)
    elif isinstance(o, list):
        for v in o:
            rady(v, out)
    return out


VSE = {}   # (objekt, veličina) -> {"unit":.., "data": {dt: val}}


def stahni(slozka, soubory, objekty):
    vyber = [(s, next((o for o in objekty if f"-{o}_" in s or f"-{o}." in s), None)) for s in soubory]; vyber = [(s, o) for s, o in vyber if o]
    print(f"  {slozka}: {len(vyber)} souborů z {len(soubory)}", flush=True)
    with ThreadPoolExecutor(8) as ex:
        data = list(ex.map(lambda sk: get(CH + slozka + sk[0]), vyber))
    for (s, o), b in zip(vyber, data):
        if not b:
            continue
        for con, unit, rr in rady(vse_json(b.decode("utf-8-sig", "replace")), []):
            z = VSE.setdefault((o, con), {"unit": unit, "data": {}})
            for dt, v in rr:
                if dt and v is not None:
                    z["data"][dt] = v


print("1) prameny", flush=True)
stahni("groundwater/historical/data/", seznam(CH + "groundwater/historical/data/"), PRAMENY)
stahni("groundwater/recent/data/", seznam(CH + "groundwater/recent/data/"), PRAMENY)
for o in PRAMENY:
    b = get(CH + f"groundwater/characteristic/data/GCHAR_0-203-1-{o}.json")
    if b:
        open(os.path.join(OUT, f"{o}_charakteristiky.json"), "wb").write(b)
print("2) Kyjovka (denní, měsíční, měsíční maxima)", flush=True)
for sl in ("daily", "monthly", "monthly_max"):
    stahni(f"historical/data/{sl}/", seznam(CH + f"historical/data/{sl}/"), STANICE)
for (o, con), z in sorted(VSE.items()):
    d = sorted(z["data"].items())
    with open(os.path.join(OUT, f"{o}_{con}.csv"), "w", encoding="utf-8") as f:
        f.write(f"datum,{con}_{z['unit']}\n")
        for dt, v in d:
            f.write(f"{dt[:10] if dt[11:19] in ('00:00:00', '05:00:00', '06:00:00', '07:00:00') else dt},{v}\n")
    print(f"   {o} {con} [{z['unit']}]: {len(d)} hodnot, {d[0][0][:10]} až {d[-1][0][:10]}", flush=True)
for o in STANICE:
    for pre, sl in (("RC", "discharge_rating_curve"), ("CHAR_MDQ", "hydrological_characteristic"), ("CHAR_MONQ", "hydrological_characteristic"), ("NY", "hydrological_characteristic")):
        b = get(CH + f"characteristic/data/{sl}/{pre}_0-203-1-{o}.json")
        if b:
            open(os.path.join(OUT, f"{o}_{pre}.json"), "wb").write(b)
for m in ("groundwater/historical/metadata/meta1.json", "historical/metadata/meta1.json"):
    b = get(CH + m)
    if b:
        for t in tabulky(json.loads(b), []):
            for r in t["values"]:
                if any(str(x) in list(PRAMENY) + list(STANICE) for x in r):
                    print("   meta", t["header"], r, flush=True)
print("hotovo", flush=True)
