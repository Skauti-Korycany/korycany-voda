# Návrh rozhraní aplikace (v0.2, 21. 10. 2026; v0.1 18. 10. 2026)

Změny v0.2: záložka Můj pozemek je průvodce po krocích (kap. 2.3, přestavba podle `POZEMEK-UX-ZADANI.md`, varianta A); upozornění aplikace je jeden rozbalovací řádek; hledání adresy RÚIAN; stav v odkazu. Zdroj pravdy HTML: `tools/build_dummy.py`.

Vychází z: 00-instrukce-projektu.md (kap. 3, 5), KATALOG.md kap. 12 (dva režimy), data/opatreni.json v0.3, NAPADY-ROZHRANI.md (posuvníky, zatím ne). Drátěný náhled: `prototyp/index.html` (syntetický pozemek, skutečný katalog).

## 1. Zásady
1. Jedno jádro (JS modul `jadro.js`), dvě obálky: Občan (výchozí) a Škola/Expert (přepínač). Stejné výpočty, expert vidí navíc vzorce, zdroje, vrstvy, surová čísla a může zadávat měření.
2. Každé číslo nese značku původu (✅ ✅⏳ 📄 🤔) a kliknutím ukáže zdroj. Kvalitativní účinky se zobrazují slovně a nikdy nevstupují do součtů.
3. Aplikace vždy řekne i to, na co opatření nestačí (věta "Nehodí se sem" a "Na co to nestačí").
4. Pořadí filtrů: místo -> data (vhodnost) -> preference uživatele (později posuvníky). Žádný krok nesmí uživatele nutit zadávat, co se dá z dat odvodit.
5. Jeden HTML soubor + složka `data/` (opatreni.json, GeoJSON vrstvy, PNG/COG dlaždice). Žádný backend. Stav (vybraná parcela, zadané plochy, zvolená opatření) v URL hash, aby šel poslat odkazem; pohodlí (poslední režim, zavřené nápovědy) v localStorage s try/catch.
6. Mobil první: mapa přes celou šířku, panel zespodu vysouvací. Na mobilu se počítá, že člověk stojí na pozemku a kouká do telefonu.
7. Když WMS státu nejede, aplikace funguje dál s vlastními vrstvami a napíše "podklad ČÚZK nedostupný".

## 2. Struktura obrazovek

```
[Úvod]  [Mapa]  [Můj pozemek]  [Celé území]  [Katalog]  [O modelu]        (přepínač: Občan | Škola/Expert)
```

### 2.1 Úvod (první návštěva, pak přeskočitelný)
- Jedna obrazovka, tři věci: (a) graf "co se stalo s vodou v Koryčanech" (blok D: epizody léta 2026 z čidla u Kachníku + srážky; později Povodí Moravy tehdy vs. dnes), (b) věta o účelu ("udržet vodu z přívalů v krajině, ne ji za hodinu poslat korytem"), (c) dvě tlačítka: "Co můžu udělat na svém" (-> Můj pozemek) a "Co může udělat obec" (-> Celé území).
- Viditelné upozornění: zjednodušený model, nevalidováno, ne projektová dokumentace.

### 2.2 Mapa (společný podklad obou režimů)
- Podklad: ČÚZK ZTM WMTS / Ortofoto WMS (přepínač). Vlastní vrstvy (zapínatelné, s legendou a zdrojem):
  - hranice modelu, intravilány, dílčí povodí sídel (GeoJSON z fáze 2)
  - sklon, akumulace odtoku / údolnice, deprese (PNG dlaždice z DMR)
  - půda: HSP A-D (až budou data VÚMOP; do té doby vrstva chybí a aplikace to říká)
  - LPIS DPB + erozní ohroženost SEO/MEO (WMS MZe, ověřit)
  - toky, nádrže (DIBAVOD), hlásné profily a čidlo Kachník (body)
  - historie: II./III. vojenské mapování (WMS CENIA) s posuvníkem průhlednosti - "kde byly tůně a mokřady"
  - expert navíc: hydrogeologie ČGS (4326), OPRL LVS, ZABAGED polohopis
- Klik do mapy = výběr místa pro režim Můj pozemek (bod + automaticky odvozená "plocha vlivu": parcela z katastru WMS, pokud jede; jinak kruh / ručně nakreslený polygon).

### 2.3 Můj pozemek (režim občan) - průvodce po krocích (v0.2, 21. 10. 2026)
Cíl: prvonávštěvník z letáku nebo webu města do 5 sekund ví, co dělat, a do minuty vidí, kolik vody mu při lijáku uteče a co s tím. Mobil první (člověk stojí na zahradě s telefonem). Přímý odkaz: `#pozemek`.

