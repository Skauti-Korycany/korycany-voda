# STAV projektu Koryčany resilience

Aktualizováno: 19. 10. 2026 (relace 5; fáze 2 - rozvodnice hotovy, čeká na spuštění u uživatele)

## Fáze: 1 hotová (katalog, vrstvy, měření, datový formát, návrh rozhraní, prototyp). Fáze 2 běží: terén a rozvodnice hotovy, další je CN/eroze a vektory (budovy, toky DIBAVOD).

### Hotovo
- Instrukce projektu (docs/00-instrukce-projektu.md).
- Blok A: seznam vrstev s ověřenými WMS adresami a licencemi -> docs/VRSTVY.md.
- Rešerše existujících platforem (16. 10.): hotový nástroj s "co kdyby" simulací pro ČR nedohledán.
- Blok C: katalog opatření v0.2 odsouhlasen 16. 10. (docs/KATALOG.md); kvantifikace Z+S, U+P, L+LES+T+C (docs/KATALOG-*.md).
- Blok C (část 3), 18. 10.: datový formát `data/opatreni.json` v0.3 (58 opatření, 81 zdrojů, 10 programů, 6 nástrojů, konstanty jádra); zdroj pravdy `tools/build_opatreni.py`. Popis: docs/DATA-FORMAT.md.
- Návrh rozhraní v0.1, 18. 10. -> docs/ROZHRANI.md.
- Drátěný prototyp, 18. 10. -> `prototyp/index.html` (= `index.html` pro GitHub Pages): syntetický pozemek, skutečný katalog a vzorce; mapa ČÚZK; režimy Můj pozemek, Celé území, Katalog, O modelu. Generuje `tools/build_dummy.py`.
- Repozitář, 19. 10.: https://github.com/Skauti-Korycany/korycany-voda - struktura data/, tools/, prototyp/, docs/. GitHub konektor funguje, Claude pushuje přímo do main. GitHub Pages: https://skauti-korycany.github.io/korycany-voda/
- Inventura měření (16. 10.): hlásné profily Koryčany pod přehradou (kat. A, Povodí Moravy), Koryčany (Kyjovka) ř. km 75,69 a Koryčany (Stříbrník) kat. C město; čidlo u Kachníku (optické, jen epizody přívalů, před zádržným profilem). CSV Kachník 10. 7. - 16. 10. 2026 analyzováno (epizody 15. 7., 23. 7., 1.-2. 8., 8. 9., 11. 9., 17. 9.; propady = výpadky optiky).
- Srážkový normál: stanice Kroměříž 1991-2020 571,5 mm ✅; Koryčany 🤔 vlhčí.
- Regionální kontext ✅ (18. 10.): Plán dílčího povodí Dyje 2021-2027 pro povodí VN Koryčany bez retenčních opatření nad nádrží.
- Zásobník nápadů: docs/NAPADY-ROZHRANI.md (posuvníky škál; pole `vahy_skaly` v JSON).
- **Blok B část 1 (fáze 2), 19. 10. - terén hotov.** 12 listů DMR 5G (BUCO25-28, 35-38, 45-48; LAZ, CC BY 4.0) -> `repo\data\dmr\dmr5g_5m.tif` (5 m, EPSG:5514, float32, 1500 × 1600 buněk, 100 % platných, 6,29 mil. bodů, hustota 0,10 bodu/m², výšky 225-534 m). Rozsah: X -562500..-555000, Y -1178000..-1170000 = 17.108-17.221 E, 49.074-49.153 N (7,5 × 8 km). Náhled reliéfu zkontrolován (přehrada, niva Kyjovky, hřebeny Chřibů). Výstupy: `dmr5g_5m.tif` (jen na PC, .gitignore), `dmr5g_5m_hillshade.png` (kopie v docs/img/), `dmr5g_5m_info.json` a `dmr5g_5m_bounds.geojson` (kopie v data/). Skript `tools/01_dmr_grid.py`, spouštěč `tools/vyrob_teren.bat` (poklepání, instaluje knihovny, ~4 min).

