# STAV projektu Koryčany resilience

Aktualizováno: 15. 11. 2026. Jen to, co je potřeba pro další vývoj. Architektura, data a pravidla: `CLAUDE.md`. Historie relací a odůvodnění starších rozhodnutí: `docs/STAV-HISTORIE.md` (číst cíleně).

## Fáze

| fáze | stav |
|---|---|
| 1 Vymezení a inventura | hotovo |
| 2 Datová příprava | hotovo |
| 3 Výpočetní jádro | `web/jadro.js` v0.3 + `J.pritok`, 40 testů OK. Chybí transformace vlny, bilance P-ET podle scénářů |
| 4 Rozhraní občan | funkční na GitHub Pages, ve zkoušce s lidmi |
| 5 Škola/expert + měření | nezačato |
| 6 Validace | ne -> aplikace nese "nevalidováno" |
| 7 Test a zveřejnění | neformální zkoušky; odkaz pro leták https://skauti-korycany.github.io/korycany-voda/#pozemek |

## Hotovo naposledy (14. 11.)

- Verze a datum v hlavičce/patičce z dat; počty RD sjednocené (1 076); náhled pro sdílení (OG, `docs/img/sdileni.png`), ikona.
- Mobil: mapová data se stahují až v Můj pozemek / Celé území (`nactiMapovaData()`); rastry bezeztrátově 6,6 -> 5,4 MB.
- Můj pozemek: přítok shora (`J.pritok`), klidné upozornění na cestu přívalové vody, průleh Z03 s vodou shora, jezírko/nádrž T07.
- Celé území kap. 3: mapa eroze orné půdy (USLE po buňkách, 3 scénáře).
- `tools/aktualizuj_z_githubu.bat`: stáhne main z GitHubu do složky repo na PC (nic nemaže).

## Hotovo naposledy (15. 11., zpětná vazba od čtenáře)

- Jak bylo: pevný nadpis podle dlouhých řad ("Prší stejně jako před sto lety. Je ale tepleji a krajina potřebuje víc vody."), perex a klíčová čísla z dat (633 mm v průměru, +0,5 °C / 10 let, tropické dny 12 -> 17); 858 mm z úvodu pryč, výpar vysvětlen v kap. 2 a srovnán se srážkami za stejné období (2001-2025: 648 mm).
- Graf srážek: průměry 1921-1950 a 1991-2020 jen nad svým obdobím, legenda (klouzavý průměr 10 let, průměr 30 let, tečka = doplněné dny).
- Kap. 3: "28 tropických dní, z toho 8 nad 35 °C"; kap. 4: četnost dnů >= 40 mm po třetinách řady (v rocnicich nové pole `Pmx`).
- "Jak to číst": odkud jsou data (stanice), průměr, normál (WMO ✅), klouzavý průměr, trend.
- Můj pozemek: svody v poměru 100/75/50/25/0 % do kanalizace (`i.kan`, `kanP()`); bez S02 mají opatření napojená na střechu jen část střechy, která už teče na pozemek. V hash `o=` číslo, staré `kanal`/`pozemek` se převedou.

## Hotovo naposledy (15. 11., měřené prameny a Kyjovka)

- `tools/15_pramen_kyjovka.py` + workflow `hydro.yml` (Actions): řady ČHMÚ do `data/hydro/*.csv` - vydatnost pramenů Koryčany PB0425 (1980-), Čeložnice, Lovčice (1959-), Staré Hutě; Kyjovka nad nádrží 483100 (denní průtok 1967-, stav 1989-) a pod přehradou 484000 (1964-), měsíční maxima, měrné křivky, N-leté průtoky.
- `tools/build_hydro.py` -> `data/hydro_rocni.json` (roční průměry z úplných let, trend, p). Výsledek: pramen Koryčany 0,27 -> 0,10 l/s (1981-1990 proti 2015-2024, p < 0,001), všechny 4 prameny klesají průkazně; Kyjovka nad nádrží 100 -> 59 l/s (1968-1977 proti 2016-2025, p 0,027); pod přehradou bez trendu (řízený odtok).
- Jak bylo: nová kap. 3 "Prameny slábnou a potoku ubývá" (2 grafy), čtvrté klíčové číslo, nadpis "Prší stejně jako před sto lety. Vody v krajině přesto ubývá." (teď doložený měřením). Kapitoly přečíslovány (horko 4, liják 5, letošek 6, výzva 7).
- Inventura dalších zdrojů (`tools/inventura_zdroju.py`, `docs/inventura/`, `docs/VRSTVY.md` kap. 5a).

