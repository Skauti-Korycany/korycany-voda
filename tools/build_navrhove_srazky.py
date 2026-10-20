# -*- coding: utf-8 -*-
"""
Návrhové 6hodinové srážky pro Koryčany (N2-N100) z WPS ČVUT (rain.fsv.cvut.cz)
-> data/navrhove_srazky.json

Zdroj: Kavka a kol. 2023, Krátkodobé srážky pro hydrologické modelování a navrhování
drobných vodohospodářských staveb v krajině (certifikovaná metodika 2/2023/SPU/O,
ISBN 978-80-01-07115-1; ČVUT, ČHMÚ, ÚFA AV ČR, Sweco). Služba WPS:
https://rain1.fsv.cvut.cz/services/wps, proces d-rain6h-timedist (PyWPS, GRASS).

Spuštění:
  python tools/build_navrhove_srazky.py            # dotaz na WPS + zápis JSON
  python tools/build_navrhove_srazky.py --offline  # jen z hodnot níže (bez sítě)

Bod dotazu = střed území modelu (S-JTSK -557700, -1174500; cca 49.1125 N, 17.1770 E).
Kontrola 20. 10. 2026: N10 v dalších bodech území 52,9-53,4 mm (Lískovec, hráz VN,
les nad Stříbrníkem) -> rastr 1 km je v území prakticky homogenní, bod stačí.
Polygon území (14,1 km² < 20 km²) by redukci úhrnu nevyvolal.
"""
import json, re, sys, os, csv, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data", "navrhove_srazky.json")
TVARY_CSV = os.path.join(ROOT, "data", "navrhove_srazky_tvary_raw.csv")

WPS = "https://rain1.fsv.cvut.cz/services/wps"
BOD = (-557700, -1174500)
DOBY = ["N2", "N5", "N10", "N20", "N50", "N100"]
TVARY = "ABCDEF"

# Hodnoty získané z WPS 20. 10. 2026 (fallback pro --offline a kontrola)
ZISKANO = {
    "N2":   {"H6h_mm": 32.2, "P_tvar_pct": {"A": 12.8, "B": 15.6, "C": 25.3, "D": 13.7, "E": 16.8, "F": 15.79}},
    "N5":   {"H6h_mm": 44.3, "P_tvar_pct": {"A": 10.4, "B": 18.8, "C": 31.5, "D": 13.7, "E": 18.3, "F": 7.36}},
    "N10":  {"H6h_mm": 53.2, "P_tvar_pct": {"A": 8.5,  "B": 20.9, "C": 34.6, "D": 13.4, "E": 19.4, "F": 3.20}},
    "N20":  {"H6h_mm": 62.6, "P_tvar_pct": {"A": 6.8,  "B": 22.7, "C": 36.4, "D": 12.8, "E": 20.3, "F": 1.10}},
    "N50":  {"H6h_mm": 76.0, "P_tvar_pct": {"A": 4.8,  "B": 24.7, "C": 37.4, "D": 11.7, "E": 21.2, "F": 0.17}},
    "N100": {"H6h_mm": 87.0, "P_tvar_pct": {"A": 3.6,  "B": 26.1, "C": 37.5, "D": 10.9, "E": 21.8, "F": 0.03}},
}
QAPI = {"A": 0.18, "B": 0.28, "C": 0.35, "D": 0.20, "E": 0.40, "F": 0.41}   # stejné pro všechna N


