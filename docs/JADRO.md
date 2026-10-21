# Jádro (fáze 3) - `web/jadro.js` v0.2

Stav: 21. 10. 2026 (v0.2: vážený odtok přes tvary deště a stav nasycení). Výpočetní jádro nad skutečnými rastry (5 m, S-JTSK), bez knihoven, běží v prohlížeči i v node. Testy `web/test_jadro.js` (node, 30 testů, vše OK proti `cn_info.json` a `povodi.geojson`). Zkušební prohlížeč `web/test.html` (Leaflet + ZTM ČÚZK).

## Datový balíček `data/web/` (`tools/09_balicek_web.py`, spouštěč `vyrob_balicek_web.bat`)

| pásmo | PNG | kódování | zdroj |
|---|---|---|---|
| vyska | 16 bit (R hi, G lo) | m = 200 + v/10 | DMR 5G |
| sklon | 8 bit | ° = v/4, 255 = nic | 02 (Horn) |
| akumulace | 8 bit | buněk = 10^((v-1)/40), přesnost ~6 % | 02 (D8) |
| smer | 8 bit | kód D8 (1 V, 2 JV, 4 J, 8 JZ, 16 Z, 32 SZ, 64 S, 128 SV) | 02 |
| cn, vyuziti, hsp, hsp_zdroj, povodi | 8 bit | hodnota přímo, 0 = nic | 04-06 |

Celkem 5,0 MB (akumulace 1,6, výška 1,5, sklon 1,1 MB). `rastr.json`: mřížka (x0 = -562500, y1 = -1170000, krok 5, 1500 × 1600), kódování, zdroje, licence.

**Souřadnice**: aplikace neřeší projekci. `rastr.json` nese polynom 2. řádu WGS84 <-> S-JTSK spočtený pyprojem na mřížce 41 × 41 bodů; chyba na celém rastru < 2 mm (kontrolní body v JSON, test). Proč ne warp do Web Mercatoru: směr odtoku D8 a sousednost buněk platí jen v původní mřížce. Zobrazení do mapy dělá `Jadro.obrazek()` převzorkováním (pixel Mercatoru -> lon/lat -> polynom -> buňka), 1024 px za ~30 ms.

Poznámka: CN a využití pokrývají jen bbox stahovaný v 04 (81,6 % rastru, celé území modelu); zbytek má v `cn` a `vyuziti` 0.

## Funkce

