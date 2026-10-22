# Katalog opatření - v0.6 (22. 10. 2026)

Změna v0.3 (21. 10. 2026, blok B rešerše dobré praxe, `docs/KATALOG-RESERSE.md`): nová opatření **Z12 Zalévací hliněné nádoby (olla)**, **Z13 Suchomilný (stepní) záhon**, **S05 Šedá voda na zálivku a WC**, **S06 Dešťová voda na splachování WC**; doplňky (nové doklady účinku a příklady praxe) k Z01, Z02, Z04, Z05, Z06, Z09, Z11, S01, S02. Každé opatření může mít blok "Kde to funguje" (příklady se zdrojem a značkou), přenositelnost do Koryčan a rizika; v aplikaci se zobrazují v kartě. Rozhodnutí uživatele 21. 10.: podrobný popis s odkazy (styl KATALOG-RESERSE.md) se přejímá i pro web.

Změna v0.6 (22. 10. 2026, blok D krajina): bez nových ID; doplňky s měřením k T02 (Sedmihorské mokřady: +11 543 m³ na 6 ha ✅), T03 (leaky dams: model 1. řád -50 %, 3. řád riziko; Pickering), T04 (Kyjovka u Moravské Nové Vsi ✅; tůně u Bohuslavic - terénní znalost uživatele), L02 (vsak pastvina 7 vs. louka 12,6 vs. neobhospodařovaný 34,5 mm/min ✅⏳ MENDELU), LES02 (rigole FVA), C03 (terasy Kypr -87 až -98 % eroze), T01 (monitoring VÚV). **Rešerše dobré praxe (bloky B, A, C, D) tím uzavřena**: 66 opatření, 157 zdrojů, 57 příkladů u 26 opatření.

Změna v0.5 (22. 10. 2026, blok C veřejný prostor a škola): nové **U09 Studie a plán hospodaření s dešťovou vodou obce** (kontextové); doplňky k U01 (Stockholm, Graz MUFUWU), U03 (Taucha 25-30 let, Werther na hlíně, náklady 35-45 €/m²), U04, U05, U07 (Trebišov, Berlín, Wiesenena, Močovice, Cehnice, Kujavy). Měřených účinků je v bloku C málo - obce realizace nevyhodnocují.

Změna v0.4 (21. 10. 2026 večer, blok A horko v obci): nová kategorie místa **H = organizační opatření obce při vedrech**; nová opatření **U08 Mlžení a kropení při letních hromadných akcích** (jen pro akce, ne trvale - rozhodnutí uživatele), **H01 Chladná místa, pitná voda a varování**, **H02 Stínění veřejných míst**; doplňky k Z06, U01, U02, U06, U07, S04 (CzechGlobe/UPOL 2018: tři úrovně ochlazení - povrch, pocitová teplota, vzduch; Köniz 2025 světlý asfalt; Kornwestheim 2026 školní dvůr). Z06: vzduch přepsán na 0,4-2,1 °C (ČR) místo EPA „až 5 °C“.


Stav: seznam a atributy pro filtrování odsouhlaseny 16. 10. 2026. Kvantifikace účinků, Kč a zdroje: viz KATALOG-Z-S.md, KATALOG-U-P.md, KATALOG-L-LES-T-C.md (18. 10. 2026) a data/opatreni.json. Kde je zde zdroj uveden, je 💻 (z paměti), pokud není označeno jinak; ověřené zdroje jsou v kvantifikačních souborech.

Rozhodnutí 16. 10. 2026 (uživatel):
- S04 albedo zůstává (černé střechy v létě jsou reálný problém). V kvantifikaci rozlišit účinek na teplotu střechy a interiéru (silný) vs. na vzduch v okolí (slabší), se zdrojem.
- Kontextová opatření samosprávy a správců (LES03, T04, T07 a další) zůstávají v katalogu.
- Náklady: orientační Kč jako rozpětí + rok (ne třídy). Třídy €/€€/€€€ níže jsou dočasný zástupný údaj.
- Zemědělci (pachtýři) nejsou cílová skupina; dobrovolná opatření od nich neočekáváme. Katalog je pro vlastníky půdy, obec, školu, spolky a správce. Sekce P oslovuje vlastníka (N01, N02).

