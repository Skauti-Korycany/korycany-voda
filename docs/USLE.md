# Eroze orné půdy (USLE) - blok N, 21. 10. 2026

Orientační dlouhodobá ztráta půdy A = R · K · L · S · C · P [t/ha/rok] pro ornou půdu v území modelu. Skript `tools/11_usle.py` (`vyrob_usle.bat`) -> `data/usle_info.json`, rastry `data/dmr/usle_ls.tif`, `usle_A_C02.tif` (mimo git), náhled `docs/img/usle_nahled.png`.

## Vstupy a zdroje
| faktor | odkud | značka |
|---|---|---|
| R | **VÚMOP/ČHMÚ „Regionalizovaný R faktor 2022“**, rastr 5 m po okresech, podmínky užití „žádné neplatí“ (metadata.vumop.cz); okres Kroměříž CZ0721 (83 MB zip, 372 MB TIF) stažen 21. 10. přes prohlížeč z owncloud.cesnet.cz. V území 62-71, průměr **66 MJ/ha·cm/h** (Janeček 2012 doporučoval paušál 40). 46 ha NoData (okraj okresu) doplněno nejbližší hodnotou. | ✅ |
| K | podle HPJ (2.-3. číslice BPEJ ze SPÚ), Janeček a kol. 2012 tab. 1.5, s. 15 - celá tabulka ve skriptu. Orná v území: průměr 0,35 (HPJ 40/41 svažité 0,24/0,33; 19/20 0,33/0,28; 08 0,49). 0,7 ha orné bez BPEJ vynecháno. | ✅⏳ |
| L, S | Janeček 2012 rov. 1.6-1.8 (McCool): S = 10,8 sin θ + 0,03 (< 9 %) / 16,8 sin θ - 0,50 (>= 9 %); L = (l/22,13)^m. Délka svahu l = přispívající plocha na šířku buňky z akumulace D8 (Desmet & Govers), omezená na 300 m. Exponent m podle sklonu 0,2/0,3/0,4/0,5 (Wischmeier & Smith) - tab. 1.7 Janečka nemám, může se lišit. | ✅⏳ / 💻 (m) |
| C | průměrný roční faktor krytu - scénáře 0,1 / 0,2 / 0,3 / 0,01 (TTP); skutečný osevní postup pozemků neznáme | 🤔 |
| P | 1 (bez protierozních opatření) | - |
| Gp | 9 t/ha/rok (od 1. 7. 2026, vyhl. 240/2021 Sb., v katalogu), Janeček 2012 doporučuje 4, pro ochranu vod 0,5-2 | ✅ |

## Výsledky - orná půda území modelu (260,5 ha, průměrný sklon 10,4 %, LS 2,45)

| scénář C | A průměr | medián | nad Gp 9 | nad 4 | nad 2 | celkem t/rok |
|---|---|---|---|---|---|---|
| obilniny, C 0,2 | **10,6 t/ha** | 8,0 | **46 %** plochy | 72 % | 87 % | 2 750 |
| zlepšené hospodaření, C 0,1 | 5,3 | 4,0 | 18 % | 50 % | 72 % | 1 380 |
| okopaniny, C 0,3 | 15,8 | 12,0 | 60 % | 81 % | 92 % | 4 130 |
| zatravnění, C 0,01 | 0,5 | 0,4 | 0 | 0 | 1 % | 140 |

Podle sklonu (C 0,2): 0-3 % (28 ha) 1,3 t/ha; 3-7 % (56 ha) 4,3; 7-12 % (71 ha) 9,3; **nad 12 % (106 ha = 41 % orné) 17,1 t/ha**. Dílčí povodí Kyjovka ř. km 75,69: 224 ha orné, 10,2 t/ha; v povodí Stříbrníku orná prakticky není.

Co to znamená pro katalog: P06 (zatravnění svažité orné nad 12 %) sníží ztrátu z ~17 na ~0,5 t/ha na 106 ha = cca 1 750 t/rok; P04 (půdoochranné technologie, C 0,2 -> 0,1) zhruba půlí; P01 (vrstevnicově, P 0,6-1,0 podle sklonu) ubere 0-40 %.

## Omezení (napsat i v aplikaci)
- Délka svahu z DMR nezná meze, cesty a hranice pozemků, takže na dlouhých svazích nadsazuje (strop 300 m to jen tlumí). Kalkulačka VÚMOP (USLE2D nad LPIS) je přesnější a pro vyhlášku závazná - tento výpočet je pro osvětu a výběr míst.
- C je scénář, ne skutečný osev; P = 1.
- m exponent z paměti (Wischmeier), ne z tab. 1.7.
- Mělké půdy (Gp 2) nerozlišeny - seznam HPJ mělkých půd neověřen.
