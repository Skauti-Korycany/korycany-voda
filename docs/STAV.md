# STAV projektu Koryčany resilience

Aktualizováno: 14. 11. 2026 (večer: drobné opravy rozhraní, verze, počty domů, náhled pro sdílení). Jen aktuální stav. Historie relací, podrobnosti bloků a všechna dřívější rozhodnutí: `docs/STAV-HISTORIE.md`. Kontext pro Claude Code: `CLAUDE.md` v kořeni repa.

## Fáze

| fáze | stav |
|---|---|
| 1 Vymezení a inventura | hotovo (VRSTVY.md, území modelu) |
| 2 Datová příprava | hotovo (DMR, rozvodnice, využití, HSP VÚMOP, CN, USLE, toky, parcely, budovy, srážky) |
| 3 Výpočetní jádro | rozpracováno: `web/jadro.js` v0.3 (SCS-CN po buňkách, vážení CN2/CN3, povodí bodu, nádrže/tůně, 37 testů OK). Chybí transformace vlny, bilance P-ET podle scénářů, opatření nad reálným pozemkem |
| 4 Rozhraní občan | funkční na GitHub Pages, ve zkoušce s lidmi |
| 5 Škola/expert + měření | nezačato |
| 6 Validace a texty | katalog hotový (v0.6), validace ne -> aplikace nese "nevalidováno" |
| 7 Test a zveřejnění | neformální zkoušky |

## Co běží

- Web: https://skauti-korycany.github.io/korycany-voda/ (záložky Jak bylo, Můj pozemek, Celé území, Katalog, O modelu), `stav.html` (veřejná stavová stránka, čísla natvrdo, stav k 25. 10.), `web/test.html` (technický prohlížeč jádra).
- Automatika: `pocasi.yml` 4× denně (ČHMÚ recent, KS Koryčany PMO, Nemotice -> `data/pocasi/denni.json`, přegeneruje index.html); `normaly.yml` ručně (v březnu 2027 spustit kvůli ročníku 2026); `stahni-vstupy.yml` (ZABAGED, HY-NET).
- Odkaz pro leták: https://skauti-korycany.github.io/korycany-voda/#pozemek

## Území modelu a klíčová čísla

- Hráz VN Koryčany (nahoře) až jez na Kyjovce před Mouchnicemi (dole), **17,7 km²**. Rozvodnice ověřeny proti ČHP a kritickým bodům VÚV.
- HSP VÚMOP 2026 (od 27. 10.): A 11 / B 68 / C 11 / D 10 %, odhad 1,2 %. CN vážené 67,4. Odtok P40 74 tis. m³, P60 195 tis. m³.
- Les 711 ha (40 %), orná 545 ha, TTP 173 ha. Budov 1 631, RD 1 075.
- USLE orná (C 0,2): průměr 10,5 t/ha/rok, 45 % plochy nad Gp 9.
- Srážky Koryčany normál 1991-2020 633 mm; návrhové 6h N2 32 / N10 53 / N100 87 mm.
- Katalog: 66 opatření, 157 zdrojů, 57 příkladů dobré praxe, 10 programů (JSON 0.9).

## Rozpracováno / čeká na uživatele

- Zkouška aplikace s dalšími lidmi (Můj pozemek kroky 1 a 4, Celé území kap. 3): kde se ztrácí.
- Zpětná vazba k nádržím v0.3 (Celé území -> Hráz na potoce).
- Žádost na Povodí Moravy (srážkoměr VD Koryčany, přítok/odtok VD, měrná křivka profilu pod přehradou, parametry nádrže) - text připraví Claude na vyžádání.
- Lokální čísla ClimRisk pro k. ú. Koryčany (uživatel odečte z mapy) a místní fotky se souhlasem autorů (nádrž v suchu, skauti měří, povodeň 12. 6. 2012).
- Chybějící podklady: NOO 2026 (XLSX), seznam platných SPPK, znění vodního zákona § 15b, 17, 46, 47, 55 (e-Sbírka), text ČSN 75 9010.
- Archiv podkladů na PC: `tools\stahni_zdroje.bat`.

## Další kroky (pořadí)

1. Napojit opatření katalogu na skutečný pozemek: sklon, HSP, přítok shora a údolnice/potok hotové (14. 11.), nádrž T07 v Můj pozemek. Zbývá: zkouška s lidmi, zda upozornění neplaší; případně vzdálenost k toku přes `toky.json`.
2. Rešerše k oblasti "Život a voda v krajině" (biodiverzita).
3. Validace: data Povodí Moravy, porovnání s epizodami u Kachníku (`docs/MERENI.md`).
4. Transformace vlny poldrem; nádrž/tůň u potoka do Můj pozemek.
5. Mapa eroze v aplikaci: hotovo 14. 11. (Celé území, kap. 3, tři scénáře). Zbývá deprese z `deprese.tif` po filtru.
6. Zmenšit data pro mobil: hotovo líné načítání (mapová data až v Můj pozemek / Celé území) a bezeztrátová komprese rastrů (5,4 MB). Zbývá ořez rastrů na území modelu a hrubší akumulace (vyžaduje `09_balicek_web.py` na PC).
7. Krátké úhrny ČSN 75 9010 pro Koryčany; podmínky otevřených dat ČHMÚ do VRSTVY.md.
8. Fáze 5: rozhraní škola/expert, formulář měření (úložiště mimo GitHub Pages zatím chybí).
9. Revitalizace toků (T02/T04, příklady Otročínský potok a Jizbický les): zjistit opevněné úseky Stříbrníku a Kyjovky, meliorační kanály v lesích nad nádrží, oslovit Povodí Moravy.

## Platná rozhodnutí

