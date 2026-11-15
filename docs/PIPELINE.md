# PIPELINE - datové zdroje, skripty a postup pro novou vrstvu

Přesunuto z CLAUDE.md 15. 11. 2026 (beze změny obsahu). Číst, když se pracuje s daty nebo skripty v `tools/`.

## 5. Datové zdroje

| vrstva | zdroj, cesta | licence | výstup v repu |
|---|---|---|---|
| Terén DMR 5G | ČÚZK, 12 listů LAZ SM5 (BUCO25-28, 35-38, 45-48), interpolace TIN -> 5 m | CC BY 4.0 | `dmr5g_5m_info.json`, `_bounds.geojson`; tif jen PC |
| Využití půdy | ZABAGED polohopis přes **WFS ČÚZK** `ags.cuzk.gov.cz/arcgis/services/ZABAGED_POLOHOPIS/MapServer/WFSServer` (limit 1000 prvků, ignoruje startIndex -> dělení bboxu) | CC BY 4.0 | `vyuziti_pudy.geojson/.json`, pásmo `vyuziti` |
| Budovy | INSPIRE BU ČÚZK po obci, Koryčany 588601 (Atom) | CC BY 4.0 | `budovy.geojson` (bez č.p., adres, ID), `budovy_info.json` |
| Parcely | INSPIRE CP ČÚZK, k.ú. Koryčany 669661, Blišice 669652, Jestřabice 659053, Lískovec 684881, Mouchnice 699969 | CC BY 4.0 | `parcely.geojson` (9 537 parcel, bez vlastníků) |
| Toky | ČÚZK INSPIRE HY-NET (GPKG, celá ČR, bez názvů toků) | CC BY 4.0 | `toky_cuzk.geojson`, `data/web/toky.json` |
| Rozvodnice ČHP (kontrola) | ZABAGED vrstva Rozvodnice | CC BY 4.0 | `povodi_chp.geojson` |
| Půda HSP | **VÚMOP HSP 2026** (GPKG na žádost, 27. 10. 2026, `data\vumop\HSP_Korycany.gpkg` jen PC) | **CC BY-NC**, uvádět "VÚMOP, v.v.i." | pásma `hsp`, `hsp_zdroj`, `cn` |
| Půda záložní | BPEJ přes WFS SPÚ `geoportal.spucr.cz/api/open-data/wfs/wfs_bpej` -> HPJ -> HSP (Janeček 2012 tab. 2.2) | otevřená data | `bpej.geojson` |
| R faktor | VÚMOP/ČHMÚ "R faktor 2022", okres Kroměříž, 5 m (jen PC) | žádné podmínky | `usle_info.json`, pásma `usle_ls`, `usle_k` |
| Kritické body | VÚV TGM HEIS (shapefile ČR) | CC BY 4.0 | `kriticke_body.geojson` |
| Srážky denní | ČHMÚ opendata, manuální stanice Koryčany 0-203-0-41701068002 (1920-), normál 1991-2020 = 632 mm | volně, uvádět ČHMÚ (podmínky v VRSTVY.md doplnit) | `srazky_chmi.json` (vč. histogramu denních úhrnů) |
| Teplota, vlhkost, vítr | ČHMÚ Nemochovice 0-203-0-41503035001 (od 12/2000) | dtto | `pocasi/normaly.json`, `denni.json` |
| Srážky hodinové | KS Koryčany (Povodí Moravy, sap.pmo.cz id=60, 24 h online), Nemotice (hladiny.cz cs=50089, ~10 h) - archiv vzniká scrapováním od 10/2026 | podmínky neuvedeny -> jen agregace | `pocasi/pmo_korycany.csv`, `nemotice.csv` |
| Návrhové srážky 6 h | Kavka a kol. 2023, WPS `rain1.fsv.cvut.cz/services/wps` (proces d-rain6h-timedist): N2 32,2 / N10 53,2 / N100 87,0 mm, tvary A-F, qAPI | neuvedena | `navrhove_srazky.json` |
| Hladina Stříbrníku | čidlo VOX 5157 u Kachníku (hladiny-vox.pwsplus.eu, CSV) | neuvedena | `kachnik_2026.json`, `docs/MERENI.md` |
| Podklady mapy | ČÚZK ZTM WMTS `ags.cuzk.gov.cz/arcgis1/rest/services/ZTM_WM/MapServer/WMTS`, ortofoto WMS | CC BY 4.0, "ČÚZK - on-line" | živě |
| Hledání adresy | RÚIAN `ags.cuzk.gov.cz/arcgis/rest/services/RUIAN/Vyhledavaci_sluzba_nad_daty_RUIAN/MapServer/exts/GeocodeSOE` (`suggest`, `findAddressCandidates`, `outSR=4326`) | služba zdarma, výslovná licence nedohledána | živě |

Další dostupné WMS (geologie ČGS, OPRL NLI, LPIS, vojenská mapování, CORINE, AOPK) a stav jejich ověření: `docs/VRSTVY.md`. **Před zabalením jakékoli nové vrstvy do repa ověřit licenci a zapsat ji do VRSTVY.md**; WMS v aplikaci je přípustné bez redistribuce.

## 6. Datová pipeline (tools)

Pořadí a závislosti. Každý skript má `.bat` spouštěč (instaluje knihovny, běží z `repo\tools`).

