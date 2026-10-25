# Katalog opatření - kvantifikace sekcí U (veřejný prostor obce) a P (orná půda, pro vlastníky)

Verze 18. 10. 2026 (oprava U05 večer 18. 10.). Doplňuje KATALOG.md a KATALOG-Z-S.md. Značky: ✅ ověřeno online 18. 10. 2026, ⏳ starší než 12 měsíců, 📄 citace z druhé ruky, 🤔 odhad/dopočet, 💻 z paměti. Ceny jen se zdrojem a datem (rozhodnutí 18. 10.); kde zdroj není, "cena neověřena".

## 0. Společné vstupy

### Eroze (USLE) - vstupy pro výpočetní jádro
- **Protierozní kalkulačka VÚMOP** ✅ https://kalkulacka.vumop.cz/ (pro MŽP k vyhlášce 240/2021 Sb.; faktory K, R, LS, C, P nad LPIS; normál 1991-2020). Manuál ✅⏳ (Novotný, Holub, Mistr, Juřicová, Drozen, 2017) https://kalkulacka.vumop.cz/docs/manual.pdf
- **Přípustná ztráta půdy Gp** (t/ha/rok, mělké půdy < 30 cm / ostatní) ✅: od 1. 7. 2022 3 / 12; **od 1. 7. 2026 2 / 9**; od 1. 7. 2030 1 / 5.
- **Faktor C** (manuál tab. 1.11, dílčí hodnoty po pěstebních obdobích) ✅: kukuřice na zrno do zorané půdy 0,70/0,90/0,70/0,35/0,70/0,40; obilniny a olejniny po obilninách 0,65/0,70/0,45/0,08/0,25/0,04; cukrovka a brambory 0,65/0,80/0,65/0,30/0,70; **travní porost 0,01**; víceleté pícniny 0,015.
- **Faktor P** (manuál tab. 1.12, 1.13) ✅: vrstevnicové obdělávání podle sklonu 0-4° 0,6; 4-6° 0,7; 6-8° 0,8; 8-10° 0,9; > 10° 1,0. Hrázkování 0-4° 0,25 ... 12-14° 0,5. Pásové střídání (Janeček a kol. 2012, ČZU ✅⏳, tab. 1.12, sklon 2-7 / 7-12 / 12-18 / 18-24 %): okopaniny + víceleté pícniny 0,30 / 0,35 / 0,40 / 0,45; okopaniny + ozimy 0,50 / 0,60 / 0,75 / 0,90; max. šířka pásu 40 / 30 / 20 / 20 m. Zdroj: https://storm.fsv.cvut.cz/data/files/p%C5%99edm%C4%9Bty/YPEO/Metodika_PEO_novelizace%20upravene%2025_1_2012.pdf
- Jádro aplikace: A = R × K × LS × C × P; změna opatření = změna C (plodina/zatravnění) a P (vrstevnice, pásy) a zkrácení L (pás přerušuje svah). Výsledek ukazovat jako rozsah a porovnat s Gp.

### Součinitele odtoku C (intravilán)
- Jako v KATALOG-Z-S.md kap. 0 (tabulka tzb-info ✅): střecha 1,0; asfalt/beton 0,7-0,9; dlažba s pískovými spárami 0,5-0,7; štěrk 0,3-0,5; trávník 0,05-0,15.

### Regulovaný odtok (návrhová praxe)
- Brno, Nařízení č. 14/2024 (Brněnské stavební předpisy) ✅: § 30 regulovaný odtok z pozemku **max. 3 l/s/ha** (min. 0,5 l/s), přetížení retence max. 1x za 5 let, srážková voda přednostně k vegetačním prvkům; § 46 vegetační střechy na střechách do 20° nad 20 m². TSK Praha, TP odvodnění komunikací 06/2025 ✅: totéž 3 l/s/ha; zasakovací průleh svahy 1:3, hladina do 0,3 m. Pro Koryčany nezávazné, ale je to standard dobré praxe pro U01-U04.

### Ceny - zdroje
- **ÚÚR/RTS, Průměrné ceny dopravní a technické infrastruktury obcí, aktualizace 2025** ✅ (kap. 3 kanalizace, 8 komunikace, 9 zeleň): https://www.uur.cz/media/4jebc4v3/09-zelen-ceny-ti-2025.pdf , https://www.uur.cz/media/y1ulzdvg/08-komunikace-ceny-ti-2025.pdf , https://www.uur.cz/media/xa3pha4j/03-kanalizace-ceny-ti-2025.pdf . Pozn.: celek ÚÚR 2025 neobsahuje vodní hospodářství (poldry, hráze).
- **NOO MŽP (Náklady obvyklých opatření) verze 2024** ✅⏳ (platné od 1. 11. 2023, bez DPH): https://mzp.gov.cz/system/files/2025-04/O610-NPO_POPFK_vyzva_c_5_2024_priloha_c_7_NOO-20240614.pdf . Novější: NOO 2025_2 (od 1. 7. 2025) https://mzp.gov.cz/system/files/2025-07/O610-NPO_POPFK_vyzva_c_2_2025_priloha_c_7_NOO-20250701.pdf a **NOO 2026** (od 1. 11. 2025, XLSX) https://mzp.gov.cz/system/files/2026-03/OAZK-NOO_2026-20261803_0.xlsx - doplnit hodnoty.

### Financování pro obec, spolky a FO (stav 18. 10. 2026)
- **OPŽP 105. výzva (opatření 1.3.4, srážková voda v intravilánu)** ✅: vsakování, retence, akumulace, zelené střechy, propustné povrchy; žadatelé obce, školy, spolky aj.; podpora 70 % (85 % propojené systémy MZI, 30 % vybrané); příjem 17. 6. - **17. 12. 2026**; 200 mil. Kč. https://opzp.cz/files/documents/storage/2026/06/02/1780378967_Text%20výzvy%20-%20105.%20výzva.pdf **Otevřená.**
- **AOPK OPŽP ZMV 17. výzva (projekty do 200 000 EUR)** ✅: tůně, MVN, revitalizace (1.3.1.1), vegetační prvky a protierozní opatření (1.3.1.2), sídelní zeleň (1.3.1.4), eliminace odvodnění (1.3.1.5); jednorázové částky podle NOO; min. 250 000 Kč bez DPH; žadatelé obce, spolky, FO (FO ne pro sídelní zeleň); max. 100 %; **znovuotevření 20. 10. - 3. 11. 2026**. https://dotace.aopk.gov.cz/-/aopk-opzp-zmv-17-vyzva
- **OPŽP 104. a 73. výzva (1.3.1 / 1.3.11, velké projekty)** ✅: tůně a MVN až 100 % (MVN 60-85 %), vegetační prvky 80 % (ÚSES 100 %), eliminace odvodnění 100 %; obě **uzavřeny 25. 9. 2026**; čekat další kolo.
- **PPK B 2026 (AOPK)** ✅: výzva 1/2026 péče o biotopy (seč, pastva, obnova tůní), výzva 2/2026 navíc vytváření krajinných prvků (výsadby, meze, nové tůně mimo zastavěné území); žadatelé FO i PO vč. obcí a spolků; max. **250 000 Kč/projekt**, až 100 %; obě **uzavřeny**; 🤔 další kolo prosinec 2026 / květen 2027. https://dotace.aopk.gov.cz/-/vyzva-ppk-b-2-pro-rok-2026
- **NPO POPFK**: program 2022-2025, pro rok 2026 **žádná výzva** ✅ https://dotace.aopk.gov.cz/npo-popfk . V katalogu uvádět jako ukončený.
- **Agrolesnictví (SZP 2023-2027, MZe metodika 2026)** ✅: zavádění 4 353 EUR/ha (cca 105 500 Kč), péče 754 EUR/ha/rok po 5 let; přesně 100 ks/ha, výška min. 120 cm, > 50 % lesních dřevin, pásy 1-10 m, rozestup 10-100 m, min. 0,5 ha. Žadatel je zemědělec (uživatel DPB), ne vlastník. https://mze.gov.cz/public/portal/mze/-a91928---kRzRGYfn/metodika-agrolesnictvi-2026

