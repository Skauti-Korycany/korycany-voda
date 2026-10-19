# STAV projektu Koryčany resilience

Aktualizováno: 19. 10. 2026 (relace 4, start fáze 2)

## Fáze: 1 hotová v podstatných částech (katalog, vrstvy, měření, datový formát, návrh rozhraní, prototyp). Hranice území čeká na DMR (fáze 2 = úzké hrdlo).

### Hotovo
- Instrukce projektu (docs/00-instrukce-projektu.md).
- Blok A: seznam vrstev s ověřenými WMS adresami a licencemi -> docs/VRSTVY.md.
- Rešerše existujících platforem (16. 10.): hotový nástroj s "co kdyby" simulací pro ČR nedohledán.
- Blok C: katalog opatření v0.2 odsouhlasen 16. 10. (docs/KATALOG.md); kvantifikace Z+S, U+P, L+LES+T+C (docs/KATALOG-*.md).
- Blok C (část 3), 18. 10.: datový formát `data/opatreni.json` v0.3 (58 opatření, 81 zdrojů, 10 programů, 6 nástrojů, konstanty jádra); zdroj pravdy `tools/build_opatreni.py`. Popis: docs/DATA-FORMAT.md.
- Návrh rozhraní v0.1, 18. 10. -> docs/ROZHRANI.md.
- **Drátěný prototyp, 18. 10. -> `prototyp/index.html` (= `index.html` pro GitHub Pages)**: syntetický pozemek, skutečný katalog a vzorce; mapa ČÚZK; režimy Můj pozemek, Celé území, Katalog, O modelu. Generuje `tools/build_dummy.py`.
- **Repozitář, 19. 10.: https://github.com/Skauti-Korycany/korycany-voda** - struktura data/, tools/, prototyp/, docs/. GitHub konektor funguje, Claude pushuje přímo do main. **GitHub Pages zapnuty: prototyp běží na https://skauti-korycany.github.io/korycany-voda/** (každý push do main se propíše).
- Inventura měření (16. 10.): hlásné profily Koryčany pod přehradou (kat. A, Povodí Moravy), Koryčany (Kyjovka) ř. km 75,69 a Koryčany (Stříbrník) kat. C město; čidlo u Kachníku (optické, epizody). CSV Kachník 10. 7. - 16. 10. 2026 analyzováno (epizody 15. 7., 23. 7., 1.-2. 8., 8. 9., 11. 9., 17. 9.; propady = výpadky optiky).
- Srážkový normál: stanice Kroměříž 1991-2020 571,5 mm ✅; Koryčany 🤔 vlhčí.
- Regionální kontext ✅ (18. 10.): Plán dílčího povodí Dyje 2021-2027 pro povodí VN Koryčany bez retenčních opatření nad nádrží.
- Zásobník nápadů: docs/NAPADY-ROZHRANI.md (posuvníky škál; pole `vahy_skaly` v JSON).

### Rozpracováno
- **Blok B (fáze 2) - DMR 5G, 19. 10.**: uživatel stáhl 12 listů SM5 BUCO25-28, 35-38, 45-48 (LAZ, 2-4,6 MB, celkem ~40 MB) do `korycany-voda\data` (mimo repozitář). Vzorek BUCO35 ověřen: LAZ 1.4, bez CRS (přiřazeno EPSG:5514), list 2,5 × 2 km, 347 tis. bodů, všechny třída 8, **hustota 0,07 bodu/m²**. Listy pokrývají Chřiby S a V od Koryčan (horní povodí k VD), **ne intravilány** - Koryčany leží v BUCO55; dostáhnout řádky 5-6, sloupce 3-6 + BUCO43, 44 (ověřit Lískovec). Skript `tools/01_dmr_grid.py` otestován na vzorku (9 s/list, výstup GeoTIFF 5 m EPSG:5514 + hillshade PNG + info JSON + obrys GeoJSON).
- Chybějící podklady od uživatele: NOO 2026 (XLSX) a NOO 2025_2; seznam platných SPPK (aopk.gov.cz/platne-standardy); znění vodního zákona (e-Sbírka) § 15b, 17, 46, 47, 55; nejbližší stanice ČHMÚ; text ČSN 75 9010; souřadnice čidla Kachník.
- Hranice území - rozhodnuto koncepčně, výpočet rozvodnice čeká na DMR 5G.
- Data z měření: uživatel požádá Povodí Moravy. Text žádosti na vyžádání.
- Zpětná vazba k prototypu (tón textů, pořadí kroků, síla "Na co to nestačí") - čeká na uživatele.
- Otevřené body rozhraní (ROZHRANI.md kap. 6).

