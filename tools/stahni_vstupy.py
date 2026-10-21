# -*- coding: utf-8 -*-
"""stahni_vstupy.py - stáhne surová vstupní data ZABAGED (WFS ČÚZK) a BPEJ (WFS SPÚ) pro bbox území modelu.

Použití: python tools/stahni_vstupy.py --out <složka>
Bbox se počítá stejně jako v 04_vyuziti_pudy.py (území modelu + 200 m) a 05_hsp.py (+ 300 m) z data/povodi.geojson.
Spouští ho workflow .github/workflows/stahni-vstupy.yml (GitHub Actions dosáhne na servery ČÚZK a SPÚ i tehdy,
když prostředí Claude ne). Výstup: <out>/zabaged/*.geojson, <out>/bpej/bpej_wfs.gml - zkopírovat do data/.
"""
import argparse, importlib.util, json, os
import numpy as np
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def modul(nazev):
    spec = importlib.util.spec_from_file_location(nazev.replace(".", "_"), os.path.join(HERE, nazev))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="vstupy"); a = ap.parse_args()
    v04, v05 = modul("04_vyuziti_pudy.py"), modul("05_hsp.py")
    to5514 = Transformer.from_crs("EPSG:4326", "EPSG:5514", always_xy=True)
    gj = json.load(open(os.path.join(ROOT, "data", "povodi.geojson"), encoding="utf-8"))
    model = next(f for f in gj["features"] if f["properties"].get("typ") == "uzemi_modelu")
    ring = np.array([to5514.transform(x, y) for x, y in model["geometry"]["coordinates"][0]])
    xmin, ymin = ring.min(axis=0); xmax, ymax = ring.max(axis=0)
    bb = lambda b: (round(xmin - b), round(ymin - b), round(xmax + b), round(ymax + b))
    os.makedirs(os.path.join(a.out, "zabaged"), exist_ok=True); os.makedirs(os.path.join(a.out, "bpej"), exist_ok=True)
    vrstvy = [v[0] for v in v04.VRSTVY] + [l[0] for l in v04.LINIE] + ["Kůlna__skleník__fóliovník__přístřešek"] + v04.EXTRA
    chyby = 0
    for L in vrstvy:
        try:
            n = v04.wfs_fetch(L, bb(200), os.path.join(a.out, "zabaged", L + ".geojson"))
            print(L, n, flush=True)
        except BaseException as e:      # sys.exit z wfs_get je BaseException
            chyby += 1; print("CHYBA", L, repr(e)[:500], flush=True)
    try:
        v05.fetch_bpej(bb(300), os.path.join(a.out, "bpej", "bpej_wfs.gml")); print("BPEJ ok", flush=True)
    except BaseException as e:
        chyby += 1; print("CHYBA BPEJ", repr(e)[:500], flush=True)
    print("chyb:", chyby)
    print("bbox zabaged", bb(200), "bpej", bb(300))


if __name__ == "__main__":
    main()