## U. Veřejný prostor obce

### U01 Uliční stromořadí s vsakovacími rabátky
- Návrhové hodnoty ✅ (IPR Praha, Manuál tvorby veřejných prostranství, kap. D.2.1): nezakrytá/propustná plocha u stromu **min. 6 m²**; prokořenitelný prostor **min. 16 m², hloubka min. 0,8 m** (🤔 cca 12,8 m³ substrátu). Brno 14/2024 ✅: výsadbový pás min. 0,8-1,5 m podle šířky ulice; parkoviště 1 strom na 8 stání.
- Účinek CH: stín -11 až -25 °C na povrchu, vzduch v zeleni až -5 °C v horku (EPA 2008 ✅⏳, viz Z06). Účinek I, Q: rabátko s 6 m² propustné plochy a strukturním substrátem zadrží řádově 🤔 1-3 m³ na strom (bez českého zdroje, zobrazit jako odhad). Odvodnění ulice do rabátka = trávník C 0,1 místo asfaltu 0,8.
- Kč ✅ (ÚÚR/RTS 2025): strom s balem 250-350 cm 6 100 Kč/ks, do 200 cm 2 835 Kč, prostokořenný 1 775 Kč. Kompletní rabátko se strukturním substrátem: cena neověřena.
- Financování: OPŽP 105 (MZI 70-85 %) ✅; AOPK ZMV 1.3.1.4 sídelní zeleň ✅.
- Povolení: 1-2 (sítě, komunikace).

### U02 Propustné povrchy parkovišť, chodníků, dvorů
- Účinek I: rozdíl C (asfalt 0,8 -> dlažba s pískovými spárami 0,6, zatravňovací tvárnice 0,3). Parkoviště 1 000 m², déšť 20 mm: 16 m³ odtoku -> 6 m³ s tvárnicemi; za rok (570 mm) 456 m³ -> 171 m³.
- Kč ✅ (ÚÚR/RTS 2025): zatravňovací tvárnice 1 136 Kč/m²; zámková dlažba 8 cm vč. podkladu 2 240 Kč/m²; asfalt celá konstrukce 1 411 Kč/m²; vsakovací boxy pod parkovištěm 500 m² 157 040 Kč, 1 000 m² 266 330 Kč.
- Financování: OPŽP 105 ✅ (některé úpravy povrchů jen 30 %).
- Povolení: 1-2.

### U03 Zasakovací pásy a průlehy podél komunikací
- Návrh ✅ (TSK Praha 06/2025): svahy 1:3 (max. 1:2), hladina do 0,3 m, regulovaný odtok 3 l/s/ha. Vyprázdnění do 72 h (ČSN 75 9010 ✅).
- Účinek I, Q, R: objem = délka × průřez; průleh 100 m × 1 m² = 100 m³ = 20 mm ze 0,5 ha komunikace.
- Kč ✅⏳ (NOO 2024): travnaté protierozní průlehy a meze s terénními úpravami 200 Kč/m².
- Financování: OPŽP 105 ✅.

### U04 Retence a zasakování vody z veřejných budov (škola, úřad)
- Účinek R, I, W: jako S01+S02+Z10 ve velkém; škola se střechou 1 500 m²: 20 mm = 30 m³, rok 855 m³.
- Kč ✅ (ÚÚR/RTS 2025): podzemní ŽB retenční nádrž 18 500-28 500 Kč/m³. Plastové nádrže viz KATALOG-Z-S S01.
- Financování: OPŽP 105 ✅ (70 %; akumulace na zálivku hřišť 30 %).
- Povolení: 1-2.

### U05 Obecní tůň, mokřad, obnova návesní nádrže
- Provedení: SPPK B02 001:2014 ✅ (viz Z02); právo: nad 300 m² ohlášení (§ 15b vodního zákona ✅), s hrází = vodní dílo (povolení 2).
- Účinek R: objem = plocha × průměrná hloubka (0,8-1,0 m); 500 m² tůň cca 400 m³. CH, B: kvalitativně.
- Kč: NOO 2024 ✅⏳ tůň strojně, materiál v lokalitě **330 Kč/m²** hladiny (odvoz do 2 km 410, nad 2 km 480), + 15 000 Kč/lokalitu; odbahnění 430 Kč/m³. Realizace: tůně Grenzteich 2024, 1 250 m², 98 875 Kč (🤔 79 Kč/m²) ✅ https://dotace.aopk.gov.cz/-/tune-grenzteich ; mokřad Malá Vrbka (SPÚ, 2024), 3 tůně, 610 473 Kč vč. DPH ✅. Poldr a hráz: **cena neověřena** (údaj "zátopa 400-600 Kč/m², hráz 2 250 Kč/m³" připsaný ÚÚR/RTS 2025 se při kontrole 18. 10. 2026 v dokumentu nenašel a byl vyřazen).
- Financování: AOPK ZMV 1.3.1.1 (20. 10. - 3. 11. 2026) ✅; PPK B (obnova tůní, max. 250 tis.) ✅; OPŽP 1.3.1/1.3.11 další kolo.

### U06 Mozaiková seč, květnaté louky na obecních plochách
- Standard: **SPPK D02 004 Sečení** ✅ (kód doložen přes SPPK C02 007 a Chytrá a kol. 2024; PDF neotevřen 📄): ponechat **10-20 % plochy neposečené**, posekat nejpozději do roka. Praha MHMP 2019 ✅⏳: výška seče 12 cm (po suchu 14), louky 10-15 cm, neseče se nad 26 °C, mozaika 20-30 %.
- Účinek E, CH, B: kvantifikace vlhkosti/teploty v ČR nedohledána; B doložena (Chytrá a kol. 2024, Příroda 44 ✅: nepravidelně kosené plochy o 20 % druhově chudší, nekosené -34 %). Zobrazit E a CH kvalitativně.
- Kč ✅⏳ (NOO 2024): seč lehkou mechanizací 17 425 Kč/ha, křovinořezem 35 000 Kč/ha; zatravnění regionální směsí 86 600 Kč/ha. ÚÚR/RTS 2025 ✅: trávník luční 40 Kč/m², parkový 63 Kč/m².
- Financování: PPK B.1 (seč bez mulčování) ✅ max. 250 tis.; jinak vlastní.

### U07 Školní zahrada jako ukázkový pozemek
- Skladba Z01-Z08 + M01-M06; účinky a ceny podle jednotlivých položek. Financování: OPŽP 105 (školy jsou žadatelé ✅), participativní rozpočet.

