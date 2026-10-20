# STAV projektu Koryčany resilience

Aktualizováno: 20. 10. 2026 (relace 7; **blok G: prototyp v0.2 nad skutečnými daty** - klik = sklon a půda z rastrů, území = budovy ČÚZK a odtok CN, srážky ČHMÚ Koryčany)

## Fáze: 1 a 2 hotové. Fáze 3 (jádro) rozpracovaná: v0.1 umí statistiku pozemku, SCS-CN po buňkách, povodí bodu, nádrž/poldr z DMR; chybí transformace vlny, bilance P-ET, USLE, napojení opatření.

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
- Srážkový normál: ~~Kroměříž 571,5 mm~~ nahrazeno 19. 10. stanicí ČHMÚ **Koryčany 632 mm** (1991-2020) - viz blok E.
- Regionální kontext ✅ (18. 10.): Plán dílčího povodí Dyje 2021-2027 pro povodí VN Koryčany bez retenčních opatření nad nádrží.
- Zásobník nápadů: docs/NAPADY-ROZHRANI.md (posuvníky škál; pole `vahy_skaly` v JSON).
- **Blok B část 1 (fáze 2), 19. 10. - terén hotov.** 12 listů DMR 5G (BUCO25-28, 35-38, 45-48; LAZ, CC BY 4.0) -> `repo\data\dmr\dmr5g_5m.tif` (5 m, EPSG:5514, float32, 1500 × 1600 buněk, 100 % platných, 6,29 mil. bodů, hustota 0,10 bodu/m², výšky 225-534 m). Rozsah: X -562500..-555000, Y -1178000..-1170000 = 17.108-17.221 E, 49.074-49.153 N (7,5 × 8 km). Náhled reliéfu zkontrolován (přehrada, niva Kyjovky, hřebeny Chřibů). Výstupy: `dmr5g_5m.tif` (jen na PC, .gitignore), `dmr5g_5m_hillshade.png` (kopie v docs/img/), `dmr5g_5m_info.json` a `dmr5g_5m_bounds.geojson` (kopie v data/). Skript `tools/01_dmr_grid.py`, spouštěč `tools/vyrob_teren.bat` (poklepání, instaluje knihovny, ~4 min).