def execute_xml(doba):
    gml = ('<ogr:FeatureCollection xmlns:ogr="http://ogr.maptools.org/" xmlns:gml="http://www.opengis.net/gml">'
           '<gml:featureMember><ogr:test fid="test.0"><ogr:geometryProperty>'
           f'<gml:Point srsName="EPSG:5514"><gml:coordinates>{BOD[0]},{BOD[1]},0</gml:coordinates></gml:Point>'
           '</ogr:geometryProperty><ogr:ID>1</ogr:ID></ogr:test></gml:featureMember></ogr:FeatureCollection>')
    def lit(k, v):
        return f"<wps:Input><ows:Identifier>{k}</ows:Identifier><wps:Data><wps:LiteralData>{v}</wps:LiteralData></wps:Data></wps:Input>"
    return ('<wps:Execute service="WPS" version="1.0.0" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1">'
            '<ows:Identifier>d-rain6h-timedist</ows:Identifier><wps:DataInputs>'
            f'<wps:Input><ows:Identifier>input</ows:Identifier><wps:Data><wps:ComplexData mimeType="text/xml">{gml}</wps:ComplexData></wps:Data></wps:Input>'
            + lit("keycolumn", "ID") + lit("return_period", doba) + "".join(lit("type", t) for t in TVARY) + lit("area_red", "False")
            + '</wps:DataInputs><wps:ResponseForm><wps:ResponseDocument>'
            '<wps:Output asReference="false"><ows:Identifier>output</ows:Identifier></wps:Output>'
            '<wps:Output asReference="true"><ows:Identifier>output_shapes</ows:Identifier></wps:Output>'
            '</wps:ResponseDocument></wps:ResponseForm></wps:Execute>')


def parse_output_csv(text):
    """CSV z WPS: ID,H_N10T360_mm,P_N10tvarA_%,...,QAPI_tvarA,... -> dict"""
    hdr, row = [l.split(",") for l in text.strip().splitlines()[:2]]
    d = dict(zip(hdr, row))
    h = [k for k in hdr if k.startswith("H_")][0]
    doba = re.match(r"H_(N\d+)T360_mm", h).group(1)
    return doba, {
        "H6h_mm": float(d[h]),
        "P_tvar_pct": {t: float(d[f"P_{doba}tvar{t}_%"]) for t in TVARY},
        "qAPI": {t: float(d[f"QAPI_tvar{t}"]) for t in TVARY},
    }


def dotaz(doba):
    req = urllib.request.Request(WPS, data=execute_xml(doba).encode("utf-8"), headers={"Content-Type": "text/xml"})
    xml = urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
    if "ProcessSucceeded" not in xml:
        raise RuntimeError(f"WPS {doba}: proces selhal\n{xml[-800:]}")
    m = re.search(r"<!\[CDATA\[([\s\S]*?)\]\]>", xml)
    hrefs = re.findall(r'href="([^"]+shapes\.csv)"', xml)
    tvary = urllib.request.urlopen(hrefs[0], timeout=60).read().decode("utf-8") if hrefs else None
    return parse_output_csv(m.group(1)), tvary


def tvary_z_csv(text):
    """Průběhy 5min úhrnů -> relativní podíly (součet 1) pro A-F."""
    rows = list(csv.reader(text.strip().splitlines()))
    hdr = rows[0]
    cols = {t: hdr.index([c for c in hdr if c.endswith(f"tvar{t}_mm")][0]) for t in TVARY}
    cas = [int(r[1]) for r in rows[1:]]
    out = {}
    for t, i in cols.items():
        v = [float(r[i]) for r in rows[1:]]
        s = sum(v)
        out[t] = [round(x / s, 5) for x in v]
    return cas, out