## P. Orná půda (vlastník: pachtovní smlouva N01 nebo vyjmutí N02)

### P01 Protierozní mez, zatravněný pás, biopás po vrstevnici
- Účinek ER, Q, I: pás přerušuje délku svahu L (zkrácení L v USLE) a má C 0,01. České měření (MŽP/TAČR, Centrum Voda, 17. 12. 2025 ✅): svah 11,3 %, čas do začátku odtoku při 0 % zatravnění 102 s, 25 % 141 s, 50 % 253 s, 100 % 461 s; rychlost odtoku zpomalena 5-6x; retence 2m pásu po 20 min deště téměř vyčerpána - **úzký pás funguje na začátku deště, ne na dlouhý příval**. % snížení ztráty půdy z českého měření nedohledáno; použít P a L z USLE.
- Návrh ✅ (VÚMOP, Dumbrovský a kol. 2021): max. šířka pásu plodiny 40 m; DZES 5 (2026) ✅: ochranný pás min. 3 m, doporučeno 22 m.
- Kč ✅⏳ (NOO 2024): meze a průlehy s terénními úpravami 200 Kč/m²; zatravnění 86 600 Kč/ha. Ušlý výnos z pásu: cena neověřena.
- Financování: AOPK ZMV 1.3.1.2 ✅; PPK B.3 (obnova mezí, mimo zastavěné území) ✅; OPŽP 1.3.1 další kolo.
- Povolení: 0-1 (změna kultury v LPIS přes uživatele DPB).

### P02 Zasakovací průleh
- Návrh: ČSN 75 9010 (kf, 72 h) ✅; VÚMOP R-Software ✅ návrhový déšť N = 10, 60 min; ustálená infiltrace TTP 1,5-23 mm/min.
- Účinek I, Q, ER: objem průlehu × délka; odvedení do zatravněné údolnice (P05).
- Kč ✅⏳ NOO 2024: 200 Kč/m². Financování: AOPK ZMV 1.3.1.2 ✅. Povolení: 1.

### P03 Rozdělení lánu, pásové střídání, orientace po vrstevnici
- Účinek ER (USLE P): vrstevnicové obdělávání P 0,6 (0-4°) až 1,0 (> 10°) ✅; pásové střídání okopaniny + pícniny P 0,30-0,45, okopaniny + ozimy 0,50-0,90 ✅⏳ (Janeček 2012); max. délka po spádnici 120 / 60 / 40 m podle sklonu.
- Kč: organizační, 0 Kč; podmínka v pachtovní smlouvě (N01).

### P04 Půdoochranné technologie (bezorebné setí, strip-till, meziplodiny, strniště)
- Účinek I, Q, ER ✅ (Vopravil, VÚMOP, polní simulátor deště, MZe 22. 10. 2025): orba - odtok od 69 s, infiltrace 27,4 mm, odtok 9,3 mm, ztráta 6,97 t/ha; setí do ozimého žita - 1,95 t/ha; **strip-till do travního porostu - infiltrace 32,2 mm, odtok 4,5 mm, ztráta 0,24 t/ha** (🤔 odtok -52 %, smyv -97 % proti orbě). https://mze.gov.cz/public/portal/mze/-a84150---QEFagIDj/prezentace-z-22.-10.-2025-vliv-pudy-a-jejiho-stavu-na-vodni-rezim-krajiny
- Povinné minimum: **DZES 5 (2026)** ✅: na SEO plodiny s nízkým ochranným vlivem (kukuřice, brambory, řepa, slunečnice, sója) zakázány nad 2 ha; na MEO jen s půdoochrannou technologií (pásy, setí do zbytků, strip-till, podsev, úzké řádky kukuřice max. 0,5 m, organická hmota min. 25 t/ha...). https://www.mze.gov.cz/public/portal/mze/-a81614---9i2f6ULe/metodicka-prirucka-k-plneni-standardu-dzes-5-dobry-zemedelsky-a-environmentalni-stav-pudy-pro-jarni-osevy-roku-2026-a-nasledujici-obdobi . Pro katalog: vlastník může ve smlouvě požadovat víc než DZES.
- Kč: 0 Kč pro vlastníka (smluvní); financování: zemědělec (AEKO, DZES), ne vlastník.

### P05 Zatravnění údolnic a drah soustředěného odtoku
- Návrh ✅ (Dumbrovský a kol. 2021): min. šířka zatravněné údolnice a souvratě **20 m**. Příklad plánu opatření (Vedrovice ✅): údolnice 20 m × 315 m, vhodnost z vrstvy LPIS/VÚV.
- Účinek ER, Q, I: C 0,01 v dráze odtoku; kvantifikace účinku nedohledána (jen návrh).
- Kč ✅⏳ NOO 2024: zatravnění 86 600 Kč/ha (údolnice 20 × 300 m = 0,6 ha = cca 52 000 Kč). Financování: AOPK ZMV 1.3.1.2 ✅.

### P06 Trvalé zatravnění / zalesnění svažitých pozemků
- Účinek ER: C z 0,65-0,90 (plodiny) na 0,01 (TTP) = snížení ztráty půdy řádově 50-90x podle USLE ✅ (hodnoty C z manuálu kalkulačky). I, E: kvalitativně.
- Kč ✅⏳ NOO 2024 zatravnění 86 600 Kč/ha. Ušlý pachtovní výnos: cena neověřena.
- Povolení: 1 (LPIS kultura; zalesnění = změna druhu pozemku, souhlas orgánu ZPF 💻).

### P07 Větrolam
- Návrh ✅ (VÚMOP, Doležal, Podhrázská a kol., Řízení rizika větrné eroze, 2016/2017): za olistěným větrolamem (porozita 10 %) rychlost větru v 50 m cca 40 %, ve 150 m cca 70 % původní; neolistěný 80 % / 90 %; účinný dosah max. 250 m = **10-17x výška**; ochranná zóna 20-30 H závětrně, 5-10 H návětrně; funkční výška min. 12-15 m; 6-8 řad stromů + 4 řady keřů. https://agronavigator.cz/sites/default/files/2025-04/Nmet%252B-%252BMetodika%252B%25C5%2599%25C3%25ADzen%25C3%25AD%252Bv%25C4%259Btrn%25C3%25A9%252Beroze.pdf . MZe 17. 5. 2022 ✅: nový větrolam šířka 7-20 m (pod 5 m neplní funkci), rozestupy 350-600 m, min. 3 m od hranice.
- Účinek E: vítr -60 % v 50 m ✅; výpar, vlhkost, výnos v ČR nekvantifikovány (jen Dufková 2007 ✅⏳, jedno měření, vlhkost půdy +102 %). V aplikaci ukazovat **plochu chráněnou** (délka × 10-17 H), ne mm.
- Kč: realizace Písková Lhota 2025 ✅: 1 408 m², 4 řady, 198 270 Kč (🤔 141 Kč/m²). NOO 2024 ✅⏳ strom s balem 5 900-6 490 Kč. ÚÚR/RTS 2025 ✅ prostokořenný 1 775 Kč.
- Financování: AOPK ZMV 1.3.1.2 ✅; PPK B.3 (liniové výsadby, max. 250 tis.) ✅.

