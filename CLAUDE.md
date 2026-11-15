# CLAUDE.md - Koryčany resilience (korycany-voda)

Předávací kontext pro práci v Claude Code. Stav k 15. 11. 2026. Aktuální stav: `docs/STAV.md`. Historie relací a starší rozhodnutí: `docs/STAV-HISTORIE.md` (dlouhý, číst cíleně podle sekcí).

## 1. Co to je

Osvětová webová aplikace pro obyvatele Koryčan (okres Kroměříž): reálná data o krajině + katalog adaptačních opatření (voda, sucho, horko, eroze) s orientačním výpočtem účinku. Nositel skautský oddíl Hříběcí hory, partner ZŠ Koryčany. Nekomerční, veřejné.

- Repozitář: https://github.com/Skauti-Korycany/korycany-voda (větev `main` = pravda)
- Web (GitHub Pages): https://skauti-korycany.github.io/korycany-voda/ (+ `stav.html`, `web/test.html`)
- Cíl není projektový model. Cíl je, aby lidé pochopili souvislosti a věděli, co může udělat kdo (domácnost, obec, zemědělec, lesník, škola).
- Aplikace musí vždy viditelně říkat: zjednodušený model pro osvětu, ne projekt; **nevalidováno** (dokud není porovnání s měřením).

## 2. Uživatel a pravidla spolupráce

