#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_balicek_web.py - datovy balicek rastru pro webovou aplikaci (jadro.js).

Vstup: rastry v data/dmr/ (vystupy 01-06, EPSG:5514, 5 m). Vystup: data/web/
 - rastr.json  : mrizka (pocatek, krok, rozmery), kodovani pasem, polynomy WGS84 <-> S-JTSK, zdroje
 - *.png       : jedno pasmo = jeden PNG (8 bit = odstiny sede; 16 bit = R vysoky + G nizky bajt)

Proc PNG: prohlizec ho dekoduje sam (canvas), bez knihoven; komprese je bezztratova.
Proc zustava mrizka S-JTSK: smer odtoku (D8) a sousednost bunek plati jen v puvodni mrizce; prevod souradnic
 WGS84 <-> S-JTSK dela polynom 2. radu spocitany tady pyprojem (chyba < 1 cm na uzemi modelu), takze
 aplikace zadnou projekci neresi. Zobrazeni do mapy (Web Mercator) dela jadro.js prevzorkovanim pres tyz polynom.

Spusteni: python tools/09_balicek_web.py   (potrebuje rasterio, numpy, pillow, pyproj)
"""
import json
import os
import sys
from datetime import date

import numpy as np

try:
    import rasterio
    from PIL import Image
    from pyproj import Transformer
except ImportError as e:
    sys.exit(f"chybi knihovna: {e}. Spust vyrob_balicek_web.bat (nainstaluje) nebo pip install rasterio pillow pyproj")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DMR = os.path.join(REPO, "data", "dmr")
OUT = os.path.join(REPO, "data", "web")
os.makedirs(OUT, exist_ok=True)


def cti(nazev):
    with rasterio.open(os.path.join(DMR, nazev)) as d:
        return d.read(1), d


def uloz8(nazev, pole):
    Image.fromarray(pole.astype(np.uint8), mode="L").save(os.path.join(OUT, nazev), optimize=True)
    return os.path.getsize(os.path.join(OUT, nazev))


def uloz16(nazev, pole):
    p = pole.astype(np.uint16)
    rgb = np.zeros(p.shape + (3,), np.uint8)
    rgb[..., 0] = p >> 8
    rgb[..., 1] = p & 255
    Image.fromarray(rgb, mode="RGB").save(os.path.join(OUT, nazev), optimize=True)
    return os.path.getsize(os.path.join(OUT, nazev))


pasma = {}
velikosti = {}

# ---------------------------------------------------------------- mrizka
z, dz = cti("dmr5g_5m.tif")
tr = dz.transform
nrow, ncol = z.shape
x0, y1, krok = tr.c, tr.f, tr.a     # levy horni roh, krok (kladny), radky jdou dolu (tr.e = -krok)
assert abs(tr.e + krok) < 1e-9 and abs(tr.b) < 1e-9 and abs(tr.d) < 1e-9
print(f"mrizka {ncol} x {nrow}, krok {krok} m, pocatek ({x0}, {y1})")

# ---------------------------------------------------------------- pasma
nd = dz.nodata
platne = z != nd
vz = np.where(platne, np.round((z - 200.0) * 10.0), 0).clip(0, 65535)
velikosti["vyska"] = uloz16("vyska.png", vz)
pasma["vyska"] = {"soubor": "vyska.png", "bity": 16, "jednotka": "m n. m. (Bpv)", "dekod": "m = 200 + hodnota / 10", "nodata": 0,
                  "zdroj": "CUZK DMR 5G (CC BY 4.0), 01_dmr_grid.py"}

s, ds = cti("sklon_deg.tif")
sv = np.where(s != ds.nodata, np.round(s * 4.0), 255).clip(0, 255)
velikosti["sklon"] = uloz8("sklon.png", sv)
pasma["sklon"] = {"soubor": "sklon.png", "bity": 8, "jednotka": "stupne", "dekod": "deg = hodnota / 4 (max 63,5)", "nodata": 255,
                  "zdroj": "02_rozvodnice.py (Horn)"}

a, da = cti("akumulace.tif")
av = np.where(a > 0, 1 + np.round(40.0 * np.log10(np.maximum(a, 1))), 0).clip(0, 255)
velikosti["akumulace"] = uloz8("akumulace.png", av)
pasma["akumulace"] = {"soubor": "akumulace.png", "bity": 8, "jednotka": "pocet bunek nad bunkou (vcetne)", "dekod": "bunek = 10 ** ((hodnota - 1) / 40); presnost ~6 %",
                      "nodata": 0, "zdroj": "02_rozvodnice.py (D8)"}

d8, dd = cti("smer_odtoku.tif")
velikosti["smer"] = uloz8("smer.png", np.where(d8 != dd.nodata, d8, 255))
pasma["smer"] = {"soubor": "smer.png", "bity": 8, "jednotka": "kod D8", "dekod": "1=V, 2=JV, 4=J, 8=JZ, 16=Z, 32=SZ, 64=S, 128=SV, 0=bez odtoku (deprese/okraj)",
                 "nodata": 255, "zdroj": "02_rozvodnice.py"}

for nazev, soubor, popis, zdroj in [
    ("cn", "cn.tif", "CN (IPS II), 0 = mimo", "06_cn.py, Janecek 2012 + TR-55"),
    ("vyuziti", "vyuziti_kod.tif", "kod vyuziti pudy, legenda data/vyuziti_pudy.json", "04_vyuziti_pudy.py (ZABAGED, INSPIRE BU)"),
    ("hsp", "hsp.tif", "hydrologicka skupina pud 1=A 2=B 3=C 4=D, 0 = mimo", "05_hsp.py (BPEJ SPU + Janecek tab. 2.2)"),
    ("hsp_zdroj", "hsp_zdroj.tif", "1 = z BPEJ, 2 = odhad (nejblizsi bonitovana plocha), 3 = VUMOP", "05_hsp.py"),
    ("povodi", "povodi_id.tif", "id dilciho povodi (data/povodi.geojson, typ sidlo), 0 = mimo", "02_rozvodnice.py"),
]:
    p, dp = cti(soubor)
    velikosti[nazev] = uloz8(nazev + ".png", np.where(p != dp.nodata, p, 0))
    pasma[nazev] = {"soubor": nazev + ".png", "bity": 8, "jednotka": popis, "dekod": "hodnota primo", "nodata": 0, "zdroj": zdroj}

# USLE (11_usle.py) - volitelne, kdyz rastry existuji
if os.path.exists(os.path.join(DMR, "usle_ls.tif")):
    ls, dls = cti("usle_ls.tif"); vyk, _ = cti("vyuziti_kod.tif"); orna = vyk == 1   # jen orna puda (mensi PNG)
    velikosti["usle_ls"] = uloz8("usle_ls.png", np.where((ls != dls.nodata) & orna, np.clip(np.round(ls * 10), 0, 255), 0))
    pasma["usle_ls"] = {"soubor": "usle_ls.png", "bity": 8, "jednotka": "LS faktor USLE (jen orna puda)", "dekod": "LS = hodnota / 10 (max 25,5)", "nodata": 0, "zdroj": "11_usle.py (Janecek 2012 rov. 1.6-1.8, l z akumulace D8, strop 300 m)"}
    kk, dk = cti("usle_k.tif")
    velikosti["usle_k"] = uloz8("usle_k.png", np.where((kk != dk.nodata) & orna, np.clip(np.round(kk * 100), 0, 255), 0))
    pasma["usle_k"] = {"soubor": "usle_k.png", "bity": 8, "jednotka": "K faktor USLE (jen orna puda)", "dekod": "K = hodnota / 100", "nodata": 0, "zdroj": "11_usle.py (HPJ z BPEJ, Janecek 2012 tab. 1.5)"}

# ---------------------------------------------------------------- polynomy WGS84 <-> S-JTSK
t = Transformer.from_crs("EPSG:5514", "EPSG:4326", always_xy=True)
xs, ys = np.meshgrid(np.linspace(x0, x0 + ncol * krok, 41), np.linspace(y1 - nrow * krok, y1, 41))
xs, ys = xs.ravel(), ys.ravel()
lon, lat = t.transform(xs, ys)
lon0, lat0, xc, yc = float(lon.mean()), float(lat.mean()), float(xs.mean()), float(ys.mean())


def navrh(u, v):
    return np.stack([np.ones_like(u), u, v, u * u, u * v, v * v], 1)


A = navrh((lon - lon0) * 100.0, (lat - lat0) * 100.0)       # vstup ve stovkach stupnu... = (deg * 100) kvuli podminenosti
cx = np.linalg.lstsq(A, xs, rcond=None)[0]
cy = np.linalg.lstsq(A, ys, rcond=None)[0]
B = navrh((xs - xc) / 1000.0, (ys - yc) / 1000.0)
cl = np.linalg.lstsq(B, lon, rcond=None)[0]
ca = np.linalg.lstsq(B, lat, rcond=None)[0]
err_xy = max(float(np.abs(A @ cx - xs).max()), float(np.abs(A @ cy - ys).max()))
err_ll_m = max(float(np.abs(B @ cl - lon).max() * 111320 * np.cos(np.radians(lat0))), float(np.abs(B @ ca - lat).max() * 111320))
print(f"polynom 2. radu: chyba WGS84->S-JTSK {err_xy:.4f} m, S-JTSK->WGS84 {err_ll_m:.4f} m")

# kontrolni body pro testy jadra (pyproj = reference)
kb = []
for X, Y in [(x0 + 100 * krok, y1 - 100 * krok), (x0 + 700 * krok, y1 - 800 * krok), (x0 + 1400 * krok, y1 - 1500 * krok), (-559180.53, -1174691.52)]:
    lo, la = t.transform(X, Y)
    kb.append({"xy5514": [X, Y], "lonlat": [float(lo), float(la)]})

lon_min, lat_min = t.transform(x0, y1 - nrow * krok)
lon_max, lat_max = t.transform(x0 + ncol * krok, y1)

info = {
    "verze": 1, "datum": date.today().isoformat(),
    "pozn": "mrizka EPSG:5514 (S-JTSK), radek 0 = sever. Bunka (col,row): X = x0 + (col+0.5)*krok, Y = y1 - (row+0.5)*krok.",
    "mrizka": {"epsg": 5514, "x0": x0, "y1": y1, "krok_m": krok, "ncol": ncol, "nrow": nrow, "plocha_bunky_m2": krok * krok},
    "obal_wgs84_priblizne": {"lon_min": float(lon_min), "lon_max": float(lon_max), "lat_min": float(lat_min), "lat_max": float(lat_max)},
    "prevod": {
        "pozn": "polynom 2. radu, clen = [1, u, v, u*u, u*v, v*v]; spocteno pyproj EPSG:4326 <-> EPSG:5514 na mrizce 41x41 bodu",
        "chyba_max_m": {"lonlat_na_xy": err_xy, "xy_na_lonlat": err_ll_m},
        "lonlat_na_xy": {"u": "(lon - lon0) * 100", "v": "(lat - lat0) * 100", "lon0": lon0, "lat0": lat0, "cx": cx.tolist(), "cy": cy.tolist()},
        "xy_na_lonlat": {"u": "(X - xc) / 1000", "v": "(Y - yc) / 1000", "xc": xc, "yc": yc, "clon": cl.tolist(), "clat": ca.tolist()},
        "kontrolni_body": kb,
    },
    "pasma": pasma, "velikost_B": velikosti,
    "licence": "data CC BY 4.0 (CUZK DMR 5G, ZABAGED, INSPIRE BU); BPEJ SPU otevrena data; odvozeno skripty tools/01-06",
}
with open(os.path.join(OUT, "rastr.json"), "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=1)
print("pasma:", {k: f"{v / 1024:.0f} kB" for k, v in velikosti.items()}, f"celkem {sum(velikosti.values()) / 1024 / 1024:.1f} MB")
print("zapsano", OUT)