- **Blok B část 2 (fáze 2), 19. 10. - rozvodnice hotovy (otestováno v Claude na skutečném dmr5g_5m.tif, 32 s).** Skript `tools/02_rozvodnice.py` + `tools/vyrob_rozvodnice.bat`: priority-flood vyplnění depresí, D8 směr, akumulace, sklon a expozice (Horn), údolnice >= 0,25 km², povodí k uzávěrovým bodům. Bez whitebox/pysheds (čistý numpy/scipy; whitebox stahuje binárku z webu, což u uživatele nemusí projít). Rastry v `repo\data\dmr\`: smer_odtoku, akumulace, sklon_deg, expozice_deg, deprese, povodi_id (.tif, mimo git). Do gitu: `data/povodi.geojson` (8 polygonů), `data/toky_dmr.geojson` (108 linií), `data/rozvodnice_body.json` (uzávěrové body, upravitelné), `data/rozvodnice_info.json`, náhledy `docs/img/rozvodnice_nahled.png`, `sklon_nahled.png`. Výsledky: hlavní povodí Kyjovka pod soutokem se Stříbrníkem **19,9 km²** (bod -559412, -1173982; nalezen automaticky po proudu od profilu Stříbrník), profil Kyjovka ř. km 75,69 = 13,7 km² (z toho pod přehradou 5,8 km² - **oříznuto východním okrajem rastru**), Stříbrník ř. km 1,07 = 4,2 km², Lískovec 0,4, Blišice 0,6, Jestřabice 0,7 km² (jen potůčky obcemi). Celý rastr odvodňuje 31,7 km² k výstupu Kyjovky na západním okraji (17.1099 E, 49.1314 N). Průměrný sklon 9,4°, 28,5 % buněk nad 12°. Souřadnice hlásných profilů ✅ edpp.cz (ORP Kroměříž): Kyjovka 75,69 = -558794,48/-1173991,39; Stříbrník 1,068 = -559180,53/-1174691,52; pod přehradou 77,76 = -556751,96/-1173879,95. Středy obcí ✅ cs.wikipedia: Lískovec 49.1236/17.1808, Blišice 49.1228/17.1656, Jestřabice 49.0919/17.1297, VN Koryčany 49.1167/17.1964.

### Rozpracováno
- **Blok B část 2 - u uživatele**: spustit `repo\tools\vyrob_rozvodnice.bat`, poslat náhled; rozhodnout o uzávěrových bodech (viz otázky) a o dotažení listů na východ (BUCO15-18, příp. BUCO05-08), aby povodí nad přehradou nebylo oříznuté.
- Chybějící podklady od uživatele: NOO 2026 (XLSX) a NOO 2025_2; seznam platných SPPK (aopk.gov.cz/platne-standardy); znění vodního zákona (e-Sbírka) § 15b, 17, 46, 47, 55; nejbližší stanice ČHMÚ; text ČSN 75 9010.
- Data z měření: uživatel požádá Povodí Moravy. Text žádosti na vyžádání.
- Zpětná vazba k prototypu (tón textů, pořadí kroků, síla "Na co to nestačí") - čeká na uživatele.
- Otevřené body rozhraní (ROZHRANI.md kap. 6).

### Další kroky (pořadí)
1. Blok B část 2 dokončit: uživatel spustí .bat, potvrdí/upraví uzávěrové body a hranici; případně dostáhne východní listy a pustí oba .bat znovu. Pak ZABAGED budovy (vektor, CC BY) a DIBAVOD toky jako GeoJSON ořezané na povodí; CN rastr (HSP + využití půdy) a USLE vstupy.
2. Jádro (fáze 3): vyčlenit výpočty z prototypu do `jadro.js` s testy na syntetickém pozemku; napojit skutečné sklony a hranici území.
3. Blok D: "reakce toku na déšť" léto 2026 z CSV Kachník + srážky ČHMÚ.
4. Uživatel ověří WMS označené ❌ ve VRSTVY.md (LPIS MZe, katastr ČÚZK, CENIA vojenská mapování); napíše na data@vumop.cz (HSP, BPEJ, zamokřené půdy).
5. Dotační okna: AOPK OPŽP ZMV 17. výzva 20. 10. - 3. 11. 2026; OPŽP 105 do 17. 12. 2026.

## Rozhodnutí
- 19. 10. 2026 - **Hydrologie bez externích knihoven**: whitebox při prvním importu stahuje binárku z whiteboxgeo.com/GitHubu (v Claude 403, u uživatele nejisté), pysheds táhne numba. Vyplnění depresí, D8 a akumulace napsány v numpy/scipy přímo ve skriptu; na 2,4 M buněk 30 s. Nerozhodovat znovu, dokud rastr nepřesáhne ~10 M buněk.
- 19. 10. 2026 - **Hlavní profil = Kyjovka těsně pod soutokem se Stříbrníkem** (automaticky z dat), ne hlásný profil ř. km 75,69 - ten leží nad soutokem, takže by vynechal povodí Stříbrníku (4,2 km², celé jižní zázemí města). Hlásné profily 75,69 a 1,07 jsou v datech jako dílčí povodí (id 1, 2). Změna profilu = úprava `data/rozvodnice_body.json` a nové spuštění .bat.
- 19. 10. 2026 - **Uzávěrové body obcí Lískovec, Blišice, Jestřabice** = tok procházející středem obce (okruh 300 m) - dávají jen malá povodí potůčků (0,4-0,7 km²). Pro model "co steče na obec" stačí; kdo chce jiné vymezení, upraví JSON.
- 19. 10. 2026 - **Lískovec leží uvnitř rastru** (17.18 E, 2 km severně od Koryčan); dřívější obava o západní okraj byla mylná. Naopak chybí východ: povodí Kyjovky nad VN Koryčany pokračuje za -555000 (listy BUCO15-18).
- 19. 10. 2026 - **Komunikace s uživatelem při spouštění skriptů**: uživatel není programátor. Žádné příkazy do terminálu, žádný git. Vše jako jeden soubor `.bat` ve složce `repo\tools`, Claude ho zapíše přímo na PC uživatele (propojení s počítačem) a instrukce píše krok za krokem: kterou složku otevřít, na co poklepat, co se objeví, co napsat zpět. Výstupy si Claude stahuje z PC sám. Nepsat "uložil jsem do tvé složky" bez cesty - uživatel hledal soubor na GitHubu.
- 19. 10. 2026 - **Listy SM5 BUCO**: první číslice = sloupec (západ -> východ), druhá = řádek (sever -> jih). Koryčany = BUCO37. Dřívější opačný výklad byl chybný.
- 19. 10. 2026 - **Rozlišení modelu 5 m všude, i v intravilánu.** DMR 5G je prořídlý TIN (0,07-0,15 bodu/m²); 1 m grid by byl jen interpolace a falešná přesnost. Dřívější záměr 1 m pro intravilán zrušen. Výšky = lineární interpolace TIN (Delaunay), buňky mimo obal NoData.
- 19. 10. 2026 - **Umístění dat na PC uživatele**: `korycany-voda\data\*.laz` (vstup, mimo git), výstupy skriptů do `repo\data\dmr\` (v .gitignore). Lehké odvozené vrstvy (GeoJSON, info JSON, PNG náhled v docs/img) se do gitu dávají po kontrole.
- 19. 10. 2026 - **Repozitář** github.com/Skauti-Korycany/korycany-voda: `data/` (JSON + schéma), `tools/` (build skripty, vendor Leaflet 1.9.4 BSD-2), `prototyp/` a `index.html` (Pages), `docs/` (sumáře). Licence: kód MIT, data a texty CC BY 4.0. Velká rastrová data (LAZ, TIF) do repozitáře nepatří.
- 18. 10. 2026 - **Rozhraní**: dva režimy nad jedním jádrem a jedním JSON; pořadí filtrů místo -> data -> preference; řazení "m³ na jednotku pracnosti"; povinné "Nehodí se sem" a "Na co to nestačí"; stav v URL hash; mobil první; zkouška vsaku (jáma, 30 min) jako vstup uživatele.
- 18. 10. 2026 - **Datový formát**: JSON generovaný Python skriptem (zdroj pravdy), MD = dokumentace. "Odhad" a "kvalitativně" se nesčítají.
- 18. 10. 2026 - **Ceny**: jen s doloženým zdrojem a datem; jinak "cena neověřena". Neověřený údaj (poldr/hráz) vyřazen.
- 18. 10. 2026 - **Les a voda**: "listnatý les zadrží víc vody" se nepoužije (AV ČR, Liz ✅); přínos smíšeného lesa = odolnost porostu.
- 18. 10. 2026 - **Zásahy v korytě (T03, LES01)**: vždy dohoda se správcem + souhlas vodoprávního úřadu (§ 17, § 46; ověřit e-Sbírka).
- 18. 10. 2026 - **Financování**: NPO POPFK ukončený; hlavní cesty OPŽP 1.3.4, AOPK OPŽP ZMV, PPK B, agrolesnictví (jen zemědělec). Zahradní opatření jednotlivce: vlastní peníze.
- 18. 10. 2026 - **Právní rámec drobných tůní** (✅): bez hráze mimo koryto nejsou vodním dílem (§ 55 odst. 3); nad 300 m² do 1,5 m ohlášení (§ 15b); do 300 m² 💻 bez povolení - ověřit na ORP Kroměříž.
- 18. 10. 2026 - **Albedo (S04)**: účinek na budovu ano, na vzduch obce jen plocha "ochlazených střech".
- 18. 10. 2026 - **Větrolamy, pásy, břehové porosty**: chráněná plocha (10-17 H), čas zpoždění odtoku, teplota vody (2-4 °C ✅ zahraniční), ne mm výparu.
- 16. 10. 2026 - **Katalog (odsouhlaseno)**: S04 zůstává; kontextová opatření zůstávají; Kč místo tříd; zemědělci/pachtýři nejsou cílová skupina - katalog pro vlastníky půdy (N01, N02), obec, školu, spolky, správce.
- 16. 10. 2026 - **Účel modelu**: udržení vody v území z přívalů a zpomalení vysychání; zploštění vlny vedlejší. Ne Qmax.
- 16. 10. 2026 - **Výpar je součást bilance**: "méně neproduktivního výparu, víc vody v půdě a biomase". "Malý vodní cyklus" jen metafora.
- 16. 10. 2026 - **Dvě měřítka účinku**: pozemek a území. Jedna tůň nikdy "neovlivní povodí".
- 16. 10. 2026 - **Drobná opatření = objekty s parametry**, ne úprava rastru.
- 16. 10. 2026 - **Výpočetní území**: intravilány + stékající svahy (podrobně); zbytek povodí kontext (WMS). Profil na Kyjovce pod Koryčany (🤔 ř. km 75,69, ověřit); dílčí součty za sídla. (Pozn. 19. 10.: rozlišení 5 m všude, viz výše.)
- 16. 10. 2026 - ÚSK ORP Kroměříž (2017) a KoPÚ (neproběhly) nejsou vstupy; KoPÚ lze vyvolat podpisy vlastníků nadpoloviční výměry (§ 6 odst. 3 zák. 139/2002 ✅).
- 15. 10. 2026 - QGIS se nepoužije; Python (rasterio, geopandas, whitebox); kontrola přes PNG náhledy.
- 15. 10. 2026 - Prostředí: Windows, Python 3.14.7, pip 26.2.1; nainstalováno laspy, lazrs, numpy, scipy, rasterio 1.5.2, matplotlib, pyproj ✅ (19. 10.).
- 15. 10. 2026 - Podklad Leaflet: ČÚZK ZTM WMTS + Ortofoto WMS. Historie: II. a III. vojenské mapování.
- 15. 10. 2026 - Hydrogeologická mapa ČGS: volat přes 4326.

## Otevřené otázky
- Dotáhnout východní listy BUCO15-18 (povodí nad přehradou), nebo brát hráz VN Koryčany jako horní hranici modelu (odtok z nádrže je řízený)? Druhá varianta je levnější a pro model opatření v intravilánu a na svazích stačí.
- Povodí Jestřabic (Kratinka) leží z většiny západně mimo rastr (BUCO5x); zatím jen 0,7 km² uvnitř.
- Kanalizace Koryčany (jednotná/oddílná): nedohledáno online. Potvrdit u města (S02).
- Data Povodí Moravy: po odpovědi na žádost.
- Nejbližší srážkoměrná stanice ČHMÚ (opendata.chmi.cz z Claude blokováno).
- Meliorace v území: žádost SPÚ (bezplatná) ✅; ISMS meliorace.vumop.cz (WMS nedohledána).
- ZABAGED budovy jako vektor ke stažení (pro předvyplnění ploch a součty za obec) - ověřit na ČÚZK (CC BY).
- Geokodér pro zadání adresy (ČÚZK RÚIAN 💻) - ověřit dostupnost a licenci.
- Licence VÚMOP, NLI, MZe, ČHMÚ: zdarma bez jmenované licence; redistribuce dat vyžaduje souhlas.
- Zapojení školy: sekce M a U07; registr estudanky.eu pro M04; úložiště měření (fáze 5).
- Zdroj klimatických scénářů 2050/2090 s licencí - nedohledán (roční bilance P-ET mimo verzi 1).
- Půdoochranné podmínky v pachtovní smlouvě: smluvně možné 🤔, právní výklad neověřen.
- SPPK kódy nedohledané: D02 003 (rok), revitalizace toků, břehové porosty, ochranné výsadby.
- R faktor a návrhový déšť pro Koryčany (kalkulačka VÚMOP, ČSN 75 9010) - doplnit do konstant JSON.
- Licence repozitáře: MIT (kód) + CC BY 4.0 (data, texty) - potvrzení uživatele.

## Zvolené předpoklady
- Metadatové záznamy Micka institucí beru jako oficiální zdroj adres a licencí.
- DMR 5G: CRS přiřazeno EPSG:5514 natvrdo (LAZ ČÚZK CRS nenese); třída 8 = body modelu terénu; výškový systém Bpv 💻.
- Součinitele odtoku z tabulky tzb-info/ČVUT ✅; text normy neotevřen.
- Návrhový déšť zatím podle Brna (ASIO) ✅; pro Koryčany ověřit v normě.
- Srážky 571,5 mm/rok (Kroměříž) jako zástupná hodnota 🤔.
- USLE faktory C a P z manuálu kalkulačky VÚMOP 2017 ✅⏳ a Janečka 2012 ✅⏳.
- Dopočty z měření jsou 🤔 z hodnot ve zdroji, ne autorův závěr.
- Paragrafy vodního zákona ověřeny jen na nestátním zrcadle bez data znění.
- Účinky leaky dams a stínění toku jsou zahraniční ✅; české měření nedohledáno.
- V prototypu jsou sklon, půda, počet domácností (1 050), průměrná střecha, plocha povodí (20 km²) a podíly sídel syntetické a jsou tak označené.

- Profil "pod soutokem" = první buňka, kde akumulace vzroste na 3× akumulace Stříbrníku; souřadnice hlásných profilů z odkazů na mapu edpp.cz (soustava stránkou neuvedena, hodnoty odpovídají S-JTSK).
- Depresní vrstva obsahuje hladinu VN Koryčany a umělé prohlubně (zářezy, lom) - pro "kde voda stojí" je nutné filtrovat podle sklonu a ortofota (fáze 3).

## Na co ses nezeptal a měl bys
- Má město pasport zeleně nebo zpevněných ploch? Ušetřilo by ruční klasifikaci z ortofota.
- Chce oddíl nebo město využít výzvu AOPK ZMV (20. 10. - 3. 11.) nebo OPŽP 105 (do 17. 12.)?
- Jsou pole kolem Koryčan v LPIS vedené jako SEO/MEO? Lesy: kdo je vlastník?
- Kdo bude mít v organizaci Skauti-Korycany práva k repozitáři po tobě (aspoň dva správci)?
- Souhlasíš s hlavním profilem pod soutokem se Stříbrníkem (19,9 km²)? Pokud má být níž (u nádraží, u silnice k Blišicím), dej mi místo - stačí popis nebo bod z mapy.
- Je Stříbrník ten potok, který přitéká do Kyjovky od jihu ze Chřibů (ústí u bodu -559412, -1173982, tj. 17.1552 E, 49.1130 N)? Skript vyšel z hlásného profilu; místní znalost to potvrdí rychleji než mapa.
- Chceš vidět v náhledu i ortofoto/ZTM podklad místo stínovaného reliéfu? Jde to přidat přes WMS, ale náhled se pak generuje déle.