- **Blok B část 2 (fáze 2), 19. 10. - rozvodnice hotovy (otestováno v Claude na skutečném dmr5g_5m.tif, 32 s).** Skript `tools/02_rozvodnice.py` + `tools/vyrob_rozvodnice.bat`: priority-flood vyplnění depresí, D8 směr, akumulace, sklon a expozice (Horn), údolnice >= 0,25 km², povodí k uzávěrovým bodům. Bez whitebox/pysheds (čistý numpy/scipy; whitebox stahuje binárku z webu, což u uživatele nemusí projít). Rastry v `repo\data\dmr\`: smer_odtoku, akumulace, sklon_deg, expozice_deg, deprese, povodi_id (.tif, mimo git). Do gitu: `data/povodi.geojson` (8 polygonů), `data/toky_dmr.geojson` (108 linií), `data/rozvodnice_body.json` (uzávěrové body, upravitelné), `data/rozvodnice_info.json`, náhledy `docs/img/rozvodnice_nahled.png`, `sklon_nahled.png`. Výsledky: hlavní povodí Kyjovka pod soutokem se Stříbrníkem **19,9 km²** (bod -559412, -1173982; nalezen automaticky po proudu od profilu Stříbrník), profil Kyjovka ř. km 75,69 = 13,7 km² (z toho pod přehradou 5,8 km² - **oříznuto východním okrajem rastru**), Stříbrník ř. km 1,07 = 4,2 km², Lískovec 0,4, Blišice 0,6, Jestřabice 0,7 km² (jen potůčky obcemi). Celý rastr odvodňuje 31,7 km² k výstupu Kyjovky na západním okraji (17.1099 E, 49.1314 N). Průměrný sklon 9,4°, 28,5 % buněk nad 12°. Souřadnice hlásných profilů ✅ edpp.cz (ORP Kroměříž): Kyjovka 75,69 = -558794,48/-1173991,39; Stříbrník 1,068 = -559180,53/-1174691,52; pod přehradou 77,76 = -556751,96/-1173879,95. Středy obcí ✅ cs.wikipedia: Lískovec 49.1236/17.1808, Blišice 49.1228/17.1656, Jestřabice 49.0919/17.1297, VN Koryčany 49.1167/17.1964.

- **Blok B část 3 (fáze 2), 19. 10. - budovy a toky hotovy.** `tools/03_vektory.py` + `tools/vyrob_vektory.bat` (čistý Python: xml.etree, sqlite3 + ruční WKB, bez geopandas). Vstupy ✅ atom.cuzk.gov.cz (CC BY 4.0, "žádné podmínky neplatí"): INSPIRE Budovy (BU) po obcích - Koryčany [588601] `services.cuzk.gov.cz/gml/inspire/bu/epsg-5514/588601.zip` (0,5 MB GML, EPSG:5514, 1 898 budov); INSPIRE Vodstvo HY-NET `openzu.cuzk.gov.cz/opendata/HY-NET/HY-NET.zip` (194 MB, GPKG, EPSG:3045, celá ČR; vrstvy HydroNode, WatercourseLink - **bez názvů toků**). Výstupy: `data/budovy.geojson` (1 487 budov v území modelu, půdorysy 25,4 ha; Koryčany 913, Lískovec 171, Blišice 22, 381 bez části obce; 957 RD = 11,5 ha střech, 75 průmysl = 6,5 ha, 303 garáže/kůlny, 44 bytové domy, 55 zemědělské, 40 veřejné; podle dílčích povodí: Kyjovka 75,69 = 600, Stříbrník 238, Lískovec 94, 555 mimo dílčí povodí), `data/budovy_info.json` (součty), `data/toky_cuzk.geojson` (140 linií v bboxu +200 m, 44 v území), náhled `docs/img/vektory_nahled.png`. Bez č.p., adres a ID budov. Vstupy na PC: `repo\data\588601\`, `repo\data\HY-NET\` (v .gitignore).

- **Veřejná stavová stránka**, 19. 10.: `stav.html` -> https://skauti-korycany.github.io/korycany-voda/stav.html (účel, území s interaktivní mapou povodí/toků/budov nad ZTM, co je hotovo, k čemu půdní data, zásady, zdroje). Určena jako odkaz do žádosti o data VÚMOP. Při změně dat ji aktualizovat (čísla jsou v HTML natvrdo).
- VÚMOP ✅ (vumop.cz/poskytovani-dat, 19. 10.): žádosti na data@vumop.cz (tel. 257 027 265), formální náležitosti web neuvádí, ceník neuvádí; **BPEJ je volně ke stažení u SPÚ** (aktualizace měsíčně; kontakt uveden na stránce), takže od VÚMOP žádáme hlavně HSP, erozní ohroženost a zamokřené půdy.

- **Blok B část 4a (fáze 2), 19. 10. - využití půdy hotovo.** `tools/04_vyuziti_pudy.py` + `tools/vyrob_vyuziti.bat`: ZABAGED polohopis přes **WFS ČÚZK** ✅ (`ags.cuzk.gov.cz/arcgis/services/ZABAGED_POLOHOPIS/MapServer/WFSServer`, WFS 2.0, GeoJSON, EPSG:5514, CC BY 4.0; limit 1000 prvků na dotaz a server ignoruje startIndex -> skript dělí bbox na čtvrtiny a slučuje podle GmlID). 25 vrstev staženo do `repo\data\zabaged\` (mimo git), vypáleno do mřížky DEM: `data/dmr/vyuziti_kod.tif` (uint8, legenda v `data/vyuziti_pudy.json`), vektor `data/vyuziti_pudy.geojson`, náhled `docs/img/vyuziti_nahled.png`. Území modelu 1 412,7 ha: les listnatý 465, smíšený 144, jehličnatý 36, druh neurčen 60 (les celkem 705 ha = 50 %), orná 261, TTP 153, zahrady 84, sady 37, křoviny 29, areály účelové zástavby 48, budovy 25,5 (INSPIRE BU, střed buňky), ostatní plocha v sídle 22, zeleň 13, komunikace 19 (silnice 7,2 / ulice 7,5 / cesty zpevněné 4,2; linie šířky 5 m), voda 1,1, bažina 0, nezařazeno 0,6. Součty i po dílčích povodích. Les podle druhu z vrstvy Lesní půda kategorizovaná (druh_k J/L/S, výška porostu).
- **Kontrola rozvodnic** ✅: vrstva ZABAGED `Rozvodnice` (povodí IV. řádu ČHP, 24 linií) -> `data/povodi_chp.geojson`. Hranice z DMR 5G se s oficiální rozvodnicí shoduje na západě, jihu i severu prakticky přesně; odchylky jen u hráze VN (naše dělení vs. ČHP). ČHP v území: 4-17-01-0680, 0690, 0710 (Kyjovka), 4-15-03-03xx (Jestřabice).

- **Blok B část 4b (fáze 2), 19. 10. - tabulka CN hotova.** `tools/build_cn.py` -> `data/cn_tabulka.json` (25 tříd = kódy využití půdy, 51 variant stavu, 10 odhadů), popis `docs/CN.md`. Zdroje ✅ Janeček a kol. 2012 (metodika ČZU; tab. 2.1 HSP, 2.2 HPJ->HSP, 2.3 CN pro IPS II; PDF na storm.fsv.cvut.cz) a ✅ USDA TR-55 (1986) tab. 2-2a/2-2c pro urbánní třídy. Kontrola: každý kód z vyuziti_pudy.json má řádek. Orientačně: vážené CN území modelu = 65 při HSP B, 77 při HSP C.

- **Blok B část 4c (fáze 2), 19. 10. - HSP a CN hotovy (náhradní HSP).** `tools/05_hsp.py`: BPEJ z **WFS SPÚ** ✅ (`geoportal.spucr.cz/api/open-data/wfs/wfs_bpej`, WFS 1.0.0, jen GML2, EPSG:5514, Fees none / AccessConstraints none; 172 polygonů v bboxu, parsování regexem bez GDAL) -> HPJ (2.-3. číslice BPEJ) -> HSP podle Janeček 2012 tab. 2.2; plochy bez BPEJ (lesy, intravilán) doplněny HSP nejbližší bonitované plochy = **odhad 48 % území** (681 ha), označeno v `hsp_zdroj.tif`. Výsledek území modelu: A 3 ha, B 796 ha, C 144 ha, D 470 ha. HPJ v území: 40/41 (svažité, 55 polygonů), 19/20 (pelozemě/těžké, 41), 08/11/10, 24/27, 49, 58, 22, 06; 17 polygonů kód 00 (bez bonitace). Výstupy `data/dmr/hsp.tif`, `hsp_zdroj.tif`, `hpj.tif`, `data/hsp_info.json`, `data/bpej.geojson` (1,5 MB), `docs/img/hsp_nahled.png`. Přepínač `--vumop <soubor>` pro data VÚMOP (GeoTIFF 1-4 nebo GeoJSON s atributem HSP) - nahradí BPEJ, zdroj = 3.
  `tools/06_cn.py`: `data/dmr/cn.tif` (CN = cn_tabulka výchozí × využití × HSP), `odtok_P20/40/60.tif`, `data/cn_info.json`. **Území modelu: vážené CN 72,0** (B 56 %, C 10 %, D 33 %); ilustrační déšť 40 mm -> Q 5,5 mm = 78 tis. m³, koef. 0,14; 60 mm -> 14 mm = 198 tis. m³. Dílčí: Kyjovka 75,69 CN 75,9 (Q40 = 7,1 mm), Stříbrník 65,2 (2,5 mm, les), Lískovec 79,0 (9,4 mm). Spouštěč `tools/vyrob_cn.bat` (05 + 06).

- **Blok E (krok 0), 19. 10. - srážky ČHMÚ hotovy** -> `docs/SRAZKY.md`. opendata.chmi.cz ✅ (`historical_csv` do 2025, `recent` 2026; formát ověřen z knihovny wetterdienst; z Claude je server blokovaný, skripty běží na PC). **V Koryčanech je manuální stanice ČHMÚ** (WSI 0-203-0-41701068002, 305 m, 1,2 km od středu území): denní úhrny 1920-2025, 88 úplných let, 2026 do 31. 8. Normál 1991-2020 **632 mm**; N2/N10/N100 denní (Gumbel, orientačně) 37/58/84 mm; max 114 mm (2. 7. 1954), 93,5 mm (12. 6. 2012). Staré Hutě (427 m, 9 km) 717 mm, N10 72 mm. Automatické stanice s 1h/10min daty: **Nemochovice (7,8 km) a Staré Hutě (9,4 km)**. Epizody Kachníku léto 2026: 14.-15. 7. (bouřka 14. 7. večer, 12 mm/h Staré Hutě 15. 7. 05 UTC), 1. 8. (21 mm/h a 10,8 mm/10 min jen u Nemochovic, Koryčany 5 mm), 8. 9. **bez deště na obou stanicích**, 11. a 17. 9. trvalý slabý déšť. Léto 2026 v Koryčanech VI-VIII 113 mm = polovina normálu. Skripty `tools/07_srazky_chmi.py` + `vyrob_srazky.bat`, `tools/08_srazky_recent.py` + `vyrob_srazky_2026.bat`; výstupy `data/srazky_chmi.json`, `srazky_stanice.json`, `srazky_2026.json`, `docs/img/srazky_nahled.png`; surovina `data/chmi/` (gitignore).

- **Blok F (fáze 3), 19. 10. - jádro v0.1 hotovo** -> `docs/JADRO.md`. `tools/09_balicek_web.py` (+ `vyrob_balicek_web.bat`): rastry -> `data/web/` (9 PNG pásem, 5,0 MB, `rastr.json` s polynomem WGS84<->S-JTSK, chyba < 2 mm). `web/jadro.js`: převody, SCS-CN (+ IPS I/III), rasterizace polygonu, statistika buněk (plocha, CN, sklon, využití, HSP, odtok po buňkách), povodí bodu (zpětné D8, 4,2 km² za 65 ms), nádrž/poldr (zatopení pod hladinou), vykreslení masky do Leafletu. `web/test_jadro.js` (node + pngjs): 22 testů OK, shoda s 06_cn.py (území modelu CN 72,0, P40 78 248 m³; Stříbrník 4,23 km², CN 65,2). `web/test.html`: zkušební prohlížeč (klik = povodí bodu nebo hráz, podklady CN/sklon/využití/HSP/akumulace), ověřen v headless Chromiu; **živě: https://skauti-korycany.github.io/korycany-voda/web/test.html**. Balíček vygenerován v Claude z rastrů staženým z PC (data/dmr), uživatel nic nespouštěl.

- **Blok G (fáze 3/4), 20. 10. - prototyp v0.2 na skutečných datech.** `tools/build_dummy.py` vkládá `web/jadro.js` a čte `budovy_info.json`, `cn_info.json`, `srazky_chmi.json`. Můj pozemek: klik -> sklon (DMR 5G, průměr v okruhu 15 m), půda A-D (BPEJ/HSP, s příznakem odhad), složení okolí 30 m (ZABAGED) jako nápověda; plochy střech/dvora zadává uživatel. Déšť navíc 58 mm (N10 Koryčany 🤔) a 94 mm (12. 6. 2012). Celé území: 957 RD, průměrný půdorys 120 m² ✅ ČÚZK BU, podíly sídel podle počtu budov v dílčích povodích, "Na co to nestačí" proti skutečnému území 1 412 ha a odtoku z CN (P20 12 876 m³). O modelu: srážky, N-leté úhrny, CN, odtok. Katalog v0.4: srážky 632 mm (zdroj `chmi_korycany`), nová konstanta `navrhovy_dest_denni_korycany` (Gumbel, značka odhad). Ověřeno v headless Chromiu (klik na TTP u Stříbrníku: sklon 1 %, HSP C z BPEJ). Jádro v0.1 opraveno 19. 10. večer: buňka hráze se nepočítá, příznak "pod rozlišením" (< 8 buněk), v test.html vidět klik i přichycený bod. **Uživatel: nádrže "nepovedené", zatím odloženo.**

- **Blok H, 20. 10. - katastrální parcely v prototypu.** `tools/10_parcely.py` + `vyrob_parcely.bat`: INSPIRE CP ČÚZK (CC BY 4.0) pro k.ú. Koryčany [669661], Blišice [669652], Jestřabice [659053], Lískovec [684881] (ve feedu ČÚZK jen "Lískovec"), ořez na území modelu -> `data/parcely.geojson` (3,4 MB; 7 013 parcel vč. Lískovce [684881] 2 481 parcel, 949 ha; 1 136 parcel s RD; parcelní číslo, k.ú., výměra, budovy a půdorysy z BU; bez vlastníků/LV/adres), `data/parcely_info.json`, `docs/img/parcely_nahled.png`. Prototyp: parcely a budovy se kreslí od zoomu 16; klik vybírá parcely (toggle, sčítá se: výměra, střechy = půdorysy budov, zeleň = zbytek po odečtení zpevněných, které zadává uživatel); sklon a půda z vybraných parcel. Zjištění: parcela s RD má medián 248 m² = stavební parcela (dům), zahrada je samostatná parcela - proto vícenásobný výběr.

- **Blok I, 20. 10. - odtok z krajiny v Celém území.** Panel "Pole, louky a les": histogram buněk území modelu (třída × HSP × údolnice ≥ 1 ha × svah ≥ 7°) z rastrů v prohlížeči (565 tis. buněk), odtok SCS-CN po třídách; scénáře mění CN podle `cn_tabulka.json` (Janeček 2012 tab. 2.3): P04 půdoochranné technologie, P01/P03 vrstevnicově + pásy, P06 zatravnění svažité orné (> 7°), P05 zatravnění údolnic, stav lesa, stav pastvin. Kontrola: "teď" = 12 876 / 78 248 m³ při 20 / 40 mm = přesně 06_cn.py. Příklad: 50 % orné vrstevnicově + údolnice při 40 mm = -6 442 m³ (-8 %). Třídy pod 5 ha sloučeny. Eroze, vlna a výpar se nepočítají (napsáno v textu).

### Rozpracováno
- **Žádost VÚMOP odeslána 19. 10. 2026** (data@vumop.cz, z adresy oddílu): vektor hydrologických skupin půd (mapa velkého měřítka, metadata ID 5cc1bdc2-de34-4eee-a439-41420a000319), správní území obce Koryčany + obal ~500 m, SHP/GPKG v EPSG:5514; dotazy na licenci pro veřejnou webovou aplikaci, zpoplatnění nekomerčního užití a HSP pro lesy mimo ZPF. Odkaz na stav.html v textu. Čeká se na odpověď. Erozní ohroženost a zamokřené půdy v žádosti nejsou - případně druhá žádost po odpovědi.
- Chybějící podklady od uživatele: NOO 2026 (XLSX) a NOO 2025_2; seznam platných SPPK (aopk.gov.cz/platne-standardy); znění vodního zákona (e-Sbírka) § 15b, 17, 46, 47, 55; nejbližší stanice ČHMÚ; text ČSN 75 9010.
- Data z měření: uživatel požádá Povodí Moravy. Text žádosti na vyžádání (vzor: žádost VÚMOP z 19. 10.).
- Zpětná vazba k prototypu (tón textů, pořadí kroků, síla "Na co to nestačí") - čeká na uživatele.
- Otevřené body rozhraní (ROZHRANI.md kap. 6).

### Další kroky (pořadí)
0. ~~srážková data~~ hotovo 19. 10. (blok E). Zbývá: licence otevřených dat ČHMÚ (otevřít podmínky na opendata.chmi.cz, zapsat do VRSTVY.md); srážkoměr VD Koryčany do žádosti na Povodí Moravy.
1. **Další kandidáti**: (a) parcely Lískovce (uživatel doběhne `vyrob_parcely.bat`, Claude nahraje), (b) průmysl/bytové domy/veřejné budovy do Celého území (střechy 14 ha mimo RD), (c) transformace vlny poldrem, (d) nádrže v jádru (uživatel řekne, co nesedí), (e) USLE pro ornou půdu (R faktor Koryčany chybí), (f) stav.html aktualizovat (parcely, srážky, jádro).
2. Návrhové úhrny N-letých dešťů pro Koryčany (ČHMÚ / ČVUT metodika 2023 "Krátkodobé srážky"), přepočet IPS I/III (J12 obr. 2.2).
3. Až přijde VÚMOP: `--vumop` v vyrob_cn.bat, přepočet, porovnat s BPEJ odhadem.
4. Názvy toků do toky_cuzk.geojson: z INSPIRE HY-P (ČÚZK) nebo DIBAVOD A02 (NAZ_TOK) - až bude potřeba v rozhraní.
5. Blok D: "reakce toku na déšť" léto 2026 z CSV Kachník + hodinová data Nemochovice/Staré Hutě (data/srazky_2026.json) - dnes už lze.
6. Uživatel ověří WMS označené ❌ ve VRSTVY.md (LPIS MZe, katastr ČÚZK, CENIA vojenská mapování); napíše na data@vumop.cz (HSP, BPEJ, zamokřené půdy).
7. Dotační okna: AOPK OPŽP ZMV 17. výzva 20. 10. - 3. 11. 2026; OPŽP 105 do 17. 12. 2026.

## Rozhodnutí
- 20. 10. 2026 - **Parcely a budovy z katastru se používají** (ČÚZK INSPIRE CP + BU, otevřená data CC BY 4.0). Pravidlo o osobních údajích se týká vlastníků, LV a adres - ty se nestahují. Parcelní číslo je veřejný identifikátor pozemku a v aplikaci se zobrazuje. (Opraveno dřívější mylné rozhodnutí z téhož dne, že se katastr nenačítá - upozornil uživatel.) Zpevněné plochy v datech nejsou, zadává uživatel.
- 20. 10. 2026 - **Srážky v katalogu = ČHMÚ Koryčany 632 mm** (místo Kroměříž 571,5); vzorce "A × 0,5715" přepsány na 0,632.
- 19. 10. 2026 - **Rastry pro web zůstávají v mřížce S-JTSK** (ne warp do Mercatoru): D8 a sousednost platí jen v původní mřížce; převod souřadnic dělá polynom 2. řádu z pyproj (v `rastr.json`), zobrazení převzorkováním v JS. Pásma jako 8/16bit PNG (bez knihoven, bezztrátově), 5 MB celkem - pro verzi 1 přijatelné; ořez na území modelu až bude třeba.
- 19. 10. 2026 - **Odtok SCS-CN se počítá po buňkách a sčítá** (ne z průměrného CN) - vzorec je nelineární; shoda s 06_cn.py.
- 19. 10. 2026 - **Nádrž = zatopení terénu pod hladinou** uvnitř povodí hráze, bez tvaru hráze a ztrát; viditelně označeno jako orientační.
- 19. 10. 2026 - **Srážky ze stanice ČHMÚ Koryčany** (ne Kroměříž, ne interpolace); pro lesní část Chřibů orientačně Staré Hutě. Stanice 8-9 km daleko se neberou jako měření nad povodím pro přívaly (1. 8. 2026: 21 mm/h Nemochovice vs. 5 mm Koryčany) - pro validaci je nutný srážkoměr v povodí (VD Koryčany nebo škola u Kachníku).
- 19. 10. 2026 - **Data ČHMÚ stahuje skript na PC** (opendata.chmi.cz je z Claude blokované); surovina mimo git, do gitu jen souhrnné JSON.
- 19. 10. 2026 - **HSP náhradně z BPEJ (SPÚ, otevřená data) + Janeček tab. 2.2**, lesy a intravilán doplněny nejbližší bonitovanou plochou a označeny jako odhad. Data VÚMOP, až přijdou, se vymění jedním parametrem (`--vumop`), navazující výpočty se přepočítají .bat souborem. Uživatel chce rychle do vizualizace a ladění; přesnost HSP v lesích je známá slabina, viditelně označená.
- 19. 10. 2026 - **CN podle Janeček 2012 (IPS II, Ia = 0,2 S)**, urbánní třídy z TR-55; stáří zdroje 2012 přijato (fyzikální metoda). Výchozí stavy: orná konzervativně (obilniny Př Šp), TTP > 75 %, les střední; nepropustné 98; voda 100. Druh lesa CN nemění.
- 19. 10. 2026 - **Využití půdy ze ZABAGED přes WFS, ne z 5,8GB GPKG ani WMS obrázku**: WFS dává vektor s atributy (druh lesa, typ zahrady/sadu, typ areálu), stahuje se jen bbox, skript to zvládne sám. Komunikace jako linie 5 m, budovy z INSPIRE BU (střed buňky, bez nadsazení plochy).
- 19. 10. 2026 - **Rozvodnice ověřeny proti ČHP** (ZABAGED) - hranice modelu se nemění.
- 19. 10. 2026 - **Jen Koryčany.** Model řeší rozhodování jedné obce, ne mikroregionu: budovy jen z obce Koryčany (588601), sousední obce (Střílky u SV rohu) se nestahují. Platí i pro další vrstvy.
- 19. 10. 2026 - **Toky z ČÚZK HY-NET, ne DIBAVOD**: jasná licence CC BY 4.0 a aktuální data (10/2026); DIBAVOD A02 je z r. 2006 a bez uvedené licence. Cena: HY-NET nenese názvy toků.
- 19. 10. 2026 - **Budovy bez identifikátorů**: do GeoJSON jde půdorys, účel (RÚIAN), část obce, plocha, podlaží, id dílčího povodí. Č.p., adresy, ID RÚIAN/ISKN se nezapisují (pravidlo projektu). Ořez = těžiště v polygonu území modelu.
- 19. 10. 2026 - **Hranice modelu = hráz VN Koryčany nahoře, profil Kyjovky pod soutokem se Stříbrníkem dole.** Odtok z nádrže je řízený, povodí nad hrází se nemodeluje (a je navíc oříznuté rastrem). Území modelu = 19,9 - 5,8 = **14,1 km²**, polygon `typ: uzemi_modelu` v `data/povodi.geojson`; v `rozvodnice_body.json` má bod id 3 příznak `vyloucit_z_modelu`. Uživatel potvrdil 19. 10. (body 1-3: hráz jako hranice, profil pod soutokem OK, Stříbrník = potok podél ulice Lhotka kolem rybníka Kachník, ústí do Kyjovky u Petrželky). Východní listy BUCO15-18 se nestahují.
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
- Povodí Jestřabic (Kratinka) leží z většiny západně mimo rastr (BUCO5x); zatím jen 0,7 km² uvnitř.
- Kanalizace Koryčany (jednotná/oddílná): nedohledáno online. Potvrdit u města (S02).
- Data Povodí Moravy: po odpovědi na žádost.
- ~~Nejbližší srážkoměrná stanice ČHMÚ~~ vyřešeno: Koryčany (manuální), Nemochovice a Staré Hutě (automatické). Otevřené: 8. 9. 2026 Kachník hlásil epizodu bez deště na obou stanicích - artefakt optiky, nebo bodová bouřka?
- Meliorace v území: žádost SPÚ (bezplatná) ✅; ISMS meliorace.vumop.cz (WMS nedohledána).
- Geokodér pro zadání adresy (ČÚZK RÚIAN 💻) - ověřit dostupnost a licenci.
- Licence VÚMOP, NLI, MZe, ČHMÚ: zdarma bez jmenované licence; redistribuce dat vyžaduje souhlas.
- Zapojení školy: sekce M a U07; registr estudanky.eu pro M04; úložiště měření (fáze 5).
- Zdroj klimatických scénářů 2050/2090 s licencí - nedohledán (roční bilance P-ET mimo verzi 1).
- Půdoochranné podmínky v pachtovní smlouvě: smluvně možné 🤔, právní výklad neověřen.
- SPPK kódy nedohledané: D02 003 (rok), revitalizace toků, břehové porosty, ochranné výsadby.
- R faktor a návrhový déšť pro Koryčany (kalkulačka VÚMOP, ČSN 75 9010) - doplnit do konstant JSON.
- Licence repozitáře: MIT (kód) + CC BY 4.0 (data, texty) - potvrzení uživatele.

## Zvolené předpoklady
- Převod CN na IPS I/III: standardní vztahy SCS (NEH-4/Hawkins) 💻; Janeček 2012 má jen graf (obr. 2.2) - ověřit, že čísla sedí.
- Polynom WGS84<->S-JTSK platí jen uvnitř rastru (extrapolace mimo něj neověřena).
- Metadatové záznamy Micka institucí beru jako oficiální zdroj adres a licencí.
- DMR 5G: CRS přiřazeno EPSG:5514 natvrdo (LAZ ČÚZK CRS nenese); třída 8 = body modelu terénu; výškový systém Bpv 💻.
- Součinitele odtoku z tabulky tzb-info/ČVUT ✅; text normy neotevřen.
- Návrhový déšť zatím podle Brna (ASIO) ✅; pro Koryčany ověřit v normě.
- Srážky: normál Koryčany 632 mm ✅ (ČHMÚ); datum denního úhrnu = začátek klimatologického dne 06 UTC (ověřeno proti hodinovým datům 14.-15. 7. 2026); N-leté úhrny Gumbel = orientační, do modelu až hodnoty ČHMÚ/ČSN 75 9010; licence dat ČHMÚ neotevřena.
- USLE faktory C a P z manuálu kalkulačky VÚMOP 2017 ✅⏳ a Janečka 2012 ✅⏳.
- Dopočty z měření jsou 🤔 z hodnot ve zdroji, ne autorův závěr.
- Paragrafy vodního zákona ověřeny jen na nestátním zrcadle bez data znění.
- Účinky leaky dams a stínění toku jsou zahraniční ✅; české měření nedohledáno.
- V prototypu jsou sklon, půda, počet domácností (1 050), průměrná střecha, plocha povodí (20 km²) a podíly sídel syntetické a jsou tak označené.

- Profil "pod soutokem" = první buňka, kde akumulace vzroste na 3× akumulace Stříbrníku; souřadnice hlásných profilů z odkazů na mapu edpp.cz (soustava stránkou neuvedena, hodnoty odpovídají S-JTSK).
- Depresní vrstva obsahuje hladinu VN Koryčany a umělé prohlubně (zářezy, lom) - pro "kde voda stojí" je nutné filtrovat podle sklonu a ortofota (fáze 3).

## Na co ses nezeptal a měl bys
- Co přesně ti na nádržích nesedí - umístění (přichycení), tvar zátopy, nebo objem? Bez toho to neopravím.
- Jak velká smí být aplikace na mobilu? 5 MB rastrů jde snížit (ořez na území modelu, hrubší akumulace) - rozhodni po vyzkoušení test.html na telefonu.
- Má škola nebo oddíl vlastní srážkoměr u Kachníku? Bez něj epizody čidla nejde spárovat s deštěm (viz 8. 9.).
- Stanice ČHMÚ Koryčany je manuální - víš, kde stojí a kdo ji odečítá? Pozorovatel může být partner projektu.
- Má město pasport zeleně nebo zpevněných ploch? Ušetřilo by ruční klasifikaci z ortofota.
- Chce oddíl nebo město využít výzvu AOPK ZMV (20. 10. - 3. 11.) nebo OPŽP 105 (do 17. 12.)?
- Jsou pole kolem Koryčan v LPIS vedené jako SEO/MEO? Lesy: kdo je vlastník?
- Kdo bude mít v organizaci Skauti-Korycany práva k repozitáři po tobě (aspoň dva správci)?
- Chceš vidět v náhledu i ortofoto/ZTM podklad místo stínovaného reliéfu? Jde to přidat přes WMS, ale náhled se pak generuje déle.
