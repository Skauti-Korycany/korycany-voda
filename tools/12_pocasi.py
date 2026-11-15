#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12_pocasi.py - denni sber pocasi pro zalozku "Jak bylo" (Korycany).

Zdroje (overeno 21. 10. 2026):
 - CHMU opendata, recent daily JSON (predbezna data, mesicni soubory):
     Korycany    0-203-0-41701068002  manualni, jen srazky (SRA 06:00 = klimatologicky den 06-06 UTC)
     Nemochovice 0-203-0-41503035001  klimatologicka, T/TMA/TMI/H/F/SRA
   Pozor: manualni Korycany chodi se zpozdenim (cely bezici mesic byva QUALITY 4 = chybi).
 - Povodi Moravy, KS Korycany: HTML tabulka "Poslednich 24h", hodinove mm a C, mistni cas, bez archivu
 - hladiny.cz, Nemotice_SR: HTML tabulka ~10 h hodinovych mm, mistni cas, bez archivu
 - ET0 = Penman-Monteith (FAO-56 rov. 6): T/TMA/TMI/H/F Nemochovice + slunecni svit Stare Mesto / Kromeriz / Holesov;
   bez svitu zareni z rozpeti teplot (rov. 50). Do 15. 11. 2026 Hargreaves-Samani (rov. 52), ktery pro Korycany nadhodnocoval o ~23 %.
   zdroj: Allen a kol. 1998, FAO Irrigation and Drainage Paper 56, kap. 3 (rov. 52) a kap. 3 priloha (Ra)

Vystupy (vse v data/pocasi/, do gitu):
 - denni.json        {datum: {P_kor, P_pmo, P_nem, T, Tmin, Tmax, H, F, ET0, bil, zdroj_P}} + metadata; sloucuje se s existujicim
 - pmo_korycany.csv  hodinovy archiv KS Korycany (cas_mistni;mm;C), prirustkove, bez duplicit
 - nemotice.csv      hodinovy archiv Nemotice_SR (cas_mistni;mm)
 - log.txt           posledni beh

Spusteni: python tools/12_pocasi.py            (stahuje z internetu - GitHub Actions nebo PC)
          python tools/12_pocasi.py --vzorek data/pocasi/vzorek   (test bez site: cte stazene soubory)
          python tools/12_pocasi.py --mesicu 10                    (jednorazove doplneni od ledna 2026)
