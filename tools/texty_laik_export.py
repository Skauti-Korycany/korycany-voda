"""Vytáhne laické texty webu do jedné tabulky pro přepis: docs/TEXTY-PRO-LAIKY.xlsx.

Původní text vlevo, prázdný sloupec "Nový text" vpravo. Texty z části "Pro zvídavé" se nevytahují.
Texty šablony a vět skládaných v JS jsou opsané ručně z tools/build_dummy.py (stav k datu STAV níže);
čísla, která web doplňuje sám, jsou ve složených závorkách {takto}.
Opatření a dotace se berou přímo z data/opatreni.json, názvy dlaždic Můj pozemek z AKCE v build_dummy.py.
Spuštění: python tools/texty_laik_export.py  (potřebuje openpyxl)
"""
import json, os, re
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "TEXTY-PRO-LAIKY.xlsx")
STAV = "16. 11. 2026"

# --- položky: ("#", "nadpis oddílu") nebo (kde na webu, druh, původní text, poznámka)
SPOLECNE = [
    ("#", "Záhlaví, záložky, upozornění, patička"),
    ("záhlaví", "nadpis", "Voda v Koryčanech", ""),
    ("záhlaví", "podtitul", "náhled - skutečný terén, půda, budovy a srážky; katalog v{verze}", "{verze} doplňuje web"),
    ("záložky", "tlačítka", "Jak bylo | Můj pozemek | Celé území | Katalog | O modelu", "názvy 5 záložek"),
    ("upozornění nahoře", "věta", "Zjednodušený model pro osvětu, ne projekt. Nevalidováno. Nic se neukládá.", "musí zůstat: model pro osvětu + nevalidováno"),
    ("upozornění nahoře, po rozkliknutí", "text", "Po kliku do mapy se sklon a půda berou z dat (DMR 5G ČÚZK, hydrologické skupiny půd VÚMOP, v.v.i., CC BY-NC); střechy a výměry z katastru (ČÚZK) po kliknutí na parcely, zpevněné plochy zadáváš sám. Katalog, vzorce, ceny a zdroje: data/opatreni.json, podrobnosti v záložce O modelu. Značky: ✅ ověřený zdroj, ✅⏳ starší než rok, 📄 citace, 🤔 odhad.", "spíš pro zvídavé; licence půd (CC BY-NC) musí zůstat"),
    ("patička", "text", "Skautský oddíl Hříběcí hory, Koryčany, s ZŠ Koryčany. Data: ČÚZK (CC BY 4.0), katalog opatření v{verze} z {datum katalogu} (vlastní kompilace, zdroje u každé položky). Data počasí k {datum}.", "uvedení licence ČÚZK musí zůstat"),
    ("všude", "štítek rozbalovací části", "Pro zvídavé - ...", "rozbalovací části se všude jmenují takto; obsah se do této tabulky nevytahuje"),
]

