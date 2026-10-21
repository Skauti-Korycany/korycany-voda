# -*- coding: utf-8 -*-
"""
11_usle.py - orientační dlouhodobá ztráta půdy vodní erozí (USLE) pro ornou půdu v území modelu.
A = R * K * L * S * C * P  [t/ha/rok]

Vstupy (repo\\data\\dmr\\, mřížka 5 m, EPSG:5514): sklon_deg.tif, akumulace.tif (02_rozvodnice.py), hpj.tif (05_hsp.py), vyuziti_kod.tif (04).
R faktor: repo\\data\\vumop\\R-2022-CZ0721.tif = VÚMOP/ČHMÚ „Regionalizovaný faktor erozní účinnosti přívalového deště (R faktor) 2022“,
   okres Kroměříž, 5 m, EPSG:5514, podmínky užití „žádné neplatí“ (metadata.vumop.cz 65379397-1a6c-4f19-b153-50fe0a000319),
   stažen 21. 10. 2026 z owncloud.cesnet.cz/index.php/s/I3hc8FqLsG7wASP.
K faktor: podle HPJ, Janeček a kol. 2012 tab. 1.5 (s. 15).
L, S: Janeček 2012 rov. 1.6-1.8 (McCool): L = (l/22,13)^m, S = 10,8 sin θ + 0,03 (sklon < 9 %) / 16,8 sin θ - 0,50 (>= 9 %);
   l = délka svahu po spádnici = přispívající plocha na jednotku šířky z akumulace D8 (Desmet & Govers), omezená na L_MAX m
   (přerušení toku polní cestou, mezí, hranicí pozemku - v datech nemáme); exponent m podle sklonu (Wischmeier & Smith 1978: 0,2/0,3/0,4/0,5) - tab. 1.7 Janečka má jiné dělení, nemám ji k dispozici.
C: scénáře osevu (opatreni.json konstanty.usle.C); P = 1 (bez opatření).
Gp: přípustná ztráta 9 t/ha/rok (ostatní půdy) resp. 2 (mělké) od 1. 7. 2026 (vyhl. 240/2021 Sb., konstanty v opatreni.json); Janeček 2012 doporučuje 4.

Výstupy: data/dmr/usle_ls.tif, usle_A_C02.tif (C = 0,2, P = 1), data/usle_info.json, docs/img/usle_nahled.png
Spuštění: python tools/11_usle.py   (na PC: vyrob_usle.bat)
"""
import os, json, sys, math
import numpy as np, rasterio
from rasterio.warp import reproject, Resampling

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DMR = os.path.join(ROOT, "data", "dmr")
R_TIF = os.path.join(ROOT, "data", "vumop", "R-2022-CZ0721.tif")
L_MAX = 300.0   # m, orientační strop délky svahu (Janeček 2012: max. délka po spádnici 120/60/40 m je pro navrhování, ne pro DMR)
ORNA = 1
K_HPJ = {1: .41, 2: .46, 3: .35, 4: .16, 5: .28, 6: .32, 7: .26, 8: .49, 9: .60, 10: .53, 11: .52, 12: .50, 13: .54, 14: .59, 15: .51, 16: .51, 17: .40, 18: .24,
         19: .33, 20: .28, 21: .15, 22: .24, 23: .25, 24: .38, 25: .45, 26: .41, 27: .34, 28: .29, 29: .32, 30: .23, 31: .16, 32: .19, 33: .31, 34: .26, 35: .36,
         36: .26, 37: .16, 38: .31, 40: .24, 41: .33, 42: .56, 43: .58, 44: .56, 45: .54, 46: .47, 47: .43, 48: .41, 49: .35, 50: .33, 51: .26, 52: .37, 53: .38,
         54: .40, 55: .25, 56: .40, 57: .45, 58: .42, 59: .35, 60: .31, 61: .32, 62: .35, 63: .31, 64: .40, 67: .44, 68: .49, 70: .41, 71: .47, 72: .48, 73: .48}
MELKE_HPJ = {37, 38, 39, 40, 41, 77, 78}   # mělké / skeletovité (Janeček 2012 kap. 1.6 💻 - ověřit)

