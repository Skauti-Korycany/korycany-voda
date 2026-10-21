# Zadání: rozšíření katalogu opatření o příklady dobré praxe (rešerše), 21. 10. 2026

Navazuje na: `docs/STAV.md`, `docs/KATALOG.md` (seznam a atributy, v0.2), `docs/KATALOG-Z-S.md`, `docs/KATALOG-U-P.md`, `docs/KATALOG-L-LES-T-C.md` (kvantifikace), `docs/DATA-FORMAT.md`, `data/opatreni.json` v0.4 (58 opatření, zdroj pravdy `tools/build_opatreni.py`).

## Cíl
Najít v kvalitních zdrojích (hlavně zahraničních, z podobných klimatických podmínek) další opatření a **příklady dobré praxe** pro:
1. **hospodaření s vodou** - zadržení, vsak, zpomalení odtoku, využití dešťové vody, voda v půdě a v krajině,
2. **ochlazování při vlnách veder** - stín, výpar, světlé povrchy, voda ve městě, chladná místa.

**Nejde o dotace.** Financování se neřeší. Jde o to, co funguje, kde to někdo udělal, s jakým změřeným účinkem a jestli se to dá přenést do Koryčan.

## Kontext Koryčan (pro posouzení přenositelnosti)
- Malé město na úpatí Chřibů, 225-534 m n. m., území modelu 17,7 km² (40 % les, orná, louky, zahrady, intravilán).
- Srážky 632 mm/rok (ČHMÚ Koryčany 1991-2020); běžný déšť 10 mm asi 17× za rok, 20 mm asi 5×; návrhové 6h N10 53 mm.
- Sucho a horko: bilance P-ET₀ záporná ve všech letech 2001-2025, 2026 leden-září nejsušší z 90 let řady; tropických dní 12 -> 18 za rok, 2026 28 dní, max 37,4 °C (data v `docs/STAV.md`, sekce Počasí).
- Půdy: převážně HSP B, část C a D (těžké, pelozemě), svahy (průměrný sklon 9,4°); niva Kyjovky a Stříbrníku s mokřinami.
- Kdo bude opatření dělat: jednotlivci na zahradě a domě, obec, škola (Ekoškola), spolky (skauti), vlastníci půdy a lesa, správci toků. **Ne** pachtýři-zemědělci jako cílová skupina.

## Kde hledat (návrh, doplnit)
- Podobné klima: střední Evropa s ročními srážkami ~500-750 mm, letními přívalovými dešti a vlnami veder - Rakousko (Weinviertel, Dolní Rakousko, Vídeň), Slovensko (Záhorie, Trnavsko, Bratislava), Maďarsko, Slovinsko, jižní Polsko, Sasko, Durynsko, Bavorsko, Braniborsko; pro horko i města s horším klimatem, pokud je opatření přenositelné do malého města.
- Typy zdrojů (pořadí kvality): recenzované studie s měřením; národní a regionální agentury (UBA, BOKU, SHMÚ, VÚVH, IMGW...); EU platformy s případovými studiemi (EEA Climate-ADAPT, katalog NWRM přírodě blízkých opatření); městské metodiky (Vídeň Schwammstadt a Hitzeaktionsplan, Kodaň cloudburst, Lipsko, Mnichov) 💻 - existenci a obsah ověřit, z paměti nic nepřebírat.
- Příklady dobré praxe ideálně z posledních ~10 let; fyzikální a hydrologické metody mohou být starší.