## 1. Atributy (podle čeho se bude filtrovat)

| Atribut | Hodnoty | K čemu |
|---|---|---|
| místo | Z zahrada/dvůr, S střecha/stavba, U veřejný prostor obce, P orná půda, L louka/pastvina, LES les, T tok/niva/prameniště, C cesta/svah/strž | filtr "kde jsem" |
| rozhoduje | J jednotlivec na svém, V vlastník půdy (přes pachtovní smlouvu nebo vyjmutí z pachtu), O obec, SP správce toku/lesa (Povodí Moravy, LČR), Š škola | filtr "kdo to může udělat" |
| pracnost | 1 víkend a ruce, 2 dny až týdny, malá technika, 3 projekt + firma | filtr |
| náklady | orientační Kč: rozpětí + rok; dočasně € do 10 tis., €€ 10-100 tis., €€€ nad 100 tis. Kč | filtr |
| účinek | R zadržení objemu, I infiltrace do půdy, Q zpomalení odtoku, E omezení neproduktivního výparu / větru, CH ochlazení mikroklimatu (stín, transpirace, albedo), ER protierozní, B biodiverzita, W šetření pitnou vodou | filtr "co chci řešit"; primární účinky velkým písmem, vedlejší v závorce |
| měřítko | pozemek / lokalita (ulice, lán, úsek toku) / území | model: co se sčítá |
| vhodnost | podmínky z dat: sklon, HSP (hydrologická skupina půd A-D), hladina podzemní vody, zamokření, expozice, vzdálenost od toku/stavby, kultura LPIS, erozní ohroženost | automatické "tady to dává smysl / nedává" |
| vazby | potřebuje (předpoklad), synergie, konflikt | řetězení, "doporučujeme nejdřív..." |
| povolení | 0 nic, 1 ohlášení / souhlas vlastníka či správce, 2 vodoprávní nebo stavební řízení | filtr "do čeho se chci pustit" |
| financování | vlastní, NZÚ, OPŽP, AOPK ZMV, PPK, participativní rozpočet obce | viz data/opatreni.json programy |
| zdroj | norma / standard / studie pro účinek a provedení | viz kvantifikační soubory |

Formát položky níže: **ID Název** | místo | rozhoduje | pracnost / náklady | účinek | měřítko | vhodnost | vazby | povolení | zdroj.

## 2. Zahrada a dvůr (Z)

