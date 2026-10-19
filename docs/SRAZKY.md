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
- N-leté denní úhrny: Gumbel (momentová metoda) z ročních maxim, jen úplné roky. Orientační, pro model použít až návrhové úhrny ČHMÚ / ČSN 75 9010 (krok 2 v STAV.md).
- Datum denního úhrnu = začátek klimatologického dne (ověřeno porovnáním s hodinovými daty 14.-15. 7. 2026 ✅).
- `recent` data ČHMÚ přepisuje po kontrole; `historical` se doplňuje jednou ročně (do února).
