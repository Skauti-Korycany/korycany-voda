# -*- coding: utf-8 -*-
"""inventura_zdroju.py - průzkum dalších zdrojů dat (vítr, sluneční svit, oblačnost, záření, půdní vlhkost, podzemní voda).

Nic nepočítá, jen zjišťuje, co je kde dostupné, a zapíše to do <out>/ (texty a JSON). Spouští ho workflow
.github/workflows/inventura-zdroju.yml v GitHub Actions, protože z prostředí Claude jsou tyto servery blokované.
Bez osobních údajů: do dotazů jde jen střed území modelu.
"""
import csv, io, json, math, os, re, subprocess, sys, urllib.request, urllib.error

OUT = sys.argv[1] if len(sys.argv) > 1 else "inventura"
os.makedirs(OUT, exist_ok=True)
LAT, LON, R_KM = 49.11, 17.17, 45
UA = {"User-Agent": "korycany-voda-inventura/0.1"}
CH = "https://opendata.chmi.cz"


def get(url, timeout=90):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        try:
            telo = e.read()[:400].decode("utf-8", "replace")
        except Exception:
            telo = ""
        print(f"  HTTP {e.code} {url} {telo}", flush=True)
    except Exception as e:  # noqa
        print(f"  CHYBA {e!r} {url}", flush=True)
    return None


def zapis(nazev, text):
    with open(os.path.join(OUT, nazev), "w", encoding="utf-8") as f:
        f.write(text)


def km(lon1, lat1, lon2, lat2):
    p1, p2, dl = math.radians(lat1), math.radians(lat2), math.radians(lon2 - lon1)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def odkazy(url):
    b = get(url)
    if b is None:
        return None
    return [h for h in re.findall(r'href="([^"?#]+)"', b.decode("utf-8", "replace")) if not h.startswith(("/", "http", ".."))]


def strom(url, hloubka, max_souboru=12, out=None, odsad=0):
    out = [] if out is None else out
    l = odkazy(url)
    if l is None:
        out.append("  " * odsad + "(nedostupné) " + url); return out
    slozky, soubory = [x for x in l if x.endswith("/")], [x for x in l if not x.endswith("/")]
    out.append("  " * odsad + f"{url}  [{len(slozky)} složek, {len(soubory)} souborů]")
    for s in soubory[:max_souboru]:
        out.append("  " * (odsad + 1) + s)
    if len(soubory) > max_souboru:
        out.append("  " * (odsad + 1) + f"... a dalších {len(soubory) - max_souboru}")
    if hloubka > 0:
        for s in slozky[:40]:
            strom(url + s, hloubka - 1, max_souboru, out, odsad + 1)
    return out


def pdf_text(url, nazev):
    b = get(url)
    if b is None:
        return
    p = os.path.join(OUT, nazev + ".pdf")
    open(p, "wb").write(b)
    try:
        subprocess.run(["pdftotext", "-layout", p, os.path.join(OUT, nazev + ".txt")], check=True)
    except Exception as e:  # noqa
        print("  pdftotext selhal", e)
    os.remove(p)


# ---------------------------------------------------------------- 1. ČHMÚ klima: prvky stanic v okolí
print("1) CHMU klima - stanice a prvky do", R_KM, "km", flush=True)
M = CH + "/meteorology/climate/historical_csv/metadata/"
zapis("chmu_klima_strom.txt", "\n".join(strom(CH + "/meteorology/climate/historical_csv/", 3, 4)))
blizke = {}
m1 = get(M + "meta1.csv")
if m1:
    for r in csv.DictReader(io.StringIO(m1.decode("utf-8-sig"))):
        try:
            d = km(LON, LAT, float(r["GEOGR1"]), float(r["GEOGR2"]))
        except (KeyError, ValueError, TypeError):
            continue
        if d <= R_KM:
            w = r["WSI"].strip(); s = blizke.setdefault(w, {"nazev": "", "km": round(d, 1), "od": "9999", "do": "", "vyska": r.get("ELEVATION")})
            s["od"] = min(s["od"], (r.get("BEGIN_DATE") or "")[:10])
            if (r.get("END_DATE") or "") > s["do"]:
                s["do"], s["nazev"] = (r.get("END_DATE") or "")[:10], (r.get("FULL_NAME") or "").strip()