Rozvržení:
- Nahoře pruh průběhu 1 Kde - 2 Co tu je - 3 Při dešti - 4 Co udělat - 5 Výsledek (kroky klikací po výběru pozemku). Dole přilepené Zpět / Dál (popisek říká, kam vede).
- Mapa velká jen v kroku 1 (mobil přes šířku a skoro výšku okna, desktop 7/11 šířky vedle úvodního textu). Od kroku 2 se zmenší na náhled vybraného pozemku (mobil 120 px nad obsahem, desktop 260 px přilepená vlevo); klepnutí na ni = Změnit místo.
- Krok 1 - Kde: pokyn „Najdi svůj dům a klepni na něj. Pak klepni i na zahradu a dvůr“; hledání adresy nebo parcely (vyhledávací služba RÚIAN ČÚZK, našeptávač omezený na Koryčany a místní části); „Jsem tady“ (poloha telefonu, jen posun mapy); odkaz „Nechci mapu, zadám plochy ručně“. Po výběru hned první číslo: kolik odteče ze střech při velkém lijáku.
- Krok 2 - Okapy a půda (nadpis „Střechy, dlažba a půda“): pod malou mapou box „Z map víme“ (sklon, půda, okolí; zdroje a souřadnice až po „podrobnosti“); otázky s tlačítky: kam vedou okapy, kolik je dlažby (0 / 20 / 60 / 150 m²), pak „Upřesnit čísla“, nakonec půda (předvyplněno z mapy, zkouška vsaku rozbalovací). Méně textu a značek na první pohled, zdroje zůstávají v rozbalovacích částech.
- Krok 3 - Při dešti: volba deště (častý 32 / velký 53 / extrémní 87 mm, další v „Jak se to počítá“), kolik spadne, kolik odteče a odkud nejvíc, rok. Tabulka s CN, součiniteli a vážením nasycení jen v „Jak se to počítá“.
- Krok 4 - Co udělat: průběžný součet, 3 opatření s nejvíc vodou za nejmíň práce, „Další možnosti“, „Nehodí se sem“ s důvodem. Karta: název, pracnost, cena, povolení, efekt v m³, zdroje a financování rozbalovací.
- Krok 5 - Výsledek: motivační box (m³ z lijáku, přirovnání, za rok, 200 domácností), pruhy teď / s opatřeními, „Na co to nestačí“, Poslat odkaz, odkazy na Celé území a Katalog.

Poctivost beze změny: značky ✅ ✅⏳ 📄 🤔 u čísel, „Nehodí se sem“, „Na co to nestačí“, upozornění „zjednodušený model, nevalidováno“ v hlavičce i ve výsledku. Bez výběru pozemku se nezobrazují žádná čísla (krok 2-5 zamčené); v ručním režimu je příklad výslovně označený.

Stav v odkazu: `#pozemek?k=krok&p=kod_ku:cislo,...&o=okapy&z=dlažba_m2&s=A-D&d=déšť_mm&m=opatření.oddělená.tečkou` (ruční režim navíc `r` střecha, `g` zeleň). Nic se neukládá; odkaz obsahuje čísla parcel a odpovědi a posílá ho jen uživatel.

Návaznost na Celé území: v kroku 5 tlačítko „Co kdyby to udělali i ostatní?“ otevře Celé území v režimu „Jedna domácnost: jako můj pozemek“ (plochy, půda, okapy a opatření z průvodce, déšť se předá); přepínač vrací „průměrná v obci“.

Výpočet (jádro, součinitele, SCS-CN, katalog) se přestavbou nezměnil.

### 2.4 Celé území (režim občan i obec)
- Mapa s dílčími povodími sídel (Koryčany, Jestřabice, Blišice, Lískovec) a profilem na Kyjovce pod městem.
- Scénář "kolik lidí se zapojí": posuvník 0-100 % domácností (základ: počet střech/adres ze ZABAGED), výběr balíčku (S02+Z01, +S01, +Z04) -> součet m³ při 20 mm a za rok, na dílčí povodí i celek.
- Kontextová opatření (kontext=true: T04, T07, LES03, U05 velké): zobrazená jako "co musí udělat obec / Povodí / vlastník lesa", s objemem z DMR (nádrž při zvolené hrázi) a cenou se zdrojem; bez tvrzení o účinku na povodeň, pokud není doloženo.
- Povinný blok "Na co to nestačí": porovnání součtu drobných opatření s objemem návrhového deště na celé povodí a s objemem nádrže; věta "na povodeň na Kyjovce drobná opatření nestačí, na vodu v půdě ano".
- Eroze (pole): pro vybraný DPB USLE výsledek (A vs. Gp 2/9 t/ha) a co změní zatravnění, pásy, vrstevnice (C, P faktory). R faktor z kalkulačky VÚMOP (doplnit do konstant).

### 2.5 Katalog
- Prohlížení opatreni.json bez mapy: filtr místo, kdo rozhoduje, pracnost, účinek, povolení, financování (jen otevřené / všechny). Karta jako v Můj pozemek + sekce zdroje a "nedohledáno". Tisk/PDF celého katalogu = náhrada "čitelného katalogu pro lidi".
- Později: posuvníky škál (NAPADY-ROZHRANI.md), až budou váhy.

