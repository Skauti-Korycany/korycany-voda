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


def stahni(slozka, soubory, klic):
    """klic(nazev) -> (objekt, typ) nebo None; vrací {(objekt, typ): (header, radky)}"""
    vyber = [(s, klic(s)) for s in soubory]; vyber = [(s, k) for s, k in vyber if k]
    print(f"  {slozka}: {len(vyber)} souborů z {len(soubory)}", flush=True)
    with ThreadPoolExecutor(8) as ex:
        data = list(ex.map(lambda sk: get(CH + slozka + sk[0]), vyber))
    res, ukazka = {}, set()
    for (s, k), b in zip(vyber, data):
        if not b:
            continue
        if k not in ukazka:
            ukazka.add(k); open(os.path.join(OUT, f"ukazka_{k[0]}_{k[1]}_{slozka.strip('/').replace('/', '-')}.txt"), "wb").write(b[:2500])
        j = vse_json(b.decode("utf-8-sig", "replace"))
        for t in tabulky(j, []):
            h = t["header"] if isinstance(t["header"], str) else ",".join(t["header"])
            res.setdefault(k, (h, []))[1].extend(t["values"])
    return res


def uloz(res, pripona):
    for (obj, typ), (h, radky) in sorted(res.items()):
        radky = sorted({json.dumps(r, ensure_ascii=False) for r in radky})
        radky = [json.loads(r) for r in radky]
        try:
            radky.sort(key=lambda r: [str(x) for x in r])
        except Exception:  # noqa
            pass
        p = os.path.join(OUT, f"{obj}_{typ}_{pripona}.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write(h + "\n")
            for r in radky:
                f.write(",".join("" if x is None else str(x) for x in r) + "\n")
        print(f"   {obj} {typ} {pripona}: {len(radky)} řádků, sloupce {h}, první {radky[0] if radky else None}, poslední {radky[-1] if radky else None}", flush=True)


print("1) prameny - historical", flush=True)
uloz(stahni("groundwater/historical/data/", seznam(CH + "groundwater/historical/data/"),
            lambda s: next(((o, s.split("_")[2]) for o in PRAMENY if f"-{o}_" in s), None)), "hist")
print("2) prameny - recent", flush=True)
uloz(stahni("groundwater/recent/data/", seznam(CH + "groundwater/recent/data/"),
            lambda s: next(((o, s.split("_")[1]) for o in PRAMENY if f"-{o}_" in s), None)), "recent")
for o in PRAMENY:
    b = get(CH + f"groundwater/characteristic/data/GCHAR_0-203-1-{o}.json")
    if b:
        open(os.path.join(OUT, f"{o}_charakteristiky.json"), "wb").write(b)
print("3) Kyjovka - historical (denní, měsíční, měsíční maxima)", flush=True)
for sl in ("daily", "monthly", "monthly_max"):
    uloz(stahni(f"historical/data/{sl}/", seznam(CH + f"historical/data/{sl}/"),
                lambda s: next(((o, s.split("_")[2]) for o in STANICE if f"-{o}_" in s), None)), "hist")
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