JAKBYLO = [
    ("#", "Úvod"),
    ("úvod", "nadtitulek", "Jak bylo · data ČHMÚ 1921-{letošní rok}", ""),
    ("úvod", "hlavní nadpis", "Prší stejně jako před sto lety. Vody v krajině přesto ubývá.", ""),
    ("úvod", "úvodní odstavec", "Roční úhrn srážek se v Koryčanech za sto let nezměnil: v letech 1921-1950 to bylo v průměru {srážky 1921-1950} mm, v letech 1991-2020 {srážky 1991-2020} mm. Od roku 2001 se ale otepluje, v průměru o {oteplení} °C za každých deset let. Teplejší vzduch si bere víc vody. Pramen v Chřibech nad Koryčany dává dnes {pramen dnes v %} % toho, co v 80. letech, a potokem přitéká do přehrady {Kyjovka dnes v %} % vody proti letům {první desetiletí měření Kyjovky}. Část té vody může zadržet každý u sebe doma.", "skládá se v JS; když se nenačtou data o pramenech, místo věty o pramenu je: \"Teplejší vzduch si bere víc vody, takže stejný déšť stačí krajině na méně.\""),
    ("úvod", "poznámka", "Data se stahují automaticky čtyřikrát denně. Poslední den s daty: {datum}, staženo {kdy}. ČHMÚ zveřejňuje denní data se zpožděním 1-2 dny (den měření končí v 8 ráno), proto tu včerejšek ještě nemusí být.", ""),
    ("klíčová čísla, karta 1", "číslo + popis", "{srážky 1991-2020} mm - naprší v průměru za rok (1991-2020). V letech 1921-1950 to bylo v průměru {srážky 1921-1950} mm.", "velké číslo nahoře, pod ním věta"),
    ("klíčová čísla, karta 2", "číslo + popis", "{+0,5} °C - za každých 10 let: tak se mění průměrná roční teplota ({2001-2025}, ČHMÚ Nemochovice).", ""),
    ("klíčová čísla, karta 3", "číslo + popis", "{tropické dny dřív} → {tropické dny teď} - tropických dní za rok: průměr 2001-2010 proti {posledních 10 let}.", ""),
    ("klíčová čísla, karta 4", "číslo + popis", "{dřív} → {teď} l/s - dává pramen u Koryčan: průměr {období} proti {období} (měření ČHMÚ).", ""),

    ("#", "Kapitola 1: Kolik u nás naprší"),
    ("kap. 1", "nadpis", "1. Kolik u nás naprší", ""),
    ("kap. 1", "věta pro laika", "V Koryčanech naprší v průměru {srážky 1991-2020} mm za rok (1991-2020). Před sto lety to bylo {srážky 1921-1950} mm (1921-1950). Mokré a suché roky se střídají, ale deště za rok dlouhodobě neubývá ani nepřibývá.", ""),
    ("kap. 1, graf", "legenda", "srážky za rok | 3 nejsušší roky | 3 nejdeštivější | klouzavý průměr 10 let | průměr 30 let | tečka pod rokem: část dní doplněna z okolní stanice", "položky legendy oddělené |"),
    ("kap. 1, pod grafem", "zdroj", "Měření ČHMÚ v Koryčanech, letošek předběžně.", ""),
    ("kap. 1", "štítek rozbalovací části", "Pro zvídavé - jak graf číst a odkud jsou data", ""),

    ("#", "Rámeček: Kam mizí déšť"),
    ("rámeček", "nadtitulek", "Vysvětlení", ""),
    ("rámeček", "nadpis", "Kam mizí déšť", ""),
    ("rámeček", "text", "V letech {2001-2025} napršelo na metr čtvereční v průměru {srážky} litrů za rok. Slunce, teplo a vítr by ale dokázaly odpařit v průměru {možný výpar} litrů, kdyby voda byla. Tomu rozdílu říkáme žízeň krajiny. Vypaří se jen tolik, kolik vody opravdu je. Čím je půda sušší, tím méně má co odpařit a tím víc rostliny strádají. Co steče do kanálu, krajině chybí.", ""),
    ("rámeček", "poznámka", "Možný výpar = kolik by se vypařilo z trávníku, který má vody dost. Skutečný je v suchu menší, protože není z čeho.", ""),
    ("rámeček, obrázek", "popisky", "naprší {srážky} mm | mohlo by se vypařit {výpar} mm | do kanálu | vsak do zásoby | žízeň o {rozdíl} mm větší", "krátké popisky v kresbě"),

    ("#", "Kapitola 2: Letní žízeň a výpar"),
    ("kap. 2", "nadpis", "2. V létě má krajina větší žízeň, než kolik naprší", ""),
    ("kap. 2", "věta pro laika", "V letech {2001-2025} napršelo v průměru {srážky} mm za rok a mohlo by se vypařit {výpar} mm. V {počet} z {počet let} let bylo deště méně, než kolik by se mohlo vypařit. Rozhoduje léto: od dubna do srpna chybí voda skoro každý rok. Letos do {datum} zatím chybí {letošní schodek} mm (předběžně).", "poslední věta jen když jsou letošní data"),
    ("kap. 2, graf", "legenda", "srážky minus výpar: voda zbyla | srážky minus výpar: voda chyběla | možný výpar za rok", ""),
    ("kap. 2, pod grafem", "zdroj", "Srážky Koryčany minus možný výpar (výpočet z měření ČHMÚ). Tečka pod rokem = část dní doplněna.", ""),
    ("kap. 2, výpar Kroměříž", "věta pro laika", "Výparu přibývá. V Kroměříži, kde se všechno potřebné měří od 50. let, vzrostl možný výpar z {dřív} mm za rok ({období}) na {teď} mm ({období}). Je tepleji, vzduch je sušší a slunce svítí déle.", "\"Výparu přibývá.\" je tučně"),
    ("kap. 2, graf Kroměříž", "legenda", "možný výpar za rok, Kroměříž (mm) | klouzavý průměr 10 let", ""),
    ("kap. 2, graf Kroměříž", "zdroj", "Výpočet z měření ČHMÚ v Kroměříži (27 km od Koryčan).", ""),
    ("kap. 2", "štítek rozbalovací části", "Pro zvídavé - jak výpar počítáme a čím je ověřený", ""),

    ("#", "Rámeček: Kde se ten rozdíl vezme?"),
    ("rámeček", "nadtitulek", "Vysvětlení", ""),
    ("rámeček", "nadpis", "Kde se ten rozdíl vezme?", ""),
    ("rámeček", "text", "Nikde. Víc vody, než naprší, se vypařit nemůže. Možný výpar je jen to, kolik by se vypařilo, kdyby vody bylo dost. Když v půdě dojde, rostliny zavřou průduchy a skutečný výpar klesne, až k nule. To, co v grafu chybí, je voda, kterou rostliny chtěly a nedostaly. Tak vypadá sucho.", ""),
    ("rámeček, obrázek 1", "nadpis", "Zima: déšť je víc než žízeň", ""),
    ("rámeček, obrázek 1", "text", "Od září do března u nás naprší asi o {přebytek} mm víc, než se může vypařit. Půda se nasytí a přebytek prosakuje dolů k podzemní vodě a do studní.", ""),
    ("rámeček, obrázek 2", "nadpis", "Jaro a léto: žízeň je větší než déšť", ""),
    ("rámeček, obrázek 2", "text", "Od dubna do srpna by se mohlo vypařit o {schodek} mm víc, než naprší. Rostliny si berou vodu ze zásoby v půdě. Letní déšť spotřebují hned a do hloubky nedojde.", ""),
    ("rámeček, obrázek 3", "nadpis", "Konec léta: zásoba došla", ""),
    ("rámeček, obrázek 3", "text", "Půda je vyčerpaná, rostliny strádají a výpar klesá. Po suché nebo teplé zimě se půda znovu nenasytí, podzemní voda se nedoplní a deficit se přenáší do dalšího roku.", ""),
    ("rámeček, kresby", "popisky", "půda je plná | zásoba ubývá | zásoba došla", ""),

    ("#", "Kapitola 3: Prameny a Kyjovka"),
    ("kap. 3", "nadpis", "3. Prameny slábnou a potoku ubývá", ""),
    ("kap. 3", "věta pro laika", "Že vody ubývá, je vidět na měření. Pramen v Chřibech nad Koryčany dával v letech {období} v průměru {dřív} litru za sekundu, v letech {období} jen {teď} litru. Stejně slábnou i další měřené prameny v okolí: {seznam pramenů s čísly}. Kyjovka přiváděla do přehrady v letech {období} v průměru {dřív} litrů za sekundu, v letech {období} už jen {teď}. Deště přitom neubylo.", "pokud se data nenačtou: \"Data o pramenech se nepodařilo načíst.\""),
    ("kap. 3, grafy", "legenda", "pramen Koryčany, průměrná vydatnost za rok (litry za sekundu) | Kyjovka nad nádrží, průměrný průtok za rok (litry za sekundu) | klouzavý průměr 10 let", ""),
    ("kap. 3, pod grafy", "zdroj", "Měření ČHMÚ, roční průměry.", ""),
    ("kap. 3", "štítek rozbalovací části", "Pro zvídavé - jak se to měří a jak jistý je pokles", ""),

    ("#", "Kapitola 4: Horko"),
    ("kap. 4", "nadpis", "4. Horka přibývá", ""),
    ("kap. 4", "věta pro laika", "Tropických dní (aspoň 30 °C) bylo v letech 2001-2010 v průměru {dřív} za rok, v letech {posledních 10 let} v průměru {teď}. Průměrná teplota se za roky {2001-2025} mění o {+0,5} °C za deset let. Letos (předběžně) bylo {počet} tropických dní, z toho {počet} s teplotou aspoň 35 °C; v letech {2001-2025} jich bylo v jednom roce nejvýš {max}.", "poslední věta jen když jsou letošní data"),
    ("kap. 4, graf", "legenda", "tropické dny (≥ 30 °C) | supertropické dny (≥ 35 °C) | letní maxima, průměr VI-VIII (pravá osa) | trend", ""),
    ("kap. 4, pod grafem", "zdroj", "Měření ČHMÚ v Nemochovicích (8 km od Koryčan).", ""),
    ("kap. 4", "štítek rozbalovací části", "Pro zvídavé - prahy, trendy a jak graf číst", ""),

    ("#", "Kapitola 5: Lijáky"),
    ("kap. 5", "nadpis", "5. Když přijde liják", ""),
    ("kap. 5", "věta pro laika", "Sucho a povodeň nejsou protiklady. Vyschlá a utužená půda nestihne vsáknout, voda steče po povrchu a vezme s sebou ornici. V koryčanské řadě velkých lijáků zatím nepřibývá ani neubývá. Největší deště za den v řadě od roku 1921:", "následuje seznam 5 největších dní"),
    ("kap. 5, pod seznamem", "poznámka", "Pro srovnání: běžný déšť má 10 mm a přichází asi {17}x za rok.", ""),
    ("kap. 5", "štítek rozbalovací části", "Pro zvídavé - přibývá lijáků?", ""),

    ("#", "Kapitola 6: Letošek"),
    ("kap. 6", "nadpis", "6. Letošek do {datum}", ""),
    ("kap. 6, karta 1", "číslo + popis", "{x} mm - srážek, {x} % normálu za stejné období", ""),
    ("kap. 6, karta 2", "číslo + popis", "{x} mm - srážky minus výpar, nejhůř od roku 2001", "\"nejhůř od roku\" jen když platí"),
    ("kap. 6, karta 3", "číslo + popis", "{x} - tropických dní, nejvíc od roku 2001 / rekord je {x} ({rok})", "jedna ze dvou variant"),
    ("kap. 6, karta 4", "číslo + popis", "{x} °C - průměr letních maxim, nejteplejší léto od roku 2001 / rekord {x} °C", "jedna ze dvou variant"),
    ("kap. 6", "zdroj", "Předběžná data ČHMÚ. Výběr období a srovnání s minulými roky najdeš níže v části Více o tématu.", ""),

    ("#", "Výhled: Co nás čeká"),
    ("výhled", "nadtitulek", "Výhled", ""),
    ("výhled", "nadpis", "Co nás čeká", ""),
    ("výhled", "text", "Do poloviny století se Česko podle klimatických modelů oteplí asi o 2 °C proti letům 1981-2010. Srážek za rok bude zhruba stejně, ale víc jich spadne v zimě a méně v létě. Čekat se dají častější a delší sucha a víc škod z přívalových dešťů.", "čísla mají zdroj (CzechGlobe) v části pro zvídavé; při změně čísel je ověřit"),
    ("výhled", "štítek rozbalovací části", "Pro zvídavé - rozpětí výhledu a zdroje", ""),

    ("#", "Kapitola 7: Výzva"),
    ("kap. 7", "nadpis", "7. Co s tím u vás doma", ""),
    ("kap. 7", "text", "Vodu, která spadne na střechu a dvůr, jde udržet tam, kde spadla: sud pod okapem, dešťový záhon, strom, propustná dlažba. Spočítej si, kolik to dělá na tvém pozemku.", ""),
    ("kap. 7", "odkazy", "Spočítej svůj pozemek → | Co se dá udělat (katalog) →", ""),

    ("#", "Více o tématu (rozbalovací část na konci)"),
    ("více o tématu", "štítek", "Více o tématu - výběr období a srovnání ročníků, trendy v číslech, měsíční bilance, pojmy, metody a zdroje", ""),
    ("více o tématu", "nadpisy", "Vyber si období | Detail: vybrané období | Extrémy období | Srovnání ročníků | Trendy v číslech | Srážky minus možný výpar po měsících", ""),
    ("více o tématu", "poznámka", "Denní data jsou od 1. 1. 2026 (ČHMÚ je zveřejňuje jen pro běžící rok); starší roky jsou v řadách nahoře.", ""),
    ("více o tématu, graf po měsících", "legenda", "zásoba se doplňuje | bere se ze zásoby | srážky Koryčany 1991-2020, možný výpar Nemochovice 2001-2025", ""),
    ("více o tématu, fakt 1", "nadpis", "Kam jde déšť v průměru za rok (celé Česko)", ""),
    ("více o tématu, fakt 1", "text", "Ze 675 mm srážek asi 505 mm skutečně odejde výparem, 170 mm odteče potoky a z toho asi 72 mm doplní podzemní vodu ✅.", "zdroj VTEI 2022/5"),
    ("více o tématu, fakt 2", "nadpis", "Co dělá teplo", ""),
    ("více o tématu, fakt 2", "text", "Mezi obdobími 1971-2010 a 1981-2019 se v Česku oteplilo o 0,4 °C. Srážek je skoro stejně (o 1,6 % méně), ale podzemní vody se doplňuje o 7-12 % méně ✅. Víc vody si vezme vzduch.", "zdroj VTEI 2022/5"),
    ("více o tématu, fakt 3", "nadpis", "Co z toho plyne pro zahradu", ""),
    ("více o tématu, fakt 3", "text", "Každý kubík, který v zimě a při lijáku zasákne místo do kanálu, je zásoba na léto. Proto má smysl udržet vodu tam, kde spadne.", ""),
]

