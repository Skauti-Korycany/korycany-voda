# korycany-voda

Jak zlepšit připravenost a odolnost města Koryčany na nedostatek vody, vysoké teploty a extrémy počasí.

Osvětová webová aplikace pro obyvatele Koryčan (Koryčany, Jestřabice, Blišice, Lískovec): reálná data o krajině + katalog opatření, která může udělat jednotlivec, vlastník půdy, obec nebo škola, s poctivě doloženým účinkem, cenou a zdrojem. Nositel: skautský oddíl Hříběcí hory, Koryčany. Partner: ZŠ Koryčany (Ekoškola). Nekomerční, veřejné.

**Stav (19. 10. 2026):** hotový katalog 58 opatření jako data, návrh rozhraní a drátěný prototyp na syntetickém pozemku. Terénní a půdní vrstvy (DMR 5G, VÚMOP) teprve přijdou. Podrobně `docs/STAV.md`.

## Struktura

```
index.html            prototyp (kopie prototyp/index.html) - pro GitHub Pages
prototyp/index.html   drátěný náhled: syntetický pozemek, skutečný katalog, mapa ČÚZK
data/opatreni.json    katalog opatření (zdroje, účinky, ceny, dotace, nástroje, konstanty)
data/opatreni.schema.json
tools/build_opatreni.py   ZDROJ PRAVDY pro data - generuje data/*.json
tools/build_dummy.py      generuje prototyp z data/opatreni.json
tools/vendor/leaflet-1.9.4/  Leaflet (BSD-2), vložený do prototypu
docs/                 sumáře: stav, katalog s odůvodněním a zdroji, vrstvy, formát dat, rozhraní
```

## Jak s tím pracovat

```
python tools/build_opatreni.py   # upravils katalog ve skriptu -> přegeneruje data/
python tools/build_dummy.py      # přegeneruje prototyp/index.html a index.html
```
Vyžaduje jen Python 3 (standardní knihovna). Prototyp otevři přímo v prohlížeči; podklad ČÚZK se načítá živě.

## Zásady
- Každé číslo má zdroj a značku původu: ✅ ověřeno online v uvedený den, ✅⏳ zdroj starší 12 měsíců, 📄 citace z druhé ruky, 🤔 odhad. Odhady a kvalitativní účinky se nikdy nesčítají.
- Ceny jen se zdrojem a datem, jinak "cena neověřena".
- Aplikace vždy řekne i to, na co opatření nestačí. Nikdy netvrdí, že drobná opatření ochrání před povodní na Kyjovce.
- Zjednodušený model pro osvětu a rozhodování, ne projektová dokumentace. Nevalidováno, dokud nebude porovnání s měřením.
- Žádné osobní údaje (žáci, vlastníci, adresy) v datech ani v sumářích.

## Licence
Kód: MIT (`LICENSE`). Data v `data/` a texty v `docs/`: CC BY 4.0 (`LICENSE-DATA`), citované zdroje mají vlastní licence uvedené u každé položky. Mapové podklady: ČÚZK - on-line (CC BY 4.0 pro otevřená data). Leaflet: BSD-2 (`tools/vendor/leaflet-1.9.4/LICENSE`).
