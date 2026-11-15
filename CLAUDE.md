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
- **Dvě úrovně textu (laik / zvídavý), platí pro celý web:** nahoře krátká úderná věta s jedním jasným číslem pro laika; metoda, nejistota, p-hodnoty, kontroly, zdroje a delší výklad v rozbalovací části "Pro zvídavé" (`<details class="jb-cist">`). Raději přesunout víc do části pro zvídavé, než zahltit laika.
- Texty pro laiky uživatel před zveřejněním přepíše vlastními slovy: psát je krátké, držet je v šabloně pohromadě a snadno dohledatelné, nerozdrobovat je do složitých výrazů v JS.
- Uživatel má místní fotografie (se souhlasem autorů); pro web je dodá, do té doby s nimi počítat v rozvržení, nevymýšlet náhrady.
- Práce po uzavřených blocích (jeden blok = jeden hotový použitelný výstup). Na konci relace aktualizovat `docs/STAV.md` (jen aktuální stav: hotové, rozpracované, další kroky, platná rozhodnutí, otevřené otázky, předpoklady) a podrobný záznam relace připsat na začátek `docs/STAV-HISTORIE.md`. V odpovědi uživateli doplnit "na co ses nezeptal" a zvolené předpoklady.
- Když na úkol LLM není vhodný nástroj (ruční klikání ve státních portálech, 2D hydraulika, kalibrace bez dat), říct to a připravit podklady, ať to uživatel udělá sám.
- Klon na PC uživatele: `C:\Users\obcho\Desktop\Claude - zoofix\skaut - aktivity\korycany-voda\repo` (`.git` na PC je starý a s GitHubem nesouvisí). Z relace běžící na PC zapisovat po pushi přímo tam. Z cloudové relace PC nedostupné (Remote Control složka se 14. 11. nezobrazila): po pushi připomenout uživateli `tools\aktualizuj_z_githubu.bat` (stáhne main, nic nemaže). PC-only rastry řeší `.bat` skripty.

## 3. Pozor při práci s repozitářem

- **Bot commituje do `main` 4× denně** (`.github/workflows/pocasi.yml`, zpráva `[bot] počasí YYYY-MM-DD`): mění `data/pocasi/*`, `index.html`, `prototyp/index.html`. Před pushem vždy `git pull --rebase`. Workflow počasí a normálů pushují do větve, ze které běžely, a web generují až po stažení cizích změn; na větvi `claude/**` se dají vyzkoušet (normaly pushem, pocasi ručním spuštěním s `ref`). Při konfliktu v `index.html` ho neřešit ručně - přegenerovat `python tools/build_dummy.py`.
- **`index.html` a `prototyp/index.html` se nikdy needitují ručně.** Zdroj = `tools/build_dummy.py` (HTML, CSS a JS aplikace jako šablona v Pythonu; vkládá Leaflet, `web/jadro.js` a zúžená data).
- **`data/opatreni.json` se needituje ručně.** Zdroj = `tools/build_opatreni.py`.
- Sekce "Doplnění z rešerše dobré praxe" v `docs/KATALOG-Z-S.md`, `KATALOG-U-P.md`, `KATALOG-L-LES-T-C.md` (mezi značkami RESERSE-START/END) generuje `tools/build_katalog_md.py`.
- Velká data (LAZ, TIF, GPKG, surové stahy) nejsou v gitu (`.gitignore`), jsou jen na PC uživatele v `repo\data\...`.
- Licence repa: kód MIT, data a texty CC BY 4.0; cizí zdroje nesou vlastní licenci (viz `docs/PIPELINE.md`).
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
web/test_jadro.js                  testy jádra (`npm test`, 40 testů)
web/test.html                      technický prohlížeč jádra (povodí bodu, hráz, podklady)
tools/NN_*.py + vyrob_*.bat        datová příprava (`docs/PIPELINE.md`)
tools/build_*.py                   generátory JSON/MD/HTML
tools/aktualizuj_z_githubu.bat     aktualizace klonu na PC z GitHubu (uživatel poklepe)
tools/vendor/leaflet-1.9.4         Leaflet (BSD-2), vkládá se do HTML
.github/workflows/                 pocasi.yml (4× denně), normaly.yml, hydro.yml, vypar.yml, inventura-zdroju.yml, stahni-vstupy.yml
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