POZEMEK = [
    ("#", "Hlavička a postup"),
    ("postup (nahoře)", "tlačítka kroků", "1 Kde | 2 Okapy a půda | 3 Při dešti | 4 Co udělat | 5 Výsledek", ""),
    ("hlavička", "nadtitulek", "Krok {n} z 5", ""),
    ("krok 1", "nadpis", "Kolik vody ti uteče při dešti?", ""),
    ("krok 1", "podnadpis, nic nevybráno", "Najdi svůj dům v mapě nebo podle adresy a klepni na něj.", ""),
    ("krok 1", "podnadpis, vybráno", "Vybráno. Patří k domu i zahrada na vlastní parcele? Klepni i na ni, pak pokračuj.", ""),
    ("krok 2", "nadpis", "Střechy, dlažba a půda", ""),
    ("krok 2", "podnadpis", "Tři rychlé otázky. Něco víme z map, ale kam vedou okapy, víš jen ty.", ""),
    ("krok 3", "nadpis", "Co se u tebe děje při dešti", ""),
    ("krok 3", "podnadpis", "Vyber déšť. Uvidíš, kolik vody spadne na tvůj pozemek, kolik odteče a kolik se vsákne.", ""),
    ("krok 4", "nadpis", "Co můžeš udělat", ""),
    ("krok 4", "podnadpis", "Klepni na to, co by u tebe šlo. Ukazatel nahoře ukáže, kolik deště pak udržíš doma.", ""),
    ("krok 5", "nadpis", "Tvůj výsledek", ""),
    ("krok 5", "podnadpis", "Kolik vody tvoje volba udrží a co můžeš udělat dál.", ""),
    ("spodní lišta", "tlačítka Dál", "Dál: okapy a půda | Dál: co se děje při dešti | Dál: co můžu udělat | Dál: výsledek | Vybrat jiný pozemek", "po krocích 1-5"),
    ("spodní lišta", "tlačítko", "Zpět", ""),

    ("#", "Krok 1: mapa a hledání"),
    ("hledání", "nápověda v poli", "Ulice a číslo domu, nebo číslo parcely", ""),
    ("hledání", "tlačítka", "Najít | ◎ Jsem tady", ""),
    ("mapa", "tlačítko", "Změnit místo", ""),
    ("pod mapou", "stav", "Zatím nic nevybráno.", ""),
    ("Z map víme", "nadpis + odkaz", "Z map víme | podrobnosti", ""),
    ("Z map víme", "řádky", "Místo | Sklon | Půda | Okolí 30 m | Přitéká shora", ""),
    ("Z map víme, přitéká shora", "hodnota", "skoro nic, pozemek je nahoře nebo na rovině / z plochy asi {plocha} (DMR 5G, odhad) / z velké plochy (přes {x} ha)", "tři varianty"),
    ("pod mapou", "poznámka", "Katastr a budovy ČÚZK (CC BY 4.0), podklad ZTM a ortofoto ČÚZK. Hledání adresy dělá vyhledávací služba RÚIAN (ČÚZK): hledaný text se pošle jí, u nás se nic neukládá. Poloha telefonu zůstává v telefonu. Vlastníci se nenačítají.", "uvedení licence ČÚZK musí zůstat"),
    ("pod mapou", "odkaz", "Nechci mapu, zadám plochy ručně", ""),
    ("Jak to půjde", "nadtitulek", "Jak to půjde", ""),
    ("Jak to půjde", "bod 1", "Klepni v mapě na svůj dům. Má zahrada vlastní parcelu? Klepni i na ni, plochy se sečtou.", ""),
    ("Jak to půjde", "bod 2", "Odpověz na tři otázky: kam vedou okapy, kolik je dlažby a jaká je půda.", ""),
    ("Jak to půjde", "bod 3", "Uvidíš, kolik vody ti při dešti uteče, a vybereš si, co by u tebe šlo udělat.", ""),
    ("První číslo (po výběru)", "nadtitulek", "První číslo", ""),
    ("První číslo", "text", "Při dešti {mm} mm ({popis deště}) odteče ze střech na vybraných parcelách ({plocha} m²) {objem} m³. To je {x} konví vody (konev 10 l). Patří k domu i zahrada? Klepni i na ni. Co se děje se zbytkem pozemku a co s tím jde udělat, ukážou další kroky.", "konve jen pod 1 m³; věta o zahradě jen když ve výběru chybí"),
    ("První číslo", "text, bez budovy", "Na vybraných parcelách nejsou budovy. Klepni i na svůj dům, nebo pokračuj se zahradou.", ""),

    ("#", "Krok 2: tři otázky"),
    ("bez mapy", "upozornění", "Bez mapy počítám s příkladem: střecha 120 m², zahrada 300 m². Oprav to v „Upřesnit čísla“.", ""),
    ("otázka 1", "otázka", "Kam vedou svody (okapové roury) ze střechy?", ""),
    ("otázka 1", "odpovědi", "všechny do kanalizace | 3/4 do kanalizace | půl na půl | 1/4 do kanalizace | všechny na zahradu | nevím", ""),
    ("otázka 2", "otázka", "Kolik máš dlažby, betonu a štěrku?", ""),
    ("otázka 2", "odpovědi", "skoro nic | cesta, malý dvůr (~20 m²) | dvůr a příjezd (~60 m²) | velký dvůr (~150 m²)", ""),
    ("otázka 2", "poznámka", "Zpevněné plochy v mapách nejsou, odhadni je. Teď počítám s {x} m², přesně v „Upřesnit čísla“.", ""),
    ("otázka 3", "otázka", "Jakou máš půdu?", ""),
    ("otázka 3", "odpovědi", "velmi propustná, písek | propustná | spíš těžká | jíl, voda stojí", ""),
    ("otázka 3", "poznámka", "Předvybráno z mapy půd. Na zahradě může být půda jiná (navezená, ušlapaná), zkouška vsaku to ukáže.", ""),
    ("otázka 3", "rozbalovací návod", "Jak to zjistit sám: Vykopej jámu 30 cm, nalij vodu a po 30 minutách změř, o kolik klesla. Přes 8 cm velmi propustná, 4-8 cm propustná, 2-4 cm spíš těžká, pod 2 cm jíl.", ""),
    ("krok 2", "štítek rozbalovací části", "Upřesnit čísla (plochy v m², sklon, dlažba, zahrada)", "uvnitř formulář pro zvídavé"),

    ("#", "Krok 3: při dešti"),
    ("výběr deště", "otázka", "Jaký déšť?", ""),
    ("výběr deště", "odpovědi", "běžný, 10 mm | silný, 20 mm | liják, 32 mm", ""),
    ("výběr deště", "poznámka", "Vzácné přívalové deště (53, 87 a 94 mm) najdeš níž v části „Pro zvídavé“.", ""),
    ("popisy deštů (ve větách)", "slovník", "10 mm: běžný déšť, asi 17x za rok | 20 mm: silný déšť, asi 5x za rok | 32 mm: liják, jednou za 2 roky | 53 mm: vzácný liják, jednou za 10 let | 87 mm: extrémní liják, jednou za 100 let | 26 mm: krátká bouřka, jednou za 5 let | 94 mm: jako 12. 6. 2012 v Koryčanech", "doplňuje se do závorky ({popis deště}) ve větách"),
    ("Jeden déšť", "nadtitulek", "Jeden déšť", ""),
    ("Jeden déšť", "text", "Při dešti {mm} mm ({popis deště}) spadne na tvůj pozemek ({plocha} m²) {objem} m³. Z toho {x} m³ odteče ({x} %), zbytek se vsákne do zahrady.", ""),
    ("Jeden déšť", "legenda", "odteče | vsákne se", ""),
    ("Jeden déšť", "věta o největším zdroji", "Nejvíc odteče ze střechy / z dlažby a betonu / ze zahrady ({x} m³).", ""),
    ("Jeden déšť, okapy do kanalizace", "věta", "Voda z okapů teče do kanalizace a dál do potoka.", ""),
    ("Jeden déšť, okapy částečně", "věta", "Voda z {x} % střechy teče do kanalizace a dál do potoka, zbytek už na zahradu.", ""),
    ("Jeden déšť, okapy na zahradu", "věta", "Okapy už vedou na zahradu, to je dobrý začátek - v kroku 4 uvidíš, jak tu vodu udržet.", ""),
    ("Jeden déšť, nevím", "věta", "Kam vedou okapy, poznáš u paty svodu: když mizí v trubce v zemi, většinou je to kanalizace 🤔.", ""),
    ("Jeden déšť", "věta o trávníku", "Trávník při dešti do {x} mm vsákne všechno.", ""),
    ("pod rámečkem", "věta za rok", "Za celý rok (v průměru naprší {x} mm) odteče ze střech a dlažby asi {x} m³, ze zahrady {x} m³.", ""),
    ("30 dní", "nadtitulek", "Skutečně u tebe, posledních 30 dní", ""),
    ("30 dní", "text", "Od {datum} do {datum} napršelo {x} mm, pršelo {n} dní (nejvíc {datum}: {x} mm). Z tvého pozemku při nich odteklo asi {x} m³, z toho {x} m³ ze střechy rovnou do kanálu. To je {x} konví vody na zálivku.", ""),
    ("30 dní", "text, bez deště", "Od {datum} do {datum} nepršelo víc než 1 mm za den, nic neodteklo. Zahrada žije ze zásoby v půdě.", ""),
    ("30 dní", "poznámka", "Předběžná měření ČHMÚ.", ""),
    ("voda shora, malá plocha", "upozornění", "Voda shora. Na pozemek stéká voda i z okolí, z plochy asi {plocha} nad ním. Při dešti {mm} mm by sem přiteklo asi {x} m³.", ""),
    ("voda shora, údolnice", "upozornění", "Možná cesta přívalové vody. Zdá se, že přívalová voda ze svahu nad tebou může protékat přes tento pozemek (stéká sem voda z asi {plocha}). Při dešti {mm} mm by sem přiteklo asi {x} m³. Při vzácném lijáku 53 mm (1x za 10 let) asi {x} m³. Doporučujeme s tou možností počítat a zvážit protiopatření.", ""),
    ("voda shora, potok", "upozornění", "Možná cesta přívalové vody. Pozemek leží v údolí, kudy teče potok nebo se slévá voda z velké plochy ({x} ha nad ním). Při přívalu tu může voda téct i mimo koryto. Doporučujeme s tou možností počítat a zvážit protiopatření.", ""),
    ("voda shora", "věta, skoro nic", "Při dešti {mm} mm se skoro všechna vsákne cestou.", ""),
    ("voda shora", "co pomůže", "Pomoct může průleh nebo nízký val na horní hraně pozemku, který vodu zpomalí a nechá vsáknout, propustné plochy a vyvýšený práh u vstupů do domu.", ""),
    ("voda shora", "poznámka", "Odhad z výškopisu a mapy půd. Ulice, obrubníky, kanalizace a ploty v něm nejsou a mohou vodu poslat jinam. Je to nápověda, ne posudek.", ""),
    ("krok 3", "štítek rozbalovací části", "Pro zvídavé - jak se to počítá, jiný déšť", ""),

    ("#", "Krok 4: co udělat (hra Kapka / Louže / Tůňka / Oáza)"),
    ("bez zahrady", "upozornění", "Ve výběru je skoro jen dům, bez zahrady. Patří k domu i zahrada? Označ ji v mapě a nabídnu i záhon, strom nebo vsak. [Označit zahradu]", ""),
    ("ukazatel", "nadtitulek", "Tvůj pozemek je", ""),
    ("ukazatel", "úrovně", "Kapka: skoro všechno odteče | Louže: něco zůstane | Tůňka: většina zůstane | Oáza: udržíš skoro všechno", "od 0, 25, 50 a 80 %"),
    ("ukazatel", "text", "Z deště {mm} mm udržíš doma {x} m³ z {x} m³, které by jinak odtekly. Za posledních 30 dní ({x} mm) by zůstalo {x} m³ z {x} m³.", ""),
    ("ukazatel", "tip", "Do další úrovně: zkus {opatření} (+{x} m³).", ""),
    ("ukazatel", "odznaky", "Pomáháš proti: přívalu | suchu | horku | pro život", ""),
    ("nad dlaždicemi", "poznámka", "Čísla platí pro tvůj pozemek a zvolený déšť. Zdroje a podrobnosti najdeš u každého opatření v „Proč a jak“.", ""),
    ("filtr", "tlačítka", "Sucho | Příval a voda do kanálu | Horko | Život a voda v krajině", "stejné jako v katalogu"),
    ("dlaždice", "nadpisy skupin", "Zadrží vodu z deště | Proti suchu, horku a pro život", ""),
    ("dlaždice", "prázdný filtr", "Pro zvolené oblasti tu nic není, zruš filtr nahoře.", ""),
    ("dlaždice", "štítky pracnosti", "za víkend | pár dní, technika | projekt s firmou", ""),
    ("dlaždice", "štítek ceny", "skoro zadarmo / od {x} Kč", ""),
    ("dlaždice, odpojení okapu", "věta", "Bez toho nefunguje sud ani záhon. Teď ti při {mm} mm odteče ze střechy {x} m³ do kanálu.", "varianta při části svodů: \"Bez toho se sud a záhon plní jen z části střechy. ...\""),
    ("dlaždice, sud a splachování", "věta", "Z deště {mm} mm zachytí {x} m³ = {x} konví na zálivku zadarmo.", ""),
    ("dlaždice, ostatní zadržení", "věta", "Z deště {mm} mm udrží doma {x} m³ ({x} konví), voda zůstane v zahradě místo v kanálu.", ""),
    ("dlaždice, bez výpočtu", "věta", "(použije se Hlavní věta opatření z listu Opatření)", ""),
    ("dlaždice", "upozornění", "Aby to fungovalo, vyber i: {opatření}.", ""),
    ("dlaždice", "hláška po kliknutí", "Přidal jsem i: {opatření} - bez toho by to nefungovalo.", ""),
    ("dlaždice", "štítek", "+ život v zahradě", ""),
    ("dlaždice", "rozbalovací část", "Proč a jak", "obsahuje název, popis a Kde to funguje z listu Opatření"),
    ("nehodí se", "rozbalovací část", "Nehodí se k tvému pozemku ({n}) - proč", "důvody jsou ve výpočtu (EFF), nejsou vytažené"),

    ("#", "Krok 5: výsledek"),
    ("výsledek", "nadtitulek", "Tvoje volba udrží doma", ""),
    ("výsledek", "text", "{x} m³ z každého deště {mm} mm ({popis deště}), to je {x} konví, které neodtečou do kanalizace. Za rok {x} m³. Za posledních 30 dní ({x} mm skutečného deště) by zůstalo {x} m³.", ""),
    ("výsledek", "odkazy", "Co kdyby to udělali i ostatní? → | Co může obec a celé území → | Všechna opatření → | Poslat odkaz", ""),
    ("výsledek", "poznámka ke sdílení", "Odkaz obsahuje čísla vybraných parcel a tvoje odpovědi. Nikam se neukládá, pošleš ho jen ty.", ""),
    ("výsledek, nic nevybráno", "upozornění", "Zatím jsi nevybral žádné opatření, které vodu zadrží. Vrať se ke kroku 4.", ""),
    ("Před a po", "nadpis", "Kolik vody odteče při dešti {mm} mm", ""),
    ("Před a po", "popisky", "teď | s tvými opatřeními | odteče pryč | zůstane u tebe (vsákne se nebo zadrží)", ""),
    ("200 domácností", "text", "Při 200 domácnostech srovnatelné velikosti zůstane při jednom běžném dešti ({mm} mm) zhruba {x} m³ vody v půdě a zahradách místo v kanálu. To je rozdíl mezi „odteklo“ a „zůstalo“, který může měnit poušť v oázu.", "\"běžném dešti\" / \"silném dešti\" / \"lijáku\" podle výběru"),
]