print("   stanic:", len(blizke), flush=True)
m2 = get(M + "meta2.csv", 300)
prvky = {}
if m2:
    t = m2.decode("utf-8-sig"); rd = csv.DictReader(io.StringIO(t))
    print("   meta2 sloupce:", rd.fieldnames, flush=True)
    ksloupec = next((c for c in rd.fieldnames if c.upper() in ("EG_EL_ABBREVIATION", "ELEMENT", "EL_ABBREVIATION")), None)
    for r in rd:
        w = (r.get("WSI") or "").strip()
        if w in blizke:
            prvky.setdefault(w, []).append({k: v for k, v in r.items() if k != "WSI"})
    zapis("chmu_meta2_vzorek.txt", "\n".join(t.splitlines()[:15]))
vyst = [dict(wsi=w, **s, prvky=prvky.get(w, [])) for w, s in sorted(blizke.items(), key=lambda x: x[1]["km"])]
# kompaktně: denní prvky a jejich období u každé stanice
kompakt = []
for s_ in vyst:
    o = {}
    for p_ in s_["prvky"]:
        if p_.get("OBS_TYPE") != "DLY":
            continue
        e = p_["EG_EL_ABBREVIATION"]; a_, b_ = p_["BEGIN_DATE"][:4], p_["END_DATE"][:4]
        o[e] = [min(a_, o[e][0]) if e in o else a_, max(b_, o[e][1]) if e in o else b_]
    kompakt.append({k: v for k, v in s_.items() if k != "prvky"} | {"denni": {e: f"{x[0]}-{x[1]}" for e, x in sorted(o.items())}})