- Vlastník projektu není programátor. Žádné příkazy do terminálu ani git pro něj. Co má spustit na PC, dostane jako jeden `.bat` v `tools\` s instrukcí krok za krokem (kterou složku otevřít, na co poklepat, co se objeví, co poslat zpět).
- Komunikace česky, stručně. **Nikdy dlouhé pomlčky** (–), jen spojovník `-`, i v kódu, HTML a textech aplikace.
- Značky původu u faktických tvrzení a čísel: ✅ ověřeno online v této relaci | 📄 doložený zdroj, originál nečten | 🤔 odhad | 💻 z paměti, neověřeno | ⏳ zdroj starší 12 měsíců. Nikdy nevymýšlet název/autory/rok/DOI. Když zdroj nejde dohledat: "nedohledal jsem".
- Klima, dotace, ceny a legislativu vždy ověřit online (klima a dotace ne starší ~5 let).
- Nic nemazat bez rozhodnutí uživatele, jen navrhovat.
- **Žádné osobní údaje** v datech, sumářích ani aplikaci: vlastníci, LV, adresy, č.p., ID RÚIAN/ISKN, jména žáků, kontakty z e-mailů. Parcelní číslo je veřejný identifikátor pozemku a smí se zobrazit.
- Práce po uzavřených blocích (jeden blok = jeden hotový použitelný výstup). Na konci relace aktualizovat `docs/STAV.md` (jen aktuální stav: hotové, rozpracované, další kroky, platná rozhodnutí, otevřené otázky, předpoklady) a podrobný záznam relace připsat na začátek `docs/STAV-HISTORIE.md`. V odpovědi uživateli doplnit "na co ses nezeptal" a zvolené předpoklady.
- Když na úkol LLM není vhodný nástroj (ruční klikání ve státních portálech, 2D hydraulika, kalibrace bez dat), říct to a připravit podklady, ať to uživatel udělá sám.
- Klon na PC uživatele: `C:\Users\obcho\Desktop\Claude - zoofix\skaut - aktivity\korycany-voda\repo` (`.git` na PC je starý a s GitHubem nesouvisí). Z relace běžící na PC zapisovat po pushi přímo tam. Z cloudové relace PC nedostupné (Remote Control složka se 14. 11. nezobrazila): po pushi připomenout uživateli `tools\aktualizuj_z_githubu.bat` (stáhne main, nic nemaže). PC-only rastry řeší `.bat` skripty.

## 3. Pozor při práci s repozitářem

- **Bot commituje do `main` 4× denně** (`.github/workflows/pocasi.yml`, zpráva `[bot] počasí YYYY-MM-DD`): mění `data/pocasi/*`, `index.html`, `prototyp/index.html`. Před pushem vždy `git pull --rebase`. Při konfliktu v `index.html` ho neřešit ručně - přegenerovat `python tools/build_dummy.py`.
- **`index.html` a `prototyp/index.html` se nikdy needitují ručně.** Zdroj = `tools/build_dummy.py` (HTML, CSS a JS aplikace jako šablona v Pythonu; vkládá Leaflet, `web/jadro.js` a zúžená data).
- **`data/opatreni.json` se needituje ručně.** Zdroj = `tools/build_opatreni.py`.
- Sekce "Doplnění z rešerše dobré praxe" v `docs/KATALOG-Z-S.md`, `KATALOG-U-P.md`, `KATALOG-L-LES-T-C.md` (mezi značkami RESERSE-START/END) generuje `tools/build_katalog_md.py`.
- Velká data (LAZ, TIF, GPKG, surové stahy) nejsou v gitu (`.gitignore`), jsou jen na PC uživatele v `repo\data\...`.
- Licence repa: kód MIT, data a texty CC BY 4.0; cizí zdroje nesou vlastní licenci (viz kap. 5).
- Síť: z prostředí Claude jsou blokované opendata.chmi.cz, SPÚ, rain1.fsv.cvut.cz, hladiny.cz, sap.pmo.cz a další státní portály. GitHub Actions na ně dosáhnou (ověřeno), SPÚ ne. Cesty: workflow v Actions, skript `.bat` na PC uživatele, nebo prohlížeč v aplikaci se souhlasem uživatele.

## 4. Architektura

```
PC uživatele (Python 3.14, Windows)        GitHub (main)                     Prohlížeč
-------------------------------------      ------------------------------    ---------------------------
LAZ, WFS, GML, CSV ČHMÚ                     data/*.geojson, *_info.json       index.html (jeden soubor)
  -> tools/01..14_*.py (.bat spouštěče)  ->  data/web/*.png + rastr.json   ->   Leaflet + jadro.js
  -> rastry repo\data\dmr\*.tif (mimo git)   data/opatreni.json                 fetch: data/web, geojson
                                             data/pocasi/* (bot, Actions)       živě: WMTS ČÚZK, RÚIAN
```

- Statický web, žádný backend, nic se neukládá. Stav Můj pozemek je v URL hash (`#pozemek?k=..&p=kod_ku:cislo,..&o=..&z=..&s=..&d=..&m=..`).
- Rastry pro web zůstávají v mřížce **S-JTSK** (EPSG:5514, 5 m, 1500 × 1600 buněk, x0 -562500, y1 -1170000). Převod WGS84 <-> S-JTSK dělá polynom 2. řádu v `data/web/rastr.json` (chyba < 2 mm uvnitř rastru, mimo neověřeno). Důvod: D8 a sousednost buněk platí jen v původní mřížce. Do mapy se kreslí převzorkováním v `Jadro.obrazek()`.
- Python skripty jsou záměrně bez GDAL/geopandas/whitebox/pysheds (numpy, scipy, rasterio, pyproj, sqlite3 + ruční WKB, xml.etree, regex na GML). Neměnit bez důvodu (instalace u uživatele, whitebox stahuje binárku z webu).

### Struktura repa

```
index.html, prototyp/index.html   GENEROVÁNO build_dummy.py (Pages)
stav.html                          veřejná stavová stránka, čísla natvrdo v HTML (při změně dat aktualizovat ručně)
web/jadro.js                       výpočetní jádro, běží v prohlížeči i v node
web/test_jadro.js                  testy jádra (node + pngjs), 40 testů
web/test.html                      technický prohlížeč jádra (povodí bodu, hráz, podklady)
tools/NN_*.py + vyrob_*.bat        datová příprava (kap. 6)
tools/build_*.py                   generátory JSON/MD/HTML
tools/aktualizuj_z_githubu.bat     aktualizace klonu na PC z GitHubu (uživatel poklepe)
tools/vendor/leaflet-1.9.4         Leaflet (BSD-2), vkládá se do HTML
.github/workflows/                 pocasi.yml (4× denně), normaly.yml, stahni-vstupy.yml
data/                              lehké odvozené vrstvy a JSON (v gitu)
data/web/                          rastrový balíček pro prohlížeč (5,4 MB, PNG překomprimované oxipng bez změny typu barev)
data/pocasi/                       denní data počasí (bot)
docs/                              sumáře: STAV, VRSTVY, JADRO, CN, SRAZKY, USLE, MERENI, KATALOG*, DATA-FORMAT, ROZHRANI, zadání UX
```

### Aplikace (`index.html`, 5 záložek, `data-tab`)

| záložka | obsah | hlavní funkce v build_dummy.py |
|---|---|---|
| `jakbylo` (výchozí) | datový příběh o počasí: srážky od 1921, srážky minus možný výpar, horko, lijáky, letošek, výhled CzechGlobe; grafy vlastní SVG, "Zvětšit" v `<dialog>` | `render`, `grafDenni`, `rocniky`, `stat`, `karta` |
| `pozemek` | průvodce 5 kroků: najdi dům (mapa, parcely od zoomu 16, hledání RÚIAN), 3 otázky (okapy, zpevněné plochy, půda), kolik odteče (+ skutečný déšť za 30 dní, přítok shora a upozornění), opatření jako dlaždice se hrou Kapka/Louže/Tůňka/Oáza (vč. jezírka T07), výsledek | `pz*`, `runoff`, `greenRunoff`, `EFF`, `evalMeasures`, `zadrzeni`, `renderPritok`, `tileHTML`, `recalc` |
| `uzemi` | Celé území v 5 kapitolách: domácnosti, velké střechy, pole/louky/les (SCS-CN + USLE scénáře + mapa eroze), hráz na potoce, velké projekty; jeden výběr deště nahoře | `renderUzemi`, `renderStrechy`, `krajinaHistogram`, `renderKrajina`, `erozeInit`, `erozeKresli`, `hrazInit`, `hrazSpocti` |
| `katalog` | 66 opatření, filtry KDE / CO ŘEŠÍM (sucho, příval, horko, život), dlaždice s náčrtky, "Kde to funguje", "Proč a jak", dotace se stavem podle data | `renderKatalog`, `katTile`, `jednoCislo`, `progStav`, `finText` |
| `model` | O modelu: co je hotové/chybí, metody, zdroje dat a licence, z čeho zaplatit, co model neumí | - |

Výchozí déšť: Můj pozemek 10 mm (běžný, ~17× ročně), Celé území 32 mm (N2 6h). Nabídka: 10 / 20 / 32 (N2) / 53 (N10) / 87 (N100) mm, navíc 26 mm/60 min a 94 mm (12. 6. 2012).

Do `index.html` se vkládá jako `D` (`__DATA__`): zúžený `opatreni.json`, `uzemi` (budovy_info, cn_info, srazky_chmi), `navrhove` (navrhove_srazky), `srazky_hist`, `cn_tabulka`, `pocasi` (denni.json + normaly.json). Až při otevření Můj pozemek nebo Celé území (`nactiMapovaData()`) se stahuje `data/web/*` (přes `Jadro.nacti`), `data/parcely.geojson` (4,4 MB, gzip 0,8 MB), `budovy.geojson`, `povodi.geojson`, `vyuziti_pudy.json`; `smer_v.png` a `toky.json` až při otevření hráze (`Jadro.nactiProNadrze()`). Jak bylo, Katalog a O modelu stahují jen `index.html`. Verze v hlavičce/patičce a datum počasí doplňuje build z `opatreni.json` a dat počasí (`__KATV__`, `__KATD__`, `__POCD__`).

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
| `12_pocasi.py` | (Actions) ČHMÚ recent + scrape PMO/Nemotice -> `pocasi/denni.json` (P, T, Tmin, Tmax, H, F, ET0, bil, zdroj_P) |
| `13_normaly_pocasi.py` | (Actions `normaly.yml`) historical_csv -> `pocasi/normaly.json`, doplňování mezer z okolních stanic; **v březnu 2027 spustit znovu** (ročník 2026) |
| `14_toky_vypaleni.py` | toky ČÚZK vypálené -2 m do DMR -> `smer_vypaleny.tif`, `data/web/toky.json` |
| `build_kachnik.py` | VOX + hodinové srážky -> `kachnik_2026.json` |
| `build_opatreni.py` -> `build_katalog_md.py` -> `build_dummy.py` | katalog -> JSON -> MD -> HTML |
| `stahni_vstupy.py` (Actions `stahni-vstupy.yml`, větev `vstupy`), `stahni_zdroje.py` | stahování surovin a archivu podkladů (mimo git) |

Po změně podkladových JSON (`budovy_info`, `cn_info`, `srazky_chmi`, `cn_tabulka`, `opatreni`) vždy znovu `build_dummy.py`. Po změně rastrů `09_balicek_web.py` a `node web/test_jadro.js`.

## 7. Území modelu

- Hranice: nahoře hráz VN Koryčany (odtok řízený, povodí nad hrází se nemodeluje), dole jez na Kyjovce před Mouchnicemi (X -560508, Y -1173975). **17,7 km²**, polygon `typ: uzemi_modelu` v `data/povodi.geojson`; body v `data/rozvodnice_body.json`.
- Rozvodnice z DMR ověřeny proti ČHP (ZABAGED) i kritickým bodům VÚV (shoda).
- Budovy jen obec Koryčany (rozhodnutí: model řeší jednu obec).
- Klíčová čísla (HSP VÚMOP): CN vážené 67,4; HSP A 11 / B 68 / C 11 / D 10 %; les 711 ha = 40 %, orná 545 ha; budov 1 631 (RD 1 075, v aplikaci RD + "bydlení" = 1 076); P40 = 74 tis. m³; USLE orná C 0,2 průměr 10,5 t/ha/rok, 45 % nad 9 t/ha.

## 8. Výpočetní jádro (`web/jadro.js` v0.3)

API `Jadro.*` (podrobně `docs/JADRO.md`):
- `nacti(base, opts)`, `lonLatNaXY`, `xyNaLonLat`, `lonLatNaBunku`
- `scsCN(P, CN, ia=0.2)`, `cnProIPS`, `vahyCN(qAPI)`, `vahaCN3`, `odtokVazeny` (vážení CN2/CN3 podle tvarů deště, Kavka 2023 tab. 6)
- `bunkyPolygonu`, `statBunek`, `statPolygon` (odtok se počítá **po buňkách a sčítá**, ne z průměrného CN)
- `povodiBodu` (zpětné D8), `prichytKToku`, `pritok(bunkyPozemku, maxBunek)` (cizí plocha nad pozemkem, `udolnice` >= 1 ha, `tok` >= 0,25 km²)
- `nadrz(lon, lat, h, opts)`: hráz jen na toku ČÚZK, osa kolmo na tok (max 300 m); povodí >= 0,25 km² = zátopa DMR, menší = tůň v údolnici jako rozsah A·L/3 až A·L/2; vrací `info`, `vodni_dilo` (> 2 m), `tbd`
- `obrazek`, `obalMasky` (překryvy pro Leaflet)

Metody mimo jádro (v `build_dummy.py`): zeleň pozemku SCS-CN podle HSP (bez sklonové úpravy - rozhodnuto), roční odtok ze zeleně z histogramu denních úhrnů 1991-2019, střechy a zpevněné plochy součinitel ČSN s počáteční ztrátou 1 mm, USLE scénáře (P06/P05 C 0,01, P04 C 0,1, P01 P 0,65/0,9), ET₀ Hargreaves-Samani (FAO-56 rov. 52).

Kontrolní hodnoty (musí sedět s Pythonem): území CN 67,4, P40 74 205 m³ (06_cn.py 74 206), Stříbrník CN 60,1, 4,23 km²; mapa eroze C 0,2 10,7 t/ha a 46 % nad 9 t/ha (`usle_info.json` 10,5 a 45 %, rozdíl = R průměr místo rastru). Spustit `node web/test_jadro.js` (potřebuje `pngjs`), musí vypsat VŠE OK.

## 9. Katalog opatření (`data/opatreni.json`, meta.verze 0.9, katalog v0.6)

- 66 opatření, 157 zdrojů, 10 programů, nástroje N01-N06, konstanty jádra. Formát: `docs/DATA-FORMAT.md`.
- ID: Z zahrada, S stavba/střecha, U obec, P pole, L louka, LES les, T tok, C cesta, M měření, H organizační při vedrech.
- Účinky: R retence, I infiltrace, Q špička odtoku, E výpar, CH ochlazení, ER eroze, B biodiverzita, W úspora vody.
- Každé číslo má zdroj a značku; `odhad` a `kvalitativne` se nikdy nesčítají. Ceny jen se zdrojem a rokem, jinak "cena neověřena".
- Pole pro UI: `hlavni_cislo` (ručně psaná věta, slovník HLAVNI_CISLO v build_opatreni.py), `priklady[]` ("Kde to funguje"), `prenositelnost`, `rizika`, `vahy_skaly` (rezerva).
- Doplňky se píšou funkcí `doplnit(id, ...)` na konci `build_opatreni.py`.
- Programy mají `od`/`do`, stav "otevřeno" se počítá v prohlížeči z data.

## 10. Jak přidat novou datovou vrstvu (postup)

1. Ověřit zdroj a licenci online, zapsat do `docs/VRSTVY.md` (URL, licence, datum, značka).
2. Jen pro zobrazení: WMS/WMTS přímo v Leafletu v `build_dummy.py`, s atribucí. Bez redistribuce.
3. Pro výpočet: skript `tools/NN_nazev.py` (stáhne bbox území nebo čte soubor z PC), převede na mřížku DMR (S-JTSK, 5 m, 1500 × 1600), výstup tif do `repo\data\dmr\` (mimo git) + lehký `data/nazev_info.json` + náhled `docs/img/nazev_nahled.png`. Spouštěč `vyrob_nazev.bat`.
4. Do balíčku: doplnit pásmo do `09_balicek_web.py` (8/16 bit PNG, kódování a licence do `rastr.json`). Pozor na velikost balíčku (mobil).
5. Načtení v jádru (`Jadro.nacti`), funkce + test v `web/test_jadro.js` proti Python výstupu.
6. UI v `build_dummy.py`, přegenerovat, zkontrolovat headless Chromium 1300 px a 390 px, světlý i tmavý režim, bez chyb v konzoli a bez vodorovného posunu.
7. Aktualizovat O modelu (zdroje dat), případně `stav.html`, a `docs/STAV.md`.

## 11. Otevřené úkoly

Aktuální pořadí je v `docs/STAV.md` (Další kroky). Trvale otevřené:
- Validace s daty Povodí Moravy; do té doby "nevalidováno".
- Transformace vlny poldrem (jádro zatím jen objemová bilance).
- Fáze 5: škola/expert + formulář měření (bez osobních údajů žáků; úložiště mimo GitHub Pages chybí).
- Neznámé: kanalizace jednotná/oddílná (S02, S06), kam odvádějí vodu velké střechy, meliorace (SPÚ), zpevněné plochy u domů.

Mimo rozsah do zveřejnění: projektová dokumentace staveb, výpočet dotačních žádostí, 3D, mobilní aplikace, 2D hydraulika intravilánu, data mimo povodí.

## 12. Fáze projektu

1 vymezení a inventura - hotovo | 2 datová příprava - hotovo | 3 jádro - rozpracováno (chybí vlna, bilance P-ET po scénářích) | 4 rozhraní občan - funkční, ve zkoušce s lidmi | 5 škola/expert + měření - nezačato | 6 validace a texty - katalog hotový, validace ne | 7 test s lidmi a zveřejnění - běží neformálně.