UZEMI = [
    ("#", "Úvod"),
    ("úvod", "nadtitulek", "Celé území", ""),
    ("úvod", "hlavní nadpis", "Kdo v Koryčanech rozhoduje o vodě", ""),
    ("úvod", "úvodní odstavec", "Při každém dešti odtéká voda ze střech domů, z velkých areálů i z polí. Tady uvidíš, kolik jí je, kdo o ní rozhoduje a co by se změnilo, kdyby se něco udělalo.", ""),
    ("obsah", "kapitoly", "1 Domácnosti - když se zapojí víc lidí | 2 Velké střechy - firmy, obec, zemědělci | 3 Pole, louky a les - jak hospodařit, aby voda neutekla | 4 Hráz na potoce - kolik vody zadrží | 5 Velké projekty - co musí obec a správci", ""),
    ("výběr deště", "popisek", "Počítáme pro déšť:", ""),
    ("výběr deště", "tlačítka", "běžný 10 mm | silný 20 mm | liják 32 mm | vzácný liják 53 mm | extrémní 87 mm", "nápověda po najetí: asi 17x za rok | asi 5x za rok | jednou za 2 roky | jednou za 10 let | jednou za 100 let"),

    ("#", "Kapitola 1: Domácnosti"),
    ("kap. 1", "nadtitulek", "Kapitola 1 · Domácnosti", ""),
    ("kap. 1", "nadpis", "Když se zapojí víc lidí", ""),
    ("kap. 1", "věta pro laika", "Kdyby se zapojilo {x} % domácností ({x} z {x}) a každá měla {opatření}, zůstane při dešti {mm} mm ({jak často}) v půdě a zahradách {x} m³ vody místo v kanálu.", "varianta \"jako můj pozemek\": \"... a každá udělala totéž co ty, ...\""),
    ("kap. 1", "věta, nikdo se nezapojí", "Posuň níž, kolik domácností se zapojí, a vyber, co udělají.", ""),
    ("kap. 1", "věta, nic nevybráno", "Vyber níž, co zapojené domácnosti udělají.", ""),
    ("Zkus si to", "nadtitulek", "Zkus si to", ""),
    ("Zkus si to", "posuvník", "Kolik domácností se zapojí: {x} %", ""),
    ("Zkus si to", "popisek + tlačítka", "Co udělají: odpojit okap od kanálu | dešťový záhon | sud nebo nádrž 1 m³ | propustná dlažba místo betonu", ""),
    ("Zkus si to", "tvary do věty", "odpojený okap | dešťový záhon | sud nebo nádrž | propustnou dlažbu", "doplňuje se do věty \"každá měla ...\""),
    ("Zkus si to", "popisek + tlačítka", "Jedna domácnost: průměrná v obci | jako můj pozemek", "druhé tlačítko má nápovědu \"Nejdřív projdi Můj pozemek\""),
    ("jako můj pozemek", "text", "Počítám, jako by každá zapojená domácnost měla pozemek jako ty: střecha {x} m², dlažba {x} m², zahrada {x} m², svody {svody}; opatření: {seznam}. Jedna domácnost tak udrží {x} m³ z deště {mm} mm. [Změnit v Můj pozemek] Domy v obci mají různé střechy a půdy, je to „co kdyby“, ne odhad pro obec 🤔. Průměrný dům v území má půdorys {x} m² (ČÚZK ✅).", ""),
    ("upozornění", "text", "Dešťový záhon a sud bez odpojeného okapu nic nezadrží, voda z okapu teče do kanálu a k nim se nedostane. Zapni i „odpojit okap od kanálu“.", ""),
    ("klíčová čísla, karta 1", "číslo + popis", "{x} - domácností z {x} se zapojí", ""),
    ("klíčová čísla, karta 2", "číslo + popis", "{x} m³ - zůstane z jednoho deště {mm} mm. Teď ze střech a dvorů všech domácností odteče {x} m³.", ""),
    ("klíčová čísla, karta 3", "číslo + popis", "{x} m³ - za rok, to je asi {x} cisteren po 10 m³", ""),
    ("Na co to nestačí", "nadtitulek", "Na co to nestačí", ""),
    ("Na co to nestačí", "text", "{x} m³ je {x} % vody, která při {mm} mm spadne na celé území ({x} m³). Povodňovou vlnu na Kyjovce to nezmění. Na tu jsou potřeba změny na polích a v lesích (kapitola 3) a na potocích (kapitola 4).", ""),
    ("Co to ale je", "nadtitulek", "Co to ale je", ""),
    ("Co to ale je", "text", "{x} m³ vody za rok zůstane v půdě a zahradách místo v kanálu, bez jediné velké stavby. A při každém takovém dešti steče do potoka o {x} m³ méně a pomaleji.", ""),
    ("kap. 1", "štítek rozbalovací části", "Pro zvídavé - upřesnit čísla, rozpad po částech území, zdroje", ""),

    ("#", "Kapitola 2: Velké střechy"),
    ("kap. 2", "nadtitulek", "Kapitola 2 · Velké střechy", ""),
    ("kap. 2", "nadpis", "Kdo rozhoduje o nejvíc vodě", ""),
    ("kap. 2", "věta pro laika", "Jedna průměrná průmyslová střecha dá při dešti tolik vody jako {x} rodinných domů. O takové střeše rozhoduje jeden majitel nebo jedna rada, ne stovky lidí.", ""),
    ("graf", "nadpis", "Voda ze střech při jednom dešti {mm} mm", ""),
    ("graf", "skupiny budov", "domácnosti | průmysl | zemědělství | vedlejší stavba (garáž, kůlna) | veřejná služba | bytový dům | obchody a služby | všechny budovy", "názvy řádků grafu"),
    ("Kdo s tím může co udělat", "nadpis", "Kdo s tím může co udělat", ""),
    ("karta Domácnosti", "seznam", "Domácnosti: odpojit okap od kanálu | sud nebo nádrž, i u garáže a kůlny | dešťový záhon nebo vsakovací objekt", "pod nadpisem karty: \"{x} domů a {x} garáží a kůlen, {x} m³ při {mm} mm\" a odkaz \"Spočítej svůj pozemek →\""),
    ("karta Firmy", "seznam", "Firmy a průmysl: odpojit svody a vodu vsakovat nebo jímat na areálu | zelená střecha | propustné parkoviště a plochy", ""),
    ("karta Obec", "seznam", "Obec, škola, kraj: zadržet vodu z veřejných budov | propustné chodníky a parkoviště | zelená střecha na škole nebo úřadě", ""),
    ("karta Zemědělci", "seznam", "Zemědělské podniky: nádrž na vodu ze střech pro závlahu | vsak a propustné dvory", ""),
    ("karta Bytové domy", "seznam", "Bytové domy (SVJ, družstva): odpojit svody, vsak nebo nádrž | zelená střecha", ""),
    ("kap. 2", "upozornění", "Co v datech chybí: kam tyhle střechy dnes odvádějí vodu (kanalizace, vsak, potok). Zjistit se to dá u provozovatelů. Otázka pro město: je kanalizace jednotná, nebo oddílná?", ""),
    ("kap. 2", "štítek rozbalovací části", "Pro zvídavé - celá tabulka podle účelu budov a zdroje", ""),

    ("#", "Kapitola 3: Pole, louky a les"),
    ("kap. 3", "nadtitulek", "Kapitola 3 · Pole, louky a les", ""),
    ("kap. 3", "nadpis", "Jak hospodařit, aby voda neutekla", ""),
    ("kap. 3", "věta pro laika", "Území má 1 770 ha a skoro všechno jsou pole, louky a les. Jak na nich hospodaří zemědělci a lesníci, rozhoduje, kolik vody při lijáku steče po povrchu do potoka a kolik se vsákne.", ""),
    ("číslo odtoku", "nadtitulek", "Jak poznáme, kolik vody z plochy steče", ""),
    ("číslo odtoku", "text", "Každá plocha má číslo odtoku. Čím vyšší, tím víc vody steče po povrchu. Záleží na tom, co na ploše je, v jakém je stavu a jaká je pod ní půda. Opatření na polích ho snižují.", ""),
    ("číslo odtoku, stupnice", "popisky", "50 = vsákne se víc | steče víc = 100 | les | louky | zahrady | orná půda | střechy, silnice", ""),
    ("číslo odtoku", "poznámka", "Stupnice od 50 (vsákne se víc) do 100 (steče všechno).", ""),
    ("číslo odtoku", "poznámka", "Do jakého deště se při běžně vlhké půdě vsákne skoro všechno: {les asi x mm, louky asi x mm, ...}; střecha a asfalt pouští vodu hned. Proto se opatření na polích projeví hlavně u lijáků.", ""),
    ("Zkus si to", "nadtitulek", "Zkus si to", ""),
    ("Zkus si to", "posuvník", "Pole bez orby, zbytky plodin a meziplodiny na povrchu: {x} % orné půdy", ""),
    ("Zkus si to", "posuvník", "Orba a setí po vrstevnici, s travnatými pásy: {x} % orné půdy", ""),
    ("Zkus si to", "posuvník", "Zatravnit strmá pole (nad 7°): {x} % z nich", ""),
    ("Zkus si to", "zaškrtávátko", "Zatravnit údolnice, kudy se na polích slévá voda (místa, kam stéká aspoň 1 ha)", ""),
    ("Zkus si to", "výběr", "Stav lesa (hrabanka, podrost): dobrý | střední (výchozí) | špatný", ""),
    ("Zkus si to", "výběr", "Louky a pastviny: hustý porost (výchozí) | řidší porost | přepasené, holá místa", ""),
    ("malý déšť", "upozornění", "Při dešti {mm} mm se na polích, loukách a v lese skoro všechno vsákne nebo zůstane na rostlinách; po povrchu teče hlavně voda ze střech a silnic. Z polí začne voda stékat až u silnějšího deště, u průměrné půdy v území nad zhruba {x} mm. Změny na polích proto uvidíš u lijáku. [Přepnout na liják 32 mm]", ""),
    ("klíčová čísla, karta 1", "číslo + popis", "{x} m³ - steče teď po povrchu z polí, luk, lesů a zastavěných ploch při dešti {mm} mm", ""),
    ("klíčová čísla, karta 2", "číslo + popis", "{x} m³ - se změnami, tedy o {x} m³ ({x} %) méně", "bez změny: \"se změnami. Zkus posuvníky výš nebo silnější déšť.\""),
    ("klíčová čísla, karta 3", "číslo + popis", "{x} t/ha - půdy smyje déšť z orné půdy průměrně za rok, se změnami {x} t/ha. Přípustné je {x} t/ha ✅.", ""),
    ("mapa eroze", "nadpis", "Kde se z polí smývá půda", ""),
    ("mapa eroze", "text", "Mapa ukazuje průměrnou roční ztrátu půdy na orné půdě. Nejvíc se smývá na dlouhých a strmých svazích a tam, kde se voda slévá. Přepni, co by se změnilo.", ""),
    ("mapa eroze", "tlačítka", "teď (obilniny) | bez orby, meziplodiny | + zatravnit strmá pole a údolnice", ""),
    ("mapa eroze", "legenda", "do 2 t/ha | 2-9 t/ha | 9-20 t/ha | nad 20 t/ha", ""),
    ("mapa eroze", "věta pod mapou", "Z orné půdy ({x} ha) se smývá průměrně {x} t/ha za rok. Na {x} % plochy je to víc, než kolik je přípustné ({x} t/ha).", ""),
    ("mapa eroze", "hlášky", "Načítám terén a půdy... | Rastry se nenačetly - mapa eroze nefunguje.", ""),
    ("kap. 3", "štítek rozbalovací části", "Pro zvídavé - tabulka ploch, jak se to počítá a zdroje", ""),

    ("#", "Kapitola 4: Hráz na potoce"),
    ("kap. 4", "nadtitulek", "Kapitola 4 · Hráz na potoce", ""),
    ("kap. 4", "nadpis", "Kolik vody zadrží hráz", ""),
    ("kap. 4", "věta pro laika", "Klikni do mapy na modrý potok. Na tom místě se postaví hráz napříč potokem a spočítá se, kam až by voda vystoupala a kolik by se jí vešlo.", ""),
    ("kap. 4", "výběr", "Výška hráze nad dnem potoka: 0,5 m | 1 m | 1,5 m | 2 m | 2,5 m (vodní dílo) | 3 m (vodní dílo) | 4 m (vodní dílo)", ""),
    ("mapa hráze", "hlášky", "Toky a terén se načtou po otevření mapy (asi 0,8 MB). | Načítám toky a terén... | Klikni na modrý potok. | Toky nebo terén se nenačetly - tato část nefunguje. | Mimo data modelu.", ""),
    ("mapa hráze", "hláška", "Hráz se staví jen na potoce (modré čáry). Nejbližší je {x} m od kliku - klikni blíž.", ""),
    ("výsledek hráze", "popisky", "nádrž za hrází / tůň / poldr v údolnici (orientačně) | zatopí {x} m², hloubka max {x} m / rozsah: údolí tvaru V až ploché dno | odteče z povodí při dešti {mm} mm | povodí k hrázi {x} km² | nádrž pojme | prázdná nádrž, bez ztrát", ""),
    ("výsledek hráze", "věta", "Hráz by byla {x} m dlouhá - údolí neuzavře.", "\"údolí neuzavře\" jen když platí"),
    ("výsledek hráze", "věta, malý déšť", "Při dešti {mm} mm z povodí po povrchu skoro nic neodteče, vsákne se. Nádrž plní hlavně silnější deště a průtok v potoce (ten model nepočítá) - pro posouzení hráze vyber silnější déšť.", ""),
    ("výsledek hráze", "upozornění", "Pro informaci: {text z výpočtu}", "texty upozornění (vodní dílo apod.) jsou ve web/jadro.js"),
    ("Bobr", "nadtitulek", "Bobr to umí sám", ""),
    ("Bobr", "text", "Bobr evropský na Kyjovce žije a jeho hráze jsou místy vysoké skoro 1 m. Zvedají hladinu, zpomalují odtok a kolem nich vznikají mokřady, kde se usazují splaveniny a daří se dalším druhům. Povolení nepotřebuje. U nás je to silně ohrožený druh.", ""),
    ("kap. 4", "štítek rozbalovací části", "Pro zvídavé - co model nepočítá a co je potřeba ke stavbě", ""),

    ("#", "Kapitola 5: Velké projekty"),
    ("kap. 5", "nadtitulek", "Kapitola 5 · Velké projekty", ""),
    ("kap. 5", "nadpis", "Co musí udělat obec a správci", ""),
    ("kap. 5", "věta pro laika", "Tohle jedna rodina ani jeden zemědělec neudělá. Kolik vody tyhle projekty zadrží, tu nepočítáme: bez projektu a měření by to byl jen odhad.", ""),
    ("karty projektů", "popisky", "Co to udělá: | rozhoduje: | povolení: | Co o tom víme a z čeho to zaplatit | Financování:", "název, popis a hlavní věta karet jsou v listu Opatření"),

    ("#", "Výzva na konci"),
    ("výzva", "nadpis", "Začni u sebe", ""),
    ("výzva", "text", "Nejrychleji se dá začít na vlastním pozemku. Spočítej, kolik vody ti uteče a co s tím jde udělat.", ""),
    ("výzva", "odkazy", "Spočítej svůj pozemek → | Všechna opatření (katalog) →", ""),
]