### P08 Polní cesta s doprovodnou zelení a zasakovacím příkopem
- Kombinace P01 + P07 + C01; účinky podle složek. Kč: cesta podle konstrukce (ÚÚR/RTS 2025 kap. 8, bez konkrétní položky neuvádím), výsadba viz P07, průleh 200 Kč/m² ✅⏳.
- Financování: OPŽP 1.3.1 (další kolo), KoPÚ (N04) - polní cesty jsou typická společná zařízení 💻.

### P09 Agrolesnictví
- Účinek CH, E ✅ (Weger, Lojka a kol., VÚK + ČZU, Senát 20. 5. 2026): průměrná teplota -0,2 až -0,8 °C/rok, v horkých dnech maxima přízemního vzduchu a povrchu půdy -4 až -5 (až 10) °C, tropické dny -1/3, vítr ve 4 m -50 %; záplavové pokusy Šardice 2023-2025 (72 mm/h): odtok 0 %, zasáknutí 99 % v agrolesnickém systému. https://bioeconomy.czu.cz/dl/156269?lang=cs . Vlhkost půdy nekvantifikována.
- Dotace ✅ (MZe 2026): 4 353 EUR/ha zavedení + 754 EUR/ha/rok 5 let; podmínky výše. Žadatel je zemědělec - pro vlastníka cesta přes N01 nebo vlastní hospodaření po N02.
- Standard: SPPK C02 003:2014 ✅.

### P10 Regulace / přerušení melioračního odvodnění
- Jak zjistit drenáž ✅: žádost SPÚ o informaci o výskytu melioračních staveb (bezplatně, k.ú. + parcela, epodatelna@spu.gov.cz) https://portal.gov.cz/sluzby-vs/S43666 ; ISMS meliorace.vumop.cz (vrstvy "Stavby dle ZVHS"), LPIS vrstva POZ (stav cca 1992) ✅ (Zajíček a kol., VÚMOP 2021). Podrobné odvodnění patří od 1991 vlastníkovi pozemku; 40 % vlastníků o něm neví; dokumentace dohledatelná v 50-60 %.
- Účinek R, I ✅ (tamtéž, tab. 3, odhad snížení odtoku): regulační opatření na drenáži **50-90 %**, snížení intenzity odvodnění 50-75 %, zasakovací drén 50-100 %, lokální eliminace 25-75 %. https://agronavigator.cz/sites/default/files/2025-04/HOZ_metodika_publ.pdf
- Kč: NOO 2024 ✅⏳ rušení odvodnění 1 650 Kč/m². Financování: AOPK ZMV 1.3.1.5 eliminace odvodnění (až 100 %) ✅; OPŽP 1.3.1 další kolo.
- Povolení: 1-2.

### P11 Remízek, drobná plocha zeleně
- Účinek B, E, CH kvalitativně. Kč ✅ ÚÚR/RTS 2025 sazenice 1 775-6 100 Kč/ks. Financování: PPK B.3 ✅, AOPK ZMV 1.3.1.2 ✅.

### P12 Zvyšování organické hmoty v půdě
- Účinek I, R: Hladík (VÚMOP) ✅ uvádí "1 % organické hmoty = +35 000 l/ha retence" - bez citovaného zdroje, v aplikaci jen jako 🤔 s označením. Vopravil 2025 ✅ ukazuje infiltraci podle stavu půdy (viz P04).
- Kč: 0 pro vlastníka (smluvní, N01).

## N. Nástroje vlastníka - doložené parametry

- **N01 Pachtovní smlouva** ✅ (OZ 89/2012 Sb.): § 2345 zemědělský pacht; § 2336 pachtýř pečuje jako řádný hospodář; § 2334 změna hospodářského určení jen se souhlasem propachtovatele; § 2347 pacht na dobu neurčitou - **výpovědní doba 12 měsíců**; pachtovní rok 1. 10. - 30. 9. Půdoochranné podmínky ve smlouvě: zákon výslovně neřeší, OZ je dispozitivní -> smluvně možné 🤔 (ověřit s právníkem; neověřený výklad).
- **N02 Vyjmutí z pachtu**: výpověď podle § 2347 (12 měsíců u doby neurčité); u smlouvy na dobu určitou podle smlouvy.
- **N04 Komplexní pozemkové úpravy** ✅ (zákon 139/2002 Sb., § 6 odst. 3): "Pozemkový úřad zahájí řízení o pozemkových úpravách vždy, pokud se pro to vysloví vlastníci pozemků **nadpoloviční výměry zemědělské půdy** v dotčeném katastrálním území." Formulář SPÚ ✅ https://spu.gov.cz/pozemkove-upravy/zadost-o-pozemkove-upravy-formular . Pro Koryčany: KoPÚ neproběhly - podpisová akce vlastníků je reálný nástroj.

## Nedohledal jsem (fáze 6)
- % snížení ztráty půdy mezí/pásem z českého měření (jen P faktory a časy do odtoku).
- Metodika zatravnění údolnic s prahem sběrné plochy a kvantifikovaným účinkem.
- Český kvantifikovaný vliv větrolamů na výpar, vlhkost, výnos.
- NOO 2026 hodnoty (XLSX).
- Cena stromového rabátka se strukturním substrátem 2025-26; metodika MZI MŽP.
- WMS adresa ISMS meliorace.vumop.cz.
- Vliv mozaikové seče na vlhkost/teplotu (ČR).
- Právní výklad k půdoochranným podmínkám v pachtu.
- Přesná % podpory v AOPK ZMV 17. výzvě (Příručka AOPK).
- Ceny poldru a hráze - dřívější údaj se v ÚÚR 2025 nepotvrdil, vyřazen. Údaje připsané "ÚÚR/RTS 2025 kap. 3" (ŽB nádrž, vsakovací boxy) při fázi 6 ověřit přímo v PDF.

---

<!-- RESERSE-START (generováno tools/build_katalog_md.py, needitovat ručně) -->
## Doplnění z rešerše dobré praxe (bloky B, A, C, D, 21.-22. 10. 2026)

Generováno z `data/opatreni.json` v0.9 (2026-10-22); podrobný rozbor a odkazy: `docs/KATALOG-RESERSE.md`. Uvedeny jen nové položky a kvantifikace, příklady, přenositelnost a rizika doplněné rešerší; původní text výše platí dál. Značky: ✅ ověřeno online, ✅⏳ zdroj starší 12 měsíců, 📄 citace, 🤔 odhad.

