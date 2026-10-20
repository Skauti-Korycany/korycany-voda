# Srážky - data ČHMÚ pro okolí Koryčan

Stav: 19. 10. 2026. Zdroj: ČHMÚ, opendata.chmi.cz ✅ (adresáře `historical_csv` do 31. 12. 2025 a `recent` pro rok 2026). Skripty `tools/07_srazky_chmi.py` (+ `vyrob_srazky.bat`) a `tools/08_srazky_recent.py` (+ `vyrob_srazky_2026.bat`). Surová data v `data/chmi/` (mimo git), souhrny v `data/srazky_chmi.json`, `data/srazky_stanice.json`, `data/srazky_2026.json`, náhled `docs/img/srazky_nahled.png`.

Formát souborů ověřen podle knihovny wetterdienst (provider/chmi) ✅; popis ČHMÚ: `meteorology/climate/Klimatologicka_data_popis.pdf` ✅. Licence: podmínky užití otevřených dat ČHMÚ na opendata.chmi.cz - **zatím neotevřeno**, před zveřejněním ověřit a zapsat do VRSTVY.md.

## Stanice (do 30 km od středu území 71 záznamů, aktivních 23)

| stanice | WSI | km | m n. m. | období denních úhrnů | typ |
|---|---|---|---|---|---|
| **Koryčany** | 0-203-0-41701068002 | 1,2 | 305 | 1920-2025 (88 úplných let), 2026 do 31. 8. | manuální |
| Nemochovice | 0-203-0-41503035001 | 7,8 | 283 | 2001-2025, 2026 do 18. 10. | **automatická** (1h, 10min) |
| Staré Hutě | 0-203-0-41701068003 | 9,4 | 427 | 1994-2025, 2026 do 18. 10. | **automatická** (1h, 10min) |
| Hýsly | 0-203-0-41701090001 | 10,2 | 217 | 2007-2025, 2026 do 31. 8. | manuální |
| Střílky | 0-203-0-11753 | 4,9 | 341 | 1931-1981 | zrušená |
| Brankovice | 0-203-0-11757 | 4,8 | 268 | 1981-2000 | zrušená |

Dál: Bučovice-Kloboučky, Ždánice (11 km, od 1881/1903, aktivní), Kyjov (do 2007), Buchlovice (13 km, aktivní). Mimo ČHMÚ: srážkoměr **VD Koryčany** (Povodí Moravy, hlásný) ✅ portalobce.cz - data jen na žádost.

## Dlouhodobé charakteristiky (denní úhrny, klimatologický den 06-06 UTC)

| | Koryčany | Staré Hutě | Nemochovice | Hýsly |
|---|---|---|---|---|
| normál 1991-2020 | **632 mm** | 717 mm | 575 mm | 538 mm |
| průměr úplných let | 625 mm | 715 mm | 581 mm | 535 mm |
| N2 / N10 / N100 denní (Gumbel, orientačně) | 37 / 58 / 84 mm | 46 / 72 / 104 mm | 39 / 60 / 85 mm | 37 / 57 / 81 mm |
| dní ≥ 20 / 30 / 50 mm za rok | 5,0 / 1,7 / 0,22 | 6,3 / 2,4 / 0,56 | 5,2 / 1,6 / 0,38 | 3,9 / 1,4 / 0,17 |

Koryčany, měsíční normál 1991-2020 (mm): I 36, II 33, III 43, IV 40, V 67, VI 82, VII 79, VIII 65, IX 60, X 45, XI 43, XII 39.

Největší denní úhrny Koryčany: 114,0 mm (2. 7. 1954), 93,5 (12. 6. 2012), 77,5 (6. 7. 1997), 72,2 (20. 6. 1964), 71,5 (22. 5. 1960). Staré Hutě: 107,1 mm (14. 9. 2024), 87,1 (31. 7. 2016). Nemochovice: 77,5 mm (14. 9. 2024).

Výškový gradient Koryčany (305 m) -> Staré Hutě (427 m): +85 mm/rok (🤔 ze dvou stanic). Pro lesní část povodí v Chřibech platí spíš hodnoty Staré Hutě.

Hodnota 571,5 mm (Kroměříž) používaná dříve je tímto nahrazena.

## Rok 2026 (data `recent`, předběžná)

Měsíční úhrny (mm), Koryčany / Nemochovice / Staré Hutě:
V 49 / 43 / 41, VI 33 / 33 / 38, VII 45 / 65 / 53, VIII 35 / 51 / 46, IX - / 45 / 55. Léto 2026 bylo v Koryčanech pod normálem (VI-VIII 113 mm proti normálu 226 mm).

Epizody čidla Kachník proti srážkám (denní úhrn = den 06 UTC až následující den 06 UTC; hodinová maxima Nemochovice / Staré Hutě):

| epizoda Kachník | Koryčany denní | Nemochovice | Staré Hutě | čtení |
|---|---|---|---|---|
| 15. 7. | 14. 7.: 19,7 mm | 14. 7.: 27,4 mm, max 10,6 mm/h 17 UTC; 15. 7. ráno 3,6 mm/h | 15. 7.: 21,3 mm, **12,1 mm/h v 05 UTC** | bouřka 14. 7. večer + déšť 15. 7. ráno |
| 23. 7. | 2,0 mm | 5,4 mm, 5,2 mm/h 10 UTC | 4,0 mm | slabé, lokální |
| 1.-2. 8. | 5,0 mm | **22,6 mm, 21,2 mm/h 17 UTC, 10,8 mm/10 min** | 5,6 mm | silná lokální bouřka u Nemochovic, Koryčany okraj |
| 8. 9. | - | 0,0 mm | 0,0 mm | **bez deště na obou stanicích** - prověřit čidlo nebo velmi lokální bouřka |
| 11. 9. | - | 9. 9.: 10,0; 11. 9.: 5,8 mm, max 1,2 mm/h | 9. 9.: 10,1; 11. 9.: 10,8 mm, max 1,6 mm/h | trvalý déšť, ne příval |
| 17. 9. | - | 16. 9.: 10,1 mm | 16. 9.: 10,0 mm | déšť 16. 9. |