KATALOG = [
    ("#", "Úvod a filtry"),
    ("úvod", "nadtitulek", "Katalog", ""),
    ("úvod", "hlavní nadpis", "Co se dá udělat", ""),
    ("úvod", "úvodní odstavec", "Od sudu pod okapem po rybník. U každého opatření najdeš, co udělá, kolik stojí, kdo ho může udělat a z čeho ho zaplatit.", ""),
    ("filtr Kde", "popisek", "Kde", ""),
    ("filtr Kde", "tlačítka", "Zahrada: záhon, dvůr, sad | Dům a střecha: okapy, nádrž, fasáda | Obec a škola: náměstí, ulice, veřejné budovy | Krajina: pole, louky, les, potok | Měř s námi: škola, dobrovolníci", ""),
    ("filtr S čím", "popisek", "S čím to pomůže", ""),
    ("filtr S čím", "tlačítka", "Sucho | Příval a voda do kanálu | Horko | Život a voda v krajině", ""),
    ("počet", "věta", "Všech {66} opatření podle místa, od nejsnazších. / Zobrazeno {x} z {66} opatření.", "bez filtru / s filtrem"),
    ("filtry", "odkaz", "Zrušit výběr", ""),
    ("podrobné filtry", "štítek", "Podrobné filtry (pro školu a úřad)", ""),
    ("podrobné filtry", "popisky", "Místo | Kdo rozhoduje | Účinek | Peníze a pracnost", ""),
    ("podrobné filtry", "tlačítka", "jen s dotací, která je teď otevřená | jen svépomoc (za víkend, bez povolení)", ""),
    ("pod filtry", "poznámka", "Čísla jsou pro vzorový dům (100 m² střechy, 50 m² dvora, běžný déšť 10 mm). Pro tvůj dům je spočítá Můj pozemek. Zdroje, ceny a podrobnosti jsou u každého opatření v „Proč a jak“.", ""),

    ("#", "Skupiny a dlaždice"),
    ("rozcestník", "popisek", "Přejít na:", ""),
    ("skupiny", "nadpisy", "Na zahradě | Na domě a střeše | V obci a ve škole | Na poli | Na louce a pastvině | V lese | U potoka, tůně a pramene | U cest, na svazích a ve stržích | Měř s námi", ""),
    ("skupiny", "tlačítko", "Ukázat další {n} opatření →", ""),
    ("prázdný výběr", "věta", "Tomuhle výběru nic neodpovídá. Zruš některý filtr.", ""),
    ("dlaždice", "spočtené číslo", "z tohoto deště zadrží {x} m³ / za rok zůstane až {x} m³ vody (vzorový dům, 10 mm)", "u zahrady a domu; jinak se použije Hlavní věta z listu Opatření"),
    ("dlaždice", "štítky", "za víkend | pár dní, technika | projekt s firmou | skoro zadarmo / od {x} Kč | udělá každý sám / rozhoduje: {kdo} | povolení: úřad / souhlas | + život | velký projekt", ""),
    ("dlaždice", "odkaz", "Spočítej u sebe →", ""),
    ("dlaždice", "rozbalovací části", "Kde to funguje ({n}) / Přenositelnost a rizika | Proč a jak", ""),
    ("Kde to funguje", "popisky", "Přenositelnost do Koryčan: | Rizika, co z toho neplyne:", "texty jsou v listu Opatření"),
    ("Proč a jak", "popisky", "Cena: | Z čeho zaplatit: | Povolení: | Kde: | rozhoduje: | Nejdřív je potřeba: | Hodí se k: | Nedohledáno: | Kód v katalogu:", "obsah je spíš pro zvídavé"),
]

