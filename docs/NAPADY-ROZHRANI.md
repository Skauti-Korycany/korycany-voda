# Nápady k rozhraní - zásobník (neřešit teď)

## 18. 10. 2026 - Filtrování opatření posuvníky na poměrných škálách (uživatel)
- Motivace: databáze opatření bude časem rozsáhlá a při výběru v interaktivním nástroji by zahltila. Uživatel si místo procházení seznamu nastaví, co ho pálí, a dostane relevantní sadu.
- Navržené škály: vlhkost (sucho - povodeň), teplota (mráz - vedro), oživení (mrtvé - bohatě pestré), nákladnost (levné - velmi drahé), případně další.
- Implementace: každé opatření dostane v tabulce váhu pro každou škálu; filtr pak řadí nebo skrývá podle shody s nastavením uživatele.

### Poznámky k pozdějšímu rozhodnutí
- Sucho a povodeň nejsou pro opatření protiklady: tůň, průleh, mez pomáhají oběma koncům (zadrží příval, drží vodu do sucha). Bipolární posuvník by je vytlačil do neutrálního středu. Návrh: váha 0-3 zvlášť pro každý extrém (sucho, příval/povodeň, vedro, mráz/vítr) a uživatel posuvníky říká, jak moc ho který extrém trápí; skóre = součet vah × priorit.
- Nákladnost a biodiverzita (účinek B) už jsou atributy v KATALOG.md; stačí doplnit váhy 0-3, až bude seznam stabilní. V opatreni.json je rezervováno pole `vahy_skaly`.
- Vazba na režim "Můj pozemek": posuvníky filtrují mezi opatřeními, která už prošla filtrem vhodnosti podle dat (sklon, půda, místo). Pořadí: místo -> data -> preference uživatele.
- Zobrazení: 3-5 posuvníků, výsledkem seřazený seznam s krátkým "proč je tu" (např. "sucho +++, příval ++, do 10 tis. Kč").