def main():
    offline = "--offline" in sys.argv
    vysledky, tvary_csv = {}, None
    if not offline:
        try:
            for doba in DOBY:
                (d, v), tv = dotaz(doba)
                vysledky[d] = v
                if doba == "N10" and tv:
                    tvary_csv = tv
                print(doba, v["H6h_mm"], "mm")
        except Exception as e:
            print("WPS nedostupné, používám uložené hodnoty:", e)
            vysledky = {}
    if not vysledky:
        vysledky = {k: dict(v, qAPI=QAPI) for k, v in ZISKANO.items()}
    if tvary_csv:
        with open(TVARY_CSV, "w", encoding="utf-8", newline="") as f:
            f.write(tvary_csv)
    with open(TVARY_CSV, encoding="utf-8") as f:
        cas, tvary = tvary_z_csv(f.read())

    # kontrola proti uloženým hodnotám
    for k, v in ZISKANO.items():
        if abs(v["H6h_mm"] - vysledky[k]["H6h_mm"]) > 0.05:
            print(f"POZOR: {k} se liší od hodnoty z 20. 10. 2026: {vysledky[k]['H6h_mm']} vs {v['H6h_mm']}")

    data = {
        "zdroj": "Kavka a kol. 2023, Krátkodobé srážky pro hydrologické modelování a navrhování drobných vodohospodářských staveb v krajině. Certifikovaná metodika 2/2023/SPU/O, ISBN 978-80-01-07115-1 (ČVUT v Praze, ČHMÚ, ÚFA AV ČR, Sweco Hydroprojekt). Data: WPS https://rain1.fsv.cvut.cz/services/wps, proces d-rain6h-timedist; portál https://rain.fsv.cvut.cz",
        "metoda": "regionální frekvenční analýza 6hodinových maximálních úhrnů z 20leté řady adjustovaných radarových odrazivostí (10 min, 1 km) a 30+ let staničních měření; výstup rastr 1 x 1 km pro ČR",
        "licence": "podmínky užití dat na portálu neuvedeny (stav 20. 10. 2026); služba je veřejná, bez registrace; pro redistribuci se zeptat autorů (ČVUT FSv, P. Kavka)",
        "stazeno": "2026-10-20",
        "bod_sjtsk": list(BOD),
        "bod_wgs84": [49.1125, 17.1770],
        "pozn_prostor": "kontrola N10 v dalších bodech území: Lískovec 52,9, hráz VN 53,1, les nad Stříbrníkem 53,4 mm - homogenní; redukce plochy (>20 km²) se území modelu 14,1 km² netýká",
        "doba_trvani_min": 360,
        "uhrny_6h_mm": {k: v["H6h_mm"] for k, v in vysledky.items()},
        "podil_tvaru_pct": {k: v["P_tvar_pct"] for k, v in vysledky.items()},
        "qAPI": vysledky["N10"]["qAPI"],
        "qAPI_pozn": "pravděpodobnost abnormálně vlhkých předchozích podmínek (API5) před daným tvarem; metodika: qAPI < 0,2 -> váha CN2 = 1; qAPI > 0,8 -> váha CN3 = 1; mezi tím lineárně (tab. 6). CN1 se pro návrh nedoporučuje.",
        "tvary_popis": {"A": "nejvíc koncentrovaný, přívalový (vrchol ~3. hodina)", "B": "jednoduchý, vrchol ~3. hodina", "C": "dva vrcholy (2. a 4. hodina)", "D": "dva vrcholy (1. a 5. hodina)", "E": "jednoduchý, plochý", "F": "nejméně koncentrovaný, trvalý déšť"},
        "tvary_cas_min": cas,
        "tvary_podil": tvary,
        "tvary_pozn": "podíl 5min úhrnu z celkového 6h úhrnu (součet 1); násobit úhrnem H6h. Odvozeno z výstupu N10, tvary jsou podle metodiky relativní a platí pro libovolný úhrn. Tvary pod 5 % zastoupení lze vynechat.",
        "srovnani_denni_gumbel_chmi_korycany_mm": {"N2": 37.3, "N5": 49.8, "N10": 58.1, "N20": 66.0, "N50": 76.3, "N100": 84.0},
        "srovnani_pozn": "denní úhrny ze stanice Koryčany (Gumbel, 88 let, odhad) jsou pro N2-N50 vyšší než 6h ČVUT (delší trvání), u N100 nižší (87 vs 84 mm) - Gumbel z momentů podceňuje horní konec; metodika sama upozorňuje na možné nadhodnocení vysokých N.",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("zapsáno", OUT)


if __name__ == "__main__":
    main()