- **Z01 Dešťová zahrada (zasakovací záhon)** | Z, U | J, O, Š | 1 / € | I, R (CH, B) | pozemek | HSP A-C, sklon do 5 %, min. cca 5 m od stavby, hladina PV hlouběji než 1 m | potřebuje S02; synergie S01 (přepad z nádrže) | 0 | ČSN 75 9010
- **Z02 Zahradní tůň (bez fólie, hliněná nebo jílem těsněná)** | Z | J, Š | 1-2 / € | R, CH, B (I) | pozemek | zamokřená místa, HSP C-D nebo jíl, rovina nebo úpatí svahu | synergie Z01, Z03 | 0 (do 300 m² a bez vzdutí toku, ověřit) | SPPK B02 001
- **Z03 Zasakovací průleh / rýha po vrstevnici (svejl) v zahradě nebo sadu** | Z, L | J | 1 / € | I, Q, ER (R) | pozemek | sklon 3-15 %, HSP A-C | synergie Z06 (výsadba na hraně), Z05 | 0 | ČSN 75 9010
- **Z04 Odstranění nebo náhrada zpevněných ploch (zatravňovací dlažba, štěrkový trávník, propustná dlažba)** | Z, U | J, O | 2 / €-€€ | I, CH (R) | pozemek | HSP A-C, rovina | synergie S02 | 0-1 | ČSN 75 9010
- **Z05 Trvalý pokryv půdy: mulč, kompost, zvyšování organické hmoty** | Z, L, P | J, V | 1 / € | I, E, CH (ER) | pozemek | všude | základ pro Z01-Z03 | 0 | 💻
- **Z06 Výsadba stromu (stín, vzrostlý strom, ovocný strom)** | Z, U, L | J, O, Š | 1 / € | CH, E (I, B) | pozemek | mimo ochranná pásma sítí, s ohledem na stavby | synergie Z07, Z03 | 0 (1 u sítí) | SPPK A02 001
- **Z07 Živý plot / keřový pás místo plotu nebo zdi** | Z, U | J, O | 1-2 / € | E, CH, B | pozemek | návětrná strana (ověřit převládající vítr z dat) | synergie Z06 | 0 | 💻
- **Z08 Květnatá louka místo trávníku, vyšší a méně častá seč, mozaika** | Z, U, L | J, O, Š | 1 / € | E, CH, B (I) | pozemek | všude | žádné | 0 | SPPK D02 004
- **Z09 Zelená fasáda / popínavky, pergola se zelení** | Z, S | J, O, Š | 1-2 / € | CH (E) | pozemek | jižní a západní fasády | žádné | 0 | 💻
- **Z10 Vsakovací objekt pro střešní vodu (štěrkové těleso, vsakovací bloky, šachta)** | Z, U | J, O | 2 / €€ | I, R | pozemek | HSP A-B, hladina PV hlouběji než 1 m, odstup od stavby | potřebuje S02; alternativa k Z01 tam, kde není místo | 0-1 | ČSN 75 9010, TNV 75 9011
- **Z12 Zalévací hliněné nádoby v záhonu (olla, oya)** | Z | J, Š | 1 / € | W, E (I) | pozemek | záhony, truhlíky; ne pod dřeviny | synergie S01, Z05, U07 | 0 | AZ1911 📄 60-70 %, Záhrada.sk fotopostup ✅
- **Z13 Suchomilný záhon (stepní, štěrkový)** | Z, U | J, O, Š | 2 / cena neověřena | W, E, B (CH) | pozemek | slunná suchá místa; HSP C/D zlehčit substrát | synergie Z06, U06; konflikt Z08 | 0 | LWG Veitshöchheim 2021 ✅
- **Z11 Zálivka ze zachycené vody, kapková závlaha místo postřiku** | Z | J, Š | 1 / € | W, E | pozemek | všude | potřebuje S01 | 0 | 💻

## 3. Střecha a stavba (S)

- **S01 Nádrž na dešťovou vodu (sud, nadzemní IBC, podzemní jímka) s využitím** | S, Z | J, O, Š | 1-3 / €-€€ | R, W (Q) | pozemek | každá střecha; objem podle plochy střechy a spotřeby | potřebuje S02; přepad do Z01/Z10, ne do kanalizace | 0 (podzemní 1) | NZÚ 2026 (jen WC)
- **S02 Odpojení dešťových svodů od kanalizace, svedení na pozemek** | S | J, O | 1 / € | Q, I, R | pozemek | ověřit u provozovatele kanalizace, kde je jednotná a kde oddílná (nedohledáno online) | předpoklad pro Z01, Z10, S01 | 0-1 (souhlas provozovatele 💻) | 💻
- **S03 Zelená střecha (extenzivní) na garáži, kůlně, veřejné budově** | S | J, O, Š | 2-3 / €€-€€€ | R, CH, Q (B) | pozemek | nosnost, sklon do 30 % | žádné | 1-2 | SZÚZ 2019
- **S05 Šedá voda ze sprchy a umyvadel na zálivku (a WC)** | S, Z | J | 3 / cena neověřena | W (R) | pozemek | rekonstrukce koupelny; ne na zeleninu | synergie Z11, S06, Z12 | 1-2 | ČSN 75 6780 ✅, SZÚ 2022 ✅, Byrne 2020 ✅
- **S06 Dešťová voda na splachování WC** | S | J, O, Š | 3 / nádrž 50 830 Kč ✅ + technologie neověřena | W, R (Q) | pozemek | místo na nádrž; střecha vs. počet osob | potřebuje S01; synergie S02, U04, S05 | 1 | ČSN 75 6780 ✅, Madzia 2019 ✅, ČSÚ 2024 ✅
- **S04 Světlé povrchy střech a ploch (albedo, "cool roof")** | S, U | J, O | 1-2 / €-€€ | CH | pozemek | tmavé ploché a mírně šikmé střechy, dvory, parkoviště | alternativa k S03 tam, kde nosnost nestačí | 0 | EPA; rozlišit účinek na střechu/interiér (silný) vs. okolní vzduch (slabší)