## Hotovo naposledy (15. 11., zpřesnění výparu)

- `tools/16_vypar_data.py` + workflow `vypar.yml` (Actions) -> `data/vypar/*.csv`: denní T, TMA, TMI, H, F, sluneční svit SSV, globální záření RGLB_D a výparoměr VY pro Nemochovice, Staré Město, Kroměříž, Holešov, Brno-Tuřany, svit Strážnice; ET0 z Open-Meteo (ERA5) 1940-2025.
- `tools/build_vypar.py` -> `data/vypar_rocni.json`: ET0 Penman-Monteith FAO-56 (ea z RHmean, vítr 10 m -> 2 m, Rs ze svitu Angström 0,25 / 0,50, G = 0) proti Hargreaves-Samani.
- Výsledky: Koryčany 2001-2025 PM 702 mm/rok, HS 862 mm (HS o 23 % výš), Open-Meteo 823 mm. Bilance P - ET0: PM -65 mm (v minusu 15 z 24 let), HS -224 mm (24 z 24). Trend PM Koryčany +11 mm / 10 let, p 0,26 (neprůkazný). Dlouhé řady: Kroměříž 1956-2025 +17 mm / 10 let (632 -> 741 mm, p < 0,001), Holešov 1961-2025 +15 mm / 10 let. Složky Kroměříž 1961-2025 za 10 let: T +0,4 °C, H -0,7 %, F -0,08 m/s; svit Holešov +48 h.
- Kontroly: Angström 0,25 / 0,50 proti měřenému záření Holešov a Brno (4 520 dní): průměr sedí (11,77 proti 11,78 MJ/m²/den), RMSE 1,5; regrese a 0,21, b 0,57. PM se svitem proti PM s měřeným zářením: rozdíl 1 %. Výparoměr Kroměříž (76 měsíců): 81 mm/měs., PM 89, HS 109.
- Jak bylo kap. 2: rámeček "Zpřesnění" (text + graf výparu Kroměříž 1956-2025), doplněné "Jak to číst". Grafy kap. 2 a čísla "žízně" zůstávají zatím z HS a jsou označené jako horní odhad.

## Další kroky (pořadí)