"""
import csv
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import unescape
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(REPO, "data", "pocasi")
os.makedirs(OUTDIR, exist_ok=True)
VZOREK = None
if "--vzorek" in sys.argv:
    VZOREK = os.path.abspath(sys.argv[sys.argv.index("--vzorek") + 1])

CHMU = "https://opendata.chmi.cz/meteorology/climate/recent/data/daily"
WSI_KOR = "0-203-0-41701068002"
WSI_NEM = "0-203-0-41503035001"
URL_PMO = "https://sap.pmo.cz/portal/Srazky/cz/pc/Mereni.aspx?id=60&oid=3"
URL_NEMOTICE = "https://www.hladiny.cz/hladiny/index.php?ca=196&cs=50089"
LAT = 49.11          # KS Korycany 49.1175 N
UA = "Mozilla/5.0 (korycany-voda; skautsky oddil Korycany; nekomercni)"
TZ = ZoneInfo("Europe/Prague")
DNES = datetime.now(timezone.utc)
LOG = []


def log(m):
    print(m)
    LOG.append(m)


# ---------------------------------------------------------------- stazeni
def stahni(url, nazev):
    """Vrati text, nebo None. V rezimu --vzorek cte soubor nazev z adresare vzorku."""
    if VZOREK:
        p = os.path.join(VZOREK, nazev)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8-sig", errors="replace") as f:
                return f.read()
        log(f"  vzorek chybi: {nazev}")
        return None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8-sig", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            log(f"  HTTP {e.code} {url}")
        except Exception as e:  # noqa
            log(f"  chyba {e} {url}")
        time.sleep(5)
    return None


# ---------------------------------------------------------------- CHMU
def chmu_mesic(wsi, rok, mes):
    nazev = f"dly-{wsi}-{rok}{mes:02d}.json"
    for url in (f"{CHMU}/{nazev}", f"{CHMU}/{mes:02d}/{nazev}"):
        t = stahni(url, nazev)
        if t and t.lstrip().startswith("{"):
            return json.loads(t)
    return None


def chmu_zaznamy(j):
    """recent JSON: data.data.header 'STATION,ELEMENT,VTYPE,DT,VAL,FLAG,QUALITY', values = seznam radku."""
    out = []

    def projdi(x):
        if isinstance(x, dict):
            if "header" in x and isinstance(x.get("values"), list):
                h = [c.strip().upper() for c in x["header"].split(",")]
                for row in x["values"]:
                    out.append(dict(zip(h, row)))
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
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def serie(zaznamy, element, vtype):
    """{datum: hodnota} pro prvek a termin; vyrazeno QUALITY >= 4 nebo prazdne VAL.
    Datum = datum z DT (u SRA 06:00 = zacatek klimatologickeho dne, viz docs/SRAZKY.md)."""
    s = {}
    for r in zaznamy:
        if r.get("ELEMENT") != element or str(r.get("VTYPE")) != vtype:
            continue
        v, q = fl(r.get("VAL")), fl(r.get("QUALITY"))
        if v is None or (q is not None and q >= 4):
            continue
        s[str(r.get("DT"))[:10]] = v
    return s


MESICU = int(sys.argv[sys.argv.index("--mesicu") + 1]) if "--mesicu" in sys.argv else 3


def chmu_stanice(wsi, prvky):
    """Stahne poslednich MESICU mesicu (manualni Korycany chodi ~6 tydnu pozadu), vrati {prvek: {datum: hodnota}}."""
    mesice, d = [], DNES.replace(day=1)
    for i in range(MESICU):
        mesice.append((d.year, d.month))
        d = (d - timedelta(days=1)).replace(day=1)
    zaz = []
    for rok, mes in mesice:
        j = chmu_mesic(wsi, rok, mes)
        if j is None:
            log(f"  {wsi} {rok}-{mes:02d}: soubor neni (404)")
            continue
        z = chmu_zaznamy(j)
        log(f"  {wsi} {rok}-{mes:02d}: {len(z)} zaznamu")
        zaz += z
    return {k: serie(zaz, el, vt) for k, (el, vt) in prvky.items()}


# ---------------------------------------------------------------- Povodi Moravy
def pmo_tabulka(html):
    """[(datetime mistni, mm, C)] z tabulky ObsahCPH_dataMereni24hGV."""
    out = []
    m = re.search(r'id="ObsahCPH_dataMereni24hGV".*?</table>', html, re.S | re.I)
    if not m:
        log("  PMO: tabulka nenalezena")
        return out
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0), re.S | re.I):
        bunky = [unescape(re.sub(r"<[^>]+>", " ", b)).strip() for b in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.I)]
        if len(bunky) < 2:
            continue
        try:
            t = datetime.strptime(bunky[0], "%d.%m.%Y %H:%M").replace(tzinfo=TZ)
        except ValueError:
            continue
        mm = fl(bunky[1].replace(",", "."))
        tc = fl(bunky[2].replace(",", ".")) if len(bunky) > 2 else None
        out.append((t, mm, tc))
    return out


# ---------------------------------------------------------------- hladiny.cz
def nemotice_tabulka(html):
    """[(datetime mistni, mm)]; tabulka ma jen casy, datum odvozeno od 'Posledni stav : X mm (St 21.10.2026 05:00)'."""
    out = []
    m = re.search(r"Posledn[^(]*\(\w+\s+(\d{1,2})\.(\d{1,2})\.(\d{4})\s+(\d{1,2}):(\d{2})\)", html)
    if not m:
        log("  Nemotice: kotva 'Posledni stav' nenalezena")
        return out
    d, mo, y, h, mi = map(int, m.groups())
    kotva = datetime(y, mo, d, h, mi, tzinfo=TZ)
    t = re.search(r'id="tabulkavpravo".*?</TABLE>', html, re.S | re.I)
    if not t:
        log("  Nemotice: tabulka nenalezena")
        return out
    den = kotva.date()
    minula = None
    for tr in re.findall(r"<TR[^>]*>(.*?)</TR>", t.group(0), re.S | re.I):
        b = [unescape(re.sub(r"<[^>]+>", " ", x)).strip() for x in re.findall(r"<TD[^>]*>(.*?)</TD>", tr, re.S | re.I)]
        if len(b) < 2 or not re.match(r"\d{1,2}:\d{2}$", b[0]):
            continue
        hh, mm_ = map(int, b[0].split(":"))
        if minula is not None and (hh, mm_) > minula:
            den -= timedelta(days=1)          # radky jdou od nejnovejsiho dolu; skok vzhuru = predchozi den
        minula = (hh, mm_)
        cas = datetime(den.year, den.month, den.day, hh, mm_, tzinfo=TZ)
        if cas > kotva:
            cas -= timedelta(days=1)
            den -= timedelta(days=1)
        out.append((cas, fl(b[1].replace(",", "."))))
    return out


# ---------------------------------------------------------------- CSV archiv
def csv_nacti(cesta):
    rows = {}
    if os.path.exists(cesta):
        with open(cesta, "r", encoding="utf-8", newline="") as f:
            for r in csv.reader(f, delimiter=";"):
                if r and re.match(r"\d{4}-\d{2}-\d{2}T", r[0]):
                    rows[r[0]] = r
    return rows


def csv_uloz(cesta, hlavicka, rows):
    with open(cesta, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(hlavicka)
        for k in sorted(rows):
            w.writerow(rows[k])


def num(x):
    return "" if x is None else f"{x:g}"


# ---------------------------------------------------------------- ET0 Hargreaves-Samani (FAO-56), jen pro srovnani
def ra_mm(den: date, lat_deg=LAT):
    """Extraterestricka radiace, FAO-56 rov. 21-24, vysledek v mm/den (x 0.408)."""
    J = den.timetuple().tm_yday
    phi = math.radians(lat_deg)
    dr = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
    delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    ws = math.acos(-math.tan(phi) * math.tan(delta))
    ra = 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.sin(ws))
    return 0.408 * ra


def et0_hs(den: date, tmean, tmin, tmax):
    """Hargreaves-Samani, FAO-56 rov. 52: ET0 = 0.0023 (Tmean + 17.8) sqrt(Tmax - Tmin) Ra."""
    if None in (tmean, tmin, tmax) or tmax < tmin:
        return None
    return round(0.0023 * (tmean + 17.8) * math.sqrt(tmax - tmin) * ra_mm(den), 2)


# ---------------------------------------------------------------- hlavni beh
# ---------------------------------------------------------------- ET0 Penman-Monteith (FAO-56), od 15. 11. 2026 hlavni metoda
ALT = 300            # nadmorska vyska Korycan [m]
U2_NAHRADNI = 1.4    # m/s ve 2 m, dlouhodoby prumer Nemochovic (1,9 m/s v 10 m); pouzije se, jen kdyz vitr chybi
S_STANICE = [("0-203-0-11754", "Staré Město", 19), ("0-203-0-11751", "Kroměříž", 27), ("0-20000-0-11774", "Holešov", 37)]


def _es(t):
    return 0.6108 * math.exp(17.27 * t / (t + 237.3))


def et0_pm(den: date, tmean, tmin, tmax, rh=None, u10=None, svit_h=None, lat_deg=LAT, alt=ALT):
    """Penman-Monteith, FAO-56 (Allen a kol. 1998) rov. 6. Vraci (ET0 mm/den, zpusob).
    Zareni: ze slunecniho svitu (Angstrom, rov. 35, a_s 0,25, b_s 0,50); bez svitu z rozpeti teplot (rov. 50, kRs 0,16).
    Tlak pary: z prumerne relativni vlhkosti (rov. 19); bez vlhkosti z minimalni teploty (rov. 48).
    Vitr: mereny v 10 m prepocteny na 2 m (rov. 47); bez vetru U2_NAHRADNI. G = 0, albedo 0,23.
    zpusob: 'pm' = vse mereno, jinak 'pm-' + chybejici vstupy (s svit, h vlhkost, f vitr)."""
    if None in (tmean, tmin, tmax) or tmax < tmin:
        return None, None
    ra = ra_mm(den, lat_deg) / 0.408                       # MJ/m2/den
    J = den.timetuple().tm_yday
    delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)
    N = 24 / math.pi * math.acos(-math.tan(math.radians(lat_deg)) * math.tan(delta))
    chybi = ""
    if svit_h is not None:
        rs = (0.25 + 0.50 * min(1.0, max(0.0, svit_h / N))) * ra
    else:
        rs = min(0.16 * math.sqrt(tmax - tmin), 0.75 + 2e-5 * alt) * ra; chybi += "s"
    rso = (0.75 + 2e-5 * alt) * ra
    esm = (_es(tmax) + _es(tmin)) / 2
    if rh is not None:
        ea = min(esm, rh / 100 * esm)
    else:
        ea = _es(tmin); chybi += "h"
    if u10 is not None:
        u2 = u10 * 4.87 / math.log(67.8 * 10 - 5.42)
    else:
        u2 = U2_NAHRADNI; chybi += "f"
    rn = 0.77 * rs - 4.903e-9 * ((tmax + 273.16) ** 4 + (tmin + 273.16) ** 4) / 2 * (0.34 - 0.14 * math.sqrt(ea)) * (1.35 * min(1.0, rs / rso) - 0.35)
    P = 101.3 * ((293 - 0.0065 * alt) / 293) ** 5.26
    g = 0.000665 * P
    D = 4098 * _es(tmean) / (tmean + 237.3) ** 2
    et = (0.408 * D * rn + g * 900 / (tmean + 273) * u2 * (esm - ea)) / (D + g * (1 + 0.34 * u2))
    return round(max(0.0, et), 2), "pm" + ("-" + chybi if chybi else "")


def main():
    log(f"12_pocasi.py {DNES:%Y-%m-%d %H:%M} UTC" + (f" (vzorek {VZOREK})" if VZOREK else ""))

    log("1) CHMU Korycany (srazky)")
    kor = chmu_stanice(WSI_KOR, {"P": ("SRA", "06:00")})
    log("2) CHMU Nemochovice")
    nem = chmu_stanice(WSI_NEM, {"P": ("SRA", "06:00"), "T": ("T", "AVG"), "Tmax": ("TMA", "20:00"),
                                 "Tmin": ("TMI", "20:00"), "H": ("H", "AVG"), "F": ("F", "AVG")})
    for k, v in nem.items():
        log(f"  Nemochovice {k}: {len(v)} dni" + (f" ({min(v)}..{max(v)})" if v else ""))
    log(f"  Korycany P: {len(kor['P'])} dni s hodnotou")
    log("2b) slunecni svit (pro vypar)")
    svit, svit_zdroj = {}, {}
    for wsi, jm, km in S_STANICE:
        try:
            x = chmu_stanice(wsi, {"S": ("SSV", "00:00")})["S"]
        except Exception as e:  # noqa - svit je doplnek, nesmi shodit sber
            log(f"  svit {jm}: chyba {e!r}"); x = {}
        log(f"  svit {jm}: {len(x)} dni" + (f" ({min(x)}..{max(x)})" if x else ""))
        for d, v in x.items():
            if d not in svit and 0 <= v <= 17:
                svit[d], svit_zdroj[d] = v, jm

    log("3) Povodi Moravy KS Korycany")
    pmo = pmo_tabulka(stahni(URL_PMO, "pmo_korycany.html") or "")
    log(f"  {len(pmo)} hodinovych radku" + (f" ({pmo[-1][0]:%d.%m. %H:%M} - {pmo[0][0]:%d.%m. %H:%M})" if pmo else ""))
    c = os.path.join(OUTDIR, "pmo_korycany.csv")
    rows = csv_nacti(c)
    for t, mm, tc in pmo:
        rows[t.isoformat()] = [t.isoformat(), num(mm), num(tc)]
    csv_uloz(c, ["cas_mistni", "srazka_mm_h", "teplota_C"], rows)
    pmo_vse = {k: (fl(v[1]), fl(v[2])) for k, v in rows.items()}
    log(f"  archiv pmo_korycany.csv: {len(rows)} radku")

    log("4) hladiny.cz Nemotice_SR")
    nmt = nemotice_tabulka(stahni(URL_NEMOTICE, "nemotice.html") or "")
    log(f"  {len(nmt)} hodinovych radku" + (f" ({nmt[-1][0]:%d.%m. %H:%M} - {nmt[0][0]:%d.%m. %H:%M})" if nmt else ""))
    c = os.path.join(OUTDIR, "nemotice.csv")
    rows = csv_nacti(c)
    for t, mm in nmt:
        rows[t.isoformat()] = [t.isoformat(), num(mm)]
    csv_uloz(c, ["cas_mistni", "srazka_mm_h"], rows)
    log(f"  archiv nemotice.csv: {len(rows)} radku")

    # denni suma PMO za klimatologicky den (06 UTC dne D az 06 UTC dne D+1); jen kdyz je vsech 24 hodin
    pmo_den, pmo_t = {}, {}
    hod = {}
    for k, (mm, tc) in pmo_vse.items():
        t = datetime.fromisoformat(k).astimezone(timezone.utc)
        if mm is None:
            continue
        # hodinova hodnota v case t pokryva (t-1h, t]; klimatologicky den D zacina v 06:00 UTC
        d = (t - timedelta(hours=6, minutes=1)).date()
        hod.setdefault(d, []).append((mm, tc))
    for d, v in hod.items():
        if len(v) >= 24:
            pmo_den[d.isoformat()] = round(sum(x[0] for x in v), 1)
            tt = [x[1] for x in v if x[1] is not None]
            if len(tt) >= 20:
                pmo_t[d.isoformat()] = (round(min(tt), 1), round(max(tt), 1), round(sum(tt) / len(tt), 1))

    log("5) denni.json")
    c = os.path.join(OUTDIR, "denni.json")
    stary = {}
    if os.path.exists(c):
        with open(c, "r", encoding="utf-8") as f:
            stary = json.load(f).get("dny", {})
    dny = dict(stary)
    datumy = set(kor["P"]) | set(nem["P"]) | set(nem["T"]) | set(pmo_den)
    for d in sorted(datumy):
        dd = date.fromisoformat(d)
        z = dict(dny.get(d, {}))
        z.update({"P_kor": kor["P"].get(d, z.get("P_kor")), "P_pmo": pmo_den.get(d, z.get("P_pmo")), "P_nem": nem["P"].get(d, z.get("P_nem")),
                  "T": nem["T"].get(d, z.get("T")), "Tmin": nem["Tmin"].get(d, z.get("Tmin")), "Tmax": nem["Tmax"].get(d, z.get("Tmax")),
                  "H": nem["H"].get(d, z.get("H")), "F": nem["F"].get(d, z.get("F")),
                  "S": svit.get(d, z.get("S")), "zdroj_S": svit_zdroj.get(d, z.get("zdroj_S"))})
        if d in pmo_t:
            z["T_pmo"] = {"min": pmo_t[d][0], "max": pmo_t[d][1], "avg": pmo_t[d][2]}
        # srazky Korycany: 1) CHMU Korycany (manualni, se zpozdenim), 2) KS Korycany PMO, 3) Nemochovice
        if z.get("P_kor") is not None:
            z["P"], z["zdroj_P"] = z["P_kor"], "chmu_korycany"
        elif z.get("P_pmo") is not None:
            z["P"], z["zdroj_P"] = z["P_pmo"], "pmo_korycany"
        elif z.get("P_nem") is not None:
            z["P"], z["zdroj_P"] = z["P_nem"], "chmu_nemochovice"
        else:
            z["P"], z["zdroj_P"] = None, None
        dny[d] = z
    # svit i pro starsi dny, ktere uz v denni.json jsou (prvni beh po zmene metody: --mesicu 12)
    for d, v in svit.items():
        if d in dny and dny[d].get("S") is None:
            dny[d]["S"], dny[d]["zdroj_S"] = v, svit_zdroj[d]
    # vypar se prepocita pro vsechny dny z ulozenych vstupu, aby cela rada mela jednu metodu
    for d, z in dny.items():
        z["ET0"], z["zdroj_ET0"] = et0_pm(date.fromisoformat(d), z.get("T"), z.get("Tmin"), z.get("Tmax"), z.get("H"), z.get("F"), z.get("S"))
        z["bil"] = round(z["P"] - z["ET0"], 2) if z.get("P") is not None and z["ET0"] is not None else None
    out = {
        "vytvoreno": DNES.strftime("%Y-%m-%dT%H:%MZ"),
        "stanice": {
            "chmu_korycany": {"wsi": WSI_KOR, "nazev": "Koryčany", "typ": "manuální srážkoměrná ČHMÚ", "vyska_m": 305, "km": 1.2,
                              "prvky": "SRA 06:00 (klimatologický den 06-06 UTC)", "pozn": "předběžná data, přichází se zpožděním"},
            "chmu_nemochovice": {"wsi": WSI_NEM, "nazev": "Nemochovice", "typ": "klimatologická ČHMÚ", "vyska_m": 283, "km": 7.8,
                                 "prvky": "SRA 06:00, T AVG, TMA 20:00, TMI 20:00, H AVG, F AVG"},
            "pmo_korycany": {"nazev": "KS Koryčany", "typ": "srážkoměr + teploměr Povodí Moravy, areál pod VD Koryčany",
                             "url": URL_PMO, "pozn": "data bez záruky, jen posledních 24 h online; vlastní archiv v pmo_korycany.csv, místní čas"},
            "nemotice": {"nazev": "Nemotice_SR", "typ": "srážkoměr obce (Fiedler, hladiny.cz)", "url": URL_NEMOTICE,
                         "pozn": "jen ~10 h online; vlastní archiv v nemotice.csv, místní čas"},
        },
        "metoda": {
            "P": "srážky Koryčany: přednostně ČHMÚ Koryčany, jinak suma hodinových hodnot KS Koryčany za klimatologický den 06-06 UTC (jen při úplných 24 h), jinak Nemochovice; pole zdroj_P",
            "ET0": "Penman-Monteith, FAO-56 (Allen a kol. 1998) rov. 6: teplota, vlhkost a vítr (10 m -> 2 m) Nemochovice, sluneční svit Staré Město / Kroměříž / Holešov (pole S, zdroj_S), záření ze svitu rov. 35 (0,25 / 0,50); bez svitu z rozpětí teplot rov. 50; pole zdroj_ET0 (pm = vše měřeno, pm-s bez svitu, pm-h bez vlhkosti, pm-f bez větru)",
            "bil": "P - ET0 [mm/den]",
            "licence": "ČHMÚ otevřená data (podmínky na opendata.chmi.cz); Povodí Moravy a hladiny.cz: podmínky neuvedeny, zobrazovat jen agregace",
        },
        "dny": {k: dny[k] for k in sorted(dny)},
        "log": LOG,
    }
    with open(c, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    s_et = [v["ET0"] for v in dny.values() if v.get("ET0") is not None]
    zp = {}
    for v in dny.values():
        zp[v.get("zdroj_ET0")] = zp.get(v.get("zdroj_ET0"), 0) + 1
    log(f"  zpusob vypoctu vyparu (dni): {zp}")
    log(f"  dni celkem {len(dny)}, s ET0 {len(s_et)}, s P {sum(1 for v in dny.values() if v.get('P') is not None)}")
    with open(os.path.join(OUTDIR, "log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
