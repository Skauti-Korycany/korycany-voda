# Katalog opatření - kvantifikace sekcí Z (zahrada, dvůr) a S (střecha, stavba)

Verze 18. 10. 2026. Doplňuje KATALOG.md (seznam a atributy). Zdroje ověřeny online 18. 10. 2026 (✅), ⏳ = starší než 12 měsíců, 📄 = citace z druhé ruky, 🤔 = odhad, 💻 = z paměti neověřeno. Kde je 🤔, aplikace zobrazí hodnotu jako "odhad" a rozsah, nebo ji nezobrazí.

## 0. Společné vstupy pro výpočet (jádro aplikace)

- **Srážky**: normál 1991-2020 stanice Kroměříž 571,5 mm/rok ✅ (VÚKROM, Obilnářské listy 2/2021, https://www.vukrom.cz/userfiles/files/obilnarske_listy/2021/2021_2/39_43.pdf). Koryčany na úpatí Chřibů 🤔 spíš vlhčí; dokud nemáme bližší stanici, počítat s 570 mm a označit.
- **Návrhový déšť** (ČSN 75 9010, tab. A.1/A.2, periodicita p = 0,2 = 1x za 5 let, příklad Brno ✅ z prezentace ASIO): 15 min 16,5 mm; 60 min 26,2 mm; 24 h 44,2 mm. Pro Koryčany použít hodnoty pro nejbližší stanici v tabulce normy (uživatel ověří v normě; tzb-info https://www.tzb-info.cz/normy/csn-75-9010-2012-02).
- **Součinitel odtoku C** (tabulka reprodukovaná na tzb-info a ve skriptech ČVUT ✅, sklon <1 % / 1-5 % / >5 %):
  - střecha běžná 1,0
  - střecha se souvrstvím >100 mm 0,5 (do 100 mm 0,7-0,8)
  - asfalt, beton, dlažba se zalitými spárami 0,7 / 0,8 / 0,9
  - dlažba s pískovými spárami 0,5 / 0,6 / 0,7
  - upravený štěrk 0,3 / 0,4 / 0,5
  - zatravňovací tvárnice 0,2 / 0,3 / 0,4; vegetační dlažba 0,25 / 0,35 / 0,45 (výrobce Izomat ✅, ne norma)
  - zahrady, hřiště 0,1 / 0,15 / 0,2
  - trávník 0,05 / 0,1 / 0,15
- **Základní vzorec**: objem odtoku V = plocha × srážka × C. Příklad: 100 m² střechy, déšť 20 mm, C = 1,0 -> 2,0 m³. Rok: 100 m² × 0,57 m = 57 m³ potenciálu (reálně méně o ztráty, 🤔 80-90 %).
- **Vsakování** (ČSN 75 9010 ✅ přes ASIO, MZe, ČVUT): zařízení se má vyprázdnit do 72 h; dno min. 1 m nad hladinou podzemní vody; odstup 5 m od nehydroizolované budovy, 2 m od hydroizolované (ČVUT, zdroj v normě neověřen); orientační prahy propustnosti (Stránský ČVUT ✅): průleh vhodný při kf > 5e-6 m/s, při nižší propustnosti průleh s rýhou, vsakovací nádrž kf > 1e-5 m/s. Jednoduchá zkouška (Praha 2009 ✅⏳): jáma, 30 min, pokles < 2 cm nevhodné, 4-8 cm střední, > 8 cm dobré.

## S. Střecha a stavba

### S01 Nádrž na dešťovou vodu
- Účinek R: každých 10 mm deště ze 100 m² střechy = 1 m³. Nádrž 1 m³ pojme 10 mm, 5 m³ pojme 50 mm, tj. celý návrhový 24h déšť p = 0,2 (44 mm) ze 100 m². Rok: potenciál 57 m³ ze 100 m², využije se jen to, co se mezi dešti spotřebuje (zálivka, WC).
- Účinek W: 🤔 zálivka zahrady v létě řádově 20-30 l/m²/týden 💻 - doplnit zdroj, nebo nezobrazovat.
- Účinek Q: zpoždění odtoku jen do naplnění; přepad musí jít do Z01/Z10, ne do kanalizace.
- Kč (ceny 18. 10. 2026, Hornbach ✅): IBC 1 000 l nový 7 250 Kč; podzemní nádrž 5 000 l vč. šachty 50 830 Kč. Montáž a výkop nedohledán (cena neověřena). Sud 200 l 💻 stovky Kč.
- Financování: NZÚ RD 2026 (SFŽP, pokyny od 28. 5. 2026 ✅ https://sfzp.gov.cz/files/documents/storage/2026/05/29/1780055187_2026-05-27_NZ%C3%9A-RD26+.pdf): forma kompenzace úroků bezúročného úvěru, ne dotace; oblast D.2 dešťová voda pro WC (+ zálivka) max. 100 000 Kč, nádrž min. 2 m³, napojena min. polovina WC; **jen v kombinaci se zateplením (A) nebo zdrojem energie (C)**; nádrž pouze na zálivku není podporována. Příjem od 25. 6. 2026.
- Povolení: 0; podzemní nádrž 🤔 1 (ohlášení dle velikosti).
- Zdroj provedení: ČSN 75 9010 ✅ (2012).

### S02 Odpojení dešťových svodů od kanalizace
- Účinek Q, I, R: 100 m² střechy a déšť 20 mm = 2 m³, které nejdou do kanalizace/toku, ale na pozemek. Součet za obec: plocha střech v intravilánu × srážka (vrstva ZABAGED).
- Kč: cena neověřena (🤔 stovky až tisíce Kč: prodloužení svodu, lapač).
- Podmínka: platí jen tam, kde svody vedou do kanalizace (jednotná). V Koryčanech neověřeno (podle uživatele místy oddílná kvůli ČOV). Souhlas provozovatele 💻.
- Zdroj: ČSN 75 9010, TNV 75 9011 ✅ (MZe 2013, https://mze.gov.cz/public/portal/-q363041---QOCSTmOG/tnv-75-9011-hospodareni-se-srazkovymi).

### S03 Zelená střecha (extenzivní)
- Účinek R, Q: zadrží cca 75 % běžného deště, u přívalu > 30 mm sníží odtok o 77-83 % ✅ (měření Žilinská univerzita, estav.cz 2. 7. 2024, https://www.estav.cz/cz/12505.strecha-s-vegetaci-jak-rostliny-chrani-dum-pred-horkem-nebo-kolik-zadrzi-vody-vedci-to-zmerili). Návrhově C = 0,5 (souvrství > 100 mm, tabulka výše); SZÚZ standard 2019 ✅⏳ uvádí příklad C = 0,3. Aplikace: rozsah C 0,3-0,5.
- Účinek CH: povrch vegetace o 5-7 °C chladnější než holá fólie, která má "téměř 60 °C" ✅ (tamtéž).
- Provedení: souvrství extenzivní 60-150 mm ✅⏳ (SZÚZ 2019, https://novazelenausporam.cz/files/documents/storage/2020/04/02/1585808609_Vegetacni_souvrstvi_zelenych_strech_Standardy_%202019_web-1.pdf).
- Kč: 1 000-2 500 Kč/m² extenzivní ✅⏳ (UJEP IEEP, leden 2023, https://www.fse.ujep.cz/wp-content/uploads/2024/01/Zprava_pro_klicove_aktery_c_4_zelene_strechy.pdf). Cena 2025-2026 nedohledána.
- Financování: NZÚ RD 2026 oblast D.1: 2 000 Kč/m² vegetační vrstvy, max. 150 000 Kč, min. mocnost 75 mm nebo C ≤ 0,55; jen s A nebo C ✅. Obce: OPŽP 1.3.4 ✅.
- Povolení: 1-2 (statika, u veřejných budov stavební úřad 💻).

### S04 Světlá střecha (albedo)
- Účinek CH: povrch chladné střechy o 28-33 °C nižší než tmavé (tmavé 66-85 °C, chladné 43-46 °C) ✅⏳ (US EPA, Cool Roofs compendium 2008, https://www.epa.gov/sites/default/files/2014-06/documents/coolroofscompendium.pdf). Vnitřní maximum o 1,2-3,3 °C nižší, špičková potřeba chlazení o 11-27 % nižší ✅ (EPA snapshot 2025, Synnefa 2007 📄). Vzduch ve městě při 50 % pokrytí střech jen o 0,2-0,3 °C ✅⏳ (simulace NYC, tamtéž).
- Závěr pro aplikaci: silný účinek na budovu a její okolí v metrech, malý na mikroklima obce; v součtu za území nezobrazovat jako teplotu vzduchu, jen jako plochu "ochlazených střech".
- Kč: cena neověřena.
- Vhodnost: tmavé ploché a mírně šikmé střechy (bytovky, haly, škola, garáže). Podíl v intravilánu odhadnout z ortofota (fáze 2).
- Povolení: 0.

## Z. Zahrada a dvůr

### Z01 Dešťová zahrada (zasakovací průleh s výsadbou)
- Dimenze: plocha 10-20 % napojené zpevněné plochy podle propustnosti (10/15/20 m² na 100 m² střechy) ✅⏳ (Praha, Ústav pro ekopolitiku + ČVUT 2009, https://www.praha14.cz/app/uploads/sites/4/2021/06/jak_hospodarit_s_destovou_vodou-1.pdf); cca 20 % ✅ (MENDELU ZF 2022, https://ubz.zf.mendelu.cz/wcd/w-zf-ubz/prednasky/seubz_2022_2_destovezahrady_prez.pdf). Max. vzdutí 25-30 cm; prázdná do 72 h; výkop 15-30 cm; sklony břehů 1:3 až 1:2; odstup od stavby 10 m (MENDELU) resp. 6-8 m u starší stavby na jílu (Praha); 1 m nad hladinou podzemní vody.
- Účinek R + I: zahrada 15 m² × 0,3 m vzdutí = 4,5 m³ = 45 mm ze 100 m² střechy, tj. celý návrhový 24h déšť p = 0,2. Rok: prakticky celý odtok ze střechy (57 m³) zasákne místo odtoku.
- Účinek CH, B: kvalitativně (výsadba, vlhké stanoviště) 🤔.
- Kč: cena neověřena.
- Vhodnost z dat: HSP A-C (po datech VÚMOP), sklon do 5 %, mimo nivu s mělkou podzemní vodou.
- Potřebuje S02. Financování: NZÚ ne ✅; vlastní.
- Povolení: 0 (do 300 m² mimo koryto; § 55 odst. 3 vodního zákona ✅).

### Z02 Zahradní tůň (bez fólie)
- Provedení: SPPK B02 001:2014 Vytváření a obnova tůní ✅ (AOPK + ČVUT FSv, https://www.mas-rakovnicko.cz/evt_file.php?file=3152): průměrná hloubka 0,8-1,0 m, max. 1,5 m; mělčiny do 50 cm min. polovina plochy; sklon břehů max. 1:3; velikost od ~1 m² po stovky m²; bez hráze a technických objektů není vodním dílem.
- Právo: vodní zákon § 55 odst. 3 ✅ - jednoduchá zařízení mimo koryta nejsou vodní díla; § 15b ✅ (zák. 312/2019 Sb.) - terénní úpravy k zadržování vody do 1,5 m hloubky a 300-20 000 m² v nezastavěném území jen na ohlášení; stavební zákon 283/2021 Sb. příloha 2 odst. 2 písm. g) ✅ totéž jako jednoduchá stavba (MMR 3. 9. 2025). Do 300 m² a 1,5 m bez hráze: 💻 drobná stavba bez povolení - **ověřit na vodoprávním úřadě ORP Kroměříž**, text přílohy 1 neotevřen.
- Účinek R: objem = plocha × průměrná hloubka (tůň 2x1 m, 0,5 m = 1 m³). Poctivě: tůň také vypařuje; v létě z volné hladiny 🤔 řádově jednotky mm/den 💻 - v aplikaci ukázat jako "zadrží X m³, část se odpaří" bez čísla, dokud nebude zdroj.
- Účinek CH, B: kvalitativně; B je hlavní přínos malé tůně 🤔.
- Vhodnost: zamokřená místa, těžké půdy (HSP C-D), úpatí svahů, niva.
- Kč: cena neověřena.
- Financování: AOPK ZMV / PPK B pro větší tůně a obce; jednotlivec vlastní.

### Z03 Zasakovací průleh / rýha po vrstevnici (svejl)
- Provedení: jako průleh dle ČSN 75 9010 (kf > 5e-6 m/s; při nižší s rýhou se štěrkem) ✅ (Stránský); prázdný do 72 h.
- Účinek I, Q, ER: zadržený objem = délka × průřez (průleh 10 m × 0,3 m² = 3 m³). Z vlastní plochy nad průlehem (ne ze střechy) zachytí povrchový odtok; u zahrady 200 m² se sklonem 10 % a C = 0,15 při 20 mm = 0,6 m³ -> jeden průleh stačí. Kvantifikace účinku na vlhkost půdy 🤔 nedohledána.
- Kč: cena neověřena (🤔 stovky Kč).
- Vhodnost: sklon 3-15 %, HSP A-C. Konflikt: nedělat nad budovou ve svahu bez odstupu (5 m).
- Povolení: 0.

### Z04 Náhrada zpevněných ploch propustnými
- Účinek I: rozdíl C. Dvůr 50 m², déšť 20 mm (1 m³): asfalt C 0,8 -> 0,8 m³ odteče; dlažba s pískovými spárami 0,6 -> 0,6; štěrk 0,4 -> 0,4; zatravňovací tvárnice 0,3 -> 0,3; trávník 0,1 -> 0,1. Zisk 0,2-0,7 m³ na každý 20mm déšť. Rok (570 mm, 50 m²): asfalt 22,8 m³ odtoku vs. tvárnice 8,6 m³.
- Účinek CH: trávník o 1-2 °C chladnější vzduch než zpevněné plochy ✅⏳ (EPA 2008); povrch 📄 - označit jako odhad.
- Kč ✅ (ÚÚR/RTS 2025): zatravňovací tvárnice 1 136 Kč/m², zámková dlažba 8 cm vč. podkladu 2 240 Kč/m², asfalt celá konstrukce 1 411 Kč/m².
- Vhodnost: HSP A-C, rovina; ne nad mělkou podzemní vodou.
- Povolení: 0-1.
- Zdroj: tabulka C (ČSN/TNV ✅ reprodukce), Izomat TL ✅.

### Z05 Mulč, kompost, trvalý pokryv půdy
- Účinek E: mulč snižuje výpar z půdy o 17-79 % za sezónu proti holé půdě, typicky ~33-40 % (slámový mulč 30-35 %) ✅ (přehledový článek Irrigation Science 2024, DOI 10.1007/s00271-024-00924-8; název a autoři nedohledáni, neuvádím).
- Účinek I, R: organická hmota zvyšuje retenci půdy 🤔 - kvantifikace nedohledána, zobrazit kvalitativně.
- Kč: 🤔 nula až stovky Kč (vlastní kompost, štěpka).
- Povolení: 0.

### Z06 Výsadba stromu
- Účinek CH: stín snižuje povrchovou teplotu stěn a střech o 11-25 °C ✅⏳ (US EPA 2008, Akbari 1997 📄, https://www.epa.gov/sites/default/files/2017-05/documents/reducing_urban_heat_islands_ch_2.pdf); vzduch ve skupinách stromů až o 5 °C nižší než nad otevřeným terénem (vrchol dne), předměstí se vzrostlými stromy o 2-3 °C ✅⏳ (tamtéž, Huang 1990, Kurn 1994 📄); městská zeleň v průměru o 1,6 °C chladnější (Knight et al. 2021, 308 studií 📄 přes EPA ✅).
- Účinek E, I, B: kvalitativně 🤔.
- Provedení: SPPK A02 001:2013 Výsadba stromů ✅ (aktualizované vydání existuje, rok neověřen 📄); ovocné: SPPK C02 003:2014 Funkční výsadby ovocných dřevin v zemědělské krajině ✅; keře: SPPK A02 003:2013 ✅.
- Kč ✅ (ÚÚR/RTS 2025): strom prostokořenný do 200 cm 1 775 Kč, s balem do 200 cm 2 835 Kč, s balem 250-350 cm 6 100 Kč; ovocné prostokořenné 240-350 Kč.
- Vhodnost: mimo ochranná pásma sítí; jižní a západní strana budov pro stín.
- Povolení: 0 (1 u sítí, 💻 u vzrostlých stromů blízko hranice občanský zákoník - odstupy).

### Z07 Živý plot / keřový pás
- Účinek E: za překážkou s propustností 40-60 % rychlost větru nižší o ~70 % ve vzdálenosti 5 H, 50 % v 10 H, 25 % v 20 H; relativní vlhkost v závětří +2-4 % ✅⏳ (Univ. Nebraska-Lincoln EC1763, https://extensionpubs.unl.edu/publication/ec1763/2006/pdf/view/ec1763-2006.pdf). Na jižní Moravě za větrolamy průměrné snížení rychlosti větru ~78 % (50 m za pásem), vlhkost půdy +102 % ✅⏳ (Dufková 2007, Acta Univ. Agric. Silvic. Mendel. Brun. 55(5), https://acta.mendelu.cz/pdfs/acu/2007/05/09.pdf; jedno měření, neobecňovat). Snížení evapotranspirace v % nedohledáno.
- Aplikace: živý plot výšky 2 m chrání pás cca 20-40 m (10-20 H) v závětří; ukázat jako plochu, ne jako °C nebo mm.
- Provedení: SPPK A02 003:2013 ✅.
- Kč: keř prostokořenný do 60 cm 190 Kč/ks ✅⏳ (NOO 2024).
- Vhodnost: návětrná strana (Z/JZ 🤔, ověřit z dat ČHMÚ).

### Z08 Květnatá louka, vyšší seč
- Účinek E, CH, B: kvantifikace vlhkosti nedohledána; trávník o 1-2 °C chladnější vzduch než zpevněné plochy ✅⏳ (EPA 2008) platí pro trávu obecně, ne pro režim seče. B: nepravidelně kosené plochy o 20 % druhově chudší, nekosené -34 % ✅ (Chytrá a kol. 2024, Příroda 44). Zobrazit E a CH kvalitativně.
- Provedení: SPPK D02 004 Sečení (10-20 % plochy ponechat) 📄; Praha MHMP 2019 ✅⏳ (výška 10-15 cm, neseče se nad 26 °C).
- Kč: trávník luční 40 Kč/m² ✅ (ÚÚR 2025); zatravnění regionální směsí 86 600 Kč/ha ✅⏳ (NOO 2024).

### Z09 Zelená fasáda, popínavky
- Účinek CH: kvantifikace nedohledána; obecně stín na fasádě viz Z06 (11-25 °C povrch ✅⏳). Zobrazit jako odhad.
- Kč: cena neověřena.

### Z10 Vsakovací objekt pro střešní vodu (štěrkové těleso, bloky, šachta)
- Dimenze: návrh na déšť p = 0,2 podle ČSN 75 9010; 100 m² střechy a 24h déšť 44 mm = 4,4 m³ minus to, co během deště zasákne; prázdný do 72 h; 1 m nad podzemní vodou; 5 m od budovy (2 m u hydroizolované) ✅ (ČVUT, ASIO, MZe). Vsakovací nádrž vhodná při kf > 1e-5 m/s ✅ (Stránský).
- Účinek I, R: celý odtok ze střechy zasákne (rok 57 m³ ze 100 m²).
- Kč: cena neověřena.
- Potřebuje: posudek vsaku (hydrogeolog) u větších objektů 💻; jednoduchá zkouška (Praha 2009 ✅⏳) pro orientaci.
- Financování: NZÚ ne ✅. Povolení: 0-1.

### Z11 Zálivka zachycenou vodou, kapková závlaha
- Účinek W: nedohledán český zdroj pro úsporu; 🤔 zobrazit jen "šetří pitnou vodu", bez čísla.
- Kč: cena neověřena.

## Co se nepodařilo dohledat (otevřené pro fázi 6)
- ČSN 75 9010: rozsahy kf "vhodné / podmíněně vhodné" a odstupy od budov přímo z textu normy.
- Samostatný součinitel odtoku pro extenzivní vs. intenzivní zelenou střechu.
- Ceny 2025-2026: zelená střecha Kč/m², montáž nádrže, reflexní nátěr, sazenice. Uživatel může poslat aktuální nabídky nebo odkazy, zapíše se s datem.
- Snížení evapotranspirace větrolamem v %; výpar z malé vodní hladiny; retenční účinek organické hmoty v půdě.
- Nejbližší srážkoměrná stanice ČHMÚ ke Koryčanům (opendata.chmi.cz; seznam stanic v `metadata/meta1.csv`, CC BY 4.0).
- Rok aktuálního vydání SPPK A02 001.

---

<!-- RESERSE-START (generováno tools/build_katalog_md.py, needitovat ručně) -->
## Doplnění z rešerše dobré praxe (bloky B, A, C, D, 21.-22. 10. 2026)

Generováno z `data/opatreni.json` v0.9 (2026-10-22); podrobný rozbor a odkazy: `docs/KATALOG-RESERSE.md`. Uvedeny jen nové položky a kvantifikace, příklady, přenositelnost a rizika doplněné rešerší; původní text výše platí dál. Značky: ✅ ověřeno online, ✅⏳ zdroj starší 12 měsíců, 📄 citace, 🤔 odhad.

### Z01 Dešťová zahrada (zasakovací záhon) (doplněno)
- Účinek infiltrace do půdy (hodnota) ✅⏳: Osázená mulda při vytrvalém dešti pojala a předala do podloží až o třetinu více vody než trávník (LWG); návrh: nádrž max. 30 cm, vyprázdnění do 24 h, k_f >= 1e-5 m/s [33 % více vody než trávník]. Zdroj: [LWG Veitshöchheim, Mit Pflanzen versickern, 2. vyd. 2010 (Schwarz, Epp](https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/merkblatt_mit_pflanzen_versickern.pdf)
- Účinek infiltrace do půdy (kvalitativne) ✅: Pilot Mnichov: po dobu sledování žádný pokles propustnosti ani při odtoku z komunikací; 57 ze 73 druhů trvalek obstálo. Zdroj: [LfU Bayern / TU München / HSWT / Bodeninstitut Prügl](https://www.cee.ed.tum.de/fileadmin/w00cbe/sww/_my_direct_uploads/LfU_Kurzdarstellung_2023_Versickerungsmulden.pdf)
- Účinek zpomalení odtoku (kvalitativne) ✅: Ozelenění zahrad snižuje odtok hlavně při dlouhých mírných deštích; při přívalu málo, na jílové vrstvě téměř nic (3 zahrady, Leeuwarden). Zdroj: [Lakhi N. 2025, Open Universiteit (diplomová práce)](https://research.ou.nl/en/studentTheses/the-impact-of-greening-measures-for-private-gardens-on-flood-prev/)
- Kde to funguje: **Mnichov (Bavorsko)** (2020-2023): pilotní multifunkční vsakovací mulda s trvalkami, projekt LfU/TU München/HSWT; sledována propustnost, zadržení znečištění z komunikací a hmyz. Měřeno: propustnost v čase (bez poklesu), zadržení Zn, Cu a biocidů. ✅ [LfU Bayern / TU München / HSWT / Bodeninstitut Prügl](https://www.cee.ed.tum.de/fileadmin/w00cbe/sww/_my_direct_uploads/LfU_Kurzdarstellung_2023_Versickerungsmulden.pdf)
- Kde to funguje: **Kecskemét (Maďarsko)** (2024): experimentální dešťová zahrada napájená ze střechy rodinného domu, různě tolerantní druhy; město ohrožené suchem. Měřeno: v abstraktu bez čísel. ✅ [Hoyk, Szórát, Farkas 2024](https://regscience.hu/items/3845b111-d508-4224-b71a-1ddfbe631ffe)
- Kde to funguje: **Bratislava** (2016-2020): dotace domácnostem a firmám na nádrže, dešťové zahrady, propustné povrchy a zelené střechy: 50 % nákladů do 1 000 €; 2016: 16 žádostí, 6 dokončeno; účinek neměřen, zájem malý. Bez měření. ✅ [Covenant of Mayors, případová studie Bratislava](https://eu-mayors.ec.europa.eu/sites/default/files/2022-10/EN_case%20study_Bratislava.pdf)
- Kde to funguje: **Rotterdam, Sponstuin** (2019): zkušební 'houbová zahrada': vlnitá mulda do 80 cm, 4 typy půdy s příměsemi, 2 roky měření. Měřeno: výsledky v letáku nejsou. ✅⏳ [De Urbanisten / Steenbreek](https://steenbreek.nl//wp-content/uploads/2019/08/20190621-sponstuin-flyer.pdf)
- Přenositelnost do Koryčan: V Koryčanech (HSP C/D, těžké půdy) pomáhá běžnému dešti 10 mm a mírným dešťům, ne N10 přívalu; na jílu počítat s rýhou nebo štěrkovým tělesem (Z10) a odstupy od domu.
- Rizika, co z toho neplyne: Účinek na přívaly je malý, aplikace to musí říkat. Stromy ne do vsakovací zóny. Trvalky volit podle tolerance k zaplavení i suchu.
- Nedohledáno: cena 2025-2026

### Z02 Zahradní tůň bez fólie (hliněná, jílem těsněná) (doplněno)
- Rizika, co z toho neplyne: V suchém létě je výpar z hladiny větší než srážky (vlastní data projektu, sekce Počasí): malá tůň bez přítoku na HSP C/D vyschne nebo žádá dolévání 🤔. Nepočítat ji jako zdroj zálivky.
- Nedohledáno: výpar z malé hladiny (mm/den); cena svépomocí; výpar zahradní tůně l/den (jen bazénové tabulky a diskuse)

### Z04 Náhrada zpevněných ploch propustnými (zatravňovací dlažba, štěrk, propustná dlažba) (doplněno)
- Účinek infiltrace do půdy (hodnota) ✅⏳: Po 4-7 letech provozu cca 90 % propustných ploch stále nad návrhem 270 l/(s·ha); čisté plochy 1 200-3 200, ucpaná místa 0-100 l/(s·ha) (jen 5-10 % plochy); mokrý povrch 210-260 [1200-3200 l/(s·ha)]. Zdroj: [MUNLV NRW, FH Bochum + IKT](https://www.lanuk.nrw.de/fileadmin/forschung/wasser/sonstiges/Kurzbericht_wasserdurchl_Flaeche.pdf)
- Účinek infiltrace do půdy (hodnota) ✅⏳: Odtok podle povrchu: štěrkový trávník a zatravňovací tvárnice 30-40 %, dlažba s travní spárou 40-50 %, dlažba s propustnou spárou, pórovitá dlažba a štěrkopísková cesta 0-20 % [0-50 % srážky]. Zdroj: [Bayerischer Landesverband für Gartenbau und Landespflege + LWG](https://mv.gartenbauvereine.org/wp-content/uploads/2020/05/MehrGruendurchBodenentsiegelung.pdf); [HLNUG / LGB RLP, Maßnahmensteckbrief 72](https://www.hlnug.de/fileadmin/dokumente/boden/Planung/Kompboden/msb_072_teilentsiegelung_versickerungsbelaege.pdf)
- Kde to funguje: **Severní Porýní-Vestfálsko** (2005): 24 objektů 4-7 let po odstranění asfaltu, 49 měření infiltrometrem; svépomocná pokládka bez měřitelného zhoršení, chyby firem (písek v pórech) propustnost srazily. Měřeno: infiltrace l/(s·ha) na stárnoucích plochách. ✅⏳ [MUNLV NRW, FH Bochum + IKT](https://www.lanuk.nrw.de/fileadmin/forschung/wasser/sonstiges/Kurzbericht_wasserdurchl_Flaeche.pdf)
- Kde to funguje: **Nizozemsko, NK Tegelwippen** (2021-2025): celostátní soutěž obcí ve 'vydlabávání dlaždic': 2025 téměř 6 mil. ks, od začátku 20 mil. (360 fotbalových hřišť); Utrecht 437 467 ks; přenositelné jako akce školy nebo oddílu. Měřeno: počet odstraněných dlaždic. ✅ [BNNVARA Vroege Vogels 17. 11. 2025](https://www.bnnvara.nl/vroegevogels/artikelen/nk-tegelwippen-2025-levert-bijna-6-miljoen-nieuwe-plekken-voor-natuur-op)
- Přenositelnost do Koryčan: Dvory, vjezdy, parkovací stání a cesty s malým provozem; sklon 2-3 % a odtok vést do zeleně. Na HSP D jen s podkladní vrstvou a bezpečnostním přepadem.
- Rizika, co z toho neplyne: Propustnost klesá ve stínu, pod mechem a u provozu; spáry čistit s odsáváním dřív, než se zanesou. Při pokládce nezametat písek do pórovité dlažby.

### Z05 Trvalý pokryv půdy: mulč, kompost, organická hmota (doplněno)
- Účinek omezení neproduktivního výparu / větru (hodnota) ✅: Slámový mulč (hořčice, svazenka, pšenice) snižuje výpar z půdy nejméně o 50 % proti holé půdě; mokrý mulč se odpařuje jako holá půda (DWD, vážené nádoby, 2012-2014) [50 % výparu z půdy]. Zdroj: [DWD Agrarmeteorologie Lipsko (Böttcher, Schmidt)](https://www.gartenbau.sachsen.de/download/Die_Wirkung_einer_Mulchbedeckung_auf_die_Evaporation.pdf)
- Účinek infiltrace do půdy (hodnota) ✅: +1 % organického uhlíku = +1,16 mm vody na 100 mm půdy (75 % studií 0,7-2 mm); nejvíc v píscích, nejméně v jílech; pro pelozemě Koryčan malý účinek (🤔 cca 3,5 mm v 30 cm ornice) [0.7-2.0 mm/100 mm půdy na 1 % C]. Zdroj: [Minasny B., McBratney A. B. 2018](https://agris.fao.org/search/en/records/65df2f3a63b8185d9cab777b)
- Účinek infiltrace do půdy (hodnota) ✅: Mulč z žita a hrachu v celeru (písek, Braniborsko 2023): vlhkost v 25 cm 15 % vs. 14 % holá půda; podsev jetele půdu vysušuje víc než holá půda [14-15 % obj. vlhkosti]. Zdroj: [Heistermann K. (IGZ Großbeeren), Wissenschaftstagung Ökologischer Land](https://orgprints.org/id/eprint/53926/1/Beitrag_279_final_a.pdf)
- Kde to funguje: **Lipsko (DWD Agrarmeteorologie)** (2012-2014): vážené Mitscherlichovy nádoby pod širým nebem, holá půda vs. mulč vs. porost, 2012-2014. Měřeno: aktuální evapotranspirace denním vážením. ✅ [DWD Agrarmeteorologie Lipsko (Böttcher, Schmidt)](https://www.gartenbau.sachsen.de/download/Die_Wirkung_einer_Mulchbedeckung_auf_die_Evaporation.pdf)
- Nedohledáno: retence půdy podle organické hmoty - český zdroj (zahraniční metaanalýza doplněna)

### Z06 Výsadba stromu (stín, vzrostlý strom, ovocný strom) (doplněno)
- Účinek ochlazení mikroklimatu (kvalitativne) ✅⏳: Výběr druhů do horka a sucha: LWG Stadtgrün 2021 (3 lokality Bavorska vč. Würzburgu, 30 druhů, 2009-2021): m. j. dub cer, dub uherský, jasan zimnář, habrovec, habr 'Frans Fontaine', lípa stříbrná; 15 ze 43 doporučených druhů ze stepních a suchých lesů. Zdroj: [LWG Veitshöchheim, Schönfeld](https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/zukunft_klimabaeume.pdf)
- Účinek ochlazení mikroklimatu (hodnota) ✅: ČR (CzechGlobe/UPOL, Olomouc 2018): ve stínu stromu na otevřené ploše pocitová teplota -8,3 až -10,9 °C, v ulici -2,8 až -7,6 °C; vzduch -0,4 až -2,1 °C podle denní doby; v noci +0,1 až +1,3 °C [0.4-2.1 °C vzduch (ČR)]. Zdroj: [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf); [ČT24 8. 8. 2022](https://ct24.ceskatelevize.cz/veda/3520774-i-travnik-pomuze-vedci-pripravili-doporuceni-ktera-maji-pomoci-ceskym-mestum-zvladat)
- Účinek ochlazení mikroklimatu (hodnota) ✅⏳: Pod stromem vs. u jižní stěny až -11,5 °C v poledne (šedý globe teploměr, 48 000 měření, 2 roky, severní Francie) [11.5 °C globe]. Zdroj: [Earthwatch Europe / PANORAMA](https://panorama.solutions/en/solution/measuring-effects-trees-heat-mitigation-northern-france)
- Účinek ochlazení mikroklimatu (hodnota) 📄: Povrch zástavby se stromy o 8-12 °C chladnější než bez stromů (satelit, ~300 evropských měst, střední Evropa); tráva 2-4x slabší; rozdíl ve vzduchu menší [8-12 °C povrch]. Zdroj: [ČT24 25. 11. 2021](https://ct24.ceskatelevize.cz/veda/3405168-stromy-vyrazne-ochlazuji-mestske-plochy-ubrat-mohou-az-12-stupnu-ukazuje-studie)
- Kde to funguje: **Würzburg, Kempten, Hof (Bavorsko)** (2009-2021): zkušební výsadby 30 druhů 'klimastromů' ve třech klimaticky odlišných městech, projekt Stadtgrün 2021. Měřeno: vitalita a růst po letech; skóre horko/sucho zdroj neuvádí. ✅⏳ [LWG Veitshöchheim, Schönfeld](https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/zukunft_klimabaeume.pdf)
- Kde to funguje: **Olomouc (a Brno, Ostrava, Plzeň)** (2018-2022): terénní měření pocitové teploty ve stínu stromů, v ulicích, u vodních prvků a na trávnících, 24. 7. 2018; doporučení a mapy horkých míst pro 4 města. Měřeno: pocitová a vzduchová teplota, stín vs. osluněná dlažba. ✅ [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf); [ČT24 8. 8. 2022](https://ct24.ceskatelevize.cz/veda/3520774-i-travnik-pomuze-vedci-pripravili-doporuceni-ktera-maji-pomoci-ceskym-mestum-zvladat)
- Kde to funguje: **Severní Francie** (2018-2020): občanská věda Earthwatch: 48 000 měření u stromů vs. u zdí a asfaltu, 2 roky. Měřeno: globe teplota. ✅⏳ [Earthwatch Europe / PANORAMA](https://panorama.solutions/en/solution/measuring-effects-trees-heat-mitigation-northern-france)

### Z09 Zelená fasáda, popínavky, pergola se zelení (doplněno)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Stěna pod přísavníkem trojcípým v průměru o 6,5 °C (jih) a 7,0 °C (západ) chladnější v době plného oslunění; účinek roste s teplotou nad 22 °C (Toronto, 6 měsíců) [6.5-7.0 °C povrch stěny]. Zdroj: [Blake M. 2021, Toronto Metropolitan University (diplomová práce)](https://rshare.library.torontomu.ca/articles/thesis/The_Potential_for_Perennial_Vines_to_Mitigate_Summer_Warming_of_an_Urban_Microclimate/14657580)
- Účinek ochlazení mikroklimatu (hodnota) 📄: Pod hustou popínavkou dopadá na zeď cca 20 % záření, povrch o cca 15 °C chladnější (sloupek inženýrské komory, studie nejmenovány) [15 °C povrch stěny]. Zdroj: [Edelhäuser K.-J. (Bayerische Ingenieurekammer-Bau), sloupek Bayerische](https://www.bayika.de/bayika-wAssets/docs/presse/standpunkte/2022-07-29.Fassadenbegruenung_und_Stadtklima_-_29-07-2022_Klaus_Juergen_Edelhaeuser.pdf)
- Kde to funguje: **Toronto (Kanada)** (2021): přísavník trojcípý na jižní a západní stěně městské budovy, teplotní loggery 6 měsíců. Měřeno: rozdíl povrchové teploty stěny. ✅ [Blake M. 2021, Toronto Metropolitan University (diplomová práce)](https://rshare.library.torontomu.ca/articles/thesis/The_Potential_for_Perennial_Vines_to_Mitigate_Summer_Warming_of_an_Urban_Microclimate/14657580)
- Přenositelnost do Koryčan: Jižní a západní stěny domů, garáží, kůlen, školy; samopnoucí druhy (přísavník) na zdravou omítku, jinak lanková konstrukce. Nehodí se na zateplené fasády bez konstrukce 🤔.
- Rizika, co z toho neplyne: Ochladí stěnu a interiér, ne ulici. Vídeňský údaj 'výkon 45 klimatizací' nemá doložený zdroj, nepřebírat. Údržba řezu u oken a okapů.
- Nedohledáno: cena

### Z12 Zalévací hliněné nádoby v záhonu (olla, oya) (nové)
- Co to je: Neglazovaná hliněná nádoba zakopaná po hrdlo mezi rostliny; naplní se vodou (nejlépe dešťovou z S01) a voda prosakuje stěnou přímo ke kořenům. Z povrchu půdy se nic neodpařuje, zalévá se jednou za několik dní. Středomořský princip, svépomocně ze dvou květináčů.
- Účinek šetření pitnou vodou (hodnota) 📄: Úspora vody 60-70 % proti zálivce konví (pokus s kukuřicí, aridní klima; citace v AZ1911) [60-70 % vody na zálivku]. Zdroj: [University of Arizona Extension AZ1911, Nickel & Brischke](https://extension.arizona.edu/sites/default/files/2024-08/az1911-2021.pdf)
- Účinek šetření pitnou vodou (hodnota) 📄: Výrobce: úspora 50-70 %, zálivka 3x řidší (studie nejmenovány); obec Ixelles po 1. sezóně: čas zálivky zhruba poloviční [50-70 % vody na zálivku]. Zdroj: [Oyas (Brusel), podklad pro zakázku obce Ixelles, bilance sezóny 2023](https://environnement.brussels/media/15711/download)
- Účinek omezení neproduktivního výparu / větru (kvalitativne) ✅: Voda jde pod povrch, neproduktivní výpar z půdy odpadá; proti kapkové závlaze úspora zhruba nulová (AZ1911). Zdroj: [University of Arizona Extension AZ1911, Nickel & Brischke](https://extension.arizona.edu/sites/default/files/2024-08/az1911-2021.pdf)
- Kde to funguje: **Roeschwoog, Alsasko (Francie)** (2022): pilotní záhon 12 m² před radnicí, 11 nádob po 6,5 l (cca 1 ks/m²), bez jiné zálivky; úspora času: dosud 3 půldny zálivky týdně. Bez měření. ✅ [Neozone 24. 5. 2022 (podle France 3)](https://www.neozone.org/ecologie-planete/un-village-alsacien-utilise-la-technique-ancestrale-des-jarres-enterrees-oyas-pour-economiser-leau-de-ses-jardins)
- Kde to funguje: **Ixelles, Brusel (Belgie)** (2023): 300 nádob ve veřejných záhonech; po sezóně 2023 čas zálivky zhruba poloviční, menší úhyn trvalek a keřů; sousední Watermael-Boitsfort dotuje domácnostem 75 % ceny do 100 €. Měřeno: čas zálivky (pozorování obce, nezávisle neověřeno). ✅ [Oyas (Brusel), podklad pro zakázku obce Ixelles, bilance sezóny 2023](https://environnement.brussels/media/15711/download)
- Kde to funguje: **Fotopostup výroby ze dvou květináčů (Záhrada.sk)** (2025): 2 terakotové květináče Ø 16-18 cm, otvor zalepit střepem a sanitárním silikonem, slepit okraji, zakopat 2 cm nad zem, 3-4 sazenice kolem, zakrýt miskou, namulčovat; na zimu vyjmout. Bez měření. ✅ [Felixová M., Záhrada.sk 15. 4. 2025](https://www.zahrada.sk/magazine/fotopostup-ako-si-doma-vyrobit-zavlazovacie-nadoby-olla/)
- Přenositelnost do Koryčan: Ano pro zeleninové a trvalkové záhony, školní zahradu (U07) a truhlíky; nezávisí na půdě ani sklonu. Nehodí se pod stromy a keře a na velké plochy.
- Rizika, co z toho neplyne: Úspora platí proti zálivce na povrch, ne proti kapkové závlaze. Póry se zanášejí solemi z tvrdé vody; sazenice prvních cca 4 týdny zalévat navíc; na zimu vyprázdnit nebo vyjmout 🤔. Neřeší vsak ani odtok, jen šetří vodu.
- Kč: svépomocně ze 2 květináčů Ø 16-18 cm + silikon: cena neověřena
- Povolení: 0
- Nedohledáno: měření v ČR nebo střední Evropě; interval dolévání (l/den) pro naše klima; trvanlivost přes zimu

### Z13 Suchomilný záhon (stepní, štěrkový): trvalky místo zalévaného trávníku a letniček (nové)
- Co to je: Záhon trvalek a trav ze stepních a suchých stanovišť v propustném substrátu s minerálním mulčem (štěrk 8-16 mm, 5-7 cm), který po zapojení nepotřebuje zálivku ani hnojení. Náhrada za zalévaný trávník nebo letničky - rostliny snášející sucho místo dodávání vody.
- Účinek šetření pitnou vodou (kvalitativne) ✅: Po roce zapojení bez zálivky (směs Blütensaum výslovně bez dozálivky); úspora v litrech ve zdroji není. Zdroj: [LWG Veitshöchheim, Staudenmischpflanzungen (vydání 2021)](https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf)
- Účinek omezení neproduktivního výparu / větru (hodnota) ✅: Údržba 2-6 min/m²/rok (podle směsi), kompost ani kůra se nepoužívají; minerální mulč 5-7 cm [2-6 min/m²/rok]. Zdroj: [LWG Veitshöchheim, Staudenmischpflanzungen (vydání 2021)](https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf)
- Účinek biodiverzita (kvalitativne) ✅: Kvetoucí směsi 10-35 druhů, písek jako hnízdiště samotářských včel. Zdroj: [LWG Veitshöchheim, Staudenmischpflanzungen (vydání 2021)](https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf)
- Kde to funguje: **Veitshöchheim, Bavorsko (LWG)** (1993-2021): zkušební a ukázkové plochy trvalkových směsí od 1993 (Silbersommer a nástupci), standard pro obce v Bavorsku; podobné srážky jako Koryčany 💻. Měřeno: pracnost údržby min/m²/rok. ✅ [LWG Veitshöchheim, Staudenmischpflanzungen (vydání 2021)](https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf)
- Přenositelnost do Koryčan: Dobrá na slunná, suchá místa: jižní svahy, pásy u chodníků, předzahrádky, okolí školy. Na pelozemích nutná výměna nebo zlehčení substrátu. Nehodí se na zamokřená a stinná místa (LWG má zvlášť stínové směsi).
- Rizika, co z toho neplyne: První rok zálivka a pletí; štěrkový mulč se v létě ohřívá (ochlazení jen z transpirace, nepřehánět). V ČR se prodávají směsi pod jinými názvy; cizí druhy volit s ohledem na invaznost 🤔.
- Kč: celkem: cena neověřena
- Povolení: 0
- Nedohledáno: české srovnání spotřeby vody trávník vs. stepní záhon; cena založení 2025-2026

### S01 Nádrž na dešťovou vodu (sud, IBC, podzemní jímka) s využitím (doplněno)
- Kde to funguje: **Kyselov u Vyššího Brodu (Český soběstačný dům)** (2022): zachycená dešťová voda po úpravě na sprchu a WC; Adapterra Awards 2022. Bez měření. ✅ [businessinfo.cz 2. 11. 2022](https://www.businessinfo.cz/clanky/adapterra-awards-2022-ocenila-sobestacny-dum-energeticky-pozitivni-skolu-i-protierozni-prvky-v-krajine/)
- Kde to funguje: **Německo** (2010): cca 1,8 mil. instalovaných nádrží, 60-65 tis. ročně (2009), 40 % do stávajících domů; 'úspora 110 mil. m³ pitné vody' je odhad výrobce. Měřeno: odhad, ne měření. ✅⏳ [Mall GmbH, studie trhu Regenwassernutzung 2010 (baulinks.de 9/2010)](https://www.baulinks.de/webplugin/2010/1798.php4)

### S02 Odpojení dešťových svodů od kanalizace, svedení na pozemek (doplněno)
- Účinek zpomalení odtoku (hodnota) ✅: Svedení ze zpevněných ploch na zeleň snížilo modelovaný odtok ze zpevněných ploch o 30 % (3 zahrady, Leeuwarden); na jílu se voda hromadí na povrchu [30 % odtoku ze zpevněných ploch]. Zdroj: [Lakhi N. 2025, Open Universiteit (diplomová práce)](https://research.ou.nl/en/studentTheses/the-impact-of-greening-measures-for-private-gardens-on-flood-prev/)
- Rizika, co z toho neplyne: Na jílu (HSP D) se voda u domu hromadí; dodržet odstupy z ČSN 75 9010 a vést vodu do Z01/Z10.
- Nedohledáno: typ kanalizace v Koryčanech; cena

### S04 Světlá střecha a plochy (albedo, cool roof) (doplněno)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Světlý asfalt (albedo 0,12-0,16 vs. 0,08): povrch o 4-5,5 °C chladnější v nejteplejší fázi dne; radiační teplota pro chodce o 0,6 °C vyšší (v rámci nejistoty) - pro lidi na ulici bez zlepšení (Köniz 2025) [4-5.5 °C povrch vozovky]. Zdroj: [Grolimund + Partner / ASTRA / BFH 2025](https://www.koeniz.ch/public/upload/assets/24417/260422%20faktenblatt_auswertung_pilotprojekt_waldeggstrasse.pdf)
- Kde to funguje: **Köniz (Bern), Waldeggstrasse** (2025): pilot ASTRA: světlé kamenivo v asfaltu, měření povrchu, vzduchu a globe teploty červen-červenec 2025. Měřeno: povrch -4 až -5,5 °C; globe +0,6 °C. ✅ [Grolimund + Partner / ASTRA / BFH 2025](https://www.koeniz.ch/public/upload/assets/24417/260422%20faktenblatt_auswertung_pilotprojekt_waldeggstrasse.pdf)
- Kde to funguje: **Aarau** (2022): město světlé vozovky odmítlo z finančních a ekologických důvodů, preferuje zeleň. Bez měření. ✅ [Stadt Aarau, odpověď na dotaz P. Benze 19. 9. 2022](https://www.aarau.ch/public/upload/assets/18407/2022-51%20Beantwortung%20Anfrage%20Pascal%20Benz%20%28FDP%29%2C%20Einsatz%20tempor%C3%A4rer%20Sonnensegel%20in%20Aarau.pdf)
- Rizika, co z toho neplyne: Na střeše ano; na chodníku a náměstí odraz vadí chodcům a povrch chladí jen sebe. Není náhrada stromů.
- Nedohledáno: cena reflexního nátěru 2025-2026

### S05 Šedá voda ze sprchy a umyvadel na zálivku (a WC) (nové)
- Co to je: Lehce znečištěná voda ze sprchy, vany a umyvadel se jímá, přefiltruje (u WC se čistí) a použije na zálivku okrasné zeleně nebo splachování. V létě je to jediná 'dešťová voda', která teče každý den, i když neprší.
- Účinek šetření pitnou vodou (hodnota) ✅: Úspora pitné vody na zahradu 33-59 % (32-39 m³/rok na dům); 3 rodinné domy, podzemní kapková závlaha trvalek a ovocných stromů, max. 10 mm/den, v zimě vypnuto [33-59 % pitné vody na zálivku]. Zdroj: [Byrne, Dallas, Anda, Ho 2020](https://www.mdpi.com/2073-4441/12/8/2310)
- Účinek šetření pitnou vodou (hodnota) ✅: Bytové domy Berlín: recyklace šedé vody snižuje spotřebu pitné vody o cca 30 %, s pračkou, zálivkou a chlazením až 60 % [30-60 % spotřeby pitné vody]. Zdroj: [IVV immobilien vermieten & verwalten 5/2026](https://www.vermieter-ratgeber.de/sites/default/files/public/data-fachartikel/IVV_2026_05_Vier-Fragen-an-Dipl_-Ing_-Erwin-Nolde_40-41.pdf)
- Kde to funguje: **Fremantle, Západní Austrálie** (2020): 3 rodinné domy, přímé odklonění šedé vody do podzemní kapkové závlahy; 12 měsíců monitoringu. Měřeno: úspora pitné vody na zahradu 33-59 %. ✅ [Byrne, Dallas, Anda, Ho 2020](https://www.mdpi.com/2073-4441/12/8/2310)
- Kde to funguje: **Berlín-Pankow** (2025): 2 novostavby bytového družstva EWG s recyklací šedé vody (sprcha, vana; v jedné i pračka + rekuperace tepla); úspora 600 a 1 200 m³ pitné vody za rok 2025. Měřeno: spotřeba pitné vody. ✅ [IVV immobilien vermieten & verwalten 5/2026](https://www.vermieter-ratgeber.de/sites/default/files/public/data-fachartikel/IVV_2026_05_Vier-Fragen-an-Dipl_-Ing_-Erwin-Nolde_40-41.pdf)
- Kde to funguje: **Praha 9, ZŠ Českobrodská** (2022): voda z umyvadel a sprch po úpravě na splachování WC, dešťová voda v retenčních nádržích na zálivku (Adapterra Awards 2022). Bez měření. ✅ [businessinfo.cz 2. 11. 2022](https://www.businessinfo.cz/clanky/adapterra-awards-2022-ocenila-sobestacny-dum-energeticky-pozitivni-skolu-i-protierozni-prvky-v-krajine/)
- Přenositelnost do Koryčan: Technicky ano u rodinného domu při rekonstrukci koupelny; smysl hlavně tam, kde v létě vyschne dešťová nádrž. Ekonomicky slabé na úrovni jednoho domu (Austrálie: 4-5x dražší než pitná voda).
- Rizika, co z toho neplyne: V ČR zatím bez závazných hygienických limitů (SZÚ 2022); k zálivce jen lehká šedá voda bez kuchyně a pračky; soli a tenzidy degradují půdu, mikroplasty z pračky, patogeny přežívají ve skladované vodě. Nešetří vodu v krajině, jen pitnou. Filtr vyžaduje údržbu.
- Kč: celkem: cena neověřena
- Povolení: 1 (🤔 1-2: změna vnitřní kanalizace; u WC nepitný rozvod podle ČSN 75 6780; ověřit u stavebního a vodoprávního úřadu)
- Nedohledáno: měření na rodinném domě ve střední Evropě; množství šedé vody z RD (l/os/den) z primárního zdroje; cena technologie pro RD 2026

### S06 Dešťová voda na splachování WC (nepitný rozvod v domě nebo škole) (nové)
- Co to je: Podzemní nádrž (S01) napojená přes filtr a čerpadlo na oddělený rozvod k WC (případně pračce) s automatickým dopouštěním pitné vody. Na rozdíl od zálivky bere vodu každý den celý rok, takže nádrž má smysl i v zimě a při každém dešti má volný objem.
- Účinek šetření pitnou vodou (hodnota) ✅: WC = cca 20-30 % spotřeby domácnosti: Praha 2020 splachování 26 l ze 112 l/os/den; Bielsko-Biała cca 30 %; ČR 2023 celkem 86,7 l/os/den [20-30 % spotřeby pitné vody]. Zdroj: [MČ Praha 14, leták Voda (2022)](https://www.praha14.cz/app/uploads/sites/4/2022/06/Letak-Voda-2022.pdf); [Madzia M. a kol. 2019](https://www.jeeng.net/Reduction-of-Treated-Water-Use-through-Application-of-Rainwater-Tanks-in-Households,112495,0,2.html); [ČSÚ 2. 5. 2024](https://csu.gov.cz/produkty/domacnosti-vodou-nadale-setri-v-prumyslu-jeji-spotreba-mirne-roste)
- Účinek šetření pitnou vodou (vzorec) 🤔: Úspora pitné vody = osoby × 17-26 l/den = 6-9,5 m³/os/rok; 4 osoby 25-38 m³/rok 🤔 odvozeno. Zdroj: [MČ Praha 14, leták Voda (2022)](https://www.praha14.cz/app/uploads/sites/4/2022/06/Letak-Voda-2022.pdf); [ČSÚ 2. 5. 2024](https://csu.gov.cz/produkty/domacnosti-vodou-nadale-setri-v-prumyslu-jeji-spotreba-mirne-roste)
- Účinek šetření pitnou vodou (hodnota) ✅: Nádrž 0,25 m³/os a střecha 30 m²/os nahradí téměř 80 % vody na splachování (přes 10 m³/os/rok); nomogram, Bielsko-Biała (vlhčí klima než Koryčany) [80 % vody na splachování]. Zdroj: [Madzia M. a kol. 2019](https://www.jeeng.net/Reduction-of-Treated-Water-Use-through-Application-of-Rainwater-Tanks-in-Households,112495,0,2.html)
- Účinek zadržení objemu (vzorec) ✅: Jako S01; nádrž se průběžně vyprazdňuje, při dešti má volný objem. Zdroj: [Tabulka součinitelů odtoku (tzb-info, reprodukce ČSN)](https://www.tzb-info.cz/docu/tabulky/0000/000088_help.html)
- Kde to funguje: **Kyselov u Vyššího Brodu (Český soběstačný dům)** (2022): dům bez přípojek; zachycená dešťová voda po úpravě na sprchu a WC (Adapterra Awards 2022, Náš domov). Bez měření. ✅ [businessinfo.cz 2. 11. 2022](https://www.businessinfo.cz/clanky/adapterra-awards-2022-ocenila-sobestacny-dum-energeticky-pozitivni-skolu-i-protierozni-prvky-v-krajine/)
- Kde to funguje: **Ořechov u Brna** (2022): obec: 4 retenční nádrže na dešťovou vodu, 3 tůně, suchý poldr, 7 ha mokřad (Adapterra Awards 2022, Volná krajina); využití nádrží na WC a objemy ve zdroji neuvedeny. Bez měření. ✅ [ceskestavby.cz 2. 11. 2022](https://www.ceskestavby.cz/clanky/sobestacny-dum-i-energeticky-pozitivni-skola-podivejte-se-vitezne-projekty-proti-zmenam-klimatu-31347.html)
- Kde to funguje: **Německo (celá země)** (2010): cca 1,8 mil. instalovaných nádrží na dešťovou vodu, 60-65 tis. ročně, 40 % do stávajících domů (studie trhu výrobce). Měřeno: odhad výrobce, ne měření. ✅⏳ [Mall GmbH, studie trhu Regenwassernutzung 2010 (baulinks.de 9/2010)](https://www.baulinks.de/webplugin/2010/1798.php4)
- Přenositelnost do Koryčan: Ano u novostaveb a rekonstrukcí RD; u veřejných budov (škola, úřad) ještě lépe, protože WC je tam hlavní spotřeba 🤔. Nehodí se tam, kde není místo na nádrž, nebo malá střecha + velká domácnost.
- Rizika, co z toho neplyne: V suchém létě 5 m³ nádrž pro 4 osoby bez deště dojde za 1-3 týdny 🤔, pak dopouští pitná voda. Nešetří vodu v krajině, šetří pitnou a odlehčí kanalizaci. NZÚ 2026 podporuje jen v kombinaci se zateplením nebo zdrojem energie.
- Kč: podzemní nádrž 5000 l vč. šachty, bez montáže (viz S01): 50830 Kč; čerpadlo, filtr, nepitný rozvod, montáž: cena neověřena
- Povolení: 1 (nepitný rozvod označený podle ČSN 75 6780, ochrana proti zpětnému toku; ohlášení 🤔; souhlas provozovatele vodovodu 💻)
- Nedohledáno: měření na RD ve střední Evropě; podíl WC na spotřebě v ČR z primárního zdroje (SOVAK/ČSÚ); cena technologie 2026
<!-- RESERSE-END -->
