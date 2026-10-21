# Měření: reakce Stříbrníku u Kachníku na déšť, léto 2026 (blok D)

Stav: 21. 10. 2026. Skript `tools/build_kachnik.py` -> `data/kachnik_2026.json`, obrázky `docs/img/kachnik_nahled.png` (celé období) a `kachnik_udalosti.png` (4 epizody v detailu).

## Data

- **Hladina** ✅: čidlo VOX 5157 „Čid5 Koryčany ul. U Rybníka, stavidlo“ = pomocný hlásný profil kat. C na Stříbrníku u rybníka Kachník (hlídá SPA 1/2/3 = 100/120/140 cm). Optické měření hladiny **u vpusti do rybníka Kachník** (upřesnil uživatel 21. 10.; manipulace stavidlem rybníka se tedy neřeší), krok 20 min, místní čas (ověřeno shodou s hodinovými srážkami). Export CSV bez přihlášení z hladiny-vox.pwsplus.eu, 10. 7. - 21. 10. 2026, 7 430 záznamů, 18 výpadků do 2 h. Podmínky užití web neuvádí (provozuje město / VOX). Surová řada uložena úsporně v `data/kachnik_2026_rle.txt` (jen změny hodnoty).
- Čidlo **„Koryčany Kyjovka pod přehradou ČHMÚ“** (36897): krok 10 min, hladina 15-17 cm, maxima 25-28 cm (15. 7., 18. 7., 21. 9., 14. 10.) - řízený odtok z nádrže, pro reakci krajiny na déšť nepoužitelné. Čidlo „PMO Kyjovka nad přehradou“ (6127) nemá žádná data. (Oba soubory, které uživatel stáhl 21. 10., jsou z čidla pod přehradou a jsou totožné.)
- **Srážky** ✅: ČHMÚ otevřená data `recent`, hodinové SRA1H Nemochovice (7,8 km, 283 m) a Staré Hutě (9,4 km, 427 m), denní Koryčany (do 31. 8.). Předběžná data. Převod UTC -> CEST +2 h; předpoklad: časová značka hodinového úhrnu = konec hodiny (sedí s epizodou 15. 7., kdy by při opačném výkladu vrchol hladiny předběhl déšť).

## Výsledky

| epizoda | déšť (Nemochovice / Staré Hutě, 12 h před vrcholem) | max 1 h | vzestup hladiny | doba vzestupu | zpoždění za max. hodinou deště | návrat k základu |
|---|---|---|---|---|---|---|
| 14.-15. 7. bouřka + ranní déšť | 23,6 / 13,6 mm (Koryčany 19,7 mm/den) | 10,6 mm/h 14. 7. 19 h; 12,1 mm/h 15. 7. 7 h (S. Hutě) | **+24 cm** (47 -> 71) | 9 h | 1,6 h za ranním deštěm | 11 h |
| 18. 7. místní přeháňka | 1,6 / 2,4 mm (Koryčany 6,7 mm/den) | - | +4 cm | 2 h | - | < 1 h |
| 23. 7. polední přeháňka | 5,4 / 2,6 mm | 5,2 mm/h 12 h | +7 cm | 20 min | 0,3 h | 1 h |
| 1. 8. bouřka večer | 22,6 / 5,6 mm (Koryčany 5,0 mm/den) | **21,2 mm/h** 19 h (jen Nemochovice) | +10 cm | 3,7 h | 4 h | 12 h |
| 20.-21. 8. večerní déšť | 11,2 / 19,1 mm (Koryčany 7,8) | 8,3 mm/h 18 h (S. Hutě) | +6 cm | 9 h | 7 h | 8 h |
| 28.-29. 8. noční déšť | 11,1 / 7,6 mm (Koryčany 7,0) | 4,6 mm/h | +6 cm | 10 h | 4-5 h | 11 h |
| 9.-10. 9. trvalý déšť | 10,0 / 10,1 mm | 3,3 mm/h | +9 cm | 8 h | 4 h | 35 h |
| 11. 9. slabý trvalý déšť | 8,0 / 11,7 mm | 1,6 mm/h | +7 cm | 7,5 h | 5-6 h | 1,5 h |
| 16.-17. 9. noční déšť | 9,2 / 9,2 mm | 5,9 mm/h | +6 cm | 6 h | 5 h | 8 h |

