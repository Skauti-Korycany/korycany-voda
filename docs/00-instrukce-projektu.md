# Instrukce projektu: Koryčany resilience

## 1. Účel projektu

Vzniká samostatně fungující interaktivní webová aplikace (jeden HTML soubor + datové balíčky), ve které obyvatelé Koryčan uvidí reálná data o své krajině (terén, půda, geologie, voda, historické mapy, klima dnes a ve scénářích 2050/2090) a mohou si zjednodušeně "zkusit" adaptační opatření: malé nádrže, mokřady, suché poldry, výsadby, meze, větrolamy, změny hospodaření. Aplikace okamžitě ukáže orientační efekt na zadržení vody, povodňovou vlnu, sucho, horko a vítr.

Cíl není model pro projektanty. Cíl je, aby víc lidí ve městě pochopilo souvislosti, chtělo se zapojit a vědělo, co může udělat kdo (obec, zemědělec, lesník, zahrádkář, škola).

Nositel: skautský oddíl v Koryčanech. Partner: ZŠ Koryčany (program Ekoškola). Nekomerční, osvětové, veřejné.

## 2. Území

Katastrální území Koryčany, Jestřabice, Blišice, Lískovec u Koryčan a navazující povodí Kyjovky nad městem (VN Koryčany, přítoky z Chřibů). Přesnou hranici modelu určí rozvodnice odvozená z DMR 5G, ne katastr. Hranici upřesnit ve fázi 1 a zapsat do STAV.md.

## 3. Cílové skupiny a dvě úrovně rozhraní

- **Občan**: jednoduché scénáře, klikni a umísti opatření, vidíš efekt v číslech a mapě, u každého opatření "kdo to může udělat a z čeho se to dá zaplatit".
- **Škola / expert**: stejné jádro, navíc vrstvy, vzorce, zdroje, možnost zadávat vlastní měření (srážky, teploty, hladina, erozní rýhy) do sdílené databáze.

Jedno výpočetní jádro, dvě obálky. Nic se nedubluje.

## 4. Definice hotového výsledku

1. Aplikace běží bez serveru (statický web, lze dát na web města nebo oddílu), funguje na mobilu.
2. Každé číslo v aplikaci má dohledatelný původ: vstupní data se zdrojem a datem, vzorec s odkazem na metodiku.
3. Každé opatření má: popis, pro jaký extrém pomáhá, realistický rozsah účinku, kdo ho realizuje, dotační/finanční cesta, odkaz na příklad z ČR.
4. V aplikaci je viditelné upozornění, že jde o zjednodušený model pro osvětu a prioritizaci, ne o projektovou dokumentaci.
5. Existuje stručná metodika (MD), aby na to šlo navázat po letech nebo to převzal někdo jiný.

## 5. Technologická rozhodnutí (fixní, neotvírat znovu bez důvodu)

- Rozhraní: jeden HTML soubor, Leaflet.js, žádný backend. Podklady živě z WMS státních institucí, vlastní vrstvy jako GeoJSON a PNG/COG dlaždice v samostatné složce.
- Výpočty: JavaScript v prohlížeči, transparentní a jednoduché metody (SCS-CN odtok z návrhového deště, objem nádrže z DMR při zvolené hrázi, zjednodušená transformace vlny poldrem, roční vodní bilance P - ET podle scénáře, USLE pro erozi, jednoduché indexy pro horko a vítr).
- Datová příprava: Python skripty (rasterio, geopandas, pysheds/whitebox) na PC uživatele. Claude skripty píše a testuje na vzorcích, uživatel je spouští nad plnými daty a nahrává odvozené výstupy. (QGIS se nakonec nepoužívá, viz STAV.)
- Souřadnice: data v S-JTSK (EPSG:5514), web ve WGS84/Web Mercator; převody dělají skripty, ne aplikace.
- Rozlišení modelového rastru: 5 m (DMR 5G převzorkovat), intravilán 1 m; hrubší vrstvy nahoru nepřevádět na falešnou přesnost.
- Vlastní měření školy: sdílená databáze artefaktu nebo export CSV, nikdy osobní údaje žáků.

## 6. Datové zdroje (priorita, licence)

Pořadí: 1) státní a akademické zdroje s otevřenou licencí (ČÚZK CC BY 4.0: DMR 5G, ortofoto, ZTM, archivní mapy), 2) odborné portály s nekomerční licencí (VÚMOP SOWAC GIS: BPEJ, hydrologické skupiny půd, eroze; ČGS: geologie, hydrogeologie; DIBAVOD: toky, povodí; ČHMÚ/Povodí Moravy: záplavová území, srážky; ClimRisk/CzechGlobe: klimatické scénáře; ÚHÚL: lesní typologie; LPIS: využití půdy), 3) historické mapy (císařské otisky stabilního katastru, 2. a 3. vojenské mapování, archivní ortofoto 50. let).