## 5. Data a skripty

Tabulky datových zdrojů s licencemi, pořadí skriptů `tools/` a postup pro novou vrstvu jsou v **`docs/PIPELINE.md`** (číst před prací s daty). Další vrstvy a stav ověření licencí: `docs/VRSTVY.md`. Stručně:

- Měřená data ČHMÚ (Actions): srážky Koryčany od 1921, teplota / vlhkost / vítr Nemochovice od 2001, sluneční svit Staré Město / Kroměříž / Holešov, prameny (Koryčany PB0425) a průtok Kyjovky nad nádrží.
- Workflow: `pocasi.yml` (4× denně, `12_pocasi.py`), `normaly.yml` (`13_normaly_pocasi.py`, znovu v březnu 2027), `hydro.yml` + `build_hydro.py`, `vypar.yml` + `build_vypar.py`, `testy.yml`, `inventura-zdroju.yml`, `stahni-vstupy.yml`. Workflow spouštěné pushem do `claude/**` slouží k práci z cloudu (servery jsou z Claude blokované).
- Generátory: `build_opatreni.py` -> `build_katalog_md.py` -> `build_dummy.py`. Po změně podkladových JSON vždy znovu `build_dummy.py`; po změně rastrů `09_balicek_web.py` a testy.
- **Před zabalením nové vrstvy do repa ověřit licenci a zapsat ji do `docs/VRSTVY.md`.** Půda HSP VÚMOP je CC BY-NC; data PMO, hladiny.cz a VOX jen jako agregace; Intersucho CC BY-NC-ND (jen odkaz).
- Kontrola UI po každé změně: headless Chromium 1300 px a 390 px, světlý i tmavý režim, bez chyb v konzoli a bez vodorovného posunu.

## 6. Území modelu

- Hranice: nahoře hráz VN Koryčany (odtok řízený, povodí nad hrází se nemodeluje), dole jez na Kyjovce před Mouchnicemi (X -560508, Y -1173975). **17,7 km²**, polygon `typ: uzemi_modelu` v `data/povodi.geojson`; body v `data/rozvodnice_body.json`.
- Rozvodnice z DMR ověřeny proti ČHP (ZABAGED) i kritickým bodům VÚV (shoda).
- Budovy jen obec Koryčany (rozhodnutí: model řeší jednu obec).
- Klíčová čísla (HSP VÚMOP): CN vážené 67,4; HSP A 11 / B 68 / C 11 / D 10 %; les 711 ha = 40 %, orná 545 ha; budov 1 631 (RD 1 075, v aplikaci RD + "bydlení" = 1 076); P40 = 74 tis. m³; USLE orná C 0,2 průměr 10,5 t/ha/rok, 45 % nad 9 t/ha.

## 7. Výpočetní jádro (`web/jadro.js` v0.3)

API `Jadro.*` (podrobně `docs/JADRO.md`):
- `nacti(base, opts)`, `lonLatNaXY`, `xyNaLonLat`, `lonLatNaBunku`
- `scsCN(P, CN, ia=0.2)`, `cnProIPS`, `vahyCN(qAPI)`, `vahaCN3`, `odtokVazeny` (vážení CN2/CN3 podle tvarů deště, Kavka 2023 tab. 6)
- `bunkyPolygonu`, `statBunek`, `statPolygon` (odtok se počítá **po buňkách a sčítá**, ne z průměrného CN)
- `povodiBodu` (zpětné D8), `prichytKToku`, `pritok(bunkyPozemku, maxBunek)` (cizí plocha nad pozemkem, `udolnice` >= 1 ha, `tok` >= 0,25 km²)
- `nadrz(lon, lat, h, opts)`: hráz jen na toku ČÚZK, osa kolmo na tok (max 300 m); povodí >= 0,25 km² = zátopa DMR, menší = tůň v údolnici jako rozsah A·L/3 až A·L/2; vrací `info`, `vodni_dilo` (> 2 m), `tbd`
- `obrazek`, `obalMasky` (překryvy pro Leaflet)