OMODELU = [
    ("#", "Úvod"),
    ("úvod", "nadtitulek", "O modelu", ""),
    ("úvod", "hlavní nadpis", "Jak to počítáme a co ještě neumíme", ""),
    ("úvod", "úvodní odstavec", "Aplikace je zjednodušený model pro osvětu: pomáhá rozhodnout, kde začít. Není to projekt stavby. Tady je, odkud čísla jsou, co je hotové a co ještě chybí.", ""),
    ("obsah", "kapitoly", "1 Co je hotové - a co ještě chybí | 2 Jak se počítá - metody a vzorce | 3 Odkud jsou data - zdroje a licence | 4 Z čeho to zaplatit - dotace a další cesty | 5 Co model neumí - a kdo za ním stojí", ""),

    ("#", "Kapitola 1: Stav"),
    ("kap. 1", "nadtitulek", "Kapitola 1 · Stav", ""),
    ("kap. 1", "nadpis", "Co je hotové a co chybí", ""),
    ("kap. 1", "věta pro laika", "Aplikace běží na skutečných datech o terénu, půdě, budovách a srážkách v Koryčanech, ale zatím jsme ji neporovnali s měřením průtoku v potoce. Proto u ní stojí nevalidováno.", ""),
    ("Hotovo", "bod", "Jak bylo: srážky ČHMÚ Koryčany od roku 1921, teploty od roku 2001, měřené prameny a průtok Kyjovky, možný výpar z měření (Penman-Monteith); denní data se stahují sama čtyřikrát denně.", ""),
    ("Hotovo", "bod", "Můj pozemek: skutečné parcely a budovy z katastru, sklon z výškopisu, půda z mapy VÚMOP, skutečný déšť za posledních 30 dní.", ""),
    ("Hotovo", "bod", "Půda: podrobná mapa hydrologických skupin půd od VÚMOP (27. 10. 2026), i pro les a zástavbu; dřív byl skoro 40 % území odhad.", ""),
    ("Hotovo", "bod", "Celé území: střechy podle účelu budov, odtok z polí, luk a lesů po čtvercích 5 m, eroze orné půdy, objem vody za hrází na potoce.", ""),
    ("Hotovo", "bod", "Katalog: 66 opatření s účinkem, cenou, zdrojem a cestou k penězům.", ""),
    ("Rozpracováno", "bod", "Měření: reakce Stříbrníku na déšť u Kachníku (léto 2026) je zpracovaná; data z přehrady od Povodí Moravy zatím nemáme.", ""),
    ("Rozpracováno", "bod", "Zkouška s lidmi: Můj pozemek prošel první test s občanem a podle něj se upravil.", ""),
    ("Chybí", "bod", "Ověření na měření (validace): porovnat výpočet s průtokem v potoce po skutečném dešti.", ""),
    ("Chybí", "bod", "Průběh povodňové vlny: model počítá objemy vody, ne to, jak rychle vlna přijde a jak ji opatření zpomalí.", ""),
    ("Chybí", "bod", "Klima 2050 a 2090 v číslech pro Koryčany: zatím jen výhled CzechGlobe a IPCC v Jak bylo.", ""),
    ("Chybí", "bod", "Horko a vítr jako mapa a formulář pro měření školy.", ""),

    ("#", "Kapitola 2: Metody"),
    ("kap. 2", "nadtitulek", "Kapitola 2 · Metody", ""),
    ("kap. 2", "nadpis", "Jak se počítá", ""),
    ("kap. 2", "věta pro laika", "Otázka je vždy stejná: kolik vody z deště zůstane a kolik odteče. Počítáme jednoduchými ověřenými metodami, aby se dal každý výsledek přepočítat ručně.", ""),
    ("kap. 2", "poznámka", "Značky u čísel: ✅ zdroj jsme otevřeli a ověřili, ⏳ zdroj starší než rok, 📄 citováno z druhé ruky, 🤔 odhad, 💻 neověřeno.", ""),
    ("kap. 2", "štítky rozbalovacích částí", "Pro zvídavé - metody po záložkách | Pro zvídavé - konstanty a vzorce", ""),

    ("#", "Kapitola 3: Data"),
    ("kap. 3", "nadtitulek", "Kapitola 3 · Data", ""),
    ("kap. 3", "nadpis", "Odkud jsou data", ""),
    ("kap. 3", "věta pro laika", "Jen z veřejných zdrojů státních a odborných institucí: mapy a katastr ČÚZK, měření ČHMÚ, půdy VÚMOP. Osobní údaje (vlastníci pozemků, adresy) aplikace nenačítá ani neukládá.", ""),
    ("kap. 3", "štítek rozbalovací části", "Pro zvídavé - tabulka zdrojů a licencí", ""),

    ("#", "Kapitola 4: Peníze"),
    ("kap. 4", "nadtitulek", "Kapitola 4 · Peníze", ""),
    ("kap. 4", "nadpis", "Z čeho to zaplatit", ""),
    ("kap. 4", "věta pro laika", "Nejrychlejší cesta jsou vlastní peníze: bez žádostí a bez čekání, a řada opatření na zahradě stojí málo nebo skoro nic. Pro větší věci jsou tu dotace. U každé je odkaz a jedna věta: kdy, kolik a na co. Dotace se mění, před žádostí vždy otevři odkaz.", ""),
    ("kap. 4", "nadpisy skupin", "Bez žádostí | Pro domácnosti | Pro obec, školu a spolky | Pro krajinu a zemědělce", "věty k jednotlivým dotacím jsou v listu Dotace"),

    ("#", "Kapitola 5: Hranice"),
    ("kap. 5", "nadtitulek", "Kapitola 5 · Hranice", ""),
    ("kap. 5", "nadpis", "Co model neumí", ""),
    ("kap. 5", "bod", "Nenahradí projekt. Pro stavbu nádrže, poldru nebo vsaku je potřeba projektant, hydrogeolog a povolení.", ""),
    ("kap. 5", "bod", "Neukáže zatopené ulice. Rozliv vody po obci (2D hydraulika) je úloha pro specializované programy.", ""),
    ("kap. 5", "bod", "Nezná skutečný stav každého pozemku. Kam vedou okapy, kolik je dlažby nebo jak se hospodaří na poli, víš líp ty.", ""),
    ("kap. 5", "bod", "Nepočítá podzemní vodu a to, jak rychle se po dešti doplní studny.", ""),
    ("Kdo za tím stojí", "nadtitulek", "Kdo za tím stojí", ""),
    ("Kdo za tím stojí", "text", "Aplikaci připravuje skautský oddíl v Koryčanech spolu se ZŠ Koryčany (program Ekoškola). Je nekomerční a otevřená: kód i data jsou veřejně na GitHubu, podrobný stav práce je na stránce Stav projektu.", ""),
]

