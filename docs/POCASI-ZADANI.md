# „Koryčaňáci - jak bylo“: zadání pro samostatný chat (21. 10. 2026)

Cíl: automatický denní sběr srážek, teplot a výparu pro Koryčany a veřejná stránka „Jak bylo“ ve stylu https://www.napajedlaci.cz/jak-bylo/mesic/2026-09/ (období den/měsíc/sezóna/rok; karty srážky / teplota / výpar ET₀ / bilance P-ET / vlhkost proti průměru minulých let; extrémy; srovnání ročníků). Nositel: skautský oddíl Hříběcí hory, nekomerční. **Je to součást osvětové aplikace, ne samostatný web** (rozhodnutí uživatele 21. 10.): „Jak bylo“ je vstupní bod celého webu - nejdřív co se tu s vodou děje (srážky, výpar, bilance, reakce potoka), pak katalog opatření jako následný krok. Technicky: nový režim/záložka v `index.html` (generuje `tools/build_dummy.py`, jádro `web/jadro.js`, stejný design a datový balíček), data v `data/pocasi/`. Samostatná `pocasi.html` jen pokud bude potřeba vložit do webu města (iframe); jinak ne. Pravidla projektu Resilientní Koryčany platí (značky původu, bez dlouhých pomlček, zdroje u každého čísla, Claude pushuje do main sám).

## Ověřené zdroje dat (21. 10. 2026 ✅)
| co | stanice | zdroj | co obsahuje | poznámka |
|---|---|---|---|---|
| srážky denně | **Koryčany** ČHMÚ, WSI 0-203-0-41701068002, manuální, 305 m, 1,2 km od středu města | opendata.chmi.cz `meteorology/climate/recent/data/daily/dly-0-203-0-41701068002-YYYYMM.json` (předběžná, měsíční soubory); historie `historical_csv` 1920-2025 | SRA (06:00 = klimatologický den 06-06 UTC), SNO, SCE, SVH, API30 | **jen srážky, žádná teplota**; normál 1991-2020 = 632 mm, měsíční normály v `data/srazky_chmi.json`; histogram denních úhrnů tamtéž |
| teplota, vlhkost, vítr, srážky | **Nemochovice** ČHMÚ klimatologická, WSI 0-203-0-41503035001, 283 m, 7,8 km SZ | recent daily `dly-0-203-0-41503035001-YYYYMM.json` | T (AVG, 06/13/20), TMA, TMI, TMInoc, TPM, H (AVG + termíny), F, Fmax, D10, E, SRA, SNO | základ pro ET₀; historii T stáhnout z `historical_csv` (rozsah neověřen) |
| srážky hodinově | Nemochovice, Staré Hutě (0-203-0-41701068003, 427 m, 9,4 km) | recent `1h-...json` (SRA1H), `10m` | | Staré Hutě jen srážky |
| srážky + teplota hodinově, jen 24 h online | **KS Koryčany** (Povodí Moravy, areál pod VD, 49.1175 N, 17.1902 E) | https://sap.pmo.cz/portal/Srazky/cz/pc/Mereni.aspx?id=60&oid=3 (HTML tabulka „Posledních 24h“, hodinové mm a °C) | | bez archivu a exportu -> denní stažení = vlastní archiv; „data bez záruky“, podmínky užití neuvedeny |
| srážky hodinově, jen ~10 h online | **Nemotice_SR** (obec, Fiedler, 49.1294 N, 17.1252 E, 4 km Z) | https://www.hladiny.cz/hladiny/index.php?ca=196&cs=50089 | | přenos 3x denně; podmínky použití na hladiny.cz |
| hladina Stříbrník u Kachníku | VOX čidlo 5157 | http://hladiny-vox.pwsplus.eu/Senzors/DownloadRecordsCsv?PeriodModel.CityID=588601&PeriodModel.Address=5&PeriodModel.FromDStr=DD.MM.YYYY&PeriodModel.FromTStr=00:00&PeriodModel.ToDStr=...&PeriodModel.ToTStr=... | CSV `datum;cm`, 20 min, místní čas | libovolné období, bez přihlášení; viz docs/MERENI.md |

