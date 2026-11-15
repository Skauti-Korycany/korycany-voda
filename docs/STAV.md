# STAV projektu Koryčany resilience

Aktualizováno: 15. 11. 2026. Jen to, co je potřeba pro pokračování. Pravidla a architektura: `CLAUDE.md`. Data a skripty: `docs/PIPELINE.md`. Podrobnosti, čísla z rozborů a starší rozhodnutí: `docs/STAV-HISTORIE.md` (číst cíleně; na konci je plné znění tohoto souboru před zkrácením).

## Kde jsme

Web běží na GitHub Pages, 5 záložek, zkouší se neformálně s lidmi. Stále nese "nevalidováno". Dnes (15. 11.) po zpětné vazbě čtenáře:

- **Jak bylo** přepsáno podle dlouhých řad a měření: nadpis "Prší stejně jako před sto lety. Vody v krajině přesto ubývá.", 7 kapitol (srážky, letní žízeň a výpar, prameny a Kyjovka, horko, lijáky, letošek, výzva). Kap. 2, 3 a 5 už mají úroveň laik + rozbalovací "Pro zvídavé".
- **Výpar** se v celé aplikaci počítá metodou Penman-Monteith FAO-56 (dřív Hargreaves z teplot, nadhodnocoval o ~23 %). Denní sběr stahuje i sluneční svit.
- **Měření ČHMÚ** nově v repu: prameny u Koryčan a průtok Kyjovky (`data/hydro/`, `hydro_rocni.json`), podklady výparu (`data/vypar/`, `vypar_rocni.json`).
- **Můj pozemek:** svody v poměru 100/75/50/25/0 % do kanalizace.
- **Laik / zvídavý na celém webu** (druhá relace 15. 11.): nahoře krátká věta s jedním číslem, metody, zdroje, značky původu a tabulky pod rozbalovacím "Pro zvídavé". Hotovo v Jak bylo (kap. 1, 4, 5, výhled), Můj pozemek (kroky 2-4, dlaždice), Celé území (kap. 1-4), Katalog a O modelu (kap. 2, 3). Zatím jen na větvi `claude/dazzling-einstein-sf1qa8`, do `main` po svolení uživatele.
- **Provoz:** workflow počasí a normálů se už nepotkají v konfliktu; testy jádra jdou přes `npm test` a běží samy na GitHubu (`testy.yml`).

## Další krok

Před zveřejněním (pořadí určí uživatel):
- Uživatel projde web po úpravě laik / zvídavý a řekne, kde je laická věta stále dlouhá nebo kde naopak něco chybí.
- Uživatel přepíše texty pro laiky vlastními slovy. Připravit mu je pohromadě: vytáhnout laické texty do jednoho souboru (např. `data/texty.json` nebo oddíl v šabloně), ať je může upravovat bez zásahu do kódu. Dnes jsou zčásti v HTML šabloně, zčásti ve větách skládaných v JS (`jb-ch1`, `jb-ch3`, `s-veta`, `er-sum`, `u-veta`, `pz-*`).
- Místní fotografie (uživatel má, se souhlasem autorů): navrhnout místa v rozvržení (úvod Jak bylo, kapitoly, katalog "Kde to funguje"), formát a velikost; fotky dodá uživatel.
- O modelu kap. 1: datum "Stav k 25. 10. 2026" je natvrdo a seznam Hotovo nezmiňuje prameny, Kyjovku ani nový výpočet výparu. Aktualizovat nebo generovat.

## Potom (pořadí)

1. Validace: denní průtoky a měsíční maxima Kyjovky nad nádrží jsou v `data/hydro/` (povodí 19,4 km², leží nad hrází, tedy mimo území modelu); porovnat epizody s SCS-CN. Dál žádost Povodí Moravy a epizody u Kachníku (`docs/MERENI.md`).
2. Widgety pro web města (iframe; nejdřív podmínky užití dat ČHMÚ a PMO, zjistit, zda web města iframe povolí).
3. Prameny: ověřit u ČHMÚ, zda se u PB0425 neměnilo jímání (2022 přechod z týdenního na denní měření); dohledat podmínky užití otevřených dat hydrologie.
4. Zkouška s lidmi: Můj pozemek, Celé území kap. 3 a mapa eroze, hráz.
5. "Co dělat při vedru" (H01, H02), kontakt / zpětná vazba z aplikace, měřená půdní vlhkost (čidlo u školy, Intersucho jen odkazem).
6. Jádro: transformace vlny poldrem, tůň u potoka v Můj pozemek. Mobil: ořez rastrů (PC + `.bat`).
7. Fáze 5 škola/expert + formulář měření. Rešerše biodiverzity. Krátké úhrny ČSN 75 9010 pro Koryčany.
8. **Březen 2027:** znovu `normaly.yml`, `hydro.yml` + `build_hydro.py`, `vypar.yml` + `build_vypar.py` (ročník 2026).