Bez odezvy (< 3 cm): 14. 9. (S. Hutě 6,1 mm za 6 h), 21.-22. 9. (Nemochovice 5,6 mm za 9 h). Deště do ~5 mm se v hladině neprojeví.

**Co z toho plyne pro osvětu:**
1. Celé léto 2026 (polovina normálu srážek) se hladina u Kachníku nedostala ani na čtvrtinu cesty k 1. SPA (max 71 cm, SPA 1 = 100 cm). Čidlo tedy letos nehlídalo povodeň, ale ukazuje běžný koloběh: déšť -> potok stoupne o 5-25 cm -> za 8-12 hodin je voda pryč.
2. **Přívalová bouřka odteče během půl dne**: 1. 8. spadlo u Nemochovic 21 mm za hodinu, Stříbrník vystoupal o 10 cm za 3,7 h a za 12 h byl zpět. 14.-15. 7. (24 mm za večer + 12 mm/h ráno): +24 cm, zpět za 11 h.
3. Zpoždění vrcholu za maximem deště je u přeháněk pod 1 h, u plošných dešťů 4-7 h - povodí Stříbrníku (4,2 km², les 70 %) reaguje pomalu a tlumeně; rychlé špičky dělá nejspíš intravilán (ulice Lhotka, střechy).
4. Konfrontace s modelem: SCS-CN (CN 65, IPS II) dává pro 20 mm na povodí Stříbrníku **nulový odtok** (Ia = 27 mm), přesto potok 15. 7. stoupl o 24 cm. Rozpor je očekávaný: SCS-CN počítá objem z celého povodí za den, ale špičku dělají nepropustné plochy u potoka (238 budov = 3,3 ha střech v dílčím povodí -> 20 mm = ~670 m³ během hodin) a nasycené dno údolí. Pro malé deště model objemově nelže (z lesa a luk opravdu nic neodteklo), ale hladinu v potoce nepředpoví. Bez měrné křivky (hladina -> průtok) objem z čidla spočítat nejde.
5. Řešení otevřené otázky z 16. 10.: **8. 9. nebyl déšť ani voda** - hodnoty 50/56 cm střídané 45/46 cm po 20 min jsou šum čidla. Propady pod 30 cm kolem 16:40-17:20 (15. 7., 23. 7., 11. 9., 17. 9., 24. 9.) jsou optický artefakt (vždy pozdní odpoledne, návrat do hodiny - nejspíš slunce). Poklesy 27.-28. 7. a 21.-23. 8. na 4-16 cm s pomalým návratem 1 cm za 20-40 min přes 15 h nastaly bez deště; příčina nedohledána (překážka před čidlem, změna reference, nebo vzdutí z rybníka, pokud čidlo stojí v jeho dosahu) - pro vyhodnocení dešťů vyřazeno.

## Omezení
- Čidlo měří hladinu u vpusti do rybníka, ne průtok. Do Stříbrníku nad Kachníkem je svedena řada střešních svodů z intravilánu (ul. Lhotka) - ty dělají rychlou špičku, i když se na trávnících déšť zadrží (uživatel, 21. 10.).
- Srážkoměry jsou 8-9 km daleko; bouřka 1. 8. měla u Nemochovic 21 mm/h, v Koryčanech 5 mm/den - pro přívaly je nutný srážkoměr v povodí (VD Koryčany / škola).
- Léto 2026 bylo suché; žádná epizoda se neblížila SPA. Validace modelu na povodeň z těchto dat nejde; jde jen ilustrace rychlosti odtoku.
- Data ČHMÚ `recent` jsou předběžná; hodinová řada končí 30. 9., denní Koryčany 31. 8.