| funkce | co dělá | zdroj metody |
|---|---|---|
| `nacti(base)` / `nactiZPoli(info, pasma)` | PNG -> typovaná pole (canvas) | - |
| `lonLatNaXY`, `xyNaLonLat`, `lonLatNaBunku` | převody | polynom z 09 |
| `scsCN(P, CN, ia=0,2)` | Q = (P-Ia)²/(P-Ia+S), S = 25400/CN - 254 | Janeček a kol. 2012 kap. 2 ✅⏳; USDA TR-55 ✅⏳ |
| `cnProIPS(CN, 1\|2\|3)` | CN1 = 4,2 CN/(10-0,058 CN), CN3 = 23 CN/(10+0,13 CN) | standardní vztahy SCS (NEH-4 / Hawkins) 💻; **ověřeno 21. 10.** proti příkladu Stašov v Kavka a kol. 2023 ✅ (CN2 81 -> CN3 90,7, tab. 7) |
| `vahyCN(qAPI)` | váha CN2/CN3 podle qAPI: <= 0,2 -> 1/0; <= 0,4 -> 0,75/0,25; <= 0,6 -> 0,5/0,5; <= 0,8 -> 0,25/0,75; > 0,8 -> 0/1 (hranice bereme „do včetně“ - metodika to neříká) | Kavka a kol. 2023 ✅ kap. 2.5, tab. 6 |
| `vahaCN3(podil_pct, qAPI)` | Σ p_i · w3_i přes tvary A-F; Koryčany N2 / N10 / N100 = 0,25 / 0,20 / 0,21 | tamtéž, kap. 2.6 (příklad Stašov: 1 333,8 m³ reprodukováno na 0,6 m³) |
| `odtokVazeny(st.odtok, podil, qAPI)` | V = (1-w3) · V_CN2 + w3 · V_CN3; vrací Q_mm, objem, rozsah [V_CN2, V_CN3], váhu | tamtéž; objem SCS-CN na průběhu deště nezávisí, tvary vstupují jen přes qAPI |
| `bunkyPolygonu(ring, díry)` | scanline rasterizace (střed buňky uvnitř, even-odd) | - |
| `statBunek(bunky, P, ips)` | plocha, vážené CN, sklon, výšky, využití (ha), HSP (ha) + podíl odhadu, max akumulace, „tok prochází“ (>= 0,25 km²), odtok **po buňkách** (Σ Q_i, ne Q z průměrného CN); od v0.2 i `Q_mm_cn3` / `objem_m3_cn3` (nasycený stav) | SCS-CN |
| `statPolygon(ring, P, ips)` | totéž pro polygon v lon/lat | |
| `prichytKToku(i, r)` | buňka s max akumulací v okruhu r m | jako 02 |
| `povodiBunky(i0)` / `povodiBodu(lon, lat, r, P, ips)` | zpětné sledování D8 (BFS), maska + statistika; příznak `orez_okrajem` | - |
| `nadrz(lon, lat, h, r)` | hráz přichycená k toku, hladina = dno + h; zatopí buňky souvislé (4-okolí) s hrází, pod hladinou a uvnitř povodí hráze; objem = Σ (hladina - z) × 25 m²; plocha, hloubky, zatopené využití, povodí k hrázi | zjednodušení; bez objemu hráze, bez ztrát, bez tvaru koruny |
| `obrazek(barva(i), bbox, šířka)` / `obalMasky(maska)` | ImageData pro `L.imageOverlay` | - |

Výkon (node, celý rastr 2,4 M buněk): povodí Stříbrníku 4,2 km² 65 ms, povodí celého rastru 31,7 km² 420 ms, obrázek 512 × 705 px 32 ms.

## Ověření proti Pythonu (06_cn.py)
Území modelu: plocha 1 412,7 ha (Python 1 412,1 - rozdíl = rasterizace polygonu), CN 72,0 = 72,0, odtok P40 78 248 m³ = 78 248 m³, les 49,9 %, HSP odhad 48,2 % (48,3). Povodí Stříbrník z hlásného profilu: 4,23 km² = 4,23, CN 65,2 = 65,2.

## Co jádro zatím neumí (další kroky fáze 3)
- Transformace vlny poldrem (zatím jen bilance objem nádrže vs. objem odtoku).
- Roční bilance P - ET (chybí ET a scénáře), USLE (chybí R faktor), indexy horko/vítr.
- Objekty opatření z `opatreni.json` nad reálným pozemkem (dnes jen v prototypu nad syntetickým pozemkem) - napojit `EFF` z prototypu na `statPolygon`.
- ~~Vážení přes tvary a qAPI~~ hotovo 21. 10. (v0.2). Území modelu N10 53 mm: CN2 152 tis. m³, CN3 332 tis., vážené **189 tis. m³** (Q 13,4 mm, koef. 0,25). V prototypu zapojeno v panelu „Pole, louky a les“; u dešťů mimo N2/N10/N100 (20 mm, 26 mm, 94 mm) se počítá jen CN2.
- Deprese (`deprese.tif`) nejsou v balíčku - nejdřív filtr (hladina VN, zářezy).
- Přichycení k toku: hlásný profil Stříbrník leží > 60 m od rastrového koryta; v UI použito 100 m. Pro malé toky (zahrady) je nutné okruh zmenšit nebo nabídnout „bez přichycení“.