## 4. Veřejný prostor obce (U)

- **U01 Uliční stromořadí s vsakovacími rabátky (stromové prohlubně napojené na odvodnění ulice)** | U | O | 3 / €€-€€€ | CH, I, Q (B) | lokalita | ulice se sklonem k rabátku, sítě | synergie U02, U03 | 1-2 | IPR Praha, Brno 14/2024
- **U02 Propustné povrchy parkovišť, chodníků, dvorů veřejných budov** | U | O | 3 / €€-€€€ | I, CH (R) | lokalita | HSP A-C | synergie U01 | 1-2 | ČSN 75 9010
- **U03 Zasakovací pásy a průlehy podél komunikací, příkopy s retencí místo trubek** | U, C | O | 2-3 / €€ | I, Q, R | lokalita | sklon, HSP | synergie C01 | 1-2 | TSK Praha 2025
- **U04 Retence a zasakování vody z veřejných budov (škola, úřad, sokolovna)** | U, S | O, Š | 2-3 / €€ | R, I, W | lokalita | podle objektu | kombinace S01+S02+Z01/Z10 ve velkém | 1 | OPŽP 1.3.4
- **U05 Obecní tůň, mokřad, obnova návesní nádrže nebo rybníčku** | U, T | O | 3 / €€-€€€ | R, CH, B (I) | lokalita | zamokřené plochy, nivy | synergie T01, T02 | 2 | SPPK B02 001; AOPK ZMV, OPŽP
- **U06 Mozaiková seč obecních ploch, květnaté louky, ponechané pásy** | U, L | O, Š | 1 / € | E, CH, B | lokalita | všude | žádné | 0 | SPPK D02 004
- **U09 Studie a plán hospodaření s dešťovou vodou obce** | U, H | O, Š | 2 / cena neověřena | R, I, Q (nepřímo) | území, kontext | všude; vstup pro U01-U07 | synergie U01, U03, U04, U05, U07, M01, M05 | 0 | Taucha 2024 ✅, Jílové 2026 ✅, Močovice 2020 ✅
- **U08 Mlžení a kropení při letních hromadných akcích** | U, H | O, Š | 1 / cena neověřena | CH | lokalita | jen akce v horkém dni, hydrant | synergie H01, H02 | 1 (hydrant, KHS) | ZHAW 2023 ✅ -0,7/-2,5 °C, CzechGlobe ✅
- **U07 Školní zahrada jako ukázkový pozemek (sada Z01-Z08 + měření)** | U, Z | Š, O | 1-2 / € | všechny výše (osvěta) | pozemek | areál školy | spojuje Z a M | 0-1 | -

## 4b. Organizační opatření obce při vedrech (H) - od v0.4

- **H01 Chladná místa, pitná voda a varování při vlně veder** | H, U | O, Š | 1 / tisíce Kč 🤔 | CH (lidé) | území, kontext | všude | synergie U08, H02, Z06, U01 | 0 | RIVM/Climate-ADAPT 2026 ✅, Vídeň 2025 ✅
- **H02 Stínění veřejných míst (plachty, pergoly s popínavkami, přístřešky)** | U, H | O, Š | 2 / cena neověřena | CH | lokalita | zastávka, hřiště, školní dvůr; ne tam, kde jde zasadit strom | synergie Z06, Z09, U07 | 1 | měření pro plachty nedohledáno; Aarau 2022 ✅, ENKI ✅

## 5. Orná půda (P) - rozhoduje vlastník: přes pachtovní smlouvu (N01) nebo vyjmutí z pachtu (N02)