def cti(n):
    with rasterio.open(os.path.join(DMR, n)) as s:
        return s.read(1), s.profile
sk, prof = cti("sklon_deg.tif"); ak, _ = cti("akumulace.tif"); hpj, _ = cti("hpj.tif"); vy, _ = cti("vyuziti_kod.tif"); pov, _ = cti("povodi_id.tif")
cell = abs(prof["transform"].a)
platne = (sk > -9000) & (ak >= 0)

# ---- R: převzorkovat na naši mřížku (nearest), NoData doplnit nejbližší hodnotou (okraj okresu)
R = np.full(sk.shape, np.nan, np.float32)
with rasterio.open(R_TIF) as rs:
    reproject(rasterio.band(rs, 1), R, dst_transform=prof["transform"], dst_crs=prof["crs"], resampling=Resampling.nearest, dst_nodata=np.nan, src_nodata=rs.nodata)
R[R < 0] = np.nan
if np.isnan(R).any():
    from scipy import ndimage
    idx = ndimage.distance_transform_edt(np.isnan(R), return_distances=False, return_indices=True)
    R_fill = R[tuple(idx)]; r_doplneno = np.isnan(R) & platne; R = R_fill
else:
    r_doplneno = np.zeros_like(platne)

# ---- K z HPJ (0 = bez BPEJ -> NaN; lesy a intravilán nás u orné nezajímají)
K = np.full(sk.shape, np.nan, np.float32)
for h, k in K_HPJ.items(): K[hpj == h] = k

# ---- L, S
theta = np.radians(np.clip(sk, 0, 89)); sl_pct = np.tan(theta) * 100
S = np.where(sl_pct < 9, 10.8 * np.sin(theta) + 0.03, 16.8 * np.sin(theta) - 0.50)
m = np.select([sl_pct < 1, sl_pct < 3, sl_pct < 5], [0.2, 0.3, 0.4], 0.5)
l = np.clip((ak + 1) * cell, cell, L_MAX)        # přispívající plocha / šířka buňky = délka dráhy odtoku [m]
L = (l / 22.13) ** m
LS = (L * S).astype(np.float32)

# ---- A pro scénáře C (P = 1)
C_SCEN = {"C02_obilniny": 0.20, "C01_zlepsene": 0.10, "C03_okopaniny": 0.30, "TTP": 0.01}
# ---- území modelu z data/povodi.geojson (polygon typ uzemi_modelu, WGS84 -> S-JTSK)
from rasterio.features import rasterize
from pyproj import Transformer
gj = json.load(open(os.path.join(ROOT, "data", "povodi.geojson"), encoding="utf-8"))
uz = [f for f in gj["features"] if f["properties"]["typ"] == "uzemi_modelu"][0]["geometry"]
tr = Transformer.from_crs(4326, 5514, always_xy=True)
def prevod(g):
    if g["type"] == "Polygon": return {"type": "Polygon", "coordinates": [[tr.transform(x, y) for x, y in r] for r in g["coordinates"]]}
    return {"type": "MultiPolygon", "coordinates": [[[tr.transform(x, y) for x, y in r] for r in pg] for pg in g["coordinates"]]}
uzemi = rasterize([(prevod(uz), 1)], out_shape=sk.shape, transform=prof["transform"], fill=0).astype(bool)
orna = platne & uzemi & (vy == ORNA) & ~np.isnan(K)
orna_bez_bpej = platne & uzemi & (vy == ORNA) & np.isnan(K)
A = {n: (R * K * LS * c).astype(np.float32) for n, c in C_SCEN.items()}

def souhrn(mask):
    n = int(mask.sum()); ha = n * cell * cell / 1e4
    if n == 0: return None
    out = {"plocha_ha": round(ha, 1), "R_prumer": round(float(np.nanmean(R[mask])), 1), "K_prumer": round(float(np.nanmean(K[mask])), 3),
           "LS_prumer": round(float(np.nanmean(LS[mask])), 2), "sklon_prumer_pct": round(float(np.nanmean(sl_pct[mask])), 1), "scenare": {}}
    for nm, c in C_SCEN.items():
        a = A[nm][mask]
        out["scenare"][nm] = {"C": c, "A_prumer_t_ha_rok": round(float(np.nanmean(a)), 2), "A_median": round(float(np.nanmedian(a)), 2),
                              "podil_nad_Gp9_pct": round(100 * float((a > 9).mean()), 1), "podil_nad_Gp4_pct": round(100 * float((a > 4).mean()), 1),
                              "podil_nad_Gp2_pct": round(100 * float((a > 2).mean()), 1), "ztrata_celkem_t_rok": round(float(np.nansum(a)) * cell * cell / 1e4, 0)}
    return out