| skript | vstup -> výstup |
|---|---|
| `01_dmr_grid.py` | LAZ -> `dmr5g_5m.tif` (5 m, float32), hillshade |
| `02_rozvodnice.py` | priority-flood, D8, akumulace, sklon/expozice (Horn), údolnice >= 0,25 km², povodí k bodům z `data/rozvodnice_body.json` -> `povodi.geojson` (vč. `typ: uzemi_modelu`), `toky_dmr.geojson` |
| `03_vektory.py` | INSPIRE BU + HY-NET -> `budovy.geojson`, `toky_cuzk.geojson` |
| `04_vyuziti_pudy.py` | ZABAGED WFS -> `vyuziti_kod.tif` (legenda `vyuziti_pudy.json`) |
| `05_hsp.py` | VÚMOP GPKG (pokud existuje) > BPEJ > nejbližší -> `hsp.tif`, `hsp_zdroj.tif` (`--bez-vumop` = stará cesta) |
| `build_cn.py` | -> `cn_tabulka.json` (25 tříd, Janeček 2012 tab. 2.3, urbánní TR-55) |
| `06_cn.py` | CN = tabulka × využití × HSP -> `cn.tif`, `odtok_P20/40/60.tif`, `cn_info.json` |
| `07_srazky_chmi.py`, `08_srazky_recent.py` | ČHMÚ historical/recent -> `srazky_chmi.json`, `srazky_2026.json` |
| `build_navrhove_srazky.py` | WPS ČVUT (nebo `--offline`) -> `navrhove_srazky.json` |
| `09_balicek_web.py` | rastry -> `data/web/*.png` + `rastr.json` (přidá `usle_*`, `smer_v`, když existují tify) |
| `10_parcely.py` | INSPIRE CP -> `parcely.geojson` |
| `11_usle.py` | R × K × LS × C × P -> `usle_info.json` |
| `12_pocasi.py` | (Actions) ČHMÚ recent + scrape PMO/Nemotice + sluneční svit -> `pocasi/denni.json` (P, T, Tmin, Tmax, H, F, S, ET0 Penman-Monteith, zdroj_ET0, bil, zdroj_P); ET0 se při každém běhu přepočítá pro všechny dny z uložených vstupů |
| `13_normaly_pocasi.py` | (Actions `normaly.yml`) historical_csv (vč. slunečního svitu 4 stanic) -> `pocasi/normaly.json` (ET0 Penman-Monteith, `ET0_HS` pro srovnání), doplňování mezer z okolních stanic; **v březnu 2027 spustit znovu** (ročník 2026) |
| `14_toky_vypaleni.py` | toky ČÚZK vypálené -2 m do DMR -> `smer_vypaleny.tif`, `data/web/toky.json` |
| `15_pramen_kyjovka.py` (Actions `hydro.yml`) -> `build_hydro.py` | ČHMÚ hydrologie: prameny a Kyjovka -> `data/hydro/*.csv` -> `hydro_rocni.json` (Jak bylo kap. 3); pak `build_dummy.py` |
| `16_vypar_data.py` (Actions `vypar.yml`) -> `build_vypar.py` | ČHMÚ svit, vítr, vlhkost, záření, výparoměry + Open-Meteo -> `data/vypar/*.csv` -> `vypar_rocni.json` (ET0 Penman-Monteith proti Hargreaves, kontroly); pak `build_dummy.py` |
| `build_kachnik.py` | VOX + hodinové srážky -> `kachnik_2026.json` |
| `build_opatreni.py` -> `build_katalog_md.py` -> `build_dummy.py` | katalog -> JSON -> MD -> HTML |
| `stahni_vstupy.py` (Actions `stahni-vstupy.yml`, větev `vstupy`), `stahni_zdroje.py` | stahování surovin a archivu podkladů (mimo git) |

Po změně podkladových JSON (`budovy_info`, `cn_info`, `srazky_chmi`, `cn_tabulka`, `opatreni`) vždy znovu `build_dummy.py`. Po změně rastrů `09_balicek_web.py` a `node web/test_jadro.js`.

## 10. Jak přidat novou datovou vrstvu (postup)

1. Ověřit zdroj a licenci online, zapsat do `docs/VRSTVY.md` (URL, licence, datum, značka).
2. Jen pro zobrazení: WMS/WMTS přímo v Leafletu v `build_dummy.py`, s atribucí. Bez redistribuce.
3. Pro výpočet: skript `tools/NN_nazev.py` (stáhne bbox území nebo čte soubor z PC), převede na mřížku DMR (S-JTSK, 5 m, 1500 × 1600), výstup tif do `repo\data\dmr\` (mimo git) + lehký `data/nazev_info.json` + náhled `docs/img/nazev_nahled.png`. Spouštěč `vyrob_nazev.bat`.
4. Do balíčku: doplnit pásmo do `09_balicek_web.py` (8/16 bit PNG, kódování a licence do `rastr.json`). Pozor na velikost balíčku (mobil).
5. Načtení v jádru (`Jadro.nacti`), funkce + test v `web/test_jadro.js` proti Python výstupu.
6. UI v `build_dummy.py`, přegenerovat, zkontrolovat headless Chromium 1300 px a 390 px, světlý i tmavý režim, bez chyb v konzoli a bez vodorovného posunu.
7. Aktualizovat O modelu (zdroje dat), případně `stav.html`, a `docs/STAV.md`.