Metody mimo jádro (v `build_dummy.py`): zeleň pozemku SCS-CN podle HSP (bez sklonové úpravy - rozhodnuto), roční odtok ze zeleně z histogramu denních úhrnů 1991-2019, střechy a zpevněné plochy součinitel ČSN s počáteční ztrátou 1 mm, USLE scénáře (P06/P05 C 0,01, P04 C 0,1, P01 P 0,65/0,9), ET₀ Penman-Monteith FAO-56 (`et0_pm` v `12_pocasi.py`: teplota, vlhkost, vítr Nemochovice, sluneční svit Staré Město / Kroměříž / Holešov; bez svitu záření z rozpětí teplot). Hargreaves-Samani (`et0_hs`) zůstává jen pro srovnání, pro Koryčany nadhodnocuje o ~23 %.

Kontrolní hodnoty (musí sedět s Pythonem): území CN 67,4, P40 74 205 m³ (06_cn.py 74 206), Stříbrník CN 60,1, 4,23 km²; mapa eroze C 0,2 10,7 t/ha a 46 % nad 9 t/ha (`usle_info.json` 10,5 a 45 %, rozdíl = R průměr místo rastru). Testy: `npm install && npm test` (jen knihovna `pngjs` na čtení rastrů), musí vypsat VSE OK; na GitHubu je pouští `testy.yml` při změně jádra nebo rastrů.

## 8. Katalog opatření (`data/opatreni.json`, meta.verze 0.9, katalog v0.6)

- 66 opatření, 157 zdrojů, 10 programů, nástroje N01-N06, konstanty jádra. Formát: `docs/DATA-FORMAT.md`.
- ID: Z zahrada, S stavba/střecha, U obec, P pole, L louka, LES les, T tok, C cesta, M měření, H organizační při vedrech.
- Účinky: R retence, I infiltrace, Q špička odtoku, E výpar, CH ochlazení, ER eroze, B biodiverzita, W úspora vody.
- Každé číslo má zdroj a značku; `odhad` a `kvalitativne` se nikdy nesčítají. Ceny jen se zdrojem a rokem, jinak "cena neověřena".
- Pole pro UI: `hlavni_cislo` (ručně psaná věta, slovník HLAVNI_CISLO v build_opatreni.py), `priklady[]` ("Kde to funguje"), `prenositelnost`, `rizika`, `vahy_skaly` (rezerva).
- Doplňky se píšou funkcí `doplnit(id, ...)` na konci `build_opatreni.py`.
- Programy mají `od`/`do`, stav "otevřeno" se počítá v prohlížeči z data.

## 9. Otevřené úkoly

Aktuální pořadí je v `docs/STAV.md` (Další kroky). Trvale otevřené:
- Validace s daty Povodí Moravy; do té doby "nevalidováno".
- Transformace vlny poldrem (jádro zatím jen objemová bilance).
- Fáze 5: škola/expert + formulář měření (bez osobních údajů žáků; úložiště mimo GitHub Pages chybí).
- Neznámé: kanalizace jednotná/oddílná (S02, S06), kam odvádějí vodu velké střechy, meliorace (SPÚ), zpevněné plochy u domů.

Mimo rozsah do zveřejnění: projektová dokumentace staveb, výpočet dotačních žádostí, 3D, mobilní aplikace, 2D hydraulika intravilánu, data mimo povodí.

## 10. Fáze projektu

1 vymezení a inventura - hotovo | 2 datová příprava - hotovo | 3 jádro - rozpracováno (chybí vlna, bilance P-ET po scénářích) | 4 rozhraní občan - funkční, ve zkoušce s lidmi | 5 škola/expert + měření - nezačato | 6 validace a texty - katalog hotový, validace ne | 7 test s lidmi a zveřejnění - běží neformálně.