Formát ČHMÚ recent JSON: `data.data.header = "STATION,ELEMENT,VTYPE,DT,VAL,FLAG,QUALITY"`, `values` = pole řádků; vyřadit QUALITY >= 4. Parser je v `tools/08_srazky_recent.py` (funkce `zaznamy`, `serie`). Metadata stanic: `recent/metadata/meta1-YYYYMMDD.json`. Z prostředí Claude je opendata.chmi.cz blokované (403) - stahovat musí GitHub Actions nebo PC.

## Rozhodnutí navržená (potvrdit v novém chatu)
1. **Automatizace = GitHub Actions** (cron denně ráno, Python, commit JSON do repozitáře, GitHub Pages servíruje stránku). Nepotřebuje PC ani Claude. Ověřit, že Actions dosáhnou na opendata.chmi.cz, sap.pmo.cz, hladiny.cz (z Claude ne).
2. **ET₀ = Hargreaves-Samani** z Tmin/Tmax/Tmean Nemochovice + extraterestrická radiace pro 49,11 N (FAO-56 rovnice 52) - stejná metoda jako Napajedla, srovnatelné; FAO-56 Penman-Monteith až s radiací/slunečním svitem. Bilance = srážky Koryčany - ET₀ (srážky z Koryčan, teploty z Nemochovic - 8 km, 20 m výškového rozdílu; napsat na stránku).
3. **Normály**: srážky Koryčany 1991-2020 (máme), teplota a ET₀ z historické řady Nemochovice (stáhnout, zjistit rozsah let; když nebude 30 let, použít co je a říct to).
4. Data: `data/pocasi/denni.json` (datum, P_korycany, P_nemochovice, T_avg/min/max, H, F, ET0, bilance), `data/pocasi/pmo_korycany.csv` + `nemotice.csv` (hodinový archiv od spuštění), měsíční/roční agregace počítat v prohlížeči nebo v Actions.
5. Záložka „Jak bylo“ v `index.html` (build_dummy.py): období měsíc/rok, karty srážky / teplota / ET₀ / bilance proti normálu, denní graf, extrémy, srovnání ročníků 1921-2026, odkaz na hladinu Kachníku (MERENI.md); grafy vlastní SVG/canvas bez knihoven třetích stran (prototyp knihovny nemá, Leaflet je vendor), mobil první, u každé karty zdroj a značka. Záložka je první v pořadí (vstup do webu), katalog a Můj pozemek navazují.

## Co se v novém chatu musí udělat (pořadí)
1. Ověřit Actions síť (jeden krátký workflow s curl na tři servery).
2. `tools/12_pocasi.py`: stažení recent (aktuální + minulý měsíc), scrape PMO a Nemotice, výpočet ET₀, zápis JSON/CSV; test na staženém vzorku.
3. Jednorázově historická řada T Nemochovice -> normály.
4. `.github/workflows/pocasi.yml` (cron, commit „[bot] počasí YYYY-MM-DD“).
5. Záložka „Jak bylo“ v build_dummy.py (měsíc/rok, karty, denní graf, extrémy, ročníky 1921-2026 ze srážek); Actions po zápisu dat spustí `build_dummy.py`, aby se index.html přegeneroval.
6. Zápis do STAV.md tohoto repozitáře (sekce „Počasí“), odkaz ze stav.html.

## Otázky pro uživatele
- Název záložky a webu: „Jak bylo“ / „Koryčaňáci“? Doména zůstává GitHub Pages, dokud web města nerozhodne jinak.
- Má oddíl/škola v plánu vlastní stanici (srážkoměr + teploměr u Kachníku)? Pak by se data ČHMÚ Nemochovice staly jen zálohou.
- Smí se zveřejňovat scrapovaná data Povodí Moravy a hladiny.cz (podmínky nejsou uvedené) - zeptat se, nebo zobrazovat jen agregace?