info = {"zdroje": {"R": "VÚMOP/ČHMÚ R faktor 2022, okres Kroměříž (CZ0721), 5 m; podmínky užití žádné; NoData v území doplněno nejbližší hodnotou",
                   "K": "Janeček a kol. 2012 tab. 1.5 podle HPJ z BPEJ (SPÚ)", "LS": "Janeček 2012 rov. 1.6-1.8 (McCool), l z akumulace D8 omezená na %d m, m podle Wischmeier & Smith" % L_MAX,
                   "C": "opatreni.json konstanty.usle.C (manuál kalkulačky VÚMOP 2017, Janeček 2012); scénář = průměrný roční C, ne osevní postup konkrétního pozemku", "P": 1},
        "pozn": "orientační model pro osvětu; délka svahu z DMR neuvažuje přerušení cestami a mezemi, proto A spíš nadsazuje na dlouhých svazích; kalkulačka VÚMOP (USLE2D, LPIS) je přesnější a závazná",
        "R_uzemi": {"min": round(float(np.nanmin(R[platne])), 1), "max": round(float(np.nanmax(R[platne])), 1), "prumer": round(float(np.nanmean(R[platne])), 1),
                    "doplneno_nodata_ha_v_uzemi": round(float((r_doplneno & uzemi).sum()) * cell * cell / 1e4, 1)},
        "orna_uzemi_modelu": souhrn(orna), "orna_bez_bpej_ha": round(float(orna_bez_bpej.sum()) * cell * cell / 1e4, 1), "orna_podle_povodi": {}, "orna_podle_sklonu": {}}
nazvy = json.load(open(os.path.join(ROOT, "data", "rozvodnice_info.json"), encoding="utf-8")) if os.path.exists(os.path.join(ROOT, "data", "rozvodnice_info.json")) else {}
for pid in np.unique(pov[orna]):
    if pid == 0: continue
    info["orna_podle_povodi"][str(int(pid))] = souhrn(orna & (pov == pid))
for lo, hi in [(0, 3), (3, 7), (7, 12), (12, 100)]:
    info["orna_podle_sklonu"][f"{lo}-{hi} %"] = souhrn(orna & (sl_pct >= lo) & (sl_pct < hi))

with rasterio.open(os.path.join(DMR, "usle_ls.tif"), "w", **dict(prof, dtype="float32", nodata=-9999, compress="deflate")) as d:
    d.write(np.where(platne, LS, -9999).astype(np.float32), 1)
with rasterio.open(os.path.join(DMR, "usle_A_C02.tif"), "w", **dict(prof, dtype="float32", nodata=-9999, compress="deflate")) as d:
    d.write(np.where(orna, A["C02_obilniny"], -9999).astype(np.float32), 1)
with open(os.path.join(ROOT, "data", "usle_info.json"), "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=1)
print(json.dumps(info["orna_uzemi_modelu"], ensure_ascii=False, indent=1)); print("R", info["R_uzemi"])

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    a = np.where(orna, A["C02_obilniny"], np.nan)
    fig, ax = plt.subplots(figsize=(9, 9)); im = ax.imshow(np.clip(a, 0, 20), cmap="YlOrRd", vmin=0, vmax=20)
    ax.imshow(np.where(uzemi & ~orna, 1, np.nan), cmap="Greys", alpha=.12)
    plt.colorbar(im, ax=ax, label="A [t/ha/rok], C = 0,2, P = 1 (oříznuto na 20)"); ax.set_title("USLE - orná půda, území modelu (orientační)"); ax.axis("off")
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "docs", "img", "usle_nahled.png"), dpi=100); print("obrázek docs/img/usle_nahled.png")
except ImportError:
    pass