### 2.6 Škola / Expert (přepínač, fáze 5)
- Všechno výše + u každého čísla vzorec a vstupy; vrstvy navíc; export CSV výpočtu.
- Měření (M01-M06): formulář bod v mapě + hodnota + datum + foto (bez osobních údajů; identifikace jen "třída/skupina"). Úložiště: sdílená databáze, nebo export CSV do repozitáře (rozhodnout ve fázi 5). Zobrazení: body v mapě, časová řada na místě.

### 2.7 O modelu
- Metodika zkráceně, seznam vrstev se zdroji a licencemi (VRSTVY.md), seznam zdrojů (z JSON), stav validace ("nevalidováno" dokud není porovnání s měřením), verze dat, kontakt na oddíl, licence.

## 3. Co jádro počítá (fáze 3) - minimum pro verzi 1
1. Odtok z ploch: V = A × P × C pro 20 mm, návrhový déšť p=0,2 (24 h), rok. Konstanty z JSON.
2. Účinek zvolených opatření na pozemku: podle `kvantifikace.typ == vzorec` (Z01, Z03, Z04, Z10, S01, S02, S03, U02, U03, C01) a `hodnota` (S03 retence %, P04 ztráta půdy). Výsledek "před/po" jako rozsah, ne bod.
3. Součet za povodí: N domácností × průměrný pozemek (ze ZABAGED: medián plochy střechy v sídle) × balíček.
4. USLE pro DPB: A = R K LS C P; LS z DMR, K z BPEJ (až bude), C a P z JSON; porovnání s Gp.
5. Objem nádrže/tůně z DMR při zadané kótě hráze (kontext).
6. Chlazení a vítr: jen zobrazení doložených rozsahů (°C povrch, chráněná plocha 10-17 H), žádný součet.
Mimo verzi 1: transformace vlny, roční bilance P-ET podle scénářů (čeká na klimatická data s licencí), index horka.

## 4. Vrstvy, které rozhraní potřebuje (stav)
| vrstva | k čemu | stav |
|---|---|---|
| hranice modelu, dílčí povodí sídel | Celé území | fáze 2 (DMR) |
| sklon, akumulace, deprese (1 m intravilán, 5 m okolí) | vhodnost Z03, P01-P06, C; údolnice P05 | fáze 2 |
| budovy / střechy (ZABAGED polohopis WMS ✅; pro součty potřebujeme GeoJSON) | předvyplnění ploch, součet za obec | ověřit stažení ZABAGED budov (ČÚZK CC BY) |
| zpevněné plochy | Z04, U02 | 🤔 z ortofota ruční klasifikace nebo odhad podílu; případně pasport obce |
| HSP A-D, BPEJ, zamokřené půdy | vhodnost Z01/Z02/Z10, USLE K | **chybí - VÚMOP, žádost** |
| LPIS DPB + SEO/MEO | P01-P12, DZES | WMS MZe ❌ z Claude; ověřit v prohlížeči |
| toky, nádrže (DIBAVOD GeoJSON ✅ stažení) | vzdálenost k toku, T | stáhnout |
| katastr (WMS ČÚZK) | obrys parcely po kliku | WMS ❌ z Claude; ověřit |
| II./III. vojenské mapování (WMS CENIA) | historie vodních prvků | ❌ z Claude; ověřit |
| hlásné profily, čidlo Kachník (body) | Úvod, validace | souřadnice známy (Stříbrník ✅), Kachník od uživatele |
| meliorace (ISMS) | P10 | WMS nedohledána |

## 5. Co aplikace nikdy neřekne
- že drobná opatření ochrání před povodní na Kyjovce;
- že listnatý les zadrží víc vody než smrkový (česká data to nepotvrzují);
- cenu bez zdroje a data;
- účinek bez zdroje jinak než slovem "odhad";
- že je model validovaný, dokud nebude porovnání s měřením.

## 6. Otevřené body k rozhodnutí
- ~~Výběr místa~~ vyřešeno 20.-21. 10.: parcely z katastru ČÚZK (INSPIRE CP), výběr klepnutím nebo hledáním adresy RÚIAN; nic se neukládá.
- Předvyplnění ploch střech ze ZABAGED: ano, pokud jde stáhnout budovy jako vektor (CC BY). Jinak uživatel zadává ručně.
- Zkouška vsaku jako náhrada HSP: ano i po získání dat VÚMOP (lokální realita vs. mapa 1:5000).
- Režim obec: samostatná záložka, nebo součást Celé území? Návrh: součást, s filtrem rozhoduje=O.
- Tisk katalogu: generovat z JSON v aplikaci (jedno místo pravdy), ne zvlášť.
- Měření školy: sdílená databáze vs. CSV v repozitáři - fáze 5.

## 7. Další krok
Fáze 2 (DMR, hranice, sklon, akumulace, budovy) je úzké hrdlo: bez ní nejde postavit krok 1 režimu Můj pozemek. Jádro (fáze 3) lze mezitím psát a testovat na syntetickém pozemku (viz prototyp).