- **P01 Protierozní mez, zatravněný pás, biopás po vrstevnici** | P | V | 2 / €-€€ | ER, Q, I (B, E) | lokalita | sklon nad 3 %, erozně ohrožené DPB, délka svahu | synergie P08 (výsadba na mezi), P02 | 0-1 (změna kultury v LPIS) | VÚMOP, DZES 5
- **P02 Zasakovací průleh (vsakovací, s odvedením do zatravněné údolnice)** | P | V | 2-3 / €€ | I, Q, ER | lokalita | sklon 3-12 %, HSP A-C | potřebuje P05 pro odvedení | 1 | VÚMOP
- **P03 Rozdělení lánu, pásové střídání plodin, orientace řádků po vrstevnici** | P | V | 1 / € (organizační) | ER, Q (I) | lokalita | svažité DPB | předpoklad pro P01, P02; vyžaduje N01 | 0 | Janeček 2012
- **P04 Půdoochranné technologie: meziplodiny, podsevy, strniště přes zimu, bezorebné setí** | P | V | 1 / € | I, E, ER (CH) | lokalita | všude, zejména svahy a HSP C-D | vyžaduje N01 | 0 | VÚMOP, DZES 5
- **P05 Zatravnění údolnic a drah soustředěného odtoku** | P | V | 2 / € | ER, Q, I | lokalita | konkávní profily z DMR (akumulace odtoku) | předpoklad pro P02 | 0-1 | VÚMOP
- **P06 Trvalé zatravnění nebo zalesnění silně svažitých a erozně ohrožených pozemků, změna kultury** | P | V | 2 / €-€€ | I, ER, E (B, CH) | lokalita | sklon nad 12 %, erozní ohroženost vysoká | vyžaduje N02 | 1 (LPIS) | USLE C
- **P07 Větrolam, liniová výsadba na hranici pozemku** | P, C | V, O | 2 / €-€€ | E, ER (větrná), CH, B (Q) | lokalita, území | kolmo na převládající vítr, otevřené lány | synergie P08, P09 | 0-1 | VÚMOP 2016
- **P08 Polní cesta s doprovodnou zelení a zasakovacím příkopem (víceúčelové: cesta + větrolam + biokoridor + zpomalení odtoku)** | P, C | V, O | 3 / €€-€€€ | E, Q, I, ER, B | lokalita | po vrstevnici nebo šikmo, hranice vlastníků | spojuje P01+P07+C01 | 1-2 | TPEO 2014
- **P09 Agrolesnictví: řady stromů v poli (alejové), ovocné stromy v pastvině** | P, L | V | 2 / €€ | E, CH, B (I, ER) | lokalita | lány, větrné polohy | synergie P07; vyžaduje N02 | 0-1 (LPIS kultura) | SPPK C02 003, MZe 2026
- **P10 Regulace nebo přerušení melioračního odvodnění (regulační šachty, zaslepení, obnova mokřadu na odvodněné ploše)** | P, L | V, O | 2-3 / €€ | R, I, B (CH) | lokalita | zamokřené plochy, existující drenáž (zjistit u SPÚ) | synergie T02 | 1-2 | VÚMOP 2021
- **P11 Remízek, drobná plocha zeleně v cípech a na neobdělatelných místech** | P | V, O | 1-2 / € | B, E, CH (I) | pozemek | neobdělatelné cípy, mokřiny, kamenité plochy | synergie P07 | 0 | 💻
- **P12 Zvyšování organické hmoty v půdě (hnůj, kompost, zelené hnojení)** | P | V | 1 / € (smluvní) | I, R (ER, E) | lokalita | všude | vyžaduje N01 | 0 | 💻

## 6. Louka a pastvina (L)

- **L01 Mozaiková nebo pozdní seč, ponechané pásy** | L | V, O | 1 / € | E, CH, B | lokalita | všude | žádné | 0 | SPPK D02 004
- **L02 Extenzivní rotační pastva, omezení přepásání a sešlapu** | L | V | 1 / € | I, ER, B | lokalita | pastviny | žádné | 0 | SPPK D02 003, VÚMOP 2015
- **L03 Solitérní stromy a skupiny v pastvině** | L | V | 1 / € | CH, E, B | pozemek | všude | oplocenky proti okusu | 0 | SPPK C02 003
- **L04 Ochrana pramenišť a mokřin v loukách před sešlapem, obnova** | L, T | V, O | 1 / € | R, B (I) | pozemek | prameniště z dat (akumulace, zamokření) | synergie T05 | 0 | 💻