### Další kroky (pořadí)
1. **Blok B (fáze 2)**: uživatel dostáhne chybějící listy (řádky 5-6, sl. 3-6, + 43, 44); spustí `python tools\01_dmr_grid.py ..\data` a pošle `data\dmr\dmr5g_5m_hillshade.png` + `_info.json`. Pak `tools/02_rozvodnice.py` (whitebox: vyplnění depresí, směr odtoku, akumulace, povodí k profilu pod Koryčany + dílčí povodí sídel, GeoJSON) a sklon/expozice. Souběžně ZABAGED budovy (vektor, CC BY) a DIBAVOD toky.
2. Jádro (fáze 3): vyčlenit výpočty z prototypu do `jadro.js` s testy na syntetickém pozemku.
3. Blok D: "reakce toku na déšť" léto 2026 z CSV Kachník + srážky ČHMÚ.
4. Uživatel ověří WMS označené ❌ ve VRSTVY.md (LPIS MZe, katastr ČÚZK, CENIA vojenská mapování); napíše na data@vumop.cz (HSP, BPEJ, zamokřené půdy).
5. Dotační okna: AOPK OPŽP ZMV 17. výzva **20. 10. - 3. 11. 2026**; OPŽP 105 do **17. 12. 2026**.

## Rozhodnutí
- 19. 10. 2026 - **Rozlišení modelu 5 m všude, i v intravilánu.** DMR 5G je prořídlý TIN (0,07 bodu/m² = bod na ~14 m²); 1 m grid by byl jen interpolace a falešná přesnost. Dřívější záměr 1 m pro intravilán zrušen. Výšky = lineární interpolace TIN (Delaunay), buňky mimo obal NoData.
- 19. 10. 2026 - **Umístění dat na PC uživatele**: `korycany-voda\data\*.laz` (vstup, mimo git), výstupy skriptů do `repo\data\dmr\` (v .gitignore). Lehké odvozené vrstvy (GeoJSON hranice, PNG náhledy pro dokumentaci) se do gitu dají až po kontrole.
- 19. 10. 2026 - **Repozitář** github.com/Skauti-Korycany/korycany-voda: `data/` (JSON + schéma), `tools/` (build skripty, vendor Leaflet 1.9.4 BSD-2), `prototyp/` a `index.html` (Pages), `docs/` (sumáře). Licence: kód MIT, data a texty CC BY 4.0 (návrh Claude, uživatel může změnit). Velká rastrová data (LAZ, TIF) se do repozitáře nedávají (.gitignore), jen odvozené lehké vrstvy.
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
- 16. 10. 2026 - **Výpočetní území**: intravilány + stékající svahy v 1 m gridu; zbytek povodí kontext (5 m, WMS). Profil na Kyjovce pod Koryčany (🤔 ř. km 75,69, ověřit); dílčí součty za sídla.
- 16. 10. 2026 - ÚSK ORP Kroměříž (2017) a KoPÚ (neproběhly) nejsou vstupy; KoPÚ lze vyvolat podpisy vlastníků nadpoloviční výměry (§ 6 odst. 3 zák. 139/2002 ✅).
- 15. 10. 2026 - QGIS se nepoužije; Python (rasterio, geopandas, whitebox); kontrola přes PNG náhledy.
- 15. 10. 2026 - Prostředí: Windows, Python 3.14.7, pip 26.2.1; rasterio 1.5.2 wheel cp314 ✅.
- 15. 10. 2026 - Podklad Leaflet: ČÚZK ZTM WMTS + Ortofoto WMS. Historie: II. a III. vojenské mapování.
- 15. 10. 2026 - Hydrogeologická mapa ČGS: volat přes 4326.

## Otevřené otázky
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
- Licence repozitáře: návrh MIT (kód) + CC BY 4.0 (data, texty) čeká na potvrzení uživatele.

## Zvolené předpoklady
- Metadatové záznamy Micka institucí beru jako oficiální zdroj adres a licencí.
- DMR 5G jako LAZ, hustota cca 1 bod/m² 💻 postačí pro 1 m grid v intravilánu.
- Součinitele odtoku z tabulky tzb-info/ČVUT ✅; text normy neotevřen.
- Návrhový déšť zatím podle Brna (ASIO) ✅; pro Koryčany ověřit v normě.
- Srážky 571,5 mm/rok (Kroměříž) jako zástupná hodnota 🤔.
- USLE faktory C a P z manuálu kalkulačky VÚMOP 2017 ✅⏳ a Janečka 2012 ✅⏳.
- Dopočty z měření jsou 🤔 z hodnot ve zdroji, ne autorův závěr.
- Paragrafy vodního zákona ověřeny jen na nestátním zrcadle bez data znění.
- Účinky leaky dams a stínění toku jsou zahraniční ✅; české měření nedohledáno.
- V prototypu jsou sklon, půda, počet domácností (1 050), průměrná střecha, plocha povodí (20 km²) a podíly sídel syntetické a jsou tak označené.

## Na co ses nezeptal a měl bys
- Má město pasport zeleně nebo zpevněných ploch? Ušetřilo by ruční klasifikaci z ortofota.
- Chce oddíl nebo město využít výzvu AOPK ZMV (20. 10. - 3. 11.) nebo OPŽP 105 (do 17. 12.)?
- Jsou pole kolem Koryčan v LPIS vedené jako SEO/MEO? Lesy: kdo je vlastník?
- Máš disk a čas na stažení DMR 5G? Po zúžení území 🤔 spíš stovky MB než GB.
- Kdo bude mít v organizaci Skauti-Korycany práva k repozitáři po tobě (aspoň dva správci)?