0a. Validace s daty Kyjovky nad nádrží (denní průtoky a měsíční maxima jsou v `data/hydro/`): porovnat epizody s SCS-CN pro povodí nad nádrží; pozor, toto povodí leží mimo území modelu (nad hrází).
0b. Převést celou stránku Jak bylo na ET0 Penman-Monteith: `13_normaly_pocasi.py` (historie: H a F už čte, přidat svit Staré Město / Kroměříž / Strážnice / Holešov do `normaly.yml`), `12_pocasi.py` (bot: svit z recent dat Starého Města; záloha bez svitu = FAO-56 rov. 50 nebo HS s opravou), měsíční normály a bilance, texty kap. 2 ("žízeň" -65 mm místo -224 mm, v minusu 15 z 24 let), obrázek "Kam mizí déšť". Pozor na bota: změnu nejdřív vyzkoušet na větvi.
0c. Prameny: zjistit u ČHMÚ, zda se u PB0425 neměnilo jímání nebo způsob měření (přechod týdenní -> denní 2022); dohledat podmínky užití otevřených dat hydrologie. V březnu 2027 znovu `hydro.yml` + `build_hydro.py`.
0. Ze zpětné vazby zbývá: režim Stručně / Podrobně; widgety pro web města (iframe, až po vyjasnění podmínek dat ČHMÚ a PMO); výpar Penman-Monteith vedle Hargreavese a měřená půdní vlhkost (Intersucho / čidlo u školy).
1. Zkouška s lidmi: Můj pozemek (krok 1, upozornění na přívalovou vodu, krok 4), Celé území kap. 3 a mapa eroze (čitelnost nad podkladem ZTM), hráz v0.3.
2. "Co dělat při vedru" (H01, H02): chladná místa, pitná voda, plán města - údaje ověřit online nebo dodá uživatel.
3. Kontakt / zpětná vazba z aplikace (bez osobních údajů, úložiště mimo Pages chybí).
4. Validace: žádost Povodí Moravy (srážkoměr VD, přítok/odtok VD, měrná křivka pod přehradou), porovnání s epizodami u Kachníku (`docs/MERENI.md`).
5. Transformace vlny poldrem; tůň/nádrž u potoka přes `Jadro.nadrz` v Můj pozemek.
6. Rešerše "Život a voda v krajině" (biodiverzita).
7. Mobil dál: ořez rastrů na území modelu, hrubší akumulace (`09_balicek_web.py` na PC + `.bat`); po jeho běhu zase překomprimovat PNG (oxipng bez změny typu barev).
8. Deprese z `deprese.tif` po filtru (hladina VN, zářezy).
9. Krátké úhrny ČSN 75 9010 pro Koryčany (teď Brno); podmínky otevřených dat ČHMÚ do `VRSTVY.md`.
10. Fáze 5: rozhraní škola/expert, formulář měření.
11. Revitalizace toků (T02/T04): opevněné úseky Stříbrníku a Kyjovky, meliorační kanály v lesích nad nádrží.
12. Březen 2027: znovu spustit workflow `normaly.yml` (ročník 2026).

## Čeká na uživatele

- Lokální čísla ClimRisk pro k. ú. Koryčany; místní fotky se souhlasem autorů.
- Podklady: NOO 2026 (XLSX), platné SPPK, vodní zákon § 15b, 17, 46, 47, 55 (e-Sbírka), text ČSN 75 9010.
- Rozhodnutí o `stav.html` (čísla natvrdo, stav k 27. 10.): aktualizovat, generovat, nebo nahradit odkazem na O modelu.

## Platná rozhodnutí

Data a území
- Území: hráz VN Koryčany nahoře, jez před Mouchnicemi dole, 17,7 km². Budovy jen obec Koryčany, parcely i k. ú. Mouchnice.
- Rozlišení 5 m; rastry pro web v mřížce S-JTSK, převod polynomem z `rastr.json`.
- HSP: VÚMOP 2026 (CC BY-NC) > BPEJ (Janeček 2012 tab. 2.2) > nejbližší; B/D = D.
- Toky ČÚZK HY-NET; vypálení toků jen pro směr odtoku hráze, jinak nevypálený terén.
- Katastr bez vlastníků, LV, adres, č.p. a ID. Hydrologie čistě numpy/scipy, bez whitebox/pysheds/QGIS.

Výpočty
- SCS-CN (Janeček 2012, IPS II, Ia = 0,2 S), urbánní TR-55, odtok po buňkách a součet; návrhový déšť Kavka a kol. 2023 s vážením CN2/CN3 podle qAPI.
- Zeleň pozemku SCS-CN bez sklonu; střechy a zpevněné plochy součinitel ČSN s počáteční ztrátou 1 mm.
- Nádrže v0.3: hráz jen na toku ČÚZK; povodí pod 0,25 km² = tůň v údolnici jako rozsah; vodní dílo/TBD jen jako informace.
- Přítok shora: povodí parcel zpětným D8 bez parcel; informace od 500 m², upozornění od 1 ha nebo údolnice, "potok" od 0,25 km² 🤔. Voda shora se do zadržení pozemku nesčítá.
- Jezírko T07 v Můj pozemek: 5 % zahrady (6-40 m²), 0,3 m volného prostoru 🤔, od 100 m² zahrady, potřebuje S02; v katalogu T07 s ručním hlavním číslem.
- Eroze v mapě: A = R průměr orné (65,9) × K × LS × C, P = 1; scénáře C 0,2 / 0,1 / + údolnice ≥ 1 ha a svahy ≥ 7° C 0,01; mělké půdy (Gp 2) nerozlišeny.
- ET₀ Hargreaves-Samani, v textu "možný výpar"; srážky ČHMÚ manuální -> KS Koryčany PMO -> Nemochovice, doplněné mezery označené.
- Počet RD = RÚIAN "rodinný dům" + "bydlení" = 1 076.