### U01 Uliční stromořadí s vsakovacími rabátky (doplněno)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Stromy v ulici: pocitová teplota -2,8 až -7,6 °C ve dne, +0,1 až +1,3 °C v noci; vzduch -0,4 až -2,1 °C (CzechGlobe/UPOL); stromy na jižním chodníku ulice V-Z důležitější než na severním (model Lee & Mayer 2019) [2.8-7.6 °C pocitově]. Zdroj: [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf); [Lee H. (Stuttgart), Mayer H. (Freiburg), DACH 2019](https://meetingorganizer.copernicus.org/DACH2019/DACH2019-24.pdf)
- Účinek zadržení objemu (vzorec) ✅⏳: Voda ze střech a chodníků do rabátka: V = napojená plocha × srážka, strop = objem substrátu × pórovitost (~30 % 🤔); Stockholm: 4 600 m² × 600 mm = 2,3 mil. l/rok. Zdroj: [Embrén B. (město Stockholm), The Stockholm System, prezentace TDAG 201](https://www.tdag.org.uk/uploads/4/2/8/0/4280686/22.06.15_the_stockholm_system_bjorn_embren.pdf)
- Účinek biodiverzita (kvalitativne) ✅: Stockholm: stromy vysazené s obvodem 30-35 cm měly po 8 letech 70-83 cm (bez kontrolního srovnání); Graz MUFUWU: střešní voda doplňuje zásobu i při malých deštích, zálivka v prvních letech nutná, retence vs. klasické rabátko nevyčíslena. Zdroj: [Embrén B. (město Stockholm), The Stockholm System, prezentace TDAG 201](https://www.tdag.org.uk/uploads/4/2/8/0/4280686/22.06.15_the_stockholm_system_bjorn_embren.pdf); [Zimmermann a kol. (3](https://nachhaltigwirtschaften.at/resources/sdz_pdf/schriftenreihe-2024-39-mufuwu.pdf)
- Kde to funguje: **Olomouc** (2018): měření v ulicích, CzechGlobe/UPOL 2018. Měřeno: pocitová teplota v uličním kaňonu. ✅ [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf)
- Kde to funguje: **Stockholm** (2002-2015): cca 2 000 stromových míst přestavěno na strukturální substrát (drcená žula 90-150 mm, od 2013 biouhel), voda ze střech a chodníků vedena do rabátek. Měřeno: obvod kmene po 8 letech; objem vody do systému. ✅⏳ [Embrén B. (město Stockholm), The Stockholm System, prezentace TDAG 201](https://www.tdag.org.uk/uploads/4/2/8/0/4280686/22.06.15_the_stockholm_system_bjorn_embren.pdf)
- Kde to funguje: **Graz, Leonhardgürtel** (2021-2024): 7 nových stromů + 4 sanované kaštany v tělesech 60 cm; měření půdní vody, toku mízy, přírůstu a přítoku/odtoku 2022-2023 (projekt MUFUWU, BMK). Měřeno: půdní voda, tok mízy, přírůst kmene. ✅ [Zimmermann a kol. (3](https://nachhaltigwirtschaften.at/resources/sdz_pdf/schriftenreihe-2024-39-mufuwu.pdf)
- Kde to funguje: **Vídeň Schönbrunn (HBLFA) + Graz Gradnerstraße + Seestadt** (2019-2024): lysimetry a dva uliční pokusy se strukturálními substráty 2019-2024; závěr: chyby při stavbě výrazně snižují hydrologický výkon, zásobování stromu plánovat spolu s retencí. Měřeno: lysimetr (čísla v abstraktu nejsou). ✅ [HBLFA Schönbrunn (Roth), DaFNE projekt 101466 Schwammstadt](https://dafne.at/projekte/schwammstadt)
- Přenositelnost do Koryčan: Náměstí a hlavní ulice při rekonstrukci chodníků. Pod rabátkem jsou v Koryčanech pelozemě (HSP C/D): nutný bezpečnostní přepad a drenáž, jinak strom stojí ve vodě.
- Rizika, co z toho neplyne: Retence proti běžnému rabátku není změřena; chyby stavby (zhutnění, jemné frakce v substrátu) výkon zničí; zálivka první 2-3 roky.
- Nedohledáno: cena rabátka; metodika MZI MŽP

### U02 Propustné povrchy parkovišť, chodníků, dvorů veřejných budov (doplněno)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Světlý asfalt: povrch -4 až -5,5 °C, pro chodce bez zlepšení (Köniz 2025); trávník v centru vzduch -0,9 °C proti dlažbě (CzechGlobe) [0.9-5.5 °C]. Zdroj: [Grolimund + Partner / ASTRA / BFH 2025](https://www.koeniz.ch/public/upload/assets/24417/260422%20faktenblatt_auswertung_pilotprojekt_waldeggstrasse.pdf); [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf)
- Rizika, co z toho neplyne: Propustná dlažba chladí jen tehdy, když je v ní voda nebo tráva s kontaktem s podložím; suchá dlažba se chová jako asfalt 🤔.

### U03 Zasakovací pásy a průlehy podél komunikací, příkopy s retencí (doplněno)
- Účinek infiltrace do půdy (hodnota) ✅: Taucha: 3 soustavy průleh-rýha po 25-30 letech: k_f 3e-6 až 9e-5 m/s (infiltrometr), 1e-5 až 1e-4 m/s (zaplavení celého průlehu); vyprázdnění do 24 h (DWA-A 138) splněno; návrh 10 % napojené plochy na písku, 20 % na hlíně; odstup od budov 1,5× hloubka výkopu [3e-06-0.0001 m/s]. Zdroj: [Grüner Ring Leipzig / město Taucha / IWS / KWL, 5/2024](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/broschuere-final-leseansicht-finale-26-06-2024.pdf); [IWS Leipzig (Milke), Abschlussbericht Messprogramm Mulden-Rigolen-Moni](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/eb-mrs-monitoring-taucha.pdf)
- Účinek zpomalení odtoku (kvalitativne) ✅⏳: Werther (sprašová hlína, k_f ~1e-7 m/s jako HSP D), 6,5 ha od 2000: odtok rozložen v čase místo špiček, ale rýhy v zimě dlouho zaplavené, lokální zamokření; v suchých létech prázdné - pro HSP C/D průleh s rýhou a regulovaným odtokem, ne čistý vsak. Zdroj: [FH Bielefeld / I.W.A. Minden 2005](https://www.lanuk.nrw.de/fileadmin/forschung/wasser/niederschlag/Abschlussberichtdezentraleversickerung.pdf)
- Kde to funguje: **Taucha (Sasko)** (1994-2024): soustavy průleh-rýha v obytných ulicích z let 1994-1999, vyhodnocení 2023; měď a zinek z měděných okapů nad limity do 25 cm půdy (nepoužívat měď). Měřeno: k_f, doba vyprázdnění, těžké kovy. ✅ [Grüner Ring Leipzig / město Taucha / IWS / KWL, 5/2024](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/broschuere-final-leseansicht-finale-26-06-2024.pdf)
- Kde to funguje: **Werther u Bielefeldu (NRW)** (2000-2005): průleh-rýha v nové zástavbě 6,5 ha na sprašové hlíně, měření 2000-2005 (hladiny v rýhách, vlhkost, podzemní voda, lysimetr). Měřeno: vsak, hladiny, podzemní voda. ✅⏳ [FH Bielefeld / I.W.A. Minden 2005](https://www.lanuk.nrw.de/fileadmin/forschung/wasser/niederschlag/Abschlussberichtdezentraleversickerung.pdf)
- Rizika, co z toho neplyne: Na HSP D se voda v rýze drží týdny; bez regulovaného odtoku hrozí zamokření sousedních pozemků. Měděné okapy kontaminují půdu průlehu. Údržba: vtoky, spád, travní drn.
- Nedohledáno: cena průlehu v ČR 2025-2026 kromě NOO

### U04 Retence a zasakování vody z veřejných budov (škola, úřad) (doplněno)
- Kde to funguje: **Trebišov (SK), střední odborná škola** (2021): dešťová zahrada 19 m², nádrž 1,5 m³ s přepadem, vsakovací rýhy 9 + 10 m², zatravňovací dlažba, zelená stěna 7,5 m s kapkovou závlahou z nádrže; účinek nevyčíslen. Bez měření. ✅ [Zeleňáková M., Junáková N. (TU Košice)](https://doi.mendelu.cz/pdfs/doi/9900/02/00.pdf)
- Kde to funguje: **Berlín Treptow-Köpenick, školní dvory** (2019-2023): 6 škol + hotová Schule am Altglienicker Wasserturm (2019/20): částečné odstranění asfaltu, výsadby, zasakovací průlehy; úspora poplatku za srážkovou vodu cca 1,80 EUR/m² napojené plochy/rok; měření žádné. Bez měření. ✅ [Berlin Treptow-Köpenick, Straßen- und Grünflächenamt](https://berlin.de/ba-treptow-koepenick/ueber-den-bezirk/nachhaltigkeit/2023-02-13-projektsteckbrief-schulhoefe-entsiegeln.pdf)
- Přenositelnost do Koryčan: ZŠ, úřad, sokolovna, hasičárna = největší jednotlivé střechy v obci; nejdřív zjistit, kam vedou svody (plán hospodaření s dešťovou vodou obce), pak odpojit svody od kanalizace a vést vodu do dešťového záhonu, vsakovacího objektu nebo nádrže na splachování.

### U05 Obecní tůň, mokřad, obnova návesní nádrže (doplněno)
- Kde to funguje: **Wiesenena (Sasko, obec Wiedemar)** (2008-2009): renaturace betonové požární nádrže: cca 1 000 m² hladiny, mělké břehy, litorál, hnízdiště břehulí, lavičky; náklady a měření neuvedeny. Bez měření. ✅⏳ [Sasko, Ländlicher Raum](https://www.laendlicher-raum.sachsen.de/download/Dorfteich_Wiesenena.pdf)
- Kde to funguje: **Močovice** (2020): koncepce: návesní rybník 4 530 m² hladiny, odbahnění 906 m³ (ponechat 10 cm pro těsnění), litorál, oprava hráze a výpusti; 2,5-2,8 mil. Kč bez DPH. Bez měření. ✅ [VRV a.s. 2/2020](https://www.mocovice.cz/mocovice/rozvoj-obce/koncepce-rozvoje-vodnich-ploch/koncepce-rozvoje-vodnich-ploch.pdf)
- Kde to funguje: **Cehnice (Jihočeský kraj)**: retenční nádrž Třtí na Cehnickém potoce: stálá hladina 11 401 m³ + retenční prostor 50 363 m³, revitalizace přítoku s tůněmi a mokřadem; 15,95 mil. Kč (OPŽP 13,56 mil.) - patří spíš k malým nádržím a poldrům. Bez měření. ✅ [SMO ČR, příklad dobré praxe](https://www.smocr.cz/Shared/Clanky/10359/sosnova-1-retencni-nadrz-trti-na-cehnickem-potoce.pdf)
- Kde to funguje: **Kujavy (Novojičínsko)** (2025-2026): 'Voda pro krajinu': obnova 3 tůní svépomocí (myslivci, mladí myslivci), nadace Hyundai a OSF; rozpracováno; finalista Adapterra 2026. Bez měření. ✅ [Zpravodaj obce Kujavy 2/2026](https://pv.svkos.cz/Zpravodaj_obce_Kujavy/Zpravodaj_obce_Kujavy_2026/Zpravodaj_obce_Kujavy_2026_2.pdf); [businessinfo.cz 26. 8. 2026](https://www.businessinfo.cz/clanky/ziska-cenu-mokrad-pole-nebo-zachranarske-zakladny-o-vitezi-adapterra-awards-2026-rozhodne-i-verejnost/)
- Rizika, co z toho neplyne: Mikroklima návesní nádrže neměřeno; podle CzechGlobe malé vodní plochy vzduch skoro neochladí - hodnota je retence a biodiverzita.
- Nedohledáno: cena poldru a hráze (dřívější údaj se v ÚÚR 2025 nepotvrdil, vyřazen); mikroklima návesní nádrže

### U06 Mozaiková seč obecních ploch, květnaté louky (doplněno)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Trávník v centru: vzduch -0,9 °C proti osluněné dlažbě; zalévaný trávník povrch až o 20 °C chladnější než nezalévaný; trávník bez kontaktu s podložím má povrch jako beton (CzechGlobe/UPOL) [0.9-20 °C (vzduch / povrch)]. Zdroj: [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf); [ČT24 8. 8. 2022](https://ct24.ceskatelevize.cz/veda/3520774-i-travnik-pomuze-vedci-pripravili-doporuceni-ktera-maji-pomoci-ceskym-mestum-zvladat)
- Rizika, co z toho neplyne: V suchu bez závlahy účinek trávníku na horko mizí (suchý trávník ~ dlažba 🤔 odvozeno).

### U07 Školní zahrada jako ukázkový pozemek (doplněno)
- Kde to funguje: **Kornwestheim (Bádensko-Württembersko), Silcherschule** (2026): termokamera města: asfalt dvora 56,2 °C ve 13:30, stín 29,7 °C; odstranění asfaltu, 2 stromové mísy se štěpkou, stromy, cesty z kůry, sezení z kamene a kmenů; 37 000 € (15 000 € dotace Klimopass), městské zahradnictví 3-4 týdny. Měřeno: povrch termokamerou před úpravou. ✅ [Stuttgarter Zeitung 7. 10. 2026](https://www.stuttgarter-zeitung.de/lokales/ludwigsburg/hitze-in-kornwestheim-562-grad-auf-schulhof-gemessen-so-reagiert-die-stadt-jetzt-79527198.html)
- Kde to funguje: **Drážďany, Montessorischule Huckepack** (2025-2027): fólie na okna, markýzy, noční provětrávání, odstranění asfaltu, stromy, plachty, nádrž na dešťovou vodu; 2025-2027, EFRE. Bez měření. ✅ [ReKIS / Sachsen EuK](https://rekis.hydro.tu-dresden.de/wp-content/uploads/2026/07/GPB_Steckbrief_FRL-EuK_Montessori-Huckepack_Formatvorlage-Fachbeitrag.pdf)
- Kde to funguje: **Červená Voda** (2026): školní zahrada 2 000 m² (koloběh vody, včely, energie, mikroklima), finalista Adapterra Awards 2026. Bez měření. ✅ [businessinfo.cz 26. 8. 2026](https://www.businessinfo.cz/clanky/ziska-cenu-mokrad-pole-nebo-zachranarske-zakladny-o-vitezi-adapterra-awards-2026-rozhodne-i-verejnost/)
- Kde to funguje: **Trebišov (SK)** (2021): školní atria: dešťová zahrada, nádrž, vsakovací rýhy, zelená stěna (jako u vody z veřejných budov). Bez měření. ✅ [Zeleňáková M., Junáková N. (TU Košice)](https://doi.mendelu.cz/pdfs/doi/9900/02/00.pdf)
- Přenositelnost do Koryčan: Pro ZŠ Koryčany je prvním krokem změřit dvůr IR teploměrem v létě: asfalt vs. stín vs. tráva. Pak odstranění části asfaltu, stromové mísy, štěpka.

### U09 Studie a plán hospodaření s dešťovou vodou obce (kam teče voda z veřejných ploch, kdo se stará) (nové)
- Co to je: Obec si nechá zpracovat (nebo se školou udělá) přehled, kam teče voda ze střech veřejných budov, silnic a náměstí, kde jsou místa pro průlehy, rabátka a nádrže, a kdo se o ně bude starat. Bez toho se opatření staví nahodile a po letech chátrají. V Koryčanech tuto roli z velké části plní tato aplikace.
- Účinek zpomalení odtoku (kvalitativne) ✅: Taucha (Sasko): u 25-30 let starých průlehů selhávaly správa a údržba (ucpané vtoky, chybějící spád, zrušené soukromé průlehy, zásahy sítí), ne princip; doporučení: vlastnictví a údržbu určit smluvně, provozní řád, kontrola vsaku každých 10 let, cedule pro obyvatele. Zdroj: [Grüner Ring Leipzig / město Taucha / IWS / KWL, 5/2024](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/broschuere-final-leseansicht-finale-26-06-2024.pdf)
- Kde to funguje: **Taucha (Sasko)** (2023-2024): vyhodnocení 3 soustav průleh-rýha po 25-30 letech provozu; obecné pokyny pro obce (plánování, vlastnictví, provoz, údržba, monitoring). Měřeno: k_f, vyprázdnění do 24 h, těžké kovy v půdě. ✅ [Grüner Ring Leipzig / město Taucha / IWS / KWL, 5/2024](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/broschuere-final-leseansicht-finale-26-06-2024.pdf); [IWS Leipzig (Milke), Abschlussbericht Messprogramm Mulden-Rigolen-Moni](https://gruenerring-leipzig.de/wp-content/uploads/2024/08/eb-mrs-monitoring-taucha.pdf)
- Kde to funguje: **Jílové u Prahy** (2026): malé město má studii retenční kapacity (vsak, malé nádrže, krajinná opatření) a hledá partnery, jak přejít 'od analýzy k realizaci'. Bez měření. ✅ [Portico / European Urban Initiative 17. 5. 2026](https://portico.urban-initiative.eu/urban-matchmaker/nature-based-rainwater-retention-climate-resilient-small-towns)
- Kde to funguje: **Močovice (Středočeský kraj)** (2020): koncepce rozvoje vodních ploch obce: návesní rybník 0,65 ha (4 530 m² hladiny), odbahnění 906 m³, varianty 2,5-2,8 mil. Kč bez DPH, jez 7,6-16,6 mil. Kč. Bez měření. ✅ [VRV a.s. 2/2020](https://www.mocovice.cz/mocovice/rozvoj-obce/koncepce-rozvoje-vodnich-ploch/koncepce-rozvoje-vodnich-ploch.pdf)
- Přenositelnost do Koryčan: Plně. Pro Koryčany: tato aplikace + pasport svodů veřejných budov (škola, úřad, sokolovna, hasičárna) + dohoda, kdo seče a čistí průlehy. Školní projekt 'kam teče voda ze školy' (srážkoměr, teploty povrchů) jako vstup.
- Rizika, co z toho neplyne: Studie bez realizace (Jílové). Náklady studie nedohledány. Dolní Rakousko dotuje obcím 'Regenwasserpläne' 📄 (web 22. 10. offline).
- Kč: celkem: cena neověřena
- Povolení: 0
- Nedohledáno: cena studie HDV pro obec do 3 000 obyvatel; NÖ Regenwasserpläne (web offline)

### U08 Mlžení a kropení při letních hromadných akcích (mlžná brána, tryska na hydrantu) (nové)
- Co to je: Mlžná brána nebo tryska na hydrantu na hodech, táboře, sportovním dni nebo trhu v horkém dni. Pomůže lidem, kteří stojí přímo u ní; ulici ani obec neochladí. Jako trvalý prvek nemá smysl (rozhodnutí 21. 10. 2026), jen pro akce.
- Účinek ochlazení mikroklimatu (hodnota) ✅: Vzduch v průměru -0,7 °C, max. -2,5 °C (Curych 2022, 180 trysek, jen za provozu, nejvíc při nízké vlhkosti po větru); autoři účinek označují za slabý [0.7-2.5 °C vzduch]. Zdroj: [Suter, Drossaart van Dusseldorp, Anet (ZHAW), EGU 2023](https://meetingorganizer.copernicus.org/EGU23/EGU23-13652.html)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Vodní prvky (trysky, mlžné brány) vzduch cca -1,2 °C jen v bezprostředním okolí; kropení ploch -1,3 až -3,1 °C pocitově na max. ~20 min; kašny na náměstí minimální účinek (CzechGlobe/UPOL) [1.2-3.1 °C]. Zdroj: [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf); [ČT24 8. 8. 2022](https://ct24.ceskatelevize.cz/veda/3520774-i-travnik-pomuze-vedci-pripravili-doporuceni-ktera-maji-pomoci-ceskym-mestum-zvladat)
- Kde to funguje: **Curych, Turbinenplatz** (2022): kruh 180 vysokotlakých trysek na náměstí, měření ZHAW celé léto 2022; mimo provoz nulový rozdíl. Měřeno: teplota vzduchu vs. referenční stanice. ✅ [Suter, Drossaart van Dusseldorp, Anet (ZHAW), EGU 2023](https://meetingorganizer.copernicus.org/EGU23/EGU23-13652.html)
- Kde to funguje: **Vídeň** (2020-2025): 100 mlžných sprch 'Sommerspritzer' a 75 mobilních 'Brunnhilde' na hydrantech při výstraze; Cooling Park Esterházypark (2020) uvádí 'až 6 °C' bez metodiky. Bez měření. ✅ [CoolLIFE / IEECP factsheet 9/2025](https://ieecp.org/wp-content/uploads/2025/12/CoolLIFE_GoodPractices_AustriaHeatActionPlanVienna.pdf); [Wien MA 20](https://www.wien.gv.at/umwelt/energie-projekt-coolspot-im-esterhazypark)
- Přenositelnost do Koryčan: Pro Koryčany jen jako vybavení letních akcí (hody, tábor, sportovní den): tryska na hydrant nebo IBC s čerpadlem 🤔. Trvalé mlžení na náměstí ne - účinek do 2,5 °C jen za provozu a spotřeba pitné vody v suchu.
- Rizika, co z toho neplyne: Ochladí místo, ne obec; kašna sama nic. Spotřeba pitné vody v suchu; hygiena rozprašované vody (legionely 💻). Vídeňské 'až 6 °C' nemá metodiku, nepřebírat.
- Kč: celkem: cena neověřena
- Povolení: 1 (souhlas provozovatele vodovodu (hydrant) 💻; hygiena vody v mlžení ověřit s KHS 💻)
- Nedohledáno: cena a spotřeba vody mlžné brány (l/h); hygienické podmínky KHS pro mlžení

### H01 Chladná místa, pitná voda a varování při vlně veder (organizační plán obce) (nové)
- Co to je: Obec před létem určí a zveřejní chladná místa (knihovna, kostel, úřad, škola), zajistí pitnou vodu (pítko, kohoutek na náměstí), při výstraze ČHMÚ rozešle varování seniorům a pečovatelům (rozhlas, SMS), posune časy akcí a prací. Nic se nestaví, jde o domluvu. Nemění teplotu v obci, snižuje riziko pro lidi.
- Účinek ochlazení mikroklimatu (hodnota) ✅: Nizozemský národní plán vedra (od 2007): odhad úmrtí z vedra v aktivačních dnech cca 4 200 (2000-2009) -> 2 400 (2010-2019); u 90+ podíl z úmrtí 2,0 -> 1,3 %; plán 'mohl přispět' (pokles začal už 2007-2011 po vlnách 2003/2006) [2400-4200 úmrtí za dekádu (NL)]. Zdroj: [Climate-ADAPT 18. 6. 2026](https://climate-adapt.eea.europa.eu/en/metadata/case-studies/evaluating-the-effectiveness-of-the-dutch-national-heatwave-plan)
- Účinek ochlazení mikroklimatu (kvalitativne) ✅: Vídeň: 29 opatření, ~1 600 pítek, 22 chladných zón VI-IX, kaskáda varování nemocnicím, pečovatelům a školám; účinky neměřeny, jen počty. Zdroj: [CoolLIFE / IEECP factsheet 9/2025](https://ieecp.org/wp-content/uploads/2025/12/CoolLIFE_GoodPractices_AustriaHeatActionPlanVienna.pdf)
- Kde to funguje: **Nizozemsko (celá země)** (2007-2025): národní plán vedra: varování + rady pro seniory, pečovatele a zdravotníky; 20 aktivací 2010-2026; vyhodnoceno RIVM 2024-2025 (epidemiologie, průzkum 804 seniorů, 586 pečujících, 405 zdravotníků). Měřeno: úmrtnost z vedra po dekádách; 9 z 10 lidí si rady v létě 2025 vybavilo; 1 ze 3 seniorů si myslí, že se ho netýkají. ✅ [Climate-ADAPT 18. 6. 2026](https://climate-adapt.eea.europa.eu/en/metadata/case-studies/evaluating-the-effectiveness-of-the-dutch-national-heatwave-plan)
- Kde to funguje: **Vídeň** (2022-2025): Hitzeaktionsplan 2022, roční vyhodnocení po sezóně; výstraha při >= 3 dnech pocitově >= 35 °C a nocích >= 20 °C; 10 ohrožených skupin. Bez měření. ✅ [CoolLIFE / IEECP factsheet 9/2025](https://ieecp.org/wp-content/uploads/2025/12/CoolLIFE_GoodPractices_AustriaHeatActionPlanVienna.pdf)
- Přenositelnost do Koryčan: Plně. Pro Koryčany: seznam chladných míst na webu a rozhlasem, pítko na náměstí, dohoda s pečovatelskou službou, škola (posun tělocviku, voda ve třídách). Práh varování převzít z výstrah ČHMÚ (SIVS), ne vídeňský 🤔.
- Rizika, co z toho neplyne: Účinek doložen jen pro celostátní systém a 'mohl přispět'; lokální efekt v obci neměřitelný. 'Chladná zóna' bez klimatizace nebo masivní stavby chladná není 🤔. Nemění mikroklima.
- Kč: pítko, hlášení rozhlasem, seznam míst: cena neověřena
- Povolení: 0 (usnesení rady/zastupitelstva, dohoda s pečovatelskou službou a školou)
- Nedohledáno: české vyhodnocení účinku výstrah ČHMÚ/MZ; vzor plánu vedra pro obec do 3 000 obyvatel

### H02 Stínění veřejných míst plachtami, pergolami s popínavkami, přístřešky (zastávka, hřiště, školní dvůr) (nové)
- Co to je: Tam, kde strom nevyroste dost rychle nebo nejde zasadit (sítě, dlažba, zastávka, hřiště), zastínit plachtou, pergolou s popínavkou nebo přístřeškem. Strom zůstává první volba (stín + výpar); plachta je náhrada na dobu, než strom doroste.
- Účinek ochlazení mikroklimatu (hodnota) ✅: Ve stínu (stromu) pocitová teplota o 8,3-10,9 °C nižší než na osluněné dlažbě (CzechGlobe/UPOL); pro plachty samostatné měření nedohledáno [8.3-10.9 °C pocitově (stín stromu)]. Zdroj: [TAČR, tisková zpráva 5. 8. 2021](https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf)
- Účinek ochlazení mikroklimatu (hodnota) ✅: Slunečník povrch 51,3 °C vs. koruna stromu 32,7 °C (IR snímek, ENKI): plachta se sama ohřívá a sálá [32.7-51.3 °C povrch]. Zdroj: [Pokorný J. (ENKI Třeboň), Ratajc U.](https://mladimyslivci.cmmj.cz/wp-content/uploads/sites/99/2025/03/Jak_stromy_chladi.pdf)
- Účinek ochlazení mikroklimatu (kvalitativne) ✅: Aarau 2022: město odmítlo uvést paušální číslo; pevné plachty brání nočnímu chladnutí, stíní, ale neodpařují; preferuje zeleň. Zdroj: [Stadt Aarau, odpověď na dotaz P. Benze 19. 9. 2022](https://www.aarau.ch/public/upload/assets/18407/2022-51%20Beantwortung%20Anfrage%20Pascal%20Benz%20%28FDP%29%2C%20Einsatz%20tempor%C3%A4rer%20Sonnensegel%20in%20Aarau.pdf)
- Kde to funguje: **Solothurn, Amtsplatz**: lanková pergola s popínavkami nad náměstím (zmíněno v odpovědi města Aarau jako vzor rostlinného stínění). Bez měření. 📄 [Stadt Aarau, odpověď na dotaz P. Benze 19. 9. 2022](https://www.aarau.ch/public/upload/assets/18407/2022-51%20Beantwortung%20Anfrage%20Pascal%20Benz%20%28FDP%29%2C%20Einsatz%20tempor%C3%A4rer%20Sonnensegel%20in%20Aarau.pdf)
- Kde to funguje: **Kornwestheim, Silcherschule** (2026): asfalt školního dvora 56,2 °C ve 13:30, ve stínu 29,7 °C (termokamera města, červenec 2026); řešení stromy a štěpka, ne plachty. Měřeno: povrch termokamerou. ✅ [Stuttgarter Zeitung 7. 10. 2026](https://www.stuttgarter-zeitung.de/lokales/ludwigsburg/hitze-in-kornwestheim-562-grad-auf-schulhof-gemessen-so-reagiert-die-stadt-jetzt-79527198.html)
- Přenositelnost do Koryčan: Zastávky, hřiště, školní dvůr, tribuna, trh. Pergola s popínavkou spojuje stín a výpar a je lepší než holá plachta.
- Rizika, co z toho neplyne: Plachta se ohřívá a sálá; stíní jen pod sebou; pevná konstrukce blokuje noční vychladnutí; vítr a sníh (demontáž na zimu). Neřeší vodu.
- Kč: celkem: cena neověřena
- Povolení: 1 (konstrukce: ohlášení nebo stavební povolení podle velikosti 🤔; sítě)
- Nedohledáno: měření teploty pod plachtou vs. pod stromem ve střední Evropě; cena
<!-- RESERSE-END -->