json.dump(kompakt, open(os.path.join(OUT, "chmu_stanice_prvky.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
# přehled: které prvky mají aktivní stanice
for s in vyst:
    zk = sorted({str(next((v for k, v in p.items() if "ABBR" in k.upper() or k.upper() == "ELEMENT"), "?")) for p in s["prvky"]})
    if s["do"].startswith("3999") or len(zk) > 3:
        print(f"   {s['km']:5.1f} km {s['nazev'][:28]:<28} {s['od'][:4]}-{s['do'][:4]} {s['wsi']}: {' '.join(zk)[:400]}", flush=True)
pdf_text(CH + "/meteorology/climate/Klimatologicka_data_popis.pdf", "chmu_klima_popis")

# ---------------------------------------------------------------- 2. ČHMÚ hydrologie (podzemní voda, průtoky)
print("2) CHMU hydrologie", flush=True)
zapis("chmu_hydro_strom.txt", "\n".join(strom(CH + "/hydrology/", 3, 8)))
for h in (odkazy(CH + "/hydrology/read_me/") or []):
    if h.lower().endswith(".pdf"):
        pdf_text(CH + "/hydrology/read_me/" + h, "chmu_hydro_" + re.sub(r"\W+", "_", h[:-4]))

# ---------------------------------------------------------------- 3. Open-Meteo (reanalýza ERA5 / ERA5-Land)
print("3) Open-Meteo", flush=True)
DV = ("et0_fao_evapotranspiration,shortwave_radiation_sum,sunshine_duration,wind_speed_10m_mean,wind_speed_10m_max,cloud_cover_mean,"
      "relative_humidity_2m_mean,vapour_pressure_deficit_max,soil_moisture_0_to_7cm_mean,soil_moisture_7_to_28cm_mean,"
      "soil_moisture_28_to_100cm_mean,soil_moisture_0_to_100cm_mean,precipitation_sum,temperature_2m_mean")
for nazev, obd, model in (("1950", "start_date=1950-07-01&end_date=1950-07-05", ""), ("2025", "start_date=2025-07-01&end_date=2025-07-05", ""),
                          ("2025_era5land", "start_date=2025-07-01&end_date=2025-07-05", "&models=era5_land"), ("1940_era5", "start_date=1940-07-01&end_date=1940-07-05", "&models=era5")):
    for v in DV.split(","):          # po jedné proměnné, ať je vidět, která neexistuje
        b = get(f"https://archive-api.open-meteo.com/v1/archive?latitude={LAT}&longitude={LON}&{obd}&daily={v}&timezone=Europe%2FBerlin{model}")
        if b:
            j = json.loads(b); print(f"   {nazev:14} {v:34} {j.get('daily', {}).get(v)} {j.get('daily_units', {}).get(v)}  bunka {j.get('latitude')},{j.get('longitude')} {j.get('elevation')} m", flush=True)

# ---------------------------------------------------------------- 4. PVGIS (družicové záření)
print("4) PVGIS", flush=True)
for db in ("PVGIS-SARAH3", "PVGIS-ERA5"):
    b = get(f"https://re.jrc.ec.europa.eu/api/v5_3/seriescalc?lat={LAT}&lon={LON}&raddatabase={db}&outputformat=json&startyear=2005&endyear=2023", 180)
    if b:
        j = json.loads(b); h = j.get("outputs", {}).get("hourly", [])
        print("   ", db, "hodin:", len(h), "od", h[0]["time"] if h else None, "do", h[-1]["time"] if h else None, json.dumps(j.get("inputs", {}).get("meteo_data"))[:300], flush=True)
        zapis(f"pvgis_{db}_meta.json", json.dumps({k: v for k, v in j.items() if k != "outputs"}, indent=1)[:6000])

# ---------------------------------------------------------------- 5. Intersucho, podmínky
print("5) Intersucho", flush=True)
b = get("https://www.intersucho.cz/")
if b:
    t = b.decode("utf-8", "replace")
    l = sorted(set(re.findall(r'href="([^"]+)"', t)))
    zapis("intersucho_odkazy.txt", "\n".join(l))
    print("   odkazy s daty/podminkami:", [x for x in l if re.search(r"podmin|licen|data|api|wms|stazen|download|o-projektu|kontakt", x, re.I)][:40], flush=True)
for cesta in ("/cs/licence-a-odpovednost/", "/cs/o-projektu/"):
    b = get("https://www.intersucho.cz" + cesta)
    if b:
        t = re.sub(r"(?s)<(script|style).*?</\1>", " ", b.decode("utf-8", "replace")); t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"\s+", " ", t)
        zapis("intersucho" + cesta.replace("/", "_") + ".txt", t[:12000])

# ---------------------------------------------------------------- 6. ČHMÚ hydrologie: objekty v okolí (vrty, prameny, vodoměrné stanice)
print("6) CHMU hydro objekty do 30 km", flush=True)


def tabulky(o, out):
    if isinstance(o, dict):
        if "header" in o and "values" in o:
            out.append(o)
        for v in o.values():
            tabulky(v, out)
    elif isinstance(o, list):
        for v in o[:50]:
            if isinstance(v, (dict, list)):
                tabulky(v, out)
    return out


for nazev, url in (("podzemni_historical", CH + "/hydrology/groundwater/historical/metadata/meta1.json"), ("podzemni_now", CH + "/hydrology/groundwater/now/metadata/meta1.json"),
                   ("povrchove_now", CH + "/hydrology/now/metadata/meta1.json"), ("podzemni_historical_meta2", CH + "/hydrology/groundwater/historical/metadata/meta2.json")):
    b = get(url, 300)
    if not b:
        continue
    try:
        j = json.loads(b)
    except Exception as e:  # noqa
        print("  neni JSON", nazev, e); zapis(f"hydro_{nazev}_zacatek.txt", b[:3000].decode("utf-8", "replace")); continue
    tt = tabulky(j, [])
    print("  ", nazev, "tabulek:", len(tt), "klice:", list(j)[:8] if isinstance(j, dict) else type(j), flush=True)
    if not tt:
        zapis(f"hydro_{nazev}_zacatek.txt", json.dumps(j, ensure_ascii=False)[:3000]); continue
    for t in tt[:2]:
        h = t["header"].split(",") if isinstance(t["header"], str) else list(t["header"])
        print("   sloupce:", h, "radku:", len(t["values"]), flush=True)
        ix = [i for i, c in enumerate(h) if re.search(r"GEOGR|LAT|LON|^X$|^Y$", c, re.I)]
        vyber = []
        for r in t["values"]:
            cis = [r[i] for i in ix if isinstance(r[i], (int, float))]
            la = next((c for c in cis if 48 < c < 51.5), None); lo = next((c for c in cis if 12 < c < 19), None)
            if la and lo and km(LON, LAT, lo, la) <= 30:
                vyber.append([round(km(LON, LAT, lo, la), 1)] + r)
        vyber.sort(key=lambda r: r[0])
        zapis(f"hydro_{nazev}_blizke.json", json.dumps({"sloupce": ["km"] + h, "radky": vyber if ix else t["values"][:5]}, ensure_ascii=False, indent=0))
        for r in vyber[:25]:
            print("    ", r, flush=True)
print("hotovo", flush=True)
