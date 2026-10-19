# -*- coding: utf-8 -*-
"""build_cn.py - tabulka čísel odtokových křivek CN pro třídy využití půdy modelu -> data/cn_tabulka.json

Zdroje (ověřeno online 19. 10. 2026):
  [J12] Janeček M. a kol. (2012): Ochrana zemědělské půdy před erozí. Metodika. ČZU Praha.
        Tab. 2.1 (s. 29) definice HSP A-D, Tab. 2.2 (s. 29-30) HPJ -> HSP, Tab. 2.3 (s. 30-31) CN pro IPS II.
        https://storm.fsv.cvut.cz/data/files/p%C5%99edm%C4%9Bty/YPEO/Metodika_PEO_novelizace%20upravene%2025_1_2012.pdf
  [TR55] USDA NRCS (1986): Urban Hydrology for Small Watersheds, TR-55, 2nd ed. Tab. 2-2a (urban), 2-2c (other agricultural).
        https://ehs.umich.edu/wp-content/uploads/2017/01/TR-55_curve_numbers.pdf
Hodnoty platí pro střední nasycení půdy (IPS II = AMC II) a počáteční ztrátu Ia = 0,2 S.

Každá třída má "vychozi" CN (co se použije, když o ploše nic víc nevíme) a "varianty" (lepší/horší stav), ze kterých
jádro odvozuje účinek opatření (např. orná: zbytky na povrchu, vrstevnicové řádky, pásové střídání). Kde Janeček řádek
nemá, bere se TR-55 a je to označeno "puvod": "TR55" + poznámka; kde jde o volbu bez přímé opory, je "odhad": true.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def cn(a, b, c, d): return {"A": a, "B": b, "C": c, "D": d}

# kódy odpovídají legendě v tools/04_vyuziti_pudy.py (data/vyuziti_pudy.json -> legenda)
TRIDY = {
 1: {"nazev": "orná půda", "vychozi": "obilniny, přímé řádky, špatný stav",
     "varianty": {
       "obilniny, přímé řádky, špatný stav": {"cn": cn(65, 76, 84, 88), "puvod": "J12 tab. 2.3 úzkořádkové Př Šp"},
       "obilniny, přímé řádky, dobrý stav": {"cn": cn(63, 75, 83, 87), "puvod": "J12 tab. 2.3 úzkořádkové Př Db"},
       "obilniny, zbytky na povrchu, dobrý stav": {"cn": cn(60, 72, 80, 84), "puvod": "J12 tab. 2.3 úzkořádkové Př+Pz Db"},
       "obilniny, vrstevnicově + pásy + zbytky, dobrý stav": {"cn": cn(58, 69, 77, 80), "puvod": "J12 tab. 2.3 úzkořádkové Vř+Pr+Pz Db"},
       "okopaniny/kukuřice, přímé řádky, špatný stav": {"cn": cn(72, 81, 88, 91), "puvod": "J12 tab. 2.3 širokořádkové Př Šp"},
       "okopaniny/kukuřice, přímé řádky, dobrý stav": {"cn": cn(67, 78, 85, 89), "puvod": "J12 tab. 2.3 širokořádkové Př Db"},
       "okopaniny/kukuřice, vrstevnicově + pásy + zbytky, dobrý stav": {"cn": cn(61, 70, 77, 80), "puvod": "J12 tab. 2.3 širokořádkové Vř+Pr+Pz Db"},
       "víceleté pícniny, vrstevnicově + zbytky, dobrý stav": {"cn": cn(51, 67, 76, 80), "puvod": "J12 tab. 2.3 víceleté pícniny Vř+Pz Db"},
       "úhor čerstvě kypřený": {"cn": cn(77, 86, 91, 94), "puvod": "J12 tab. 2.3 úhor Šp"},
     },
     "pozn": "Výchozí = obilniny v přímých řádcích, špatný stav: konzervativní, bez znalosti osevu. Skutečné plodiny z LPIS (fáze 5)."},
 2: {"nazev": "ostatní nespecifikovaná plocha", "vychozi": "otevřená plocha, střední travní pokryv",
     "varianty": {"otevřená plocha, střední travní pokryv": {"cn": cn(49, 69, 79, 84), "puvod": "TR55 tab. 2-2a open space fair", "odhad": True}},
     "pozn": "ZABAGED 'ostatní dále nespecifikovaná plocha' - bez bližšího určení, volba TR-55 fair."},
 3: {"nazev": "trvalý travní porost", "vychozi": "pastvina/louka, pokryv > 75 %",
     "varianty": {
       "pastvina/louka, pokryv > 75 %": {"cn": cn(39, 61, 74, 80), "puvod": "J12 tab. 2.3 pastviny > 75 %"},
       "louka sklizená": {"cn": cn(30, 58, 71, 78), "puvod": "J12 tab. 2.3 louky"},
       "pastvina, pokryv 50-75 %": {"cn": cn(49, 69, 79, 84), "puvod": "J12 tab. 2.3 pastviny 50-75 %"},
       "pastvina přepasená, pokryv < 50 %": {"cn": cn(68, 79, 86, 89), "puvod": "J12 tab. 2.3 pastviny < 50 %"},
     }},
 4: {"nazev": "les (druh neurčen)", "vychozi": "les, střední stav", "varianty": {
       "les, dobrý stav (hrabanka, podrost)": {"cn": cn(30, 55, 70, 77), "puvod": "J12 tab. 2.3 lesy Db"},
       "les, střední stav": {"cn": cn(36, 60, 73, 79), "puvod": "J12 tab. 2.3 lesy Stř"},
       "les, špatný stav (pastva, sešlap, bez hrabanky)": {"cn": cn(45, 66, 77, 83), "puvod": "J12 tab. 2.3 lesy Šp"}}},
 5: {"nazev": "křoviny", "vychozi": "křoviny, pokryv 50-75 %", "varianty": {
       "křoviny, pokryv > 75 %": {"cn": cn(30, 48, 65, 73), "puvod": "J12 tab. 2.3 křoviny > 75 %"},
       "křoviny, pokryv 50-75 %": {"cn": cn(35, 56, 70, 77), "puvod": "J12 tab. 2.3 křoviny 50-75 %"},
       "křoviny, pokryv < 50 %": {"cn": cn(48, 67, 77, 83), "puvod": "J12 tab. 2.3 křoviny < 50 %"}}},
 6: {"nazev": "ovocný sad", "vychozi": "sad se zatravněným meziřadím, střední stav", "varianty": {
       "sad se zatravněným meziřadím, dobrý stav": {"cn": cn(32, 58, 72, 79), "puvod": "J12 tab. 2.3 sady Db"},
       "sad se zatravněným meziřadím, střední stav": {"cn": cn(43, 65, 76, 82), "puvod": "J12 tab. 2.3 sady Stř"},
       "sad, holé/špatné meziřadí": {"cn": cn(57, 73, 82, 86), "puvod": "J12 tab. 2.3 sady Šp"}}},
 7: {"nazev": "zahrada", "vychozi": "zahrada, trávník > 75 %", "varianty": {
       "zahrada, trávník > 75 %": {"cn": cn(39, 61, 74, 80), "puvod": "TR55 tab. 2-2a open space good", "odhad": True},
       "zahrada, trávník 50-75 % (záhony, cesty)": {"cn": cn(49, 69, 79, 84), "puvod": "TR55 tab. 2-2a open space fair", "odhad": True}},
     "pozn": "Budovy, kůlny a zpevněné plochy jsou v rastru zvlášť (kód 30, 31, 20-22), proto zahrada = jen propustná část."},
 8: {"nazev": "ostatní trvalá kultura", "vychozi": "jako sad, střední stav",
     "varianty": {"jako sad, střední stav": {"cn": cn(43, 65, 76, 82), "puvod": "J12 tab. 2.3 sady Stř", "odhad": True}}},
 9: {"nazev": "udržovaná zeleň, park", "vychozi": "trávník > 75 %",
     "varianty": {"trávník > 75 %": {"cn": cn(39, 61, 74, 80), "puvod": "TR55 tab. 2-2a open space good"}}},
 10: {"nazev": "ostatní plocha v sídle", "vychozi": "otevřená plocha, střední travní pokryv",
      "varianty": {"otevřená plocha, střední travní pokryv": {"cn": cn(49, 69, 79, 84), "puvod": "TR55 tab. 2-2a open space fair", "odhad": True}},
      "pozn": "Směs dvorků, nezpevněných ploch a zeleně v intravilánu; zpevněné části jsou zachyceny jen tam, kde je ZABAGED vede zvlášť."},
 11: {"nazev": "areál účelové zástavby", "vychozi": "průmyslový/zemědělský areál bez budov",
      "varianty": {
        "průmyslový/zemědělský areál bez budov": {"cn": cn(59, 74, 82, 86), "puvod": "J12 tab. 2.3 zemědělské dvory; TR55 farmsteads", "odhad": True},
        "průmyslový areál vč. zpevněných ploch (TR-55 industrial 72 % neprop.)": {"cn": cn(81, 88, 91, 93), "puvod": "TR55 tab. 2-2a industrial"}},
      "pozn": "Budovy jsou v rastru zvlášť (kód 30), takže výchozí hodnota popisuje jen zbytek areálu (dvory, zpevněné i nezpevněné). Podíl zpevnění neznáme - ověřit ortofotem."},
 12: {"nazev": "hřbitov", "vychozi": "trávník > 75 %", "varianty": {"trávník > 75 %": {"cn": cn(39, 61, 74, 80), "puvod": "TR55 tab. 2-2a open space (cemeteries) good"}}},
 13: {"nazev": "skládka, úložiště", "vychozi": "nezpevněný povrch", "varianty": {"nezpevněný povrch": {"cn": cn(72, 82, 87, 89), "puvod": "TR55 tab. 2-2a dirt roads", "odhad": True}}},
 14: {"nazev": "parkoviště", "vychozi": "zpevněné", "varianty": {"zpevněné": {"cn": cn(98, 98, 98, 98), "puvod": "TR55 tab. 2-2a paved parking lots"}}},
 15: {"nazev": "kolejiště", "vychozi": "štěrkové lože", "varianty": {"štěrkové lože": {"cn": cn(76, 85, 89, 91), "puvod": "TR55 tab. 2-2a gravel", "odhad": True}}},
 16: {"nazev": "vodní plocha", "vychozi": "vodní hladina", "varianty": {"vodní hladina": {"cn": cn(100, 100, 100, 100), "puvod": "konvence: srážka na hladinu = odtok; J12 místo CN zavádí koeficient f pro nádrže a mokřady (tab. 2.5)", "odhad": True}}},
 17: {"nazev": "bažina, močál", "vychozi": "trvale zamokřeno", "varianty": {"trvale zamokřeno": {"cn": cn(100, 100, 100, 100), "puvod": "konvence jako vodní plocha", "odhad": True}}},
 20: {"nazev": "silnice", "vychozi": "živičný povrch", "varianty": {
        "živičný povrch": {"cn": cn(98, 98, 98, 98), "puvod": "TR55 tab. 2-2a streets paved"},
        "silnice s příkopy (J12)": {"cn": cn(72, 82, 87, 89), "puvod": "J12 tab. 2.3 komunikace s příkopy"}},
      "pozn": "Rastr vede silnici jako pruh 5 m = vozovka; příkopy spadají do okolní třídy, proto výchozí 98."},
 21: {"nazev": "ulice", "vychozi": "živičný povrch", "varianty": {"živičný povrch": {"cn": cn(98, 98, 98, 98), "puvod": "TR55 tab. 2-2a streets paved"}}},
 22: {"nazev": "cesta zpevněná", "vychozi": "štěrk/panel/asfalt bez odvodnění", "varianty": {"štěrk/panel/asfalt bez odvodnění": {"cn": cn(83, 89, 92, 93), "puvod": "J12 tab. 2.3 komunikace dlážděné/živičné/makadamové/štěrkové"}}},
 30: {"nazev": "budova", "vychozi": "střecha", "varianty": {"střecha": {"cn": cn(98, 98, 98, 98), "puvod": "TR55 tab. 2-2a roofs"}},
      "pozn": "Účinek opatření na střeše (S01-S04: zasakování, nádrž, zelená střecha) se nemodeluje změnou CN, ale odečtem objemu v jádře."},
 31: {"nazev": "kůlna, skleník, přístřešek", "vychozi": "střecha", "varianty": {"střecha": {"cn": cn(98, 98, 98, 98), "puvod": "TR55 tab. 2-2a roofs"}}},
}
for k in (41, 42, 43):
    TRIDY[k] = dict(TRIDY[4]); TRIDY[k]["nazev"] = {41: "les jehličnatý", 42: "les listnatý", 43: "les smíšený"}[k]
    TRIDY[k]["pozn"] = "CN stejné jako les bez určení druhu: J12 druh dřevin nerozlišuje; rozdíl listnatý/jehličnatý je v intercepci a výparu, ne v CN (rozhodnutí 18. 10.: 'listnatý les zadrží víc vody' se nepoužije)."

HSP = {
    "A": {"popis": "vysoká infiltrace > 0,12 mm/min; hluboké, dobře až nadměrně odvodněné písky a štěrky", "puvod": "J12 tab. 2.1"},
    "B": {"popis": "střední infiltrace 0,06-0,12 mm/min; středně hluboké až hluboké hlinitopísčité až jílovitohlinité půdy", "puvod": "J12 tab. 2.1"},
    "C": {"popis": "nízká infiltrace 0,02-0,06 mm/min; půdy s málo propustnou vrstvou, jílovitohlinité až jílovité", "puvod": "J12 tab. 2.1"},
    "D": {"popis": "velmi nízká infiltrace < 0,02 mm/min; bobtnavé jíly, trvale vysoká hladina podzemní vody, mělké půdy na nepropustném podloží", "puvod": "J12 tab. 2.1"},
}

VZORCE = {
    "S_mm": "S = 25400 / CN - 254",
    "Ia_mm": "Ia = 0,2 S",
    "Q_mm": "Q = (P - Ia)^2 / (P - Ia + S) pro P > Ia, jinak 0  (P = úhrn návrhového deště v mm)",
    "CN_vazene": "CN plochy = suma(CN_i * A_i) / suma(A_i)  (vážení plochou buněk 5 m; J12 kap. 2.3)",
    "IPS": "hodnoty pro IPS II (střední nasycení, 5denní předchozí srážka); IPS I/III přepočet podle J12 obr. 2.2 - v modelu jako posuvník 'suchá/nasycená půda' (fáze 3)",
    "puvod": "J12 kap. 2 (metoda CN, SCS); TR55 kap. 2",
}

def main():
    out = {
        "meta": {"verze": "0.1", "datum": "2026-10-19", "generuje": "tools/build_cn.py",
                 "zdroje": {
                     "J12": {"citace": "Janeček M. a kol. (2012): Ochrana zemědělské půdy před erozí. Metodika. ČZU Praha. Tab. 2.1-2.3, s. 28-31.",
                             "url": "https://storm.fsv.cvut.cz/data/files/p%C5%99edm%C4%9Bty/YPEO/Metodika_PEO_novelizace%20upravene%2025_1_2012.pdf", "overeno": "2026-10-19"},
                     "TR55": {"citace": "USDA NRCS (1986): Urban Hydrology for Small Watersheds, TR-55, 2nd ed., tab. 2-2a, 2-2c.",
                              "url": "https://ehs.umich.edu/wp-content/uploads/2017/01/TR-55_curve_numbers.pdf", "overeno": "2026-10-19"}},
                 "pozn": "CN pro IPS II, Ia = 0,2 S. Položky s 'odhad': true nemají přímý řádek ve zdroji - volba nejbližší kategorie. "
                         "HSP pro území zatím chybí (žádost VÚMOP 19. 10. 2026); záložně J12 tab. 2.2 z HPJ (BPEJ ze SPÚ)."},
        "hsp": HSP,
        "vzorce": VZORCE,
        "tridy": {str(k): v for k, v in sorted(TRIDY.items())},
    }
    p = os.path.join(ROOT, "data", "cn_tabulka.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    n_od = sum(1 for t in TRIDY.values() for v in t["varianty"].values() if v.get("odhad"))
    print(f"zapsáno {p}: {len(TRIDY)} tříd, {sum(len(t['varianty']) for t in TRIDY.values())} variant, z toho {n_od} odhadů")

if __name__ == "__main__":
    main()
