# Seznam vrstev a datových zdrojů - stav k 15. 10. 2026

Legenda: ✅ otevřeno online v relaci 15. 10. 2026 (GetCapabilities vrátil XML nebo stránka přečtena) | 📄 adresa/údaj z oficiální metadatové stránky, GetCapabilities se nepodařilo otevřít | ❌ fetch selhal (uvedena zkoušená URL) | 🤔 odhad.

Pozn. k ❌: většina selhání je blokace na straně nástroje Claude (proxy), ne nutně nefunkční server. Před škrtnutím vrstvy ověřit v běžném prohlížeči: `URL?service=WMS&request=GetCapabilities`.

Licenční shrnutí:
- Výslovně CC BY 4.0 (✅ přečteno): ČÚZK otevřená data a Atom (DMR 5G, ortofoto, ZTM, ZABAGED), VÚV Q100 INSPIRE zip, CENIA CORINE a Natura 2000, AOPK chráněná území, ČGS datasety ke stažení.
- "Zdarma", licence nejmenována: VÚMOP, NLI/ÚHÚL, MZe/LPIS, ČHMÚ, VÚV WMS. Použití: WMS v aplikaci ano, redistribuce dat ne bez souhlasu.
- Vyňato z CC BY: ČÚZK letecké měřické snímky a archiválie (ortofoto 50. let, císařské otisky).

## 1. ČÚZK

Licence (společná): ✅ "Zásady užívání dat a služeb ZÚ" https://geoportal.cuzk.gov.cz/Dokumenty/Podminky.pdf (č.j. ZÚ-01256/2026-13310, 23. 3. 2026). ✅ https://www.cuzk.gov.cz/Uvod/Produkty-a-sluzby/Otevrena-data/Otevrena-data-zakladni-informace.aspx - otevřená data CC BY 4.0, výjimka letecké měřické snímky a archiválie. ✅ https://atom.cuzk.gov.cz/ - CC BY 4.0. ✅ Podmínky síťových služeb: https://cuzk.gov.cz/Predpisy/Podminky-poskytovani-sitovych-sluzeb-CUZK/Podminky-poskytovani-sitovych-sluzeb-CUZK.aspx - WMS zdarma, povinné uvedení "ČÚZK - on-line". Seznam služeb ✅: https://geoportal.cuzk.gov.cz/Default.aspx?mode=TextMeta&side=wms.uvod&text=WMS.uvod&head_tab=sekce-03-gp&menu=31

| Vrstva | WMS/WMTS URL | GetCapabilities | Vrstvy | Pozn. |
|---|---|---|---|---|
| DMR 5G stínovaný reliéf | https://ags.cuzk.gov.cz/arcgis2/services/dmr5g/ImageServer/WMSServer | ✅ WMS 1.3.0 | `dmr5g`, `dmr5g:GrayscaleHillshade`, `dmr5g:GrayscaleHillshadeZ10`, `dmr5g:GrayscaleHillshadeZ20`, `dmr5g:TintedHillshadeContinuous`, `dmr5g:SlopeRGBMap`, `dmr5g:SlopeRGBMap2`, `dmr5g:AspectRGBMap` | CRS 3857, 4326, 5514 |
| Ortofoto ČR | https://ags.cuzk.gov.cz/arcgis1/services/ORTOFOTO/MapServer/WMSServer | ✅ WMS 1.3.0 | `0` | CRS 3857, 4326, 5514 |
| ZTM25 | https://ags.cuzk.gov.cz/arcgis1/services/ZTM/ZTM25/MapServer/WMSServer | ✅ | `0` | ZTM5/10/50 obdobně, neotvíráno |
| ZTM WMTS (Web Mercator) | https://ags.cuzk.gov.cz/arcgis1/rest/services/ZTM_WM/MapServer/WMTS | ✅ WMTS 1.0.0 | layer `ZTM_WM`, TileMatrixSet `GoogleMapsCompatible`; šablona `.../WMTS/tile/1.0.0/ZTM_WM/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}` | ideální podklad pro Leaflet; v prototypu použito se Style=default |
| ZABAGED polohopis | https://ags.cuzk.gov.cz/arcgis/services/ZABAGED_POLOHOPIS/MapServer/WmsServer | ✅ | `0`-`13` (lesní půda, TTP, orná, vinice, sad, `12` vodní plocha, `13` bažina...) | číselné názvy vrstev |
| Archivní ortofoto | https://geoportal.cuzk.gov.cz/WMS_ORTOFOTO_ARCHIV/WMService.aspx | ❌ robots | 📄 jedna vrstva = jeden rok, čb 1998-2001, barevné od 2002 | snímky 50. let v této WMS NEJSOU, jen aplikace https://ags.cuzk.gov.cz/archiv/ (archiválie, mimo CC BY) |
| Katastrální mapa | https://services.cuzk.gov.cz/wms/local-km-wms.asp | ❌ robots | - | 📄 URL z metadat |
| Císařské otisky stabilního katastru | WMS nedohledal jsem | - | - | 📄 jen aplikace Archiv a placené skeny (ÚAZK, 25 Kč/list) |