## 7. Les (LES)

- **LES01 Lesní tůně a přehrážky v lesních stržích (dřevěné, kamenné)** | LES, C | SP, V, O | 1-2 / € | Q, R, ER (I, B) | pozemek, lokalita | strže z DMR, lesní cesty | synergie C02 | 1 (souhlas vlastníka/LČR) | MZe TD 2020
- **LES02 Odvodnění lesních cest a svážnic do lesa, ne do strží (svodnice, příčné prahy)** | LES, C | SP, V | 1-2 / € | ER, I, Q | lokalita | svahové cesty | synergie LES01 | 1 | vyhl. 239/2017
- **LES03 Druhově pestrý les, přirozená obnova, ponechání mrtvého dřeva a humusu** | LES | V, SP | 3 / €€-€€€ (dlouhodobé) | B (I, E, CH) | území | smrkové monokultury na nevhodných stanovištích (OPRL) | kontext (správce) | 1 (LHP) | AV ČR 2023 (pozor: voda nepotvrzena)
- **LES04 Lesní okraj s keřovým pláštěm (ekoton)** | LES, P | V, O | 1-2 / € | E, B, CH | lokalita | hranice les/pole | synergie P07 | 0 | 💻

## 8. Tok, niva, prameniště (T)

- **T01 Tůň v nivě (bez fólie), soustava tůní, obnova zazemněné tůně** | T | V, O, SP | 1-3 / €-€€ | R, CH, B (I, Q) | pozemek, lokalita | niva, hladina PV mělko, HSP C-D | synergie T02, T06 | 0-2 (podle velikosti a vzdálenosti od toku) | SPPK B02 001; AOPK ZMV
- **T02 Mokřad, zamokření nivy přerušením odvodnění** | T | V, O | 2-3 / €-€€ | R, CH, B (I, Q) | lokalita | odvodněné nivy | synergie P10, T01 | 1-2 | VÚMOP 2021
- **T03 Mrtvé dřevo a dřevní přehrážky v korytě drobného toku (zpomalení, zadržení)** | T | SP (souhlas), V | 1 / € | Q, R, B | lokalita | drobné toky mimo intravilán, bez ohrožení staveb | synergie T04 | 1-2 (souhlas správce toku + vodoprávní úřad) | AOPK 2020; zahraniční leaky dams
- **T04 Revitalizace drobného toku (odstranění opevnění, rozvlnění, snížení břehů)** | T | SP, O | 3 / €€€ | Q, R, B, CH | lokalita, území | napřímené úseky (porovnání s II./III. voj. mapováním) | kontext (obec, správce) | 2 | OPŽP
- **T05 Obnova prameniště, studánky, ochrana před sešlapem a splachy** | T, L, LES | J, V, Š, O | 1 / € | R, B | pozemek | prameniště z dat + terén | synergie L04 | 0-1 | MOP 2025
- **T06 Břehové porosty podél toku a kolem nádrží** | T | V, O, SP | 1-2 / € | CH, E, ER, B | lokalita | nezastíněné úseky | synergie T01 | 0-1 | Kalny 2017, Trimmel 2018
- **T07 Malá vodní nádrž, suchý poldr, rybník** | T | O, SP | 3 / €€€ | R, Q (B, CH) | území | profil z DMR, objem při hrázi | kontext (obec, správce) | 2 | TNV 75 2415; OPŽP

## 9. Cesta, svah, strž (C)

- **C01 Zasakovací příkopy a svodnice u cest, odvedení vody do průlehů místo do toku** | C | O, V | 1-2 / € | I, Q, ER | lokalita | svahové cesty | synergie U03, P08 | 0-1 | TPEO 2014
- **C02 Přehrážky v erozních rýhách a stržích (kámen, dřevo, proutí)** | C, LES | V, O, Š | 1 / € | ER, Q (R, I) | pozemek | rýhy z DMR a terénu | synergie LES01 | 0-1 | MZe TD 2020
- **C03 Zatravnění a výsadba na svazích, terasování starých úvozů** | C | V, O | 2 / €-€€ | ER, I, E | lokalita | sklon nad 15 % | synergie P06 | 0-1 | TPEO 2014