Pravidla: před zabalením jakékoli vrstvy do distribuovaného balíčku ověřit licenci a zapsat ji do seznamu vrstev. WMS v aplikaci je přípustné bez redistribuce dat. Pokud zdroj nelze dohledat nebo otevřít, napsat "nedohledal jsem", ne nahradit podobným.

## 7. Vědecké zásady

- Každá vazba "opatření -> efekt" musí mít citovanou metodiku nebo studii (české prostředí přednostně: VÚMOP, VÚV TGM, ČZU, MENDELU, CzechGlobe, metodiky MŽP/AOPK). Bez zdroje se efekt v aplikaci nezobrazí, nebo se zobrazí jako "odhad" s viditelným označením.
- Nejistotu ukazovat jako rozsah, ne jako jedno číslo.
- Model validovat alespoň na jednom dostupném měření (limnigraf, známá povodeň, Intersucho); dokud to není hotové, aplikace nese označení "nevalidováno".
- Klimatické scénáře brát z aktuálních českých výstupů (ClimRisk, hodnocení ČHMÚ/CzechGlobe), uvádět scénář a horizont u každého čísla.
- Nepoužívat zdroje starší než cca 5 let pro klima a dotace, u fyzikálních metod stáří nevadí.

## 8. Dělba práce

**Claude**: rešerše a ověření zdrojů, seznam vrstev s WMS adresami, Python skripty, výpočetní jádro, HTML aplikace, texty a vysvětlivky, katalog opatření a dřevin, metodika, MD sumáře.

**Uživatel**: stažení velkých rastrů z portálů, spouštění skriptů, nahrání odvozených výstupů, terénní znalost (kde teče voda, co je v územním plánu, vlastnické poměry), kontakty na město, školu a Povodí Moravy, konečné rozhodnutí o tom, co se zveřejní.

**Claude otevřeně říká, že není vhodný nástroj na**: 2D hydrauliku povodní, kalibraci modelu bez dat, ruční klikání ve státních portálech. V takovém případě připraví podklady a postup, uživatel klikne sám.

## 9. Pracovní pravidla

- Stručně a jasně. Žádné dlouhé pomlčky, jen spojovník "-", i v kódu a HTML.
- U faktických tvrzení a odkazů značky původu: ✅ ověřeno v dané relaci online, 📄 doložený zdroj nečtený, 🤔 odhad, 💻 z paměti neověřeno, ⏳ zdroj starší 12 měsíců.
- Před každým úkolem si říct o podklady, bez kterých by výsledek nebyl kvalitní. Nedomýšlet chybějící vstupy.
- Práce po uzavřených blocích: jeden blok = jeden hotový, použitelný výstup (soubor, skript, vrstva).
- Na konci každé relace: aktualizovat STAV.md (co je hotové, co je rozpracované, jaké jsou další kroky, jaká rozhodnutí padla), doplnit "na co ses nezeptal a měl bys" a seznam zvolených předpokladů.
- Na začátku každé relace: číst STAV.md a navázat.
- Nikdy nemazat soubory ani data bez rozhodnutí uživatele, jen navrhovat.
- Osobní údaje (žáci, vlastníci pozemků, adresy) se nikdy nezapisují do dat aplikace ani do sumářů.

## 10. Fáze

1. **Vymezení a inventura** (hotové = STAV.md s hranicí území a seznam vrstev s ověřenými WMS adresami a licencemi)
2. **Datová příprava** (hotové = skripty + odvozené rastry: povodí, sklon, akumulace odtoku, CN, eroze, deprese, expozice)
3. **Výpočetní jádro** (hotové = JS modul s testy na vzorovém povodí, dokumentované vzorce a zdroje)
4. **Rozhraní občan** (hotové = funkční HTML s mapou, opatřeními a výsledky)
5. **Rozhraní škola/expert + sběr měření** (hotové = vrstvy, zdroje, formulář měření)
6. **Validace a texty** (hotové = porovnání s měřením, katalog opatření s financováním, metodika)
7. **Test s lidmi a zveřejnění** (hotové = opravená verze na webu, krátký návod)

## 11. Mimo rozsah (neřešit, dokud není hotová fáze 7)

Projektová dokumentace konkrétních staveb, výpočet dotačních žádostí, 3D vizualizace, mobilní aplikace, přesné hydraulické modelování intravilánu, data mimo vymezené povodí.
