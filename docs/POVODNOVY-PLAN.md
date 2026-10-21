# Výtah z digitálního povodňového plánu města Koryčany (pro přívaly a měření)

Zdroj ✅ (21. 10. 2026): https://www.portalobce.cz/povodnovy-plan/korycany/ (aktualizace 24. 9. 2025) a evidenční list ČHMÚ profilu kat. A (hydro.chmi.cz seq 307008). Jen fakta, která se hodí pro model a měření; organizační část vynechána.

## Hlásné profily a SPA

| profil | kat. | kde | SPA 1 / 2 / 3 | data |
|---|---|---|---|---|
| Koryčany pod přehradou, Kyjovka | A (Povodí Moravy) | pravý břeh 150 m pod hrází, 49.1168 N, 17.1890 E, ř. km 77,76, povodí **27,54 km²**, nula vodočtu 285,08 m n. m. | 80 / 100 / 120 cm = **4,77 / 8,15 / 12,34 m³/s** | hydro.chmi.cz, sap.pmo.cz (H, Q po 10 min; 21. 10. 2026: 15 cm = 0,024 m³/s) |
| Koryčany, Kyjovka | C (město) | lať na mostě silnice 43233 směr Blišice, 49.1135 N, 17.1636 E | 80 / 190 / 240 cm | jen lať, bez přenosu; hlásí JSDH |
| Koryčany, Stříbrník | C (město) | ultrazvukové čidlo + lať na mostní konstrukci, parcela 461/4 u č. p. 223, 49.1070 N, 17.1592 E | 100 / 120 / 140 cm; běžný stav 60 cm | hladiny-vox.pwsplus.eu/Senzors/Details/5157 (náš Kachník) |

N-leté průtoky profilu A (evidenční list ČHMÚ): Q1 2,4 / Q5 7,8 / Q10 11,7 / Q50 25,1 / **Q100 33,2 m³/s**, Qa 0,0718 m³/s (web dPP uvádí 0,00708 - překlep). Platí pro povodí nad hrází (27,5 km²), tj. mimo území modelu, ale dává měřítko: Q100 ≈ 1,2 m³/s na km². Pro Stříbrník a Kyjovku v profilech C N-leté průtoky neuvedeny.

Doplňková pravidla SPA v dPP: I. SPA i při dešti trvajícím přes 4 h, II. přes 8 h, III. přes 16 h (nebo kombinace s táním).

## Srážkoměry v dPP

| stanice | poloha | provozovatel | data |
|---|---|---|---|
| **VD Koryčany** | areál pod nádrží, 49.1175 N, 17.1902 E | Povodí Moravy | sap.pmo.cz (sekce Srážky; 21. 10. z Claude neotevřeno) |
| **Nemotice** | zahrada OÚ č. p. 66, 49.1294 N, 17.1252 E (cca 4 km Z od Koryčan) | automatická stanice s SMS varováním (provozovatel neuveden) | hladiny.cz |
| Nemochovice | u č. p. 2 | ČHMÚ | opendata ČHMÚ (máme) |
| Staré Hutě | plot u č. p. 19, 427 m n. m. | ČHMÚ Brno | opendata ČHMÚ (máme) |
| Ždánice | ul. Polní, 238 m n. m. | ČHMÚ Brno | - |

-> Pro přívaly v povodí jsou VD Koryčany (1 km od hráze, v území) a Nemotice (4 km) lepší než Nemochovice/Staré Hutě (8-9 km). Oba zdroje zatím neotevřeny; zapsáno do úkolů.

## Odtokové poměry a přívaly
- Místo ohrožené bleskovou povodní (POVIS): **„Povodí potoka Stříbrník“** - bez souřadnic a plochy. Potvrzuje volbu Stříbrníku jako hlavního dílčího povodí modelu.
- Místo omezující odtok: **mostek na silnici 43231** (tok a ř. km neuvedeny).
- Kritické body přívalových povodní (metoda VÚV TGM, DMT 10 m): ID 41 202 859 (přispívající plocha 111 ha, sklon 23,1 %, orná 0 %) a ID 41 202 864 (326 ha, sklon 22,2 %, orná 0 %) - souřadnice v dPP nejsou; oba mají 0 % orné půdy, tedy lesní povodí (Chřiby). Dohledat polohu v dPP ČR (dppcr.cz) nebo v POVIS.
- Dráhy soustředěného odtoku: linie s přispívající plochou > 5 ha, jen mapa.
- Záplavové území Kyjovky ř. km 70,200-84,680 (KÚ Zlínského kraje, 30. 7. 2004, č. j. KUZL 7819/2004 ŽPZE-DZ), PDF editor.dppcr.cz/pk_zuz/doc/zapluz/cz072_15.pdf.
- Rybníky Kachník (intravilán) a Prokop (J okraj) podle dPP „bez významného vlivu na odtokové poměry“.
- Historie: 2010 Kyjovka na přítoku do VN kulminovala na 10-20letém průtoku, sesuv silnice II/432 Koryčany-Jestřabice (80 m); konkrétní přívalové epizody v dPP nejsou.
- Ohrožené objekty: cca 5 budov v záplavovém území Kyjovky (4 průmyslové, 1 autokemp), bez trvale bydlících.

## Území (dPP, ČSÚ 2024)
Katastr 4 112,7 ha: les 52 %, orná 28 %, TTP 8 %, zahrady 3 %, voda 1,7 %, zastavěno 1,4 %. Obyvatel 2 732 (1. 1. 2025). Klima MT7, sever T2; normál 1981-2010 601-650 mm (klimatickazmena.cz) - náš normál 1991-2020 ze stanice Koryčany 632 mm sedí.

## Správci toků
Povodí Moravy: Kyjovka (IDVT 10100029), Lískovecký potok. Lesy ČR: **Stříbrník (10201157)**, Kratinka, Jestřabický potok a přítoky. VD Koryčany: II. kategorie, manipulační řád schválen KÚ ZK 3/2009; parametry nádrže (objemy, kóty) v dPP nejsou - jen Povodí Moravy.

## Co z toho plyne
1. Žádost na Povodí Moravy rozšířit o: srážkoměr VD Koryčany (10min/1h řada 2026+), přítok/odtok VD a měrnou křivku profilu pod přehradou (H -> Q existuje, viz sap.pmo.cz).
2. Pro Stříbrník zatím nikdo N-leté průtoky nestanovil - model je může odhadnout jen orientačně (SCS-CN + jednotkový hydrogram), s viditelným „neověřeno“.
3. Kritické body VÚV v lese nad městem jsou kandidáti na „kde zadržet“ - po dohledání polohy porovnat s našimi údolnicemi z DMR.