NAVOD = [
    "Texty webu Voda v Koryčanech pro přepis vlastními slovy (laická úroveň). Stav k " + STAV + ".",
    "",
    "Jak s tím pracovat",
    "1. Každý list je jedna záložka webu (Společné = záhlaví, upozornění a patička). Řádky jdou v pořadí, jak je vidíš na stránce shora dolů.",
    "2. Sloupec D \"Původní text\" je dnešní text. Do žlutého sloupce E \"Nový text\" napiš svou verzi. Když text měnit nechceš, nech E prázdné.",
    "3. Do sloupce F \"Tvoje poznámka\" můžeš psát cokoli (např. \"zkrátit\", \"tohle vyhodit\", \"nerozumím\").",
    "4. Čísla ve složených závorkách {takto} doplňuje web sám z dat. Nech je ve svém textu (můžeš je přesunout jinam ve větě), ať se dál počítají.",
    "5. Svislá čára | odděluje samostatné krátké texty (tlačítka, popisky v legendě). Přepiš je ve stejném pořadí a oddělené stejně.",
    "6. Lomítko / odděluje varianty, které se zobrazují podle situace.",
    "7. Pravidla textu: tykání, klidný tón, jen spojovník -, nikdy dlouhá pomlčka. Každé číslo \"za rok\" nese \"v průměru\" a období.",
    "",
    "Co tu není",
    "- Obsah rozbalovacích částí \"Pro zvídavé\" (metody, zdroje, tabulky, značky původu). Je jen štítek té části.",
    "- Popisky os grafů, technické hlášky a formuláře v části Upřesnit čísla.",
    "- Hlavní věta, popis a \"Kde to funguje\" u opatření jsou v listu Opatření; věty k dotacím v listu Dotace.",
    "",
    "Až budeš hotový, pošli soubor zpět; nové texty se přenesou do webu.",
]

