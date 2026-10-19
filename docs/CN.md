# Čísla odtokových křivek (CN) - tabulka pro model

Zdroj pravdy: `tools/build_cn.py` -> `data/cn_tabulka.json` (v0.1, 19. 10. 2026). Tento soubor je jen popis.

## K čemu
SCS-CN je metoda odhadu objemu přímého odtoku z návrhového deště. Každá buňka 5 m dostane CN podle dvojice
(třída využití půdy z `data/dmr/vyuziti_kod.tif`) × (hydrologická skupina půd A-D). Z CN se spočítá
S = 25400/CN - 254 (mm), Ia = 0,2 S a odtok Q = (P - Ia)² / (P - Ia + S) pro P > Ia. Hodnoty platí pro
střední nasycení půdy (IPS II); suchá/nasycená půda bude v rozhraní posuvník (fáze 3).

## Zdroje
- ✅ Janeček a kol. (2012): Ochrana zemědělské půdy před erozí, metodika ČZU. Tab. 2.1 (definice HSP), 2.2 (HPJ -> HSP),
  2.3 (CN pro IPS II). Rok 2012, ale jde o fyzikální metodu, stáří zdroje nevadí (instrukce projektu, kap. 7).
- ✅ USDA NRCS TR-55 (1986), tab. 2-2a a 2-2c - pro třídy, které česká metodika nemá (trávníky, parkoviště, areály).

## Co obsahuje
25 tříd (shodné kódy s `vyuziti_pudy.json`), 51 variant stavu, 10 z nich označeno `odhad: true` = volba nejbližší
kategorie bez přímého řádku ve zdroji (zahrady, ostatní plochy v sídle, areály bez budov, skládka, kolejiště, voda,
bažina). Každá třída má `vychozi` variantu (bez další znalosti) a varianty lepšího/horšího stavu, ze kterých jádro
odvodí účinek opatření (zbytky na povrchu, vrstevnicové řádky, pásové střídání, stav lesa a pastvin).

## Zvolené předpoklady
- Orná půda výchozí = obilniny, přímé řádky, špatný stav (65/76/84/88): konzervativní; skutečné plodiny z LPIS později.
- TTP výchozí = pokryv > 75 % (39/61/74/80).
- Les = střední stav (36/60/73/79) bez ohledu na druh dřevin (J12 druh nerozlišuje).
- Budovy, kůlny, silnice, ulice, parkoviště = 98 (nepropustné). Opatření na střechách se nemodelují změnou CN,
  ale odečtem objemu v jádře.
- Vodní plocha a bažina = 100 (konvence; J12 používá místo toho koeficient f).

## Orientační výsledek
Při jednotné HSP B by vážené CN území modelu (1 413 ha) bylo 65, při HSP C 77. Skutečné HSP: čeká se na VÚMOP;
záloha = J12 tab. 2.2 z HPJ (BPEJ zdarma ze SPÚ).

## Co chybí
- HSP rastr (VÚMOP nebo BPEJ -> HPJ -> J12 tab. 2.2).
- Lesy mimo zemědělský půdní fond nemají BPEJ: HSP pro les odvodit z geologie/ČGS nebo půdní mapy (otázka na VÚMOP v žádosti).
- Přepočet IPS I/III (J12 obr. 2.2) - doplnit do konstant jádra.
