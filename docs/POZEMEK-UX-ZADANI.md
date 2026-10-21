# Zadání: přestavba záložky „Můj pozemek“ (UX), 21. 10. 2026

Navazuje na: `docs/ROZHRANI.md` (návrh v0.1, 18. 10.), `docs/STAV.md`, `docs/JADRO.md`, `docs/KATALOG.md`, `data/opatreni.json`. Zdroj pravdy pro HTML je `tools/build_dummy.py` (generuje `index.html` i `prototyp/index.html`; HTML nikdy needitovat ručně).

## Proč
„Můj pozemek“ má být jádro webu: občan zjistí, co se s vodou děje na jeho pozemku, a co může udělat. Dnes to tak nefunguje (zpětná vazba uživatele 21. 10.):
- mapa je malá a prvonávštěvník neví, co s ní má dělat,
- kroky 1-5 jsou rozházené po stránce,
- Krok 1 (kde) s instrukcemi se krčí pod mapou, kroky 2-5 jsou vpravo, pořadí není vidět.

## Současný stav (co tam je a funguje - zachovat logiku, změnit uspořádání)
- Rozvržení: `<section id="tab-pozemek" class="grid two">`, vlevo mapa (`#map`, 340 px, od 900 px šířky 520 px) + panel „Krok 1 - kde“, vpravo panely Krok 2-5. CSS proměnné, světlý i tmavý režim, písma Fraunces / IBM Plex.
- Mapa: Leaflet, podklad ČÚZK ZTM (WMTS) + ortofoto (WMS) přepínač. Klik = `vyberParcelu()` (parcely ČÚZK `data/parcely.geojson`, kreslí se od zoomu 16, toggle, sčítá se: výměra, půdorysy budov) a `odvodZMapy()` (sklon DMR 5G průměr 15 m, půda A-D z BPEJ s příznakem odhad, složení okolí 30 m ze ZABAGED) přes `web/jadro.js` (rastry `data/web/`).
- Krok 2 - co tu je: střecha m², zpevněné m² + typ, zelené m² + typ (trávník / se záhony), svody (kanalizace / pozemek / nevím), sklon %, půda (zkouška vsaku 30 min, A-D), déšť (N2 32 / N10 53 výchozí / N100 87 mm 6 h; 20 mm; 26 mm ČSN; 94 mm 12. 6. 2012). Výměry se předvyplní z vybraných parcel, zpevněné zadává člověk.
- Krok 3 - co se děje při dešti: tabulka toku vody, pruhy „odteče / zůstane“, roční bilance (zeleň SCS-CN z histogramu denních úhrnů, střechy a zpevněné součinitele ČSN + 1 mm počáteční ztráta).
- Krok 4 - co můžeš udělat: karty opatření z katalogu (zaškrtávací), řazení „nejvíc vody za nejmíň práce“, „Nehodí se sem“.
- Krok 5 - shrnutí + „Na co to nestačí“ (měřítko pozemek vs. území).
- Nic se neukládá, vlastníci se nenačítají (pravidlo projektu).

## Cíl nového uspořádání (k ověření a domyšlení v novém chatu)
1. Prvonávštěvník do 5 sekund pochopí, co má udělat: „Najdi svůj dům a klikni na něj“ (případně hledání adresy - geokodér ČÚZK/RÚIAN, licence a dostupnost ověřit online).
2. Jeden jasný postup krok za krokem, viditelný průběh (1 kde -> 2 co tu je -> 3 co se děje -> 4 co udělat -> 5 výsledek), žádné rozházené panely.
3. Mapa velká tam, kde je potřeba (výběr místa), a ustoupí, když člověk vyplňuje a čte výsledky.
4. Mobil první (lidé budou stát na zahradě s telefonem): mapa přes celou šířku, panel zespodu nebo pod mapou, velké klikací plochy, žádné vodorovné posouvání.
5. Výsledek musí být motivační a srozumitelný bez odborných pojmů (CN, SCS-CN, HSP patří do „Jak se to počítá“ / O modelu).
6. Zachovat poctivost: značky původu (✅ 🤔 📄), „Nehodí se sem“, „Na co to nestačí“, upozornění „zjednodušený model, nevalidováno“.
7. Stav v URL hash (sdílitelný odkaz) a nic osobního se neukládá - beze změny pravidla.

## Postup v novém chatu
1. Načíst `docs/STAV.md`, tento soubor, `docs/ROZHRANI.md`; projít současnou záložku v prohlížeči (desktop 1300 px i mobil 390 px, světlý i tmavý režim), udělat snímky.
2. UX rozbor: kdo přijde (občan z odkazu na webu města / letáku / školy), co chce vědět, kde se zasekne. Seznam problémů s prioritou.
3. Návrh 2-3 variant uspořádání (drátěný náčrt / skica v artefaktu), uživatel vybere. Teprve pak kód.
4. Přestavba v `tools/build_dummy.py` po blocích, po každém bloku ověření v headless prohlížeči (desktop + mobil), push na GitHub a zápis stejných souborů do `repo` na PC.
5. Na konci: STAV.md, ROZHRANI.md (nová verze), „na co ses nezeptal“.

## Omezení
- Jeden HTML soubor bez backendu, Leaflet (vendor), data z `data/`. Žádné nové knihovny bez důvodu.
- Výpočty se nemění (jen přesun a texty), pokud se nedohodne jinak. Kontrola: `node web/test_jadro.js` VŠE OK.
- Nepoužívat dlouhé pomlčky, jen spojovník „-“ (i v HTML).