COLS = [("Č.", 8), ("Kde na webu", 24), ("Druh textu", 16), ("Původní text", 62), ("Nový text (piš sem)", 62), ("Tvoje poznámka", 26), ("Poznámka k textu", 30)]
THIN = Side(style="thin", color="BBBBBB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
F_HEAD = PatternFill("solid", fgColor="1F6F8B")
F_SEC = PatternFill("solid", fgColor="DCE9EF")
F_NEW = PatternFill("solid", fgColor="FFF6CC")


def list_sheet(wb, nazev, prefix, polozky):
    ws = wb.create_sheet(nazev)
    for c, (t, w) in enumerate(COLS, 1):
        cell = ws.cell(row=1, column=c, value=t)
        cell.font = Font(bold=True, color="FFFFFF"); cell.fill = F_HEAD; cell.alignment = WRAP; cell.border = BOX
        ws.column_dimensions[get_column_letter(c)].width = w
    r, n = 2, 0
    for p in polozky:
        if p[0] == "#":
            ws.cell(row=r, column=1, value=p[1]).font = Font(bold=True, size=12)
            for c in range(1, len(COLS) + 1):
                ws.cell(row=r, column=c).fill = F_SEC
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(COLS))
            r += 1; continue
        n += 1
        kde, druh, text, pozn = p
        vals = [f"{prefix}-{n:03d}", kde, druh, text, "", "", pozn]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.alignment = WRAP; cell.border = BOX
            if c == 5: cell.fill = F_NEW
        r += 1
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{r - 1}"
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"
    return n


def opatreni_polozky(op, akce):
    SK = [("Z", "Na zahradě"), ("S", "Na domě a střeše"), ("U", "V obci a ve škole"), ("P", "Na poli"), ("L", "Na louce a pastvině"),
          ("LES", "V lese"), ("T", "U potoka, tůně a pramene"), ("C", "U cest, na svazích a ve stržích"), ("M", "Měř s námi")]
    pred = lambda o: "U" if re.sub(r"\d+$", "", o["id"]) == "H" else re.sub(r"\d+$", "", o["id"])
    out = []
    for p, t in SK:
        ops = [o for o in op["opatreni"] if pred(o) == p]
        if not ops: continue
        out.append(("#", f"{t} ({len(ops)})"))
        for o in ops:
            k = f"{o['id']} {o['nazev'].split(' (')[0]}"
            out.append((k, "název", o["nazev"], "text v závorce se ukazuje jako podnázev"))
            if o["id"] in akce:
                out.append((k, "název v Můj pozemek", akce[o["id"]], "krátce, jako úkol"))
            if o.get("popis"): out.append((k, "popis", o["popis"], ""))
            h = o.get("hlavni_cislo") or {}
            if h.get("text"): out.append((k, "hlavní věta (jedno číslo)", h["text"], "píše se malým písmenem, web ji v Můj pozemek začne velkým; číslo musí odpovídat zdroji"))
            if o.get("prenositelnost"): out.append((k, "přenositelnost do Koryčan", o["prenositelnost"], "v části Kde to funguje"))
            if o.get("rizika"): out.append((k, "rizika", o["rizika"], "v části Kde to funguje"))
    return out


def dotace_polozky(op):
    SK = [("Bez žádostí", ["vlastni", "participativni"]), ("Pro domácnosti", ["nzu_rd_2026"]),
          ("Pro obec, školu a spolky", ["aopk_zmv", "opzp_1_3_4", "opzp_1_3_1"]), ("Pro krajinu a zemědělce", ["ppk_b", "szp_agroles", "kopu"])]
    out, P = [], op["programy"]
    for t, ks in SK:
        out.append(("#", t))
        for k in ks:
            if k not in P: continue
            p = P[k]
            out.append((p["nazev"], "věta: kdy, kolik, na co", p.get("veta") or p.get("pozn") or "", "termíny a částky před zveřejněním ověřit online"))
    return out


def main():
    op = json.load(open(os.path.join(ROOT, "data", "opatreni.json"), encoding="utf-8"))
    src = open(os.path.join(ROOT, "tools", "build_dummy.py"), encoding="utf-8").read()
    blok = src[src.index("const AKCE = {"):src.index("const AK = o =>")]
    akce = dict(re.findall(r"(\w+):\{t:'([^']+)'", blok))
    wb = Workbook(); ws = wb.active; ws.title = "Návod"
    ws.column_dimensions["A"].width = 120
    for k, t in enumerate(NAVOD, 1):
        c = ws.cell(row=k, column=1, value=t); c.alignment = Alignment(wrap_text=True)
        if t in ("Jak s tím pracovat", "Co tu není") or k == 1: c.font = Font(bold=True, size=12 if k == 1 else 11)
    pocty = []
    for nazev, pre, pol in [("Společné", "SP", SPOLECNE), ("Jak bylo", "JB", JAKBYLO), ("Můj pozemek", "PZ", POZEMEK),
                            ("Celé území", "UZ", UZEMI), ("Katalog", "KT", KATALOG), ("Opatření", "OP", opatreni_polozky(op, akce)),
                            ("Dotace", "DT", dotace_polozky(op)), ("O modelu", "OM", OMODELU)]:
        pocty.append((nazev, list_sheet(wb, nazev, pre, pol)))
    r = len(NAVOD) + 2
    ws.cell(row=r, column=1, value="Počet textů v listech").font = Font(bold=True)
    for k, (nazev, n) in enumerate(pocty, 1):
        ws.cell(row=r + k, column=1, value=f"{nazev}: {n}")
    wb.save(OUT)
    print(OUT, sum(n for _, n in pocty), "textů")


if __name__ == "__main__":
    main()