## Čeká na uživatele

- Místní fotky; lokální čísla ClimRisk; podklady NOO 2026, SPPK, vodní zákon, ČSN 75 9010.
- Rozhodnutí o `stav.html` (čísla natvrdo k 27. 10.): aktualizovat, generovat, nebo nahradit odkazem na O modelu.
- Zítra zkontrolovat, že se datum počasí na webu posunulo (první noční běh sběru s novou metodou).

## Platná rozhodnutí

Obsah a tón
- Východisko jsou dlouhé řady a trendy, ne jeden rok; letošek je doplněk. Nestranně, jen čísla z dat. Zpráva: vody ubývá, i vy můžete něco změnit, začněme doma.
- Tvrdit jen to, co data ukazují: srážky za rok se od 1921 nemění; teplota roste (+0,5 °C / 10 let, průkazně); prameny a přítok Kyjovky klesají (průkazně, příčinu měření neurčuje); výpar roste průkazně v Kroměříži a Holešově od 50. let, pro Koryčany je řada krátká; velkých lijáků v místní řadě nepřibývá - častější extrémy srážek jen jako výhled se zdrojem.
- Každé číslo "za rok" nese "v průměru" a období. Tykání, klidný tón. "Listnatý les zadrží víc vody" se nepoužívá.
- Dvě úrovně textu laik / zvídavý (viz `CLAUDE.md` kap. 2). Rozbalovací část se všude jmenuje "Pro zvídavé - ..." (`<details class="jb-cist">`, v Celém území a O modelu navíc `uz-det`). Značky původu (✅ 📄 🤔 ⏳) se v laické větě neukazují, jsou u téhož čísla v části pro zvídavé nebo v "Proč a jak". "Proč a jak" a "Kde to funguje" u opatření zůstávají pod svým názvem (praktické informace, ne metoda).

Výpočty
- SCS-CN (Janeček 2012, Ia = 0,2 S), urbánní TR-55, odtok po buňkách; návrhový déšť Kavka 2023 s vážením CN2/CN3. Zeleň pozemku bez sklonu; střechy a dlažba součinitel ČSN s počáteční ztrátou 1 mm.
- Výpar: Penman-Monteith FAO-56; náhrady při chybějícím měření označené v datech (`zdroj_ET0`).
- Svody: podíl do kanalizace po 25 %, "nevím" = vše do kanalizace; bez odpojení svodů mají sud a záhon jen část střechy, která už teče na pozemek.
- Přítok shora se do zadržení pozemku nesčítá. Nádrže: hráz jen na toku ČÚZK, pod 0,25 km² tůň v údolnici. Eroze: USLE po buňkách, 3 scénáře.
- Území 17,7 km² (hráz VN - jez před Mouchnicemi), budovy jen obec Koryčany, RD 1 076.

Rozhraní a provoz
- Výchozí déšť: Můj pozemek 10 mm, Celé území 32 mm. Můj pozemek = průvodce 5 kroků se hrou Kapka / Louže / Tůňka / Oáza.
- Katalog: KDE + CO ŘEŠÍM, jedno číslo na kartě, bez kódů opatření v textu.
- Verze a datum nikdy natvrdo. Stav v URL hash, nic se neukládá. `index.html` a `opatreni.json` jen generovat.
- Z cloudu jsou datové servery blokované: stahuje se skriptem ve workflow spouštěném pushem do větve `claude/**`, výsledek bot commitne do téže větve.
- Do `main` se pouští po svolení uživatele; po pushi připomenout `tools\aktualizuj_z_githubu.bat`.

## Otevřené otázky

- Kanalizace jednotná / oddílná; kam odvádějí vodu velké střechy; zpevněné plochy u domů; meliorace.
- Smí se data VOX a PMO použít veřejně (teď jen agregace)? Podmínky otevřených dat ČHMÚ (klima i hydrologie) výslovně nedohledány.
- Sdílený odkaz obsahuje čísla parcel: stačí upozornění u tlačítka?
- Aspoň dva správci repozitáře; upozornění při selhání workflow počasí.

## Předpoklady

- Polynom WGS84 <-> S-JTSK platí jen uvnitř rastru. USLE: exponent m 💻, délka svahu se stropem 300 m. Nádrž mezi dešti prázdná 🤔.
- Vítr měřený v 10 m se přepočítává na 2 m; sluneční svit z nejbližší stanice, která ten den měřila. Roční průměry jen z úplných let.
