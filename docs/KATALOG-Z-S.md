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