Výpar
- Přesnější metoda je Penman-Monteith FAO-56; HS z teplot nadhodnocuje pro Koryčany o ~23 %. Tvrzení "výpar roste" opírat o dlouhé řady Kroměříž a Holešov (průkazné), pro Koryčany je řada 2001-2025 krátká (neprůkazné). Open-Meteo je model, jen pro srovnání.

Rozhraní
- "Vody ubývá" se opírá o měření pramenů a Kyjovky (ČHMÚ), ne o výpočet výparu; příčinu měření neurčuje a text to říká.
- Jak bylo vychází z dlouhých řad a trendů, ne z jednoho roku; letošek je jen doplněk (kap. 5). Nadpis pevný. Tvrdit jen to, co data ukazují: srážky za rok se nemění (trend p 0,59), teplota roste (+0,5 °C / 10 let, p 0,01), výpar a tropické dny jen náznak (p 0,14), velkých lijáků v místní řadě nepřibývá (p 0,69) - častější extrémy srážek uvádět jen jako výhled se zdrojem (CzechGlobe, IPCC).
- Každé číslo "za rok" nese "v průměru" a období. Svody v poměru po 25 %.
- Výchozí déšť: Můj pozemek 10 mm, Celé území 32 mm.
- Můj pozemek = průvodce 5 kroků, krok 4 hra Kapka / Louže / Tůňka / Oáza. Jezírko se nabízí i v zástavbě.
- Upozornění klidným tónem, tykání jako celá aplikace.
- Styl datové žurnalistiky, nadpisy Source Serif 4, vlastní SVG.
- Katalog: KDE + CO ŘEŠÍM, jedno číslo na kartě, bez kódů opatření v textu, dotace větou KDY-KOLIK-NA CO; "Přejít na:" je jen navigace.
- Verze a datum nikdy natvrdo. Stav v URL hash, nic se neukládá. Mapová data až v mapových záložkách.
- "Listnatý les zadrží víc vody" se nepoužívá; přínos smíšeného lesa = odolnost.

Provoz
- `index.html` a `opatreni.json` jen generovat. Licence: kód MIT, data a texty CC BY 4.0.
- PC uživatele: z cloudové relace nedostupné (složka přes Remote Control se 14. 11. nezobrazila). Po pushi uživateli připomenout `tools\aktualizuj_z_githubu.bat`; z relace běžící na PC zapisovat přímo.

## Otevřené otázky

- Kanalizace Koryčany jednotná/oddílná (klíčové pro S02, S06); kam odvádějí vodu velké střechy.
- Zpevněné plochy u domů nejsou v žádné vrstvě; meliorace (žádost SPÚ); zamokřené louky vedené jako TTP?
- Srážkoměr v povodí (škola/oddíl u Kachníku).
- Smí se data VOX a PMO použít veřejně (teď jen agregace)?
- Klimatické scénáře 2050/2090 s licencí nedohledány.
- Sdílený odkaz obsahuje čísla parcel: stačí upozornění u tlačítka?
- Aspoň dva správci repozitáře; upozornění při selhání workflow počasí.

## Platné předpoklady

- Polynom WGS84 <-> S-JTSK platí jen uvnitř rastru.
- Hranice qAPI v tab. 6 Kavka 2023 "do včetně"; tvary deště A-F z N10 platí relativně pro všechna N.
- USLE: C a P z VÚMOP 2017 a Janečka 2012, exponent m Wischmeier 💻, délka svahu z D8 se stropem 300 m.
- Nádrž mezi dešti prázdná 🤔; S06: 4 osoby, nádrž 5 m³, WC 20-30 % spotřeby 🤔.
- Ceny v EUR ponechány v EUR s rokem; `overeno_dne` u zdrojů katalogu = datum buildu.