## Pravidla (beze změny z projektu)
- Stručně, jasně. Žádné dlouhé pomlčky, jen spojovník „-“.
- Značky původu u každého faktického tvrzení a odkazu: ✅ otevřeno v této relaci, 📄 citace z druhé ruky, 🤔 odhad, 💻 z paměti neověřeno, ⏳ zdroj starší než 12 měsíců. ✅ jen tomu, co chat skutečně otevřel.
- Nikdy nevymýšlet název, autory, rok, DOI ani čísla. Když zdroj nejde dohledat: „nedohledal jsem“, nenahrazovat podobným.
- Účinek bez zdroje se do katalogu nedostane, nebo jen slovně jako „odhad“.
- Nejistotu jako rozsah, ne jedno číslo; vždy podmínky (klima, půda, měřítko), za kterých bylo měřeno.
- Před začátkem si říct o podklady, které chybí; nedomýšlet je. Když na něco LLM není vhodný nástroj (např. placené databáze, klikání v portálech), říct to rovnou a připravit postup pro uživatele.
- Práce po uzavřených blocích; každý blok = hotový, použitelný výstup.

## Postup
1. Načíst `docs/STAV.md`, tento soubor, `docs/KATALOG.md`, `docs/KATALOG-*.md`, `docs/DATA-FORMAT.md` a seznam opatření z `data/opatreni.json` (58 položek, kategorie Z, S, U, P, L, LES, T, C, M). **Duplicity nevytvářet**: když rešerše najde příklad k existujícímu opatření, doplní ho k němu (nový doklad účinku, příklad praxe), ne jako nové opatření.
2. Navrhnout plán bloků a zeptat se uživatele. Návrh:
   - A: horko v obci (stín, stromy, voda, povrchy, chladná místa, organizační opatření při vlnách veder),
   - B: voda na soukromém pozemku a domě,
   - C: veřejný prostor obce a škola,
   - D: krajina - louky, pole vlastníků, les, toky a niva.
3. Každý blok: rešerše -> `docs/KATALOG-RESERSE.md` (doplňuje se po blocích) -> odsouhlasení uživatelem. Teprve potom zápis do `tools/build_opatreni.py` (zdroj pravdy), přegenerování `data/opatreni.json`, `python tools/build_dummy.py`, `node web/test_jadro.js` (VŠE OK), kontrola aplikace (desktop + mobil), push na GitHub a zápis stejných souborů do složky `repo` na PC.
4. Na konci: STAV.md, KATALOG.md (nová verze), „na co ses nezeptal“ a zvolené předpoklady.

## Formát jedné položky v `docs/KATALOG-RESERSE.md`
- **Návrh ID a název** (nové ID navazuje v kategorii, např. Z12, U08; nebo „doplněk k Z06“)
- místo (Z/S/U/P/L/LES/T/C), rozhoduje (J/V/O/SP/Š), pracnost (1/2/3), účinky (R/I/Q/E/CH/ER/B/W) - stejné číselníky jako `opatreni.json`
- Co to je (1-2 věty, srozumitelně pro občana)
- Změřený účinek: rozsah + jednotky + podmínky měření + zdroj se značkou
- Příklad dobré praxe: kde, kdy, kdo, odkaz se značkou; případně foto/dokumentace k nahlédnutí
- Přenositelnost do Koryčan: klima, půda HSP, sklon, měřítko; kdy se nehodí („Nehodí se sem“)
- Rizika a co z toho neplyne (např. „ochladí povrch, ne vzduch v ulici“)
- Cena jen pokud je ve zdroji (se zdrojem a rokem), jinak vynechat
- Co se nepodařilo dohledat

## Otevřené otázky k rozhodnutí s uživatelem na začátku
- Mají do katalogu patřit i **organizační opatření při vlnách veder** (pitné fontány, chladná místa ve veřejných budovách, varovný systém, úprava časů prací a akcí)? Dnes katalog obsahuje jen fyzická opatření a měření (M).
- Kolik nových položek je cílem (rozsah práce a limity)? Návrh: kvalita před počtem, 3-8 na blok.
- Zobrazovat příklady dobré praxe v aplikaci (karta opatření „Kde to funguje“ s odkazem)? Pokud ano, přidat pole do formátu JSON (`priklady`) a do `DATA-FORMAT.md`.