Data a území
- Hranice modelu: hráz VN nahoře, jez před Mouchnicemi dole (21. 10.). Budovy jen obec Koryčany, parcely i k. ú. Mouchnice.
- Rozlišení 5 m všude; rastry pro web v mřížce S-JTSK, převod polynomem z `rastr.json` (19. 10.).
- HSP: VÚMOP 2026 (CC BY-NC) > BPEJ (Janeček 2012 tab. 2.2) > nejbližší hodnota; B/D = D (27. 10.).
- Toky z ČÚZK HY-NET (ne DIBAVOD). Vypálení toků jen pro směr odtoku hráze; globální D8 a povodí z nevypáleného terénu.
- Katastr (INSPIRE CP + BU) se používá; vlastníci, LV, adresy, č.p. a ID se nestahují (20. 10.).
- Hydrologie bez whitebox/pysheds, čistý numpy/scipy (19. 10.). QGIS se nepoužívá.

Výpočty
- CN podle Janeček 2012 (IPS II, Ia = 0,2 S), urbánní TR-55; odtok po buňkách a součet.
- Návrhový déšť = 6h úhrny Kavka a kol. 2023, vážení CN2/CN3 podle qAPI.
- Zeleň pozemku přes SCS-CN, sklon do CN nevstupuje. Střechy a zpevněné plochy součinitel ČSN s počáteční ztrátou 1 mm.
- Nádrže v0.3: hráz jen na toku ČÚZK; povodí pod 0,25 km² = tůň v údolnici jako rozsah. Hráze jako informace (vodní dílo nad 2 m, TBD nad 1 m a 1 000 m³), ne strašení.
- ET₀ Hargreaves-Samani; prezentovat jako "možný výpar", P-ET₀ jako "srážky minus výpar".
- Srážky Koryčany: ČHMÚ manuální -> KS Koryčany PMO -> Nemochovice; mezery v historii doplněny z okolních stanic a označeny.

Rozhraní
- Výchozí déšť: Můj pozemek 10 mm, Celé území liják 32 mm (25. 10.).
- Můj pozemek = průvodce 5 kroků, krok 4 jako hra Kapka / Louže / Tůňka / Oáza, krok 5 motivační.
- Styl celé aplikace = datová žurnalistika (Jak bylo), písmo nadpisů Source Serif 4, vlastní SVG ilustrace.
- Katalog: výběr KDE + CO ŘEŠÍM, karta s jedním číslem (`hlavni_cislo`), podrobnosti rozbalovací, bez kódů opatření v textu, dotace odkazem s větou KDY-KOLIK-NA CO.
- Hledání adresy přes RÚIAN ČÚZK; stav v URL hash, nic se neukládá.
- Nádrž (jezírko) se v Můj pozemek nabízí i v zástavbě (14. 11.).
- Cesta přívalové vody: upozornění klidným tónem od 1 ha cizí plochy nebo údolnice, informace od 500 m² 🤔 (14. 11.).
- Verze a datum v hlavičce a patičce se berou z `opatreni.json` a dat počasí, nikdy natvrdo (14. 11.).
- Počet rodinných domů v aplikaci = RÚIAN "rodinný dům" + "bydlení" = 1 076 (14. 11.).
- Les a voda: "listnatý les zadrží víc vody" se nepoužívá; přínos smíšeného lesa = odolnost.

Provoz
- Uživatel není programátor: vše jako `.bat` s instrukcí krok za krokem. Claude zapisuje soubory přímo na PC a po pushi synchronizuje klon `...\korycany-voda\repo`.
- `index.html` a `opatreni.json` jen generovat (`build_dummy.py`, `build_opatreni.py`).
- Licence repa: kód MIT, data a texty CC BY 4.0.

## Otevřené otázky

- Kanalizace Koryčany jednotná/oddílná (Plán povodí 2009 říká jednotná, stav po rekonstrukci ČOV neověřen) - klíčové pro S02, S06.
- Kam odvádějí vodu velké střechy (průmysl, škola, úřad).
- Zpevněné plochy u domů nejsou v žádné vrstvě (pasport města?).
- Meliorace v území: žádost SPÚ (bezplatná).
- Mokřiny u soutoku: ZABAGED má jen 0,19 ha bažin; zamokřené louky vedené jako TTP?
- Srážkoměr v povodí (škola/oddíl u Kachníku) - bez něj přívaly neověřitelné.
- Smí se data VOX a PMO použít ve veřejné aplikaci (podmínky neuvedeny)? Teď jen agregace.
- Klimatické scénáře 2050/2090 s licencí nedohledány.
- Sdílený odkaz obsahuje čísla parcel: stačí upozornění u tlačítka?
- Kdo bude mít po uživateli práva k repozitáři (aspoň dva správci)?
- `stav.html` (čísla natvrdo, stav k 27. 10.): aktualizovat, generovat, nebo nahradit odkazem na O modelu?
- Upozornění z GitHubu při neúspěšném běhu workflow počasí (jinak data tiše přestanou přibývat).

## Platné předpoklady

- Polynom WGS84 <-> S-JTSK platí jen uvnitř rastru.
- Hranice qAPI v tab. 6 Kavka 2023 bráno "do včetně".
- USLE: C a P z VÚMOP 2017 a Janečka 2012, exponent m Wischmeier 💻, délka svahu z D8 se stropem 300 m.
- Tvary deště A-F z N10 platí relativně pro všechna N.
- Nádrž mezi dešti prázdná 🤔 (skutečný déšť za 30 dní).
- S06: 4 osoby, nádrž 5 m³, WC 20-30 % spotřeby 🤔.
- Ceny v EUR ponechány v EUR s rokem.
- `overeno_dne` u zdrojů katalogu = datum buildu.