## 10. Podpůrná opatření: měření a osvěta (M) - škola, oddíl

- **M01 Srážkoměr (jednoduchý, denní odečet)** | Š, J | 1 / € | základ pro bilanci a validaci | synergie všech
- **M02 Hladina ve studních (měsíční odečet, síť dobrovolníků)** | Š, J | 1 / € | indikátor podzemní vody
- **M03 Vlhkost půdy (jednoduché čidlo nebo gravimetricky)** | Š | 1 / € | validace účinku opatření
- **M04 Stav drobných toků a pramenišť (fotomonitoring, "teče / neteče"; registr estudanky.eu)** | Š | 1 / € | validace, argumentace
- **M05 Teplota povrchů (IR teploměr) v různých typech ploch, vč. tmavé vs. světlé střechy** | Š | 1 / € | ukázka CH účinku stromů, trávy a albeda (S04)
- **M06 Mapování erozních rýh po přívalu** | Š | 1 / € | lokalizace C02, P05

## 11. Nástroje vlastníka a obce (N) - nejsou opatření, ale podmínka jejich realizace

- **N01 Pachtovní smlouva s podmínkami (půdoochranné technologie, pásy, organická hmota)** | V | 0 | umožňuje P03, P04, P12
- **N02 Vyjmutí pozemku nebo jeho části z pachtu** (OZ § 2347: výpovědní doba 12 měsíců u doby neurčité) | V | 0 | umožňuje P01, P05-P09, P11
- **N03 Směna nebo koupě pozemku v klíčové poloze (údolnice, niva)** | V, O | 0 | umožňuje T01, T02, P05
- **N04 Žádost o komplexní pozemkové úpravy** (zák. 139/2002 § 6 odst. 3: vlastníci nadpoloviční výměry ZP v k.ú.) | V, O | - | odemyká P01, P02, P08 ve velkém
- **N05 Dotace** (stav k 18. 10. 2026 v data/opatreni.json) | J, V, O | - | -
- **N06 Dohoda se správcem toku (Povodí Moravy) nebo lesa (LČR)** | O, SP | - | umožňuje T03, T06, LES01

## 12. Co z katalogu plyne pro data a interaktivní část

Vhodnost opatření se automaticky vyhodnotí z těchto vrstev (jinak nic z "vhodnosti" nefunguje):
1. Sklon a expozice (DMR) - Z03, P01-P06, C03.
2. Akumulace odtoku, údolnice, strže (DMR) - P05, C02, LES01, T05.
3. Hydrologická skupina půd / infiltrace (VÚMOP) - Z01, Z10, U02, P02. **Bez dat VÚMOP nelze rozlišit "zasakovat" vs. "zadržet"** - nejdůležitější chybějící vrstva. Náhrada: zkouška vsaku na místě (jáma, 30 min).
4. Zamokření, hladina podzemní vody, nivy (ČGS hydrogeologie, VÚMOP zamokřené půdy, DIBAVOD) - Z02, T01, T02, P10.
5. Kultura a hranice DPB (LPIS) + erozní ohroženost SEO/MEO - rozlišení P vs. L, rozhoduje V; DZES 5.
6. Erozní ohroženost (VÚMOP, MZe) - P01, P04, P06.
7. Převládající vítr (ČHMÚ stanice, nebo 💻 obecně Z/JZ) - P07, Z07.
8. Zastavěné plochy a střechy (ZABAGED, ortofoto) - S01, S02, S04, Z04, U02: plocha střech a zpevněných ploch v intravilánu je přímý vstup do součtu.
9. Existující drenáže (SPÚ, ISMS) - P10.
10. Historické vodní prvky (II./III. voj. mapování vs. dnes) - T01, T02, T04, U05.

Interaktivní část má dva režimy: (a) **"Můj pozemek"**: klikni na parcelu/plochu, aplikace nabídne opatření vhodná pro to místo podle vrstev 1-8 a spočítá příspěvek (objem, plocha); (b) **"Celé území"**: součet příspěvků podle scénáře "kolik lidí se zapojí" a kontextová velká opatření. Podrobně ROZHRANI.md.