Stažení DMR 5G: ✅ https://geoportal.cuzk.gov.cz/Default.aspx?mode=TextMeta&side=vyskopis&metadataID=CZ-CUZK-DMR5G-V&head_tab=sekce-02-gp&menu=302 - formát LAZ (mračno bodů), EPSG:5514, jednotka list SM5, bez poplatků, CC BY 4.0, distribuce Atom nebo e-shop (export vlastního území). Atom feed 📄 https://atom.cuzk.gov.cz/DMR5G-SJTSK/DMR5G-SJTSK.xml (metadata ✅ https://geoportal.gov.cz/php/micka/record/basic/CZ-CUZK-ATOM-DMR5G-SJTSK?dlang=eng, "free of charge", registrace nezmíněna; feed sám ❌). 🤔 DMR 5G není rastr - do gridu se interpoluje (PDAL/whitebox), patří do skriptů fáze 2.

## 2. VÚMOP (SOWAC GIS)

Licence: nedohledal jsem (https://www.vumop.cz/poskytovani-dat ❌, https://geoportal.vumop.cz/ ❌). Kontakt z metadat: data@vumop.cz. Nutný dotaz.

| Vrstva | WMS URL | GetCapabilities | Licence | Pozn. |
|---|---|---|---|---|
| Vodní/větrná eroze | https://wms.vumop.cz/public/eroze.php | ❌ | metadata ✅ https://metadata.vumop.cz/en/record/full/5242cc65-3d9c-4ba3-808c-28487f000001 : "otherRestrictions" | 📄 |
| Erozní události (monitoring) | https://wms.vumop.cz/public/udalosti.php | ❌ | ✅ https://me.vumop.cz/ "poskytována bezplatně" | 📄 |
| BPEJ | WMS VÚMOP nedohledal jsem | - | metadata ✅ https://metadata.vumop.cz/en/record/full/d2da8900-8900-12da-9a36-4745e3f89a4a odkazují na SPÚ https://geoportal.spucr.cz/web/cz/bpej-open-data (❌), kód CC BY-SA 4.0 | alternativa: vrstva `BPEJ_WMS` ve WMS MZe plpis.fcgi (bod 8) |
| Hydrologické skupiny půd | WMS nedohledal jsem | - | **Data poskytnuta 27. 10. 2026 na žádost (e-mail VÚMOP): vektor HSP 2026, GPKG, EPSG:5514, obec + 500 m, licence CC BY-NC - nekomerční použití, úpravy i prezentace povoleny, uvádět autora „VÚMOP, v.v.i.“**; metadata ✅ https://metadata.vumop.cz/record/xml/5cc1bdc2-de34-4eee-a439-41420a000319 | Soubor `data/vumop/HSP_Korycany.gpkg` jen na PC (ne v gitu); 1 352 polygonů A/B/C/D, 2× B/D (= D), 8× bez hodnoty. VÚMOP: letos celorepubliková aktualizace mimo ZPF, lesy podrobněji rozdělené do HSP. |
| R faktor, C faktor (stažení) | https://owncloud.cesnet.cz/index.php/s/I3hc8FqLsG7wASP (R faktor) | metadata ✅ https://metadata.vumop.cz/record/basic/65379397-1a6c-4f19-b153-50fe0a000319 | "žádné podmínky neplatí" | pro USLE |
| Infiltrace, retenční vodní kapacita | nedohledal jsem | - | - | - |

## 3. ČGS

Seznam služeb ✅ https://cgs.gov.cz/en/maps-and-data/web-services. Podmínky ✅ https://cgs.gov.cz/en/copyright: datasety ke stažení CC BY 4.0 s citací "(CC BY 4.0) Czech Geological Survey"; u mapových služeb v cizí aplikaci povinná citace.

| Vrstva | WMS URL | GetCapabilities | Vrstvy | Pozn. |
|---|---|---|---|---|
| Hydrogeologická mapa 1:50 000 | https://mapy.geology.cz/arcgis/services/HydroGeologie/HG50_mapa/MapServer/WMSServer | ✅ WMS 1.3.0 | `0` HG jednotky/transmisivita, `1` HG prostředí, `2` kolektory a izolátory, `3` tektonické linie | CRS jen 4326, 5514, 102067 - 3857 chybí, Leaflet musí volat 4326 |
| GeoČR50 geologická mapa | https://mapy.geology.cz/arcgis/services/Geologie/geologicka_mapa50/MapServer/WMSServer | server odpověděl, obsah nečitelný nástrojem | - | metadata ✅ micka 60b0cd00: "no conditions apply" |
| Hydrogeologické rajony | https://mapy.geology.cz/arcgis/services/HydroGeologie/HG_rajony/MapServer/WMSServer | ❌ | - | 📄 |
| IG rajony 1:50 000 | https://mapy.geology.cz/arcgis/services/Geohazardy/IG_rajony50/MapServer/WMSServer | ❌ | - | metadata ✅ 5b31eacc: "no conditions apply" |
| Svahové deformace | https://mapy.geology.cz/arcgis/services/Geohazardy/svahove_deformace/MapServer/WMSServer | ❌ | - | metadata ✅ 680fa331: "žádné podmínky neplatí" |

## 4. VÚV TGM (DIBAVOD / HEIS)

| Vrstva | URL | Otevřeno | Licence | Pozn. |
|---|---|---|---|---|
| WMS ISVS (toky, povodí, nádrže, záplavová území) | http://heis.vuv.cz/data/webmap/wms.dll?SERVICE=WMS&MU=CZ&LANG=CS-CZ&REQUEST=GetCapabilities | ❌ robots | ✅ metadata CZ-VUV-MD-HEISWMS: bezplatně, povinné uvedení VÚV TGM | 📄 datasety Toky, HydrologPovodi, Nadrze, ZaplavUzemi |
| DIBAVOD shapefile ke stažení | ✅ https://www.dibavod.cz/index.php?id=27 | ano | licence na stránce neuvedena; záplavová území "pouze orientační" | zdarma bez registrace; A01-A16 toky/povodí, B nádrže, D záplavová území |
| Q100 INSPIRE (Atom) | ✅ https://heis.vuv.cz/xmicka/record/atom/CZ-VUV-MD-ATOM-Inspire-FD_FA | ano | CC BY 4.0 (v záznamu) | zip https://www.dibavod.cz/data/download/atom/inspire_priority_ds/fd_fa.zip |

## 5. ČHMÚ a Intersucho

| Zdroj | URL | Otevřeno | Obsah | Licence |
|---|---|---|---|---|
| ČHMÚ otevřená data | https://opendata.chmi.cz/ (❌); popis ✅ https://opendata.chmi.cz/meteorology/climate/Klimatologicka_data_popis.pdf | PDF ano | staniční data (10min až rok, JSON/CSV, od 6/2024); gridy srážek nezmíněny; seznam stanic v `metadata/meta1.csv` | ✅ https://www.chmi.cz/files/portal/docs/hydro/denni_data/Podminky_uziti.pdf (22. 4. 2020): volně, bez registrace, povinné uvedení ČHMÚ; CC BY 4.0 podle dokumentace wetterdienst ✅ |
| ČHMÚ WMS srážek | nedohledal jsem | - | jen WFS stanic přes CENIA https://gis.cenia.cz/geoserver/chmu_meteo_stanice/wfs 📄 | - |
| Hlásné profily (hpps) | ✅ https://hydro.chmi.cz/hpps/pov/objekt/307008 (Koryčany pod přehradou, Kyjovka, kat. A, Povodí Moravy) | ano | stav a průtok | - |
| Intersucho | https://www.intersucho.cz/ ❌ | - | - | nedohledal jsem |

## 6. ClimRisk

Web ❌. Z druhé ruky: ✅ tisková zpráva AV ČR 2022 (CzechGlobe, 500 m grid, periody 2011-2040 až 2061-2090); ✅ abstrakt EMS2026-518 (ClimRisk.eu, 4 SSP, CMIP6, 0,5 km, "users can download data for any specific location"). WMS nedohledal jsem, licence dat nedohledal jsem. Nutno ověřit ručně v prohlížeči a případně napsat CzechGlobe.

## 7. NLI (dříve ÚHÚL)

Seznam ✅ https://nli.gov.cz/portfolio/webove-mapove-sluzby/ (stará adresa geoportal2.uhul.cz nefunkční ✅ https://nli.gov.cz/nefunkcni-wms-sluzba/).

| Vrstva | URL | GetCapabilities | Vrstvy | Licence |
|---|---|---|---|---|
| OPRL WMS | https://gp.nli.gov.cz/wms/oprl | ✅ WMS 1.3.0 | `Lesnicka_typologie`, `Lesni_vegetacni_stupne`, `Cilove_hospodarske_soubory`, `Ochrana_pudy`, `Ochrana_vody`, `Ochrana_prirody`, `Ochrana_lesa`, `Zpristupneni_lesu`, `Potencialni_ohrozeni_smrkovych_porostu_klimatickou_zmenou`, `Provozni_soubory`, `Reprodukcni_zdroje`, `Socialni_funkce`, `Obory_a_bazantnice`, `Prehledova_mapa` | nejmenována (AccessConstraints prázdné) |
| OPRL WMTS | https://gpc.nli.gov.cz/wmts/oprl | neotvíráno | - | - |

CRS OPRL WMS: 5514, 32633, 3857, 4326.

## 8. LPIS / MZe

Příručka ✅ https://mze.gov.cz/public/portal/mze/-q333487---eHsqm8vv/prirucka-k-pouziti-wms-wfs-a-wcs-platna (v2.1, 1. 6. 2026): data zdarma pro celou ČR; licence a redistribuce neuvedeny.

| Vrstva | URL | GetCapabilities | Vrstvy |
|---|---|---|---|
| Evidence půdy (DPB) | https://mze.gov.cz/public/app/wms/public_DPB_PB_OPV.fcgi | ❌ | 📄 `LPIS_FB4`, `LPIS_FB_KUL`, `LPIS_FB4_KOD` |
| Eroze (MZe) | https://mze.gov.cz/public/app/wms/public_eroze.fcgi | ❌ | - |
| Starý plpis | http://eagri.cz/public/app/wms/plpis.fcgi | ❌ | 📄 vč. `BPEJ_WMS`, `LPIS_FB4`, `VRSTEVNICE_2M_V2` (po 2018 bez nových vrstev) |
| WFS LPIS | https://mze.gov.cz/public/app/wms/plpis_wfs.fcgi | neotvíráno | - |

## 9. Historická vojenská mapování (CENIA)

| Vrstva | WMS URL | GetCapabilities | Licence |
|---|---|---|---|
| II. vojenské mapování | https://gis.cenia.cz/mapcache/II_vojenske_mapovani/wms ; alt. https://geoportal.gov.cz/ArcGIS/services/CENIA/cenia_rt_II_vojenske_mapovani/MapServer/WMSServer | ❌ obě | ✅ metadata https://micka.cenia.cz/en/record/full/4e678953-ba1c-49a2-a61e-3b96c0a80137?dlang=cze : bez omezení, žádné podmínky |
| III. vojenské mapování | https://gis.cenia.cz/mapcache/III_vojenske_mapovani/wms ; alt. .../cenia_rt_III_vojenske_mapovani/MapServer/WMSServer | ❌ | ✅ metadata 53df7ed6: totéž |

Arcanum/Mapire: 💻 komerční, neověřováno.

## 10. CENIA / AOPK

| Vrstva | WMS URL | GetCapabilities | Licence |
|---|---|---|---|
| CORINE Land Cover | https://gis.cenia.cz/geoserver/corine_land_cover/wms | ❌ | ✅ metadata micka 4e92de1c: CC BY 4.0, atribuce EU Copernicus/EEA |
| Natura 2000 | https://gis.cenia.cz/geoserver/natura_2000/wms | ❌ | ✅ metadata 5721ad55: CC BY 4.0 |
| Chráněná území INSPIRE (AOPK) | https://gis.nature.cz/arcgis/services/INSPIRE/InspireProtectedSites/MapServer/WMSServer | ❌ | ✅ https://geoportal.gov.cz/php/micka/record/basic/58e3584c-5dd8-488e-8bef-73280a02080a?dlang=eng : CC BY 4.0 |
| AOPK Opendata | https://gis.nature.cz/arcgis/services/Aplikace/Opendata/MapServer/WMSServer | ❌ | ✅ metadata 600e7eaf: CC BY 4.0 |
| ÚSES | WMS nedohledal jsem | - | 🤔 bývá v ÚAP Zlínského kraje, neprověřeno |

## 11. Meliorace (doplněno 18. 10. 2026)

- Žádost SPÚ o informaci o výskytu melioračních staveb (bezplatně, k.ú. + parcela) ✅ https://portal.gov.cz/sluzby-vs/S43666
- ISMS meliorace.vumop.cz (vrstvy "Stavby dle ZVHS"), LPIS vrstva POZ (stav cca 1992) 📄 (Zajíček a kol., VÚMOP 2021). WMS adresa nedohledána.

## Nedohledáno / neotevřeno

- Nedohledal jsem: WMS císařských otisků, WMS VÚMOP pro BPEJ/HSP/infiltraci/RVK, WMS ÚSES, WMS gridových srážek ČHMÚ, WMS a licenci ClimRisk a Intersucho, PUPFL jako samostatnou vrstvu, licenční text VÚMOP, WMS ISMS meliorací.
- ❌ (blokace nástroje, ověřit v prohlížeči): VÚMOP, SPÚ BPEJ, ČGS kromě HG50, CENIA, AOPK, MZe, ČHMÚ opendata, Intersucho, ClimRisk, Atom DMR5G, HEIS WMS, katastr ČÚZK.
