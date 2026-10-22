# Zadání: zobrazení a výběr opatření (UX), 22. 10. 2026

Navazuje na: `docs/STAV.md` (relace 12), `docs/KATALOG.md` v0.6, `data/opatreni.json` v0.8 (66 opatření, 57 příkladů), `docs/ROZHRANI.md`, `docs/POZEMEK-UX-ZADANI.md`, `tools/build_dummy.py` (zdroj pravdy pro index.html).

## Rozhodnutí uživatele (22. 10. 2026)
- Vybírá **občan**; výběr podle **oblastí** (co řeším), ne podle technických štítků.
- Karta v prvním pohledu **zjednodušená**: název, jedna věta, jedno číslo, pracnost, zaškrtávátko; vše ostatní až po kliknutí.
- Katalog dnes není dobře řešený: štítků je moc a pro návštěvníka nejsou relevantní. Upravit buď podle **místa / velikosti zásahu** (zahrada / dům / obec / krajina), nebo podle **řešené oblasti** (sucho / příval / horko) jako na pozemku.

## Návrh (k odsouhlasení): jeden princip pro pozemek i katalog
**Krok 1 - KDE** (čtyři velké dlaždice, bez výběru = vše): Zahrada | Dům a střecha | Obec a škola | Krajina (pole, louky, les, potok). Mapování: Z -> Zahrada; S -> Dům; U, H -> Obec; P, L, LES, T, C -> Krajina; M -> samostatná dlaždice „Měř s námi“ (škola).
**Krok 2 - CO ŘEŠÍM** (tři přepínače, lze víc najednou): Sucho | Příval a voda do kanálu | Horko. Mapování na účinky: Sucho = I, R, W, E; Příval = Q, R, I, ER; Horko = CH, E. Biodiverzita (B) se nezobrazuje jako filtr, jen jako zelená poznámka na kartě („+ život v zahradě“).
**Krok 3 - KARTY** (seřazené: nejdřív co jde svépomocí a má číslo):
- řádek 1: název + ikona pracnosti (ruce / malá technika / firma) + zaškrtávátko (jen na pozemku)
- řádek 2: jedna věta (pole `popis`, zkráceno na ~120 znaků)
- řádek 3: **jedno číslo** s významem pro zvolenou oblast: Sucho -> „za rok zůstane až X m³“ nebo „úspora pitné vody X %“; Příval -> „z tohoto deště zadrží X m³“; Horko -> „ve stínu o 8-11 °C chladněji“ apod. Když číslo není, slovně: „účinek doložen, bez čísla“. Značka původu zůstává (✅/📄/🤔).
- po kliknutí (rozbalení): Kde to funguje, přenositelnost, rizika, zdroje, cena, povolení, financování - vše, co je dnes v `details`.
**Pozemek**: krok 1 je už dán průvodcem (střecha, dvůr, zahrada = Zahrada + Dům), takže se zobrazí jen krok 2 a karty; „Nehodí se sem“ zůstane sbalené dole.
**Katalog**: krok 1 + krok 2 + karty; dnešní filtry rozhoduje / účinek / financování / svépomoc se schovají pod „Podrobné filtry (pro školu a úřad)“.
**Celé území**: kontextová opatření (obec, správci) jen v dlaždicích Obec a Krajina.

## Co se mění v datech
- Nic ve zdroji pravdy; mapování oblast <-> účinky a místo <-> dlaždice je v `build_dummy.py` (konstanta). Volitelně do `opatreni.json` pole `oblasti[]` (sucho/prival/horko) jen tam, kde automatické mapování z účinků dává špatný výsledek (ověřit při implementaci na všech 66).
- `popis` chybí u části starších položek (kontrola: kolik), doplnit jednou větou v `build_opatreni.py`.

## Co se neřeší teď
- Posuvníky škál (`vahy_skaly`, NAPADY-ROZHRANI.md), napojení EFF na skutečný pozemek (statPolygon), nová grafika/ikony nad rámec CSS.

## Otevřené otázky
1. Tři oblasti stačí (sucho / příval / horko), nebo přidat čtvrtou „voda v krajině a život“ (B, T, L)?
2. „Jedno číslo“ na pozemku počítá EFF z tvého pozemku; v katalogu (bez pozemku) ukázat příklad pro „100 m² střechy, 10 mm déšť“ - ano?
3. Dlaždice Krajina: cílí na vlastníky půdy a obec, ne na běžného občana - nechat v hlavním výběru, nebo až za „Více“?

## Postup
1. Odsouhlasit návrh a otázky 1-3.
2. Implementace v `build_dummy.py` (Katalog + Můj pozemek), kontrola desktop/mobil, test VŠE OK, push, PC.
3. STAV.md, ROZHRANI.md (v0.2), nezeptal ses / předpoklady.
