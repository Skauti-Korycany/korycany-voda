# Datový formát katalogu opatření (data/opatreni.json)

Verze 0.3, 18. 10. 2026.

**Zdroj pravdy je `tools/build_opatreni.py`** (Python, generuje `data/opatreni.json` a `data/opatreni.schema.json`, kontroluje odkazy mezi položkami, zdroji a programy). MD soubory `docs/KATALOG*.md` jsou dokumentace a odůvodnění, ne data. Změna katalogu = úprava skriptu + `python tools/build_opatreni.py`.

## Struktura

```
meta          verze, datum, upozornění, odkazy na MD
ciselniky     misto, rozhoduje, pracnost, ucinek, meritko, povoleni, znacka, kvantifikace_typ
konstanty     srážky (571,5 mm Kroměříž), návrhový déšť p=0,2, součinitele odtoku C, pravidla vsaku, USLE (Gp, C, P), regulovaný odtok
zdroje        {id: nazev, url, rok, znacka, overeno_dne, pozn}   - 81 položek, každá se značkou původu
programy      {id: nazev, zadatel[], stav, od, do, pozn, zdroj}  - 10 programů (stav k 18. 10. 2026)
nastroje      N01-N06 (pacht, vyjmutí, směna, KoPÚ, dotace, dohoda se správcem) s odkazy, co umožňují
opatreni[]    58 položek Z/S/U/P/L/LES/T/C/M
```

## Položka opatření

| pole | obsah |
|---|---|
| id, nazev, popis | Z01 ... M06 |
| misto[] | Z, S, U, P, L, LES, T, C |
| rozhoduje[] | J, V, O, SP, S |
| pracnost | 1-3 |
| ucinky.primarni[], ucinky.vedlejsi[] | R, I, Q, E, CH, ER, B, W |
| meritko | pozemek / lokalita / uzemi |
| kontext | true = velké opatření samosprávy/správců, ne svépomoc |
| kvantifikace[] | {ucinek, typ (vzorec/hodnota/kvalitativne), popis, hodnota, jednotka, rozsah, vzorec, zdroj[], znacka} |
| vhodnost{} | pravidla pro automatický filtr z dat: hsp[], sklon_min/max_pct, nad_hladinou_pv_min_m, odstup_stavba_min_m, misto_typ[], erozni_ohrozenost[] ... (klíče volné, aplikace zná seznam) |
| vazby | potrebuje[] (A|B = alternativy), synergie[], konflikt[] |
| povoleni, povoleni_pozn | 0-2 + text |
| ceny[] | {polozka, hodnota, rozsah, jednotka, rok, zdroj, pozn}; bez zdroje = "cena neověřena" |
| financovani[] | id programů |
| standardy[] | id zdrojů (SPPK, normy, metodiky) |
| nedohledano[] | co chybí (fáze 6) |
| pozn_poctivost | upozornění pro text v aplikaci |
| vahy_skaly | null, rezervováno pro posuvníky (NAPADY-ROZHRANI.md): sucho, prival, vedro, vitr_mraz, biodiverzita 0-3 |

## Značky původu (ciselniky.znacka)
overeno ✅ | overeno_stare ✅⏳ | citace 📄 | odhad 🤔 | pamet 💻. Aplikace zobrazuje značku u každého čísla; "odhad" a "kvalitativne" se zobrazují slovně, bez čísla v součtu.

## Stav k 18. 10. 2026
- 58 opatření, 81 kvantifikací (19 kvalitativních), 25 cenových položek bez zdroje ("cena neověřena").
- Validace: `jsonschema.validate` prošla.
- Co doplnit: váhy škál (až bude seznam stabilní), NOO 2026 ceny, kódy SPPK (D02 003, revitalizace, břehové porosty), znění vodního zákona z e-Sbírky, R faktor pro Koryčany z kalkulačky VÚMOP, návrhový déšť pro Koryčany z ČSN 75 9010.