Závěr: přívaly v létě 2026 byly bodové (10 mm/10 min u Nemochovic 1. 8. se v Koryčanech neprojevil), takže stanice 8-9 km daleko nelze brát jako měření nad povodím Stříbrníku. Pro validaci modelu je nutný srážkoměr v povodí (VD Koryčany - Povodí Moravy, nebo vlastní měření školy u Kachníku).

## Metoda a předpoklady
- Úplný rok = chybí max. 5 dnů; normál = průměr měsíčních úhrnů 1991-2020 z měsíců s >= 26 dny.
- N-leté denní úhrny: Gumbel (momentová metoda) z ročních maxim, jen úplné roky. Orientační, jen pro srovnání; model používá 6hodinové návrhové úhrny ČVUT/ČHMÚ 2023 (níže).
- Datum denního úhrnu = začátek klimatologického dne (ověřeno porovnáním s hodinovými daty 14.-15. 7. 2026 ✅).
- `recent` data ČHMÚ přepisuje po kontrole; `historical` se doplňuje jednou ročně (do února).

## Návrhové 6hodinové srážky (ČVUT/ČHMÚ metodika 2023) - 20. 10. 2026

Zdroj ✅: Kavka a kol. 2023, *Krátkodobé srážky pro hydrologické modelování a navrhování drobných vodohospodářských staveb v krajině*, certifikovaná metodika 2/2023/SPU/O, ISBN 978-80-01-07115-1 (ČVUT v Praze, ČHMÚ, ÚFA AV ČR, Sweco Hydroprojekt), PDF rain.fsv.cvut.cz. Data z WPS `https://rain1.fsv.cvut.cz/services/wps`, proces `d-rain6h-timedist` (PyWPS/GRASS; z Claude je server blokovaný, dotaz šel přes prohlížeč v aplikaci). Metoda: regionální frekvenční analýza 6h maxim z 20 let adjustovaných radarových dat (10 min, 1 km) + 30 a více let staničních řad; výstup rastr 1 km pro ČR. Skript `tools/build_navrhove_srazky.py` -> `data/navrhove_srazky.json` (+ `data/navrhove_srazky_tvary_raw.csv` = surový výstup WPS).

Bod: střed území modelu (S-JTSK -557700, -1174500). Kontrola dalších bodů (Lískovec, hráz VN, les nad Stříbrníkem): N10 52,9-53,4 mm -> území homogenní. Redukce úhrnu na plochu se dělá až nad 20 km² (území modelu 14,1 km²).

| doba opakování | N2 | N5 | N10 | N20 | N50 | N100 |
|---|---|---|---|---|---|---|
| **6 h úhrn, Koryčany** ✅ | **32,2** | **44,3** | **53,2** | **62,6** | **76,0** | **87,0 mm** |
| průměr ČR podle metodiky 📄 | 29 | 39 | 46 | 53 | 64 | 73 mm |
| denní, stanice Koryčany, Gumbel 🤔 | 37 | 50 | 58 | 66 | 76 | 84 mm |

Koryčany jsou o 10-20 % nad průměrem ČR (Chřiby). Denní Gumbel ze stanice je pro N2-N50 vyšší (delší trvání), u N100 nižší než 6h hodnota - momentový Gumbel podceňuje horní konec; metodika sama upozorňuje, že vysoké N mohou být lokálně nadhodnocené.

Tvary průběhu A-F (podíl v %, Koryčany) a qAPI:

| | A příval | B jednoduchý | C dva vrcholy | D dva vrcholy | E plochý | F trvalý |
|---|---|---|---|---|---|---|
| N2 | 12,8 | 15,6 | 25,3 | 13,7 | 16,8 | 15,8 |
| N10 | 8,5 | 20,9 | 34,6 | 13,4 | 19,4 | 3,2 |
| N100 | 3,6 | 26,1 | 37,5 | 10,9 | 21,8 | 0,03 |
| qAPI | 0,18 | 0,28 | 0,35 | 0,20 | 0,40 | 0,41 |

qAPI = pravděpodobnost abnormálně vlhkého stavu před deštěm (API5). Metodika (tab. 6): qAPI < 0,2 -> počítat s CN2, qAPI > 0,8 -> CN3, mezi tím lineární váha; CN1 se pro návrh nepoužívá. Pro Koryčany to znamená váhu CN3 0-0,35 podle tvaru - místo dřívějšího záměru "přepočet IPS I/III" se v jádru použije tento vážený postup. Při N10 tvar A (9 %) spadne 36 % úhrnu (19 mm) za 15 minut; tvar C má dva vrcholy po 2 a 4 hodinách.

Použití v modelu: výchozí návrhový déšť = N10 6h 53 mm (prototyp nabízí i N100 87 mm); SCS-CN objem = vážený průměr přes tvary (váhy = podíl tvaru) a stavy CN2/CN3 (váhy z qAPI). Krátké úhrny (15 min, 60 min) pro dimenzování vsaku zůstávají z ČSN 75 9010 (zatím příklad Brno); z tvarů A-F je lze odvodit jen orientačně.

Licence: podmínky užití dat portál neuvádí; služba je veřejná bez registrace. Pro zveřejnění odvozených čísel v aplikaci stačí citace; při případné redistribuci rastrů se zeptat autorů (ČVUT FSv, Ing. Petr Kavka, Ph.D.).
