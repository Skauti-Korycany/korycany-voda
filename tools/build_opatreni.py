# -*- coding: utf-8 -*-
"""Sestaví data/opatreni.json pro aplikaci Koryčany resilience z katalogu (docs/KATALOG*.md).
Spustit z libovolné složky: python tools/build_opatreni.py  -> data/opatreni.json, data/opatreni.schema.json
Zdroj pravdy je tento skript; MD soubory v projektu jsou dokumentace.
"""
import json, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data")
os.makedirs(OUT, exist_ok=True)

DNES = "2026-10-20"

# ---------------------------------------------------------------- zdroje
# znacka: "overeno" (✅ otevřeno online), "overeno_stare" (✅⏳ >12 měs.), "citace" (📄), "odhad" (🤔), "pamet" (💻)
Z = {}
def zdroj(id, nazev, url=None, rok=None, znacka="overeno", pozn=None):
    Z[id] = {"id": id, "nazev": nazev, "url": url, "rok": rok, "znacka": znacka, "overeno_dne": DNES if znacka.startswith("overeno") else None, "pozn": pozn}

zdroj("csn759010", "ČSN 75 9010 Vsakovací zařízení srážkových vod (2012) - výtah přes tzb-info/ASIO/MZe/ČVUT", "https://www.tzb-info.cz/normy/csn-75-9010-2012-02", 2012, "overeno", "text normy neotevřen; hodnoty z prezentací ASIO, MZe (Novotná), ČVUT (Stránský)")
zdroj("tnv759011", "TNV 75 9011 Hospodaření se srážkovými vodami (MZe, 2013)", "https://mze.gov.cz/public/portal/-q363041---QOCSTmOG/tnv-75-9011-hospodareni-se-srazkovymi", 2013, "overeno")
zdroj("tab_c", "Tabulka součinitelů odtoku (tzb-info, reprodukce ČSN)", "https://www.tzb-info.cz/docu/tabulky/0000/000088_help.html", None, "overeno", "zdroj normy na stránce neuveden")
zdroj("izomat", "Izomat, technický list vegetační a zatravňovací dlažby (součinitel odtoku)", "https://www.izomat.cz/out/media/114-tl_dlazby_vegetacni_a_zatravnovaci-1.pdf", None, "overeno", "výrobce, ne norma")
zdroj("nzu2026", "SFŽP, Závazné pokyny NZÚ Rodinné domy, platné od 28. 5. 2026", "https://sfzp.gov.cz/files/documents/storage/2026/05/29/1780055187_2026-05-27_NZ%C3%9A-RD26+.pdf", 2026, "overeno")
zdroj("szuz2019", "SZÚZ, Vegetační souvrství zelených střech - standardy 2019", "https://novazelenausporam.cz/files/documents/storage/2020/04/02/1585808609_Vegetacni_souvrstvi_zelenych_strech_Standardy_%202019_web-1.pdf", 2019, "overeno_stare")
zdroj("zilina2024", "estav.cz 2. 7. 2024: měření zelené střechy, Žilinská univerzita", "https://www.estav.cz/cz/12505.strecha-s-vegetaci-jak-rostliny-chrani-dum-pred-horkem-nebo-kolik-zadrzi-vody-vedci-to-zmerili", 2024, "overeno")
zdroj("ujep2023", "UJEP IEEP, Zpráva pro klíčové aktéry č. 4: zelené střechy (leden 2023)", "https://www.fse.ujep.cz/wp-content/uploads/2024/01/Zprava_pro_klicove_aktery_c_4_zelene_strechy.pdf", 2023, "overeno_stare")
zdroj("hornbach_nadrz", "Hornbach 18. 10. 2026: podzemní nádrž 4rain Flat 5000 l vč. šachty", "https://www.hornbach.cz/p/nadrz-na-destovou-vodu-4rain-flat-295126-podzemni-5000-l-vc-sachtove-kopule/10356772/", 2026, "overeno")
zdroj("hornbach_ibc", "Hornbach 18. 10. 2026: IBC kontejner 1000 l nový", "https://www.hornbach.cz/p/ibc-kontejner-tba-un-1000-l-paleta-novy/10235182/", 2026, "overeno")
zdroj("mendelu2022_dz", "MENDELU ZF, přednáška Dešťové zahrady (2022)", "https://ubz.zf.mendelu.cz/wcd/w-zf-ubz/prednasky/seubz_2022_2_destovezahrady_prez.pdf", 2022, "overeno")
zdroj("praha2009_dv", "Praha / Ústav pro ekopolitiku + ČVUT: Jak hospodařit s dešťovou vodou na soukromém pozemku (2009)", "https://www.praha14.cz/app/uploads/sites/4/2021/06/jak_hospodarit_s_destovou_vodou-1.pdf", 2009, "overeno_stare")
zdroj("sppk_b02_001", "SPPK B02 001:2014 Vytváření a obnova tůní (AOPK, ČVUT)", "https://www.mas-rakovnicko.cz/evt_file.php?file=3152", 2014, "overeno")
zdroj("vz_55", "Vodní zákon 254/2001 Sb. § 55 (zrcadlo pracepropravniky.cz, bez data znění)", "https://www.pracepropravniky.cz/zakony/vodni-zakon/paragraf-55/", None, "overeno", "ověřit v e-Sbírce")
zdroj("vz_15b", "Vodní zákon § 15b (zák. 312/2019 Sb.)", "https://www.sagit.cz/info/sb19312", 2019, "overeno")
zdroj("mmr2025_sz", "MMR, odpověď 3. 9. 2025 ke stavebnímu zákonu 283/2021 příl. 2 (terénní úpravy k zadržování vody)", "https://mmr.gov.cz/getmedia/484d345e-55e0-402b-bab1-7a6f2e5c2f0d/MMR-60951-25-31-ze-dne-3-9-2025.pdf.aspx?ext=.pdf", 2025, "overeno")
zdroj("sppk_a02_001", "SPPK A02 001:2013 Výsadba stromů (AOPK)", "https://www.mashlinecko.cz/_uploads/content/431/12-6-standard-aopk.pdf", 2013, "overeno", "existuje aktualizované vydání, rok neověřen")
zdroj("sppk_a02_003", "SPPK A02 003:2013 Výsadba a řez keřů a lián (AOPK)", "https://www.mashlinecko.cz/_uploads/content/431/12-6-standard-aopk.pdf", 2013, "overeno")
zdroj("sppk_c02_003", "SPPK C02 003:2014 Funkční výsadby ovocných dřevin v zemědělské krajině (AOPK, MENDELU)", "https://www.mashlinecko.cz/_uploads/content/431/12-6-standard-aopk.pdf", 2014, "overeno")
zdroj("sppk_d02_004", "SPPK D02 004 Sečení (AOPK) - kód doložen přes SPPK C02 007 a Chytrá a kol. 2024", "https://www.mashlinecko.cz/_uploads/content/438/7.pdf", None, "citace")
zdroj("sppk_d02_003", "SPPK D02 003 Pastva (AOPK, FŽP ČZU) - existence potvrzena, rok a PDF nedohledány", "https://aopk.gov.cz/web/cz/standardy-pece-o-prirodu-a-krajinu", None, "citace")
zdroj("epa2008_trees", "US EPA, Reducing Urban Heat Islands: Compendium, kap. 2 Trees and Vegetation (2008)", "https://www.epa.gov/sites/default/files/2017-05/documents/reducing_urban_heat_islands_ch_2.pdf", 2008, "overeno_stare")
zdroj("epa_trees_benefits", "US EPA, Benefits of Trees and Vegetation (cituje Knight et al. 2021, 308 studií)", "https://epa.gov/heatislands/benefits-trees-and-vegetation", None, "overeno")
zdroj("epa2008_coolroof", "US EPA, Cool Roofs Compendium (2008)", "https://www.epa.gov/sites/default/files/2014-06/documents/coolroofscompendium.pdf", 2008, "overeno_stare")
zdroj("epa2025_coolroof", "US EPA, Using Cool Roofs (snapshot 2025; cituje Synnefa 2007)", "https://19january2025snapshot.epa.gov/heatislands/using-cool-roofs-reduce-heat-islands/index.html", 2025, "overeno")
zdroj("mulc2024", "Přehledový článek Irrigation Science 2024, DOI 10.1007/s00271-024-00924-8 (mulč a výpar z půdy)", "https://link.springer.com/article/10.1007/s00271-024-00924-8", 2024, "overeno", "název a autoři nedohledáni")
zdroj("unl_windbreak", "Univ. Nebraska-Lincoln EC1763 How Windbreaks Work (2002-2006)", "https://extensionpubs.unl.edu/publication/ec1763/2006/pdf/view/ec1763-2006.pdf", 2006, "overeno_stare")
zdroj("dufkova2007", "Dufková J. 2007, Acta Univ. Agric. Silvic. Mendel. Brun. 55(5), větrolamy jižní Morava", "https://acta.mendelu.cz/pdfs/acu/2007/05/09.pdf", 2007, "overeno_stare", "jedno měření, neobecňovat")
zdroj("vumop_vitr2016", "VÚMOP, Doležal, Podhrázská a kol.: Řízení rizika větrné eroze, certifikovaná metodika (2016/2017)", "https://agronavigator.cz/sites/default/files/2025-04/Nmet%252B-%252BMetodika%252B%25C5%2599%25C3%25ADzen%25C3%25AD%252Bv%25C4%259Btrn%25C3%25A9%252Beroze.pdf", 2017, "overeno")
zdroj("mze2022_vitr", "MZe, prezentace Podhrázská a kol., opatření proti větrné erozi (17. 5. 2022)", "https://mze.gov.cz/public/portal/mze/-a74770---r9wNxZdR/prezentace-podhrazska-jana-opatreni-proti-vetrne-erozi", 2022, "overeno")
zdroj("cvut_rain_2023", "Kavka a kol. 2023, Krátkodobé srážky pro hydrologické modelování a navrhování drobných vodohospodářských staveb v krajině (certifikovaná metodika 2/2023/SPU/O, ISBN 978-80-01-07115-1; ČVUT, ČHMÚ, ÚFA AV ČR, Sweco) - 6h návrhové úhrny N2-N100 z WPS rain1.fsv.cvut.cz pro bod v Koryčanech, tools/build_navrhove_srazky.py", "https://rain.fsv.cvut.cz/data/files/metodika_N_srazky_2023_web.pdf", 2023, "overeno", "rastr 1 km, radar 20 let + stanice 30+ let; podmínky užití dat portál neuvádí")
zdroj("vumop_r2022", "VÚMOP / ČHMÚ / MŽP 2022-2023: Regionalizovaný faktor erozní účinnosti přívalového deště (R faktor), rastr 5 m po okresech, podmínky užití žádné (metadata.vumop.cz, záznam 65379397-1a6c-4f19-b153-50fe0a000319); okres Kroměříž stažen 21. 10. 2026", "https://metadata.vumop.cz/record/basic/65379397-1a6c-4f19-b153-50fe0a000319", 2023, "overeno")
zdroj("chmi_korycany", "ČHMÚ, otevřená data (opendata.chmi.cz): stanice Koryčany 0-203-0-41701068002, denní úhrny 1920-2025; zpracování tools/07_srazky_chmi.py, docs/SRAZKY.md", "https://opendata.chmi.cz/meteorology/climate/", 2026, "overeno")
zdroj("vukrom2021", "VÚKROM, Obilnářské listy 2/2021: srážkové normály stanice Kroměříž", "https://www.vukrom.cz/userfiles/files/obilnarske_listy/2021/2021_2/39_43.pdf", 2021, "overeno")
zdroj("kalkulacka_manual", "VÚMOP, Protierozní kalkulačka - manuál (Novotný a kol. 2017); kalkulacka.vumop.cz", "https://kalkulacka.vumop.cz/docs/manual.pdf", 2017, "overeno")
zdroj("janecek2012", "Janeček a kol. 2012, Ochrana zemědělské půdy před erozí (ČZU)", "https://storm.fsv.cvut.cz/data/files/p%C5%99edm%C4%9Bty/YPEO/Metodika_PEO_novelizace%20upravene%2025_1_2012.pdf", 2012, "overeno_stare")
zdroj("dumbrovsky2021", "Dumbrovský, Šarapatka a kol. 2021, Vrstevnicové obdělávání a pásové střídání plodin (VÚMOP)", "https://protieroznipasy.vumop.cz/data/Vrstevnicové%20obdělávání%20a%20pásové%20střídaní%20plodin.pdf", 2021, "overeno")
zdroj("vumop_pasy2022", "VÚMOP 2022, Návrh protierozních travních pásů (R-Software), příručka", "https://protieroznipasy.vumop.cz/data/protierozni_pasy_metodika.pdf", 2022, "overeno")
zdroj("tacr2025_pasy", "MŽP/TAČR PTK Ochranné pásy, 17. 12. 2025 (pilotní měření Centrum Voda)", "https://tacr.gov.cz/wp-content/uploads/documents/2026/01/14/1768398787_TACR%20Ochranne%20pasy%20-%20PTK%2017122025%20-%20V%C3%A1clav%20B%C3%ADl%C3%BD.pdf", 2025, "overeno")
zdroj("vopravil2025", "Vopravil (VÚMOP), prezentace MZe 22. 10. 2025: polní simulátor deště, půdoochranné technologie", "https://mze.gov.cz/public/portal/mze/-a84150---QEFagIDj/prezentace-z-22.-10.-2025-vliv-pudy-a-jejiho-stavu-na-vodni-rezim-krajiny", 2025, "overeno")
zdroj("hladik_pot", "Hladík (VÚMOP), prezentace Půdoochranné technologie (bez data)", "https://aa.ecn.cz/img_upload/410697af7dfcb092dfd4e3937dd69e3f/pudoochranne-technologie_zandov_jiri-hladik_prezentace.pdf", None, "overeno", "tvrzení o organické hmotě bez zdroje")
zdroj("dzes5_2026", "MZe, Metodická příručka DZES 5 pro jarní osevy 2026 (verze září 2025)", "https://www.mze.gov.cz/public/portal/mze/-a81614---9i2f6ULe/metodicka-prirucka-k-plneni-standardu-dzes-5-dobry-zemedelsky-a-environmentalni-stav-pudy-pro-jarni-osevy-roku-2026-a-nasledujici-obdobi", 2025, "overeno")
zdroj("agroles2026", "MZe, Metodika agrolesnictví 2026 (SZP 2023-2027)", "https://mze.gov.cz/public/portal/mze/-a91928---kRzRGYfn/metodika-agrolesnictvi-2026", 2026, "overeno")
zdroj("czu2026_als", "Weger, Lojka a kol. (VÚK, ČZU): Agrolesnictví jako součást bioekonomiky, Senát 20. 5. 2026", "https://bioeconomy.czu.cz/dl/156269?lang=cs", 2026, "overeno")
zdroj("zajicek2021", "Zajíček a kol. (VÚMOP) 2021, metodika revitalizace HOZ a drenáží (TAČR TH02030397)", "https://agronavigator.cz/sites/default/files/2025-04/HOZ_metodika_publ.pdf", 2021, "overeno")
zdroj("spu_meliorace", "Portál gov.cz: Žádost o informaci o výskytu melioračních staveb (SPÚ)", "https://portal.gov.cz/sluzby-vs/S43666", None, "overeno")
zdroj("ipr_manual", "IPR Praha, Manuál tvorby veřejných prostranství, kap. D.2.1 Stromy", "https://iprpraha.cz/uploads/assets/manual_tvorby_verejnych_prostranstvi/pdf/D.2.pdf", None, "overeno")
zdroj("brno2024", "Brno, Nařízení č. 14/2024 Brněnské stavební předpisy", "https://www.cka.cz/++api++/sluzby/legislativa/pravni-predpisy/provadeci-vyhlasky/narizeni-c-142024-o-pozadavcich-na-vystavbu-ve-statutarnim-meste-brne-brnenske-stavebni-predpisy.pdf/@@download/file", 2024, "overeno")
zdroj("tsk2025", "TSK Praha, TP odvodnění komunikací 06/2025", "https://cdn.tsk-praha.cz/portal/2026/01/TP_Odvodneni-komunikaci-TSK-06.2025.pdf", 2025, "overeno")
zdroj("uur2025_zelen", "ÚÚR/RTS, Průměrné ceny dopravní a technické infrastruktury obcí 2025, kap. 9 zeleň", "https://www.uur.cz/media/4jebc4v3/09-zelen-ceny-ti-2025.pdf", 2025, "overeno")
zdroj("uur2025_komunikace", "ÚÚR/RTS 2025, kap. 8 komunikace", "https://www.uur.cz/media/y1ulzdvg/08-komunikace-ceny-ti-2025.pdf", 2025, "overeno")
zdroj("uur2025_kanalizace", "ÚÚR/RTS 2025, kap. 3 kanalizace", "https://www.uur.cz/media/xa3pha4j/03-kanalizace-ceny-ti-2025.pdf", 2025, "overeno", "při druhé kontrole 18. 10. znovu neotevřeno; ověřit ve fázi 6")
zdroj("noo2024", "MŽP, Náklady obvyklých opatření (NOO) verze 2024, platné od 1. 11. 2023, bez DPH", "https://mzp.gov.cz/system/files/2025-04/O610-NPO_POPFK_vyzva_c_5_2024_priloha_c_7_NOO-20240614.pdf", 2024, "overeno_stare", "novější NOO 2025_2 a 2026 existují, z Claude nevytažitelné")
zdroj("aopk_grenzteich", "AOPK, realizace Tůně Grenzteich (2024, NPO POPFK)", "https://dotace.aopk.gov.cz/-/tune-grenzteich", 2024, "overeno")
zdroj("spu_malavrbka", "SPÚ Hodonín, stavba mokřadu Malá Vrbka (kolaudace 20. 11. 2024)", "https://spu.gov.cz/frontend/webroot/uploads/files/2025/02/170a24801._stavba_mokradu_1_v_k24801.u24801._mala_vrbka24801.pdf", 2024, "overeno")
zdroj("aopk_piskova", "AOPK, realizace Větrolam Písková Lhota (podzim 2025)", "https://dotace.aopk.gov.cz/-/vetrolam-piskova-lhota", 2025, "overeno")
zdroj("chytra2024", "Chytrá a kol. 2024, Příroda 44: 87-104 (seč suchých trávníků, jižní Morava)", "https://www.priroda.nature.cz/index.php/priroda/article/download/66/94/289", 2024, "overeno")
zdroj("mhmp2019_sec", "MHMP, Management travnatých ploch v období sucha a horka (2019)", "https://eud.praha.eu/pub/deska/6000004/4/6000003%23MHMPAWO0A020%23MHMP1011LEE0%230/6000003%23MHMPAWO0A020%23MHMP1011HPIR/1_Metodick%C3%A9%20doporu%C4%8Den%C3%AD%20k%20se%C4%8Den%C3%AD%20tr%C3%A1vn%C3%ADk%C5%AF.pdf", 2019, "overeno_stare")
zdroj("oz_pacht", "Občanský zákoník 89/2012 Sb., § 2334-2348 (pacht, zemědělský pacht)", "https://businesscenter.podnikatel.cz/pravo/zakony/obcansky-zakonik/f4586359/", None, "overeno")
zdroj("zak139_2002", "Zákon 139/2002 Sb. o pozemkových úpravách, § 6 odst. 3", "https://www.dauc.cz/predpisy/247/139-2002-sb", None, "overeno")
zdroj("spu_kopu_form", "SPÚ, Žádost o pozemkové úpravy - formulář", "https://spu.gov.cz/pozemkove-upravy/zadost-o-pozemkove-upravy-formular", 2023, "overeno")
zdroj("fucik2015_pastva", "Fučík a kol. 2015, Metodický postup pro hodnocení vlivu pastvy skotu (VÚMOP, ČZU, JČU, CzechGlobe)", "https://agronavigator.cz/sites/default/files/2025-04/metodika-PASTVA_VUMOP_komplet_final%252Bend.pdf", 2015, "overeno_stare", "čísla v metodice jsou zahraniční citace (📄)")
zdroj("mze2020_bystriny", "MZe, Technická doporučení pro hrazení bystřin a strží (2020)", "https://mze.gov.cz/public/portal/mze/-q321647---Qfn_joPV/td-pro-hrazeni-bystrin-a-strzi-mze-2020", 2020, "overeno")
zdroj("vyhl239_2017", "Vyhláška č. 239/2017 Sb. (lesní cesty, hrazení bystřin)", "https://www.tzb-info.cz/docu/predpisy/download/V239-2017.pdf", 2017, "overeno")
zdroj("lcr_strani", "LČR, zadávací list Černý potok ve Strání PŠ 2024 (smlouvy.gov.cz)", "https://smlouvy.gov.cz/smlouva/soubor/43163565/SML-00211-2025-957-P.pdf", 2025, "overeno")
zdroj("avcr2023_liz", "AV ČR, Ústav pro hydrodynamiku, TZ 23. 11. 2023: smrk vs. buk, povodí Liz (DOI 10.1016/j.jhydrol.2019.124285)", "https://www.avcr.cz/export/sites/avcr.cz/.content/galerie-souboru/tiskove-zpravy/2023/TZ-UH-23.11.23-BUKY-NAKLADAJI-S-PUDNI-VODOU-MENE-HOSPODARNE-NEZ-SMRKY-.pdf", 2023, "overeno")
zdroj("hemr2023", "Hemr, Vichta, Kupec et al. 2023, Eur. J. For. Res. 142 (intercepce buk, dub)", "https://link.springer.com/article/10.1007/s10342-023-01592-7", 2023, "overeno")
zdroj("czu2011_plo36", "ČZU FLD 2011, PLO 36 Středomoravské Karpaty - zastoupení LVS", "https://rozcestnik.fld.czu.cz/vyzkum/maps/kolm/PLO36.pdf", 2011, "overeno_stare")
zdroj("wolstenholme2024", "Wolstenholme et al., EGUsphere preprint 2024-2132 (leaky dams, CAESAR-Lisflood)", "https://egusphere.copernicus.org/preprints/2024/egusphere-2024-2132/egusphere-2024-2132-manuscript-version3.pdf", 2024, "overeno")
zdroj("aopk2020_toky", "Just a kol., Ochrana a zlepšování morfologického stavu vodních toků, AOPK 2020", "https://vodnitoky.ochranaprirody.cz/download/183/aopk_metodika_ochrana_vodnich_toku_kap_1_az_7.pdf", 2020, "overeno")
zdroj("vz_17_46_47", "Vodní zákon § 17, § 46, § 47 (zrcadlo pracepropravniky.cz, bez data znění)", "https://www.pracepropravniky.cz/zakony/vodni-zakon/", None, "overeno", "ověřit v e-Sbírce")
zdroj("studanky2025", "Mladí ochránci přírody, Od pramene ke studánce (2025), ISBN 978-80-87221-34-1", "https://wp.estudanky.eu/down/let/nrps-od-pramene-ke-studance.pdf", 2025, "overeno")
zdroj("kalny2017", "Kalny et al. 2017, KMAE 418:5 (stínění toku a teplota vody)", "https://www.kmae-journal.org/articles/kmae/abs/2017/01/kmae160097/kmae160097.html", 2017, "overeno")
zdroj("trimmel2018", "Trimmel et al. 2018, HESS 22:437-461 (vegetace a teplota vody, Pinka)", "https://hess.copernicus.org/articles/22/437/2018/hess-22-437-2018.pdf", 2018, "overeno")
zdroj("tnv752415", "TNV 75 2415 Suché nádrže (MZe, leden 2013)", "https://mze.gov.cz/public/portal/mze/-q363047---5Jh01CKw/tnv-75-2415-suche-nadrze", 2013, "overeno")
zdroj("tpeo2014", "Kadlec a kol. 2014, Navrhování technických protierozních opatření (VÚMOP, ČVUT)", "https://storm.fsv.cvut.cz/data/files/p%C5%99edm%C4%9Bty/YPEO/Metodika_TPEO.pdf", 2014, "overeno_stare")
zdroj("vumop2020_siltfence", "VÚMOP 2020 (Kincl a kol.), Metodika projektování krajinných opatření, část II: silt-fence", "https://www.mzp.gov.cz/system/files/2024-12/OAZK-Metodika_projektovani_a_realizace_krajinnych_opatreni_cast2-20240801.pdf", 2020, "overeno")
zdroj("zivavoda2018", "Živá voda z.s. (Malík), Zádrž vody v povodí Zdoňovsko, studie proveditelnosti 2018", "https://www.zememeric.cz/wp-content/uploads/2020/05/VODA-Zdonov.pdf", 2018, "overeno_stare", "autory označena za předběžnou")
zdroj("opzp105", "OPŽP, 105. výzva (opatření 1.3.4, srážková voda v intravilánu), příjem 17. 6. - 17. 12. 2026", "https://opzp.cz/files/documents/storage/2026/06/02/1780378967_Text%20výzvy%20-%20105.%20výzva.pdf", 2026, "overeno")
zdroj("aopk_zmv17", "AOPK, OPŽP ZMV 17. výzva SC 1.3 (projekty do 200 000 EUR), znovuotevření 20. 10. - 3. 11. 2026", "https://dotace.aopk.gov.cz/-/aopk-opzp-zmv-17-vyzva", 2026, "overeno")
zdroj("opzp104", "OPŽP, 104. výzva (1.3.1), uzavřena 25. 9. 2026", "https://opzp.cz/files/documents/storage/2026/06/30/1782797467_104.%20výzva%20SC%201.3%20Opatření%201.3.1_změna%20č.%201_v2.pdf", 2026, "overeno")
zdroj("ppkb2026", "AOPK, PPK B výzvy 1/2026 a 2/2026 (uzavřeny)", "https://dotace.aopk.gov.cz/-/vyzva-ppk-b-2-pro-rok-2026", 2026, "overeno")
zdroj("popfk", "AOPK, NPO POPFK - program 2022-2025, pro 2026 bez výzvy", "https://dotace.aopk.gov.cz/npo-popfk", 2026, "overeno")
zdroj("pdp_zk2021", "Plány dílčích povodí 2021-2027, základní informace pro Zlínský kraj (12/2021)", "https://zlinskykraj.cz/file/6526a2a5cc8b4a0f8404e1a4", 2021, "overeno")

# ------------------------------------------------------- dotační programy
PROGRAMY = {
 "vlastni": {"nazev": "Vlastní prostředky", "zadatel": ["J","V","O","S","SP"], "stav": "vzdy", "pozn": None, "zdroj": None},
 "nzu_rd_2026": {"nazev": "NZÚ Rodinné domy 2026 (kompenzace úroků úvěru, ne dotace)", "zadatel": ["J"], "stav": "otevreno", "od": "2026-06-25", "do": None,
    "pozn": "D.2 dešťová voda pro WC (+zálivka) max. 100 000 Kč úvěr, nádrž min. 2 m³; D.1 zelená střecha 2 000 Kč/m², max. 150 000 Kč; jen v kombinaci se zateplením (A) nebo zdrojem (C). Nádrž jen na zálivku a zasakování nejsou podporovány.", "zdroj": "nzu2026"},
 "opzp_1_3_4": {"nazev": "OPŽP 105. výzva, opatření 1.3.4 - srážková voda v intravilánu", "zadatel": ["O","S"], "stav": "otevreno", "od": "2026-06-17", "do": "2026-12-17",
    "pozn": "70 % (85 % propojené systémy MZI, 30 % vybrané); obce, školy, spolky; 200 mil. Kč", "zdroj": "opzp105"},
 "aopk_zmv": {"nazev": "AOPK OPŽP ZMV 17. výzva - malé projekty do 200 000 EUR", "zadatel": ["O","S","V","J"], "stav": "otevreno", "od": "2026-10-20", "do": "2026-11-03",
    "pozn": "tůně, MVN, revitalizace (1.3.1.1), vegetační prvky a protierozní opatření (1.3.1.2), sídelní zeleň (1.3.1.4, ne FO), eliminace odvodnění (1.3.1.5); jednorázové částky dle NOO; min. 250 000 Kč bez DPH; max. 100 %", "zdroj": "aopk_zmv17"},
 "opzp_1_3_1": {"nazev": "OPŽP 1.3.1 / 1.3.11 - velké projekty (tůně, MVN, vegetační prvky, odvodnění)", "zadatel": ["O","S","V","SP"], "stav": "uzavreno", "od": None, "do": "2026-09-25",
    "pozn": "tůně až 100 %, MVN 60-85 %, vegetační prvky 80 % (ÚSES 100 %), eliminace odvodnění 100 %; čekat další kolo", "zdroj": "opzp104"},
 "ppk_b": {"nazev": "Program péče o krajinu B (AOPK)", "zadatel": ["J","V","O","S"], "stav": "uzavreno", "od": None, "do": "2026-06-18",
    "pozn": "max. 250 000 Kč/projekt, až 100 %; B.1 péče (seč, pastva, obnova tůní), B.3 nové prvky (výsadby, meze, tůně) jen mimo zastavěné území; 🤔 další kolo 12/2026 nebo 5/2027", "zdroj": "ppkb2026"},
 "popfk": {"nazev": "NPO POPFK (ukončen)", "zadatel": [], "stav": "ukonceno", "pozn": "program 2022-2025, pro 2026 žádná výzva", "zdroj": "popfk"},
 "szp_agroles": {"nazev": "SZP 2023-2027 - agrolesnické systémy", "zadatel": ["zemedelec"], "stav": "otevreno", "od": None, "do": "2026-11-30",
    "pozn": "4 353 EUR/ha zavedení, 754 EUR/ha/rok 5 let; 100 ks/ha, pásy 1-10 m; žadatel je uživatel DPB, ne vlastník", "zdroj": "agroles2026"},
 "kopu": {"nazev": "Komplexní pozemkové úpravy (SPÚ) - společná zařízení", "zadatel": ["V","O"], "stav": "nastroj", "pozn": "vlastníci nadpoloviční výměry ZP v k.ú. mohou vyvolat (§ 6 odst. 3 zák. 139/2002); financuje stát", "zdroj": "zak139_2002"},
 "participativni": {"nazev": "Participativní rozpočet obce", "zadatel": ["J","S"], "stav": "zavisi_na_obci", "pozn": "zjistit, zda Koryčany mají", "zdroj": None},
}

# ---------------------------------------------------------- společné konstanty
KONSTANTY = {
 "srazky_rocni_mm": {"hodnota": 632.0, "pozn": "normál 1991-2020 stanice ČHMÚ Koryčany (1,2 km od středu území, 305 m n. m.); Staré Hutě (427 m) 717 mm", "zdroj": "chmi_korycany", "znacka": "overeno"},
 "navrhovy_dest_6h_korycany": {"N2_mm": 32.2, "N5_mm": 44.3, "N10_mm": 53.2, "N20_mm": 62.6, "N50_mm": 76.0, "N100_mm": 87.0, "pozn": "6hodinové návrhové úhrny, ČVUT/ČHMÚ metodika 2023, bod střed území (rastr 1 km, v území homogenní 52,9-53,4 mm pro N10); tvary A-F a qAPI v data/navrhove_srazky.json", "zdroj": "cvut_rain_2023", "znacka": "overeno"},
 "navrhovy_dest_denni_korycany": {"N2_mm": 37.3, "N5_mm": 49.8, "N10_mm": 58.1, "N20_mm": 66.0, "N50_mm": 76.3, "N100_mm": 84.0, "pozn": "N-leté denní úhrny, Gumbel z ročních maxim 1921-2025 (88 let), stanice ČHMÚ Koryčany - orientační odhad, ne ČSN 75 9010", "zdroj": "chmi_korycany", "znacka": "odhad"},
 "navrhovy_dest_p02": {"15min_mm": 16.5, "60min_mm": 26.2, "24h_mm": 44.2, "pozn": "ČSN 75 9010 tab. A.1/A.2, periodicita 0,2 (1x za 5 let), příklad Brno; pro Koryčany ověřit v normě", "zdroj": "csn759010", "znacka": "overeno"},
 "soucinitel_odtoku": {
   "pozn": "sklon <1 % / 1-5 % / >5 %",
   "strecha": [1.0,1.0,1.0], "strecha_souvrstvi_nad_100mm": [0.5,0.5,0.5], "strecha_souvrstvi_do_100mm": [0.7,0.7,0.8],
   "asfalt_beton_zalita_dlazba": [0.7,0.8,0.9], "dlazba_piskove_spary": [0.5,0.6,0.7], "sterk_upraveny": [0.3,0.4,0.5],
   "zatravnovaci_tvarnice": [0.2,0.3,0.4], "vegetacni_dlazba": [0.25,0.35,0.45], "zahrady_hriste": [0.1,0.15,0.2], "travnik": [0.05,0.1,0.15],
   "zdroj": ["tab_c","izomat"], "znacka": "overeno"},
 "vsak": {"vyprazdneni_max_h": 72, "nad_hladinou_pv_min_m": 1.0, "odstup_budova_nehydroizolovana_m": 5, "odstup_budova_hydroizolovana_m": 2,
   "kf_pruleh_min_m_s": 5e-6, "kf_nadrz_min_m_s": 1e-5, "zkouska_30min_cm": {"nevhodne_pod": 2, "stredni": [4,8], "dobre_nad": 8},
   "zdroj": ["csn759010","praha2009_dv"], "znacka": "overeno", "pozn": "prahy kf podle Stránský (ČVUT), ne přímo text normy"},
 "usle": {
   "Gp_t_ha_rok": {"od_2022-07-01": {"melke": 3, "ostatni": 12}, "od_2026-07-01": {"melke": 2, "ostatni": 9}, "od_2030-07-01": {"melke": 1, "ostatni": 5}},
   "C": {"kukurice_zrno_orba": [0.70,0.90,0.70,0.35,0.70,0.40], "obilniny_olejniny_po_obilninach": [0.65,0.70,0.45,0.08,0.25,0.04], "cukrovka_brambory": [0.65,0.80,0.65,0.30,0.70], "travni_porost": 0.01, "vicelete_picniny": 0.015},
   "P_vrstevnice_podle_sklonu_stupne": {"0-4": 0.6, "4-6": 0.7, "6-8": 0.8, "8-10": 0.9, ">10": 1.0},
   "P_pasove_stridani_sklon_pct": {"okopaniny+picniny": {"2-7": 0.30, "7-12": 0.35, "12-18": 0.40, "18-24": 0.45}, "okopaniny+ozimy": {"2-7": 0.50, "7-12": 0.60, "12-18": 0.75, "18-24": 0.90}, "max_sirka_pasu_m": {"2-7": 40, "7-12": 30, "12-18": 20, "18-24": 20}},
   "R_korycany": {"prumer": 66.0, "rozsah": [62.4, 71.4], "orna_prumer": 65.9, "jednotka": "MJ/ha·cm/h", "pozn": "regionalizovaný R faktor 2022 (VÚMOP/ČHMÚ), rastr 5 m, území modelu; Janeček 2012 doporučoval paušálně 40", "zdroj": "vumop_r2022", "znacka": "overeno"},
   "K_hpj": {"zdroj": "janecek2012", "pozn": "tab. 1.5, hodnoty v tools/11_usle.py"},
   "zdroj": ["kalkulacka_manual","janecek2012","vumop_r2022"], "znacka": "overeno", "pozn": "výpočet pro ornou půdu území modelu: tools/11_usle.py -> data/usle_info.json"},
 "regulovany_odtok_l_s_ha": {"hodnota": 3, "zdroj": ["brno2024","tsk2025"], "pozn": "praxe Brno/Praha, pro Koryčany nezávazné"},
}

# ------------------------------------------------------------- opatření
O = []
def op(id, nazev, misto, rozhoduje, pracnost, ucinky_prim, ucinky_ved, meritko, kontext=False, popis=None,
       kvant=None, vhodnost=None, vazby=None, povoleni=None, povoleni_pozn=None, ceny=None, financovani=None, standardy=None, nedohledano=None, pozn_poctivost=None):
    O.append({
        "id": id, "nazev": nazev, "popis": popis,
        "misto": misto, "rozhoduje": rozhoduje, "pracnost": pracnost,
        "ucinky": {"primarni": ucinky_prim, "vedlejsi": ucinky_ved},
        "meritko": meritko, "kontext": kontext,
        "kvantifikace": kvant or [],
        "vhodnost": vhodnost or {},
        "vazby": vazby or {"potrebuje": [], "synergie": [], "konflikt": []},
        "povoleni": povoleni, "povoleni_pozn": povoleni_pozn,
        "ceny": ceny or [], "financovani": financovani or ["vlastni"],
        "standardy": standardy or [],
        "nedohledano": nedohledano or [],
        "pozn_poctivost": pozn_poctivost,
        "vahy_skaly": None,  # rezervováno: {"sucho":0-3,"prival":0-3,"vedro":0-3,"vitr_mraz":0-3,"biodiverzita":0-3}
    })

def kv(ucinek, typ, popis, hodnota=None, jednotka=None, rozsah=None, vzorec=None, zdroj=None, znacka="overeno"):
    """typ: 'vzorec' (jádro počítá), 'hodnota' (doložená konstanta/rozsah), 'kvalitativne' (bez čísla)."""
    return {"ucinek": ucinek, "typ": typ, "popis": popis, "hodnota": hodnota, "jednotka": jednotka, "rozsah": rozsah, "vzorec": vzorec, "zdroj": zdroj, "znacka": znacka}

def cena(polozka, hodnota, jednotka, rok, zdroj, pozn=None, rozsah=None):
    return {"polozka": polozka, "hodnota": hodnota, "rozsah": rozsah, "jednotka": jednotka, "rok": rok, "zdroj": zdroj, "pozn": pozn}

NEOVERENA = {"polozka": "celkem", "hodnota": None, "rozsah": None, "jednotka": "Kč", "rok": None, "zdroj": None, "pozn": "cena neověřena"}

# ===== Z zahrada a dvůr
op("Z01", "Dešťová zahrada (zasakovací záhon)", ["Z","U"], ["J","O","S"], 1, ["I","R"], ["CH","B"], "pozemek",
   popis="Mělká prohlubeň s výsadbou, do které je svedena voda ze střechy nebo dvora; voda se do 72 h vsákne.",
   kvant=[kv("R","vzorec","Objem zadržený = plocha zahrady × hloubka vzdutí (max 0,25-0,3 m)", vzorec="V_m3 = A_zahrada_m2 * h_vzduti_m", zdroj=["mendelu2022_dz","praha2009_dv"]),
          kv("I","vzorec","Plocha zahrady 10-20 % napojené zpevněné plochy podle propustnosti; při správném návrhu zasákne celý odtok ze střechy (rok: A_strechy × 0,63 m)", vzorec="A_zahrada_m2 = A_zpevnena_m2 * (0.10..0.20); V_rok_m3 = A_strechy_m2 * 0.632", zdroj=["praha2009_dv","mendelu2022_dz"]),
          kv("CH","kvalitativne","Vlhké stanoviště, výsadba", znacka="odhad"), kv("B","kvalitativne","Výsadba, vlhké stanoviště", znacka="odhad")],
   vhodnost={"hsp": ["A","B","C"], "sklon_max_pct": 5, "odstup_stavba_min_m": 5, "odstup_stavba_jil_m": [6,10], "nad_hladinou_pv_min_m": 1, "vyloucit": ["niva s mělkou podzemní vodou"]},
   vazby={"potrebuje": ["S02"], "synergie": ["S01","Z05"], "konflikt": []},
   povoleni=0, povoleni_pozn="do 300 m² mimo koryto; § 55 odst. 3 vodního zákona", ceny=[NEOVERENA], financovani=["vlastni"],
   standardy=["csn759010"], nedohledano=["cena 2025-2026"])

op("Z02", "Zahradní tůň bez fólie (hliněná, jílem těsněná)", ["Z"], ["J","S"], 1, ["R","CH","B"], ["I"], "pozemek",
   popis="Mělká tůň napájená srážkami a povrchovým odtokem, bez hráze a technických objektů.",
   kvant=[kv("R","vzorec","Objem = plocha × průměrná hloubka (0,5-1,0 m); tůň 2x1 m, 0,5 m = 1 m³", vzorec="V_m3 = A_m2 * h_prum_m", zdroj=["sppk_b02_001"]),
          kv("B","kvalitativne","Hlavní přínos malé tůně", znacka="odhad"), kv("CH","kvalitativne","Výpar z hladiny chladí okolí; část zadržené vody se odpaří (bez čísla, zdroj nedohledán)", znacka="odhad")],
   vhodnost={"hsp": ["C","D"], "misto_typ": ["zamokřené místo","úpatí svahu","niva"], "sklon_max_pct": 3},
   vazby={"potrebuje": [], "synergie": ["Z01","Z03"], "konflikt": []},
   povoleni=0, povoleni_pozn="bez hráze mimo koryto není vodní dílo (§ 55 odst. 3); do 300 m² a 1,5 m 💻 bez povolení - ověřit na vodoprávním úřadě ORP Kroměříž; nad 300 m² ohlášení (§ 15b)",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["sppk_b02_001","vz_55","vz_15b","mmr2025_sz"],
   nedohledano=["výpar z malé hladiny (mm/den)", "cena svépomocí"],
   pozn_poctivost="SPPK B02 001: průměrná hloubka 0,8-1,0 m, max 1,5 m, mělčiny do 50 cm min. polovina plochy, břehy max 1:3.")

op("Z03", "Zasakovací průleh / rýha po vrstevnici (svejl) v zahradě nebo sadu", ["Z","L"], ["J"], 1, ["I","Q","ER"], ["R"], "pozemek",
   kvant=[kv("R","vzorec","Objem = délka × průřez", vzorec="V_m3 = L_m * S_m2", zdroj=["csn759010"]),
          kv("Q","vzorec","Zachytí povrchový odtok z vlastní plochy nad průlehem: V = A_nad × srážka × C", vzorec="V_odtok_m3 = A_nad_m2 * P_m * C", zdroj=["tab_c"]),
          kv("I","kvalitativne","Vliv na vlhkost půdy nekvantifikován", znacka="odhad")],
   vhodnost={"hsp": ["A","B","C"], "sklon_min_pct": 3, "sklon_max_pct": 15, "odstup_stavba_min_m": 5},
   vazby={"potrebuje": [], "synergie": ["Z06","Z05"], "konflikt": ["nad budovou ve svahu bez odstupu"]},
   povoleni=0, ceny=[NEOVERENA], financovani=["vlastni"], standardy=["csn759010"], nedohledano=["kvantifikace účinku na vlhkost půdy","cena"])

op("Z04", "Náhrada zpevněných ploch propustnými (zatravňovací dlažba, štěrk, propustná dlažba)", ["Z","U"], ["J","O"], 2, ["I","CH"], ["R"], "pozemek",
   kvant=[kv("I","vzorec","Zisk = plocha × srážka × (C_puvodni - C_nove); asfalt 0,8 -> tvárnice 0,3", vzorec="dV_m3 = A_m2 * P_m * (C_old - C_new)", zdroj=["tab_c","izomat"]),
          kv("CH","hodnota","Trávník: vzduch o 1-2 °C chladnější než zpevněné plochy (EPA); povrch - citace 📄", rozsah=[1,2], jednotka="°C", zdroj=["epa2008_trees"], znacka="overeno_stare")],
   vhodnost={"hsp": ["A","B","C"], "sklon_max_pct": 3, "nad_hladinou_pv_min_m": 1},
   vazby={"potrebuje": [], "synergie": ["S02"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[cena("zatravňovací tvárnice vč. podkladu", 1136, "Kč/m²", 2025, "uur2025_komunikace"), cena("zámková dlažba 8 cm vč. podkladu", 2240, "Kč/m²", 2025, "uur2025_komunikace"), cena("asfalt celá konstrukce (pro srovnání)", 1411, "Kč/m²", 2025, "uur2025_komunikace")],
   financovani=["vlastni","opzp_1_3_4"], standardy=["csn759010"])

op("Z05", "Trvalý pokryv půdy: mulč, kompost, organická hmota", ["Z","L","P"], ["J","V"], 1, ["I","E","CH"], ["ER"], "pozemek",
   kvant=[kv("E","hodnota","Mulč snižuje výpar z půdy o 17-79 % za sezónu proti holé půdě, typicky 33-40 %; slámový mulč 30-35 %", rozsah=[17,79], hodnota=35, jednotka="%", zdroj=["mulc2024"]),
          kv("I","kvalitativne","Organická hmota zvyšuje retenci půdy; kvantifikace nedohledána", znacka="odhad")],
   vhodnost={"vsude": True}, vazby={"potrebuje": [], "synergie": ["Z01","Z02","Z03"], "konflikt": []}, povoleni=0,
   ceny=[cena("vlastní kompost, štěpka", 0, "Kč", 2026, None, pozn="🤔 nula až stovky Kč")], financovani=["vlastni"], nedohledano=["retence půdy podle organické hmoty (český zdroj)"])

op("Z06", "Výsadba stromu (stín, vzrostlý strom, ovocný strom)", ["Z","U","L"], ["J","O","S"], 1, ["CH","E"], ["I","B"], "pozemek",
   kvant=[kv("CH","hodnota","Stín snižuje povrchovou teplotu stěn a střech o 11-25 °C", rozsah=[11,25], jednotka="°C", zdroj=["epa2008_trees"], znacka="overeno_stare"),
          kv("CH","hodnota","Vzduch ve skupinách stromů až o 5 °C nižší (vrchol dne); předměstí se stromy o 2-3 °C; městská zeleň průměr -1,6 °C (Knight 2021, 308 studií)", rozsah=[1.6,5], jednotka="°C", zdroj=["epa2008_trees","epa_trees_benefits"], znacka="overeno_stare"),
          kv("E","kvalitativne","Zástin půdy, zpomalení větru", znacka="odhad")],
   vhodnost={"mimo_ochranna_pasma_siti": True, "strana_budovy_pro_stin": ["J","Z"]},
   vazby={"potrebuje": [], "synergie": ["Z07","Z03"], "konflikt": []}, povoleni=0, povoleni_pozn="1 u sítí; odstupy od hranice dle OZ 💻",
   ceny=[cena("strom prostokořenný do 200 cm", 1775, "Kč/ks", 2025, "uur2025_zelen"), cena("strom s balem do 200 cm", 2835, "Kč/ks", 2025, "uur2025_zelen"), cena("strom s balem 250-350 cm", 6100, "Kč/ks", 2025, "uur2025_zelen"), cena("ovocný strom prostokořenný", None, "Kč/ks", 2025, "uur2025_zelen", rozsah=[240,350])],
   financovani=["vlastni","ppk_b","aopk_zmv"], standardy=["sppk_a02_001","sppk_c02_003"])

op("Z07", "Živý plot / keřový pás místo plotu nebo zdi", ["Z","U"], ["J","O"], 1, ["E","CH","B"], [], "pozemek",
   kvant=[kv("E","hodnota","Za překážkou s propustností 40-60 % rychlost větru nižší o ~70 % v 5 H, 50 % v 10 H, 25 % v 20 H; RH v závětří +2-4 %", rozsah=[25,70], jednotka="% rychlosti větru", zdroj=["unl_windbreak"], znacka="overeno_stare"),
          kv("E","vzorec","Chráněná plocha = délka × (10-20) × výška", vzorec="A_chranena_m2 = L_m * H_m * (10..20)", zdroj=["unl_windbreak"], znacka="overeno_stare")],
   vhodnost={"strana": "návětrná (Z/JZ 🤔, ověřit z dat ČHMÚ)"}, vazby={"potrebuje": [], "synergie": ["Z06"], "konflikt": []}, povoleni=0,
   ceny=[cena("listnatý keř prostokořenný do 60 cm", 190, "Kč/ks", 2024, "noo2024")], financovani=["vlastni"], standardy=["sppk_a02_003"], nedohledano=["snížení evapotranspirace v %"])

op("Z08", "Květnatá louka místo trávníku, vyšší a méně častá seč, mozaika", ["Z","U","L"], ["J","O","S"], 1, ["E","CH","B"], ["I"], "pozemek",
   kvant=[kv("E","kvalitativne","Vyšší porost stíní půdu; kvantifikace vlhkosti nedohledána", znacka="odhad"),
          kv("B","hodnota","Nepravidelně kosené plochy o 20 % druhově chudší než pravidelně fázovaně kosené; nekosené -34 % (jižní Morava)", rozsah=[20,34], jednotka="% druhů", zdroj=["chytra2024"])],
   vhodnost={"vsude": True}, vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=0,
   ceny=[cena("trávník luční (založení)", 40, "Kč/m²", 2025, "uur2025_zelen"), cena("zatravnění regionální směsí", 86600, "Kč/ha", 2024, "noo2024")],
   financovani=["vlastni","ppk_b"], standardy=["sppk_d02_004","mhmp2019_sec"], pozn_poctivost="SPPK D02 004: 10-20 % plochy ponechat neposečené; Praha 2019: výška 10-15 cm, neseče se nad 26 °C.")

op("Z09", "Zelená fasáda, popínavky, pergola se zelení", ["Z","S"], ["J","O","S"], 1, ["CH"], ["E"], "pozemek",
   kvant=[kv("CH","hodnota","Stín na fasádě: povrch o 11-25 °C chladnější (obecná hodnota pro stín stromů, EPA)", rozsah=[11,25], jednotka="°C", zdroj=["epa2008_trees"], znacka="overeno_stare")],
   vhodnost={"strana_budovy": ["J","Z"]}, vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=0, ceny=[NEOVERENA], financovani=["vlastni"], nedohledano=["kvantifikace pro zelené fasády","cena"])

op("Z10", "Vsakovací objekt pro střešní vodu (štěrkové těleso, vsakovací bloky, šachta)", ["Z","U"], ["J","O"], 2, ["I","R"], [], "pozemek",
   kvant=[kv("R","vzorec","Návrh na déšť p=0,2 (24 h 44 mm): V = A_strechy × 0,044 minus vsak během deště", vzorec="V_m3 = A_strechy_m2 * 0.044 - V_vsak", zdroj=["csn759010"]),
          kv("I","vzorec","Rok: celý odtok ze střechy zasákne", vzorec="V_rok_m3 = A_strechy_m2 * 0.632", zdroj=["csn759010","chmi_korycany"])],
   vhodnost={"hsp": ["A","B"], "kf_min_m_s": 1e-5, "nad_hladinou_pv_min_m": 1, "odstup_stavba_min_m": 5},
   vazby={"potrebuje": ["S02"], "synergie": [], "konflikt": []}, povoleni=0, povoleni_pozn="0-1; u větších objektů posudek vsaku 💻",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["csn759010","tnv759011"], nedohledano=["cena bloků a výkopu 2025-2026"])

op("Z11", "Zálivka zachycenou vodou, kapková závlaha", ["Z"], ["J","S"], 1, ["W","E"], [], "pozemek",
   kvant=[kv("W","kvalitativne","Šetří pitnou vodu; úspora nekvantifikována (český zdroj nedohledán)", znacka="odhad")],
   vhodnost={"vsude": True}, vazby={"potrebuje": ["S01"], "synergie": [], "konflikt": []}, povoleni=0, ceny=[NEOVERENA], financovani=["vlastni"])

# ===== S střecha a stavba
op("S01", "Nádrž na dešťovou vodu (sud, IBC, podzemní jímka) s využitím", ["S","Z"], ["J","O","S"], 2, ["R","W"], ["Q"], "pozemek",
   kvant=[kv("R","vzorec","Každých 10 mm deště ze 100 m² střechy = 1 m³; nádrž pojme V_nadrz, zbytek přepad", vzorec="V_zachyceno_m3 = min(V_nadrz_m3, A_strechy_m2 * P_m * 1.0)", zdroj=["tab_c"]),
          kv("R","vzorec","Rok: potenciál A × 0,632 m; využije se jen spotřeba mezi dešti", vzorec="V_rok_potencial_m3 = A_strechy_m2 * 0.632", zdroj=["chmi_korycany"]),
          kv("W","kvalitativne","Zálivka/WC z dešťovky; spotřeba nekvantifikována", znacka="odhad")],
   vhodnost={"kazda_strecha": True}, vazby={"potrebuje": ["S02"], "synergie": ["Z01","Z10","Z11"], "konflikt": ["přepad do kanalizace"]},
   povoleni=0, povoleni_pozn="podzemní nádrž 🤔 1",
   ceny=[cena("IBC kontejner 1000 l nový", 7250, "Kč", 2026, "hornbach_ibc", pozn="18. 10. 2026, s DPH"), cena("podzemní nádrž 5000 l vč. šachty, bez montáže", 50830, "Kč", 2026, "hornbach_nadrz", pozn="18. 10. 2026, s DPH"), {"polozka": "montáž a výkop", "hodnota": None, "rozsah": None, "jednotka": "Kč", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["vlastni","nzu_rd_2026"], standardy=["csn759010"], pozn_poctivost="NZÚ 2026 podporuje jen nádrž pro WC (min. 2 m³) a jen s A/C; nádrž pouze na zálivku ne.")

op("S02", "Odpojení dešťových svodů od kanalizace, svedení na pozemek", ["S"], ["J","O"], 1, ["Q","I","R"], [], "pozemek",
   kvant=[kv("Q","vzorec","Objem, který nejde do kanalizace: A_strechy × srážka × 1,0", vzorec="V_m3 = A_strechy_m2 * P_m", zdroj=["tab_c"])],
   vhodnost={"podminka": "svody vedou do jednotné kanalizace - v Koryčanech neověřeno (podle uživatele místy oddílná kvůli ČOV)"},
   vazby={"potrebuje": [], "synergie": ["Z01","Z10","S01"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1; souhlas provozovatele kanalizace 💻",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["csn759010","tnv759011"], nedohledano=["typ kanalizace v Koryčanech","cena"])

op("S03", "Zelená střecha (extenzivní)", ["S"], ["J","O","S"], 3, ["R","CH","Q"], ["B"], "pozemek",
   kvant=[kv("R","hodnota","Zadrží ~75 % běžného deště; u přívalu >30 mm odtok nižší o 77-83 %", rozsah=[75,83], jednotka="%", zdroj=["zilina2024"]),
          kv("Q","vzorec","Návrhově C 0,3-0,5 (souvrství >100 mm 0,5; SZÚZ příklad 0,3)", vzorec="V_odtok_m3 = A_m2 * P_m * (0.3..0.5)", zdroj=["tab_c","szuz2019"]),
          kv("CH","hodnota","Povrch vegetace o 5-7 °C chladnější než holá fólie (fólie téměř 60 °C)", rozsah=[5,7], jednotka="°C", zdroj=["zilina2024"])],
   vhodnost={"nosnost": "ověřit", "sklon_max_pct": 30, "souvrstvi_mm": [60,150]},
   vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=1, povoleni_pozn="1-2 (statika; veřejné budovy stavební úřad 💻)",
   ceny=[cena("extenzivní zelená střecha", None, "Kč/m²", 2023, "ujep2023", rozsah=[1000,2500], pozn="⏳ 2023; 2025-2026 nedohledáno")],
   financovani=["vlastni","nzu_rd_2026","opzp_1_3_4"], standardy=["szuz2019"], nedohledano=["cena 2025-2026", "C extenzivní vs. intenzivní z normy"])

op("S04", "Světlá střecha a plochy (albedo, cool roof)", ["S","U"], ["J","O"], 1, ["CH"], [], "pozemek",
   kvant=[kv("CH","hodnota","Povrch chladné střechy o 28-33 °C nižší než tmavé (tmavé 66-85 °C, chladné 43-46 °C)", rozsah=[28,33], jednotka="°C povrch", zdroj=["epa2008_coolroof"], znacka="overeno_stare"),
          kv("CH","hodnota","Vnitřní maximum o 1,2-3,3 °C nižší; špičková potřeba chlazení -11 až -27 %", rozsah=[1.2,3.3], jednotka="°C interiér", zdroj=["epa2025_coolroof"]),
          kv("CH","hodnota","Vzduch ve městě při 50 % pokrytí střech jen o 0,2-0,3 °C (simulace NYC) - v součtu za území ukazovat jen plochu ochlazených střech, ne °C vzduchu", rozsah=[0.2,0.3], jednotka="°C vzduch", zdroj=["epa2008_coolroof"], znacka="overeno_stare")],
   vhodnost={"strecha_typ": ["tmavá plochá","mírně šikmá"], "objekty": ["bytovky","haly","škola","garáže","parkoviště"]},
   vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=0, ceny=[NEOVERENA], financovani=["vlastni"], nedohledano=["cena reflexního nátěru 2025-2026"],
   pozn_poctivost="Rozlišovat účinek na budovu (silný) vs. na mikroklima obce (slabý).")

# ===== U veřejný prostor obce
op("U01", "Uliční stromořadí s vsakovacími rabátky", ["U"], ["O"], 3, ["CH","I","Q"], ["B"], "lokalita",
   kvant=[kv("CH","hodnota","Stín -11 až -25 °C povrch; vzduch v zeleni až -5 °C v horku", rozsah=[11,25], jednotka="°C povrch", zdroj=["epa2008_trees"], znacka="overeno_stare"),
          kv("I","vzorec","Rabátko: min. 6 m² propustné plochy, prokořenitelný prostor min. 16 m² × 0,8 m; retence 🤔 1-3 m³ na strom (bez českého zdroje)", vzorec="V_m3 = A_rabatko_m2 * h_m * porovitost", rozsah=[1,3], jednotka="m³/strom", zdroj=["ipr_manual"], znacka="odhad"),
          kv("Q","vzorec","Odvodnění ulice do rabátka: C 0,1 místo 0,8", vzorec="dV_m3 = A_ulice_m2 * P_m * (0.8 - 0.1)", zdroj=["tab_c"])],
   vhodnost={"ulice_se_sklonem_k_rabatku": True, "site": "ověřit", "vysadbovy_pas_min_m": [0.8,1.5]},
   vazby={"potrebuje": [], "synergie": ["U02","U03"], "konflikt": []}, povoleni=2, povoleni_pozn="1-2 (sítě, komunikace)",
   ceny=[cena("strom s balem 250-350 cm", 6100, "Kč/ks", 2025, "uur2025_zelen"), {"polozka": "rabátko se strukturním substrátem", "hodnota": None, "rozsah": None, "jednotka": "Kč/ks", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["opzp_1_3_4","aopk_zmv"], standardy=["ipr_manual","brno2024","sppk_a02_001"], nedohledano=["cena rabátka","metodika MZI MŽP"])

op("U02", "Propustné povrchy parkovišť, chodníků, dvorů veřejných budov", ["U"], ["O"], 3, ["I","CH"], ["R"], "lokalita",
   kvant=[kv("I","vzorec","Zisk = A × P × (C_old - C_new); parkoviště 1000 m², 20 mm: 16 -> 6 m³ s tvárnicemi; rok 456 -> 171 m³", vzorec="dV_m3 = A_m2 * P_m * (C_old - C_new)", zdroj=["tab_c","izomat"])],
   vhodnost={"hsp": ["A","B","C"]}, vazby={"potrebuje": [], "synergie": ["U01"], "konflikt": []}, povoleni=2, povoleni_pozn="1-2",
   ceny=[cena("zatravňovací tvárnice", 1136, "Kč/m²", 2025, "uur2025_komunikace"), cena("zámková dlažba 8 cm vč. podkladu", 2240, "Kč/m²", 2025, "uur2025_komunikace"), cena("vsakovací boxy pod parkovištěm 500 m²", 157040, "Kč", 2025, "uur2025_kanalizace"), cena("vsakovací boxy pod parkovištěm 1000 m²", 266330, "Kč", 2025, "uur2025_kanalizace")],
   financovani=["opzp_1_3_4"], standardy=["csn759010"])

op("U03", "Zasakovací pásy a průlehy podél komunikací, příkopy s retencí", ["U","C"], ["O"], 2, ["I","Q","R"], [], "lokalita",
   kvant=[kv("R","vzorec","Objem = délka × průřez; 100 m × 1 m² = 100 m³ = 20 mm z 0,5 ha", vzorec="V_m3 = L_m * S_m2", zdroj=["tsk2025"]),
          kv("Q","hodnota","Regulovaný odtok praxe 3 l/s/ha", hodnota=3, jednotka="l/s/ha", zdroj=["brno2024","tsk2025"])],
   vhodnost={"sklon": "podle TSK svahy 1:3", "hsp": ["A","B","C"]}, vazby={"potrebuje": [], "synergie": ["C01"], "konflikt": []}, povoleni=2, povoleni_pozn="1-2",
   ceny=[cena("travnaté průlehy a meze s terénními úpravami", 200, "Kč/m²", 2024, "noo2024")], financovani=["opzp_1_3_4"], standardy=["csn759010","tsk2025"])

op("U04", "Retence a zasakování vody z veřejných budov (škola, úřad)", ["U","S"], ["O","S"], 3, ["R","I","W"], [], "lokalita",
   kvant=[kv("R","vzorec","Škola střecha 1500 m²: 20 mm = 30 m³; rok 948 m³", vzorec="V_m3 = A_strechy_m2 * P_m", zdroj=["tab_c","chmi_korycany"])],
   vhodnost={"podle_objektu": True}, vazby={"potrebuje": ["S02"], "synergie": ["S01","Z01","Z10"], "konflikt": []}, povoleni=1, povoleni_pozn="1-2",
   ceny=[cena("podzemní ŽB retenční nádrž", None, "Kč/m³", 2025, "uur2025_kanalizace", rozsah=[18500,28500]), cena("plastová nádrž 5000 l bez montáže", 50830, "Kč", 2026, "hornbach_nadrz")],
   financovani=["opzp_1_3_4"], standardy=["csn759010"])

op("U05", "Obecní tůň, mokřad, obnova návesní nádrže", ["U","T"], ["O"], 3, ["R","CH","B"], ["I"], "lokalita",
   kvant=[kv("R","vzorec","Objem = plocha × průměrná hloubka 0,8-1,0 m; 500 m² ~ 400 m³", vzorec="V_m3 = A_m2 * (0.8..1.0)", zdroj=["sppk_b02_001"])],
   vhodnost={"misto_typ": ["zamokřené plochy","niva"]}, vazby={"potrebuje": [], "synergie": ["T01","T02"], "konflikt": []}, povoleni=2, povoleni_pozn="nad 300 m² ohlášení (§ 15b); s hrází vodní dílo",
   ceny=[cena("tůň strojně, materiál v lokalitě", 330, "Kč/m² hladiny", 2024, "noo2024", pozn="+15 000 Kč/lokalitu; odvoz do 2 km 410, nad 2 km 480"), cena("odbahnění", 430, "Kč/m³", 2024, "noo2024"),
         cena("realizace Tůně Grenzteich 1250 m²", 98875, "Kč", 2024, "aopk_grenzteich", pozn="🤔 79 Kč/m²"), cena("realizace mokřad Malá Vrbka, 3 tůně", 610473, "Kč vč. DPH", 2024, "spu_malavrbka")],
   financovani=["aopk_zmv","ppk_b","opzp_1_3_1"], standardy=["sppk_b02_001","vz_15b"], nedohledano=["cena poldru a hráze (dřívější údaj se v ÚÚR 2025 nepotvrdil, vyřazen)"])

op("U06", "Mozaiková seč obecních ploch, květnaté louky", ["U","L"], ["O","S"], 1, ["E","CH","B"], [], "lokalita",
   kvant=[kv("B","hodnota","Nepravidelně kosené -20 % druhů, nekosené -34 %; fázovaná seč ve 3 termínech", rozsah=[20,34], jednotka="% druhů", zdroj=["chytra2024"]),
          kv("E","kvalitativne","Vlhkost/teplota v ČR nekvantifikovány", znacka="odhad")],
   vhodnost={"vsude": True}, vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=0,
   ceny=[cena("seč lehkou mechanizací", 17425, "Kč/ha", 2024, "noo2024"), cena("seč křovinořezem", 35000, "Kč/ha", 2024, "noo2024"), cena("trávník luční", 40, "Kč/m²", 2025, "uur2025_zelen")],
   financovani=["vlastni","ppk_b"], standardy=["sppk_d02_004","mhmp2019_sec"])

op("U07", "Školní zahrada jako ukázkový pozemek", ["U","Z"], ["S","O"], 1, ["R","I","CH","B"], [], "pozemek",
   popis="Sada Z01-Z08 + měření M01-M06 na školním pozemku; účinky a ceny podle složek.",
   vhodnost={"areal_skoly": True}, vazby={"potrebuje": [], "synergie": ["Z01","Z02","Z05","Z06","Z08","S01","S02","M01","M02","M03","M04","M05","M06"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[], financovani=["opzp_1_3_4","participativni","vlastni"])

# ===== P orná půda
op("P01", "Protierozní mez, zatravněný pás, biopás po vrstevnici", ["P"], ["V"], 2, ["ER","Q","I"], ["B","E"], "lokalita",
   kvant=[kv("ER","vzorec","Pás zkracuje délku svahu L v USLE a má C 0,01", vzorec="A = R*K*LS(L_zkracene)*C*P", zdroj=["kalkulacka_manual","dumbrovsky2021"]),
          kv("Q","hodnota","Čas do začátku odtoku (svah 11,3 %): 0 % zatravnění 102 s, 25 % 141 s, 50 % 253 s, 100 % 461 s; rychlost odtoku 5-6x nižší; retence 2 m pásu po 20 min deště vyčerpána", rozsah=[102,461], jednotka="s", zdroj=["tacr2025_pasy"])],
   vhodnost={"sklon_min_pct": 3, "erozni_ohrozenost": ["SEO","MEO"], "max_sirka_pasu_plodiny_m": 40, "sirka_pasu_min_m": 3, "sirka_pasu_dopor_m": 22},
   vazby={"potrebuje": ["N01|N02"], "synergie": ["P07","P02","P08"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1 (změna kultury v LPIS přes uživatele DPB)",
   ceny=[cena("meze a průlehy s terénními úpravami", 200, "Kč/m²", 2024, "noo2024"), cena("zatravnění regionální směsí", 86600, "Kč/ha", 2024, "noo2024"), {"polozka": "ušlý výnos z pásu", "hodnota": None, "rozsah": None, "jednotka": "Kč/ha/rok", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["aopk_zmv","ppk_b","opzp_1_3_1"], standardy=["dumbrovsky2021","dzes5_2026"], nedohledano=["% snížení ztráty půdy z českého měření"],
   pozn_poctivost="Úzký pás funguje na začátku deště, ne na dlouhý příval.")

op("P02", "Zasakovací průleh na orné půdě", ["P"], ["V"], 2, ["I","Q","ER"], [], "lokalita",
   kvant=[kv("R","vzorec","Objem = délka × průřez", vzorec="V_m3 = L_m * S_m2", zdroj=["csn759010","vumop_pasy2022"])],
   vhodnost={"sklon_min_pct": 3, "sklon_max_pct": 12, "hsp": ["A","B","C"]}, vazby={"potrebuje": ["P05"], "synergie": ["P01"], "konflikt": []}, povoleni=1,
   ceny=[cena("průlehy s terénními úpravami", 200, "Kč/m²", 2024, "noo2024")], financovani=["aopk_zmv"], standardy=["csn759010","tpeo2014"])

op("P03", "Rozdělení lánu, pásové střídání plodin, orientace po vrstevnici", ["P"], ["V"], 1, ["ER","Q"], ["I"], "lokalita",
   kvant=[kv("ER","hodnota","USLE P: vrstevnice 0,6 (0-4°) až 1,0 (>10°); pásové střídání okopaniny+pícniny 0,30-0,45, okopaniny+ozimy 0,50-0,90; max. délka po spádnici 120/60/40 m", rozsah=[0.3,1.0], jednotka="P faktor", zdroj=["kalkulacka_manual","janecek2012"])],
   vhodnost={"svazite_dpb": True}, vazby={"potrebuje": ["N01"], "synergie": ["P01","P02"], "konflikt": []}, povoleni=0,
   ceny=[cena("organizační opatření", 0, "Kč", 2026, None)], financovani=["vlastni"], standardy=["janecek2012","dumbrovsky2021"])

op("P04", "Půdoochranné technologie: bezorebné setí, strip-till, meziplodiny, strniště", ["P"], ["V"], 1, ["I","E","ER"], ["CH"], "lokalita",
   kvant=[kv("I","hodnota","Polní simulátor deště: orba infiltrace 27,4 mm / odtok 9,3 mm / ztráta 6,97 t/ha; setí do ozimého žita ztráta 1,95 t/ha; strip-till do TTP infiltrace 32,2 mm / odtok 4,5 mm / ztráta 0,24 t/ha (🤔 odtok -52 %, smyv -97 %)", rozsah=[0.24,6.97], jednotka="t/ha ztráta půdy", zdroj=["vopravil2025"])],
   vhodnost={"vsude": True, "zejmena": "svahy, HSP C-D"}, vazby={"potrebuje": ["N01"], "synergie": [], "konflikt": []}, povoleni=0,
   ceny=[cena("pro vlastníka smluvní", 0, "Kč", 2026, None)], financovani=["vlastni"], standardy=["dzes5_2026"],
   pozn_poctivost="DZES 5 (2026) už na SEO zakazuje erozně nebezpečné plodiny nad 2 ha a na MEO vyžaduje POT; vlastník může ve smlouvě chtít víc.")

op("P05", "Zatravnění údolnic a drah soustředěného odtoku", ["P"], ["V"], 2, ["ER","Q","I"], [], "lokalita",
   kvant=[kv("ER","vzorec","C 0,01 v dráze odtoku; min. šířka 20 m", vzorec="A_udolnice_ha = 20 m * L_m / 10000", zdroj=["dumbrovsky2021","kalkulacka_manual"])],
   vhodnost={"konkavni_profil_z_dmr": True, "akumulace_odtoku": "vysoká"}, vazby={"potrebuje": ["N02"], "synergie": ["P02"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[cena("zatravnění regionální směsí", 86600, "Kč/ha", 2024, "noo2024", pozn="údolnice 20 × 300 m = 0,6 ha ~ 52 000 Kč")], financovani=["aopk_zmv"], standardy=["dumbrovsky2021"], nedohledano=["kvantifikovaný účinek"])

op("P06", "Trvalé zatravnění nebo zalesnění svažitých a erozně ohrožených pozemků", ["P"], ["V"], 2, ["I","ER","E"], ["B","CH"], "lokalita",
   kvant=[kv("ER","vzorec","C z 0,65-0,90 na 0,01 = ztráta půdy řádově 50-90x nižší", vzorec="A_new/A_old = 0.01 / C_old", zdroj=["kalkulacka_manual"])],
   vhodnost={"sklon_min_pct": 12, "erozni_ohrozenost": ["SEO"]}, vazby={"potrebuje": ["N02"], "synergie": [], "konflikt": []}, povoleni=1, povoleni_pozn="LPIS kultura; zalesnění = souhlas orgánu ZPF 💻",
   ceny=[cena("zatravnění regionální směsí", 86600, "Kč/ha", 2024, "noo2024"), {"polozka": "ušlý pachtovní výnos", "hodnota": None, "rozsah": None, "jednotka": "Kč/ha/rok", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["vlastni","aopk_zmv"])

op("P07", "Větrolam, liniová výsadba na hranici pozemku", ["P","C"], ["V","O"], 2, ["E","ER","CH","B"], ["Q"], "lokalita",
   kvant=[kv("E","hodnota","Za olistěným větrolamem (porozita 10 %) rychlost větru v 50 m ~40 %, ve 150 m ~70 % původní; neolistěný 80/90 %; účinný dosah max. 250 m = 10-17 H", rozsah=[40,70], jednotka="% původní rychlosti", zdroj=["vumop_vitr2016"]),
          kv("E","vzorec","Chráněná plocha = délka × (10-17) × výška; nový větrolam šířka 7-20 m, rozestupy 350-600 m", vzorec="A_chranena_m2 = L_m * H_m * (10..17)", zdroj=["vumop_vitr2016","mze2022_vitr"]),
          kv("E","hodnota","Vlhkost půdy za větrolamem +102 % (jedno měření, j. Morava 2007) - neobecňovat", hodnota=102, jednotka="%", zdroj=["dufkova2007"], znacka="overeno_stare")],
   vhodnost={"orientace": "kolmo na převládající vítr", "otevrene_lany": True, "odstup_hranice_min_m": 3},
   vazby={"potrebuje": ["N02"], "synergie": ["P08","P09","Z07"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[cena("realizace Písková Lhota 1408 m², 4 řady", 198270, "Kč", 2025, "aopk_piskova", pozn="🤔 141 Kč/m²"), cena("strom s balem ok 10-12 cm", 5900, "Kč/ks", 2024, "noo2024"), cena("strom prostokořenný do 200 cm", 1775, "Kč/ks", 2025, "uur2025_zelen")],
   financovani=["aopk_zmv","ppk_b"], standardy=["vumop_vitr2016","sppk_a02_001"], nedohledano=["snížení evapotranspirace v % (ČR)"])

op("P08", "Polní cesta s doprovodnou zelení a zasakovacím příkopem", ["P","C"], ["V","O"], 3, ["E","Q","I","ER","B"], [], "lokalita",
   popis="Víceúčelové: cesta + větrolam + biokoridor + zpomalení odtoku. Účinky podle složek P01 + P07 + C01.",
   vhodnost={"po_vrstevnici_nebo_sikmo": True, "hranice_vlastniku": True}, vazby={"potrebuje": ["N02|kopu"], "synergie": ["P01","P07","C01"], "konflikt": []}, povoleni=2, povoleni_pozn="1-2",
   ceny=[cena("průleh/mez", 200, "Kč/m²", 2024, "noo2024"), {"polozka": "konstrukce cesty", "hodnota": None, "rozsah": None, "jednotka": "Kč/m", "rok": None, "zdroj": None, "pozn": "podle konstrukce, ÚÚR 2025 kap. 8; bez konkrétní položky neuvádím"}],
   financovani=["opzp_1_3_1","kopu"], standardy=["tpeo2014"])

op("P09", "Agrolesnictví: řady stromů v poli, ovocné stromy v pastvině", ["P","L"], ["V"], 2, ["E","CH","B"], ["I","ER"], "lokalita",
   kvant=[kv("CH","hodnota","V ALS průměrná teplota -0,2 až -0,8 °C/rok; v horkých dnech maxima přízemního vzduchu a povrchu půdy -4 až -5 (až 10) °C; tropické dny -1/3", rozsah=[4,10], jednotka="°C maxima", zdroj=["czu2026_als"]),
          kv("E","hodnota","Vítr ve 4 m -50 %", hodnota=50, jednotka="%", zdroj=["czu2026_als"]),
          kv("I","hodnota","Záplavové pokusy Šardice 2023-2025 (72 mm/h): odtok 0 %, zasáknutí 99 % v ALS", hodnota=99, jednotka="% zasáknutí", zdroj=["czu2026_als"])],
   vhodnost={"lany": True, "vetrne_polohy": True, "min_dpb_ha": 0.5}, vazby={"potrebuje": ["N01|N02"], "synergie": ["P07"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1 (LPIS kultura)",
   ceny=[cena("dotace zavedení ALS (pro zemědělce)", 105500, "Kč/ha", 2026, "agroles2026", pozn="4 353 EUR/ha; péče 754 EUR/ha/rok 5 let")],
   financovani=["szp_agroles"], standardy=["sppk_c02_003","agroles2026"], nedohledano=["vlhkost půdy v ALS (ČR)"])

op("P10", "Regulace nebo přerušení melioračního odvodnění", ["P","L"], ["V","O"], 2, ["R","I","B"], ["CH"], "lokalita",
   kvant=[kv("R","hodnota","Odhad snížení odtoku: regulační opatření na drenáži 50-90 %, snížení intenzity odvodnění 50-75 %, zasakovací drén 50-100 %, lokální eliminace 25-75 %", rozsah=[25,100], jednotka="% odtoku z drenáže", zdroj=["zajicek2021"])],
   vhodnost={"existujici_drenaz": "zjistit u SPÚ (bezplatně) / ISMS meliorace.vumop.cz / LPIS POZ", "misto_typ": ["zamokřené plochy"]},
   vazby={"potrebuje": ["N01|N02"], "synergie": ["T02"], "konflikt": []}, povoleni=1, povoleni_pozn="1-2",
   ceny=[cena("rušení odvodnění", 1650, "Kč/m²", 2024, "noo2024")], financovani=["aopk_zmv","opzp_1_3_1"], standardy=["zajicek2021","spu_meliorace"],
   pozn_poctivost="Podrobné odvodnění patří od 1991 vlastníkovi; 40 % vlastníků o něm neví.")

op("P11", "Remízek, drobná plocha zeleně v cípech a na neobdělatelných místech", ["P"], ["V","O"], 1, ["B","E","CH"], ["I"], "pozemek",
   kvant=[kv("B","kvalitativne","Útočiště, biokoridor", znacka="odhad")],
   vhodnost={"misto_typ": ["neobdělatelné cípy","mokřiny","kamenité plochy"]}, vazby={"potrebuje": ["N02"], "synergie": ["P07"], "konflikt": []}, povoleni=0,
   ceny=[cena("sazenice stromů", None, "Kč/ks", 2025, "uur2025_zelen", rozsah=[1775,6100]), cena("keř prostokořenný", 190, "Kč/ks", 2024, "noo2024")], financovani=["ppk_b","aopk_zmv"])

op("P12", "Zvyšování organické hmoty v půdě (hnůj, kompost, zelené hnojení)", ["P"], ["V"], 1, ["I","R"], ["ER","E"], "lokalita",
   kvant=[kv("R","hodnota","Tvrzení VÚMOP (Hladík, bez citace): 1 % organické hmoty = +35 000 l/ha retence - v aplikaci jen jako odhad", hodnota=35000, jednotka="l/ha na 1 % OH", zdroj=["hladik_pot"], znacka="odhad")],
   vhodnost={"vsude": True}, vazby={"potrebuje": ["N01"], "synergie": ["P04"], "konflikt": []}, povoleni=0, ceny=[cena("smluvní", 0, "Kč", 2026, None)], financovani=["vlastni"])

# ===== L louka a pastvina
op("L01", "Mozaiková nebo pozdní seč, ponechané pásy", ["L"], ["V","O"], 1, ["E","CH","B"], [], "lokalita",
   kvant=[kv("B","hodnota","Viz U06 (Chytrá a kol. 2024)", rozsah=[20,34], jednotka="% druhů", zdroj=["chytra2024"])],
   vhodnost={"vsude": True}, vazby={"potrebuje": [], "synergie": [], "konflikt": []}, povoleni=0,
   ceny=[cena("seč lehkou mechanizací", 17425, "Kč/ha", 2024, "noo2024")], financovani=["ppk_b","vlastni"], standardy=["sppk_d02_004"])

op("L02", "Extenzivní rotační pastva, omezení přepásání a sešlapu", ["L"], ["V"], 1, ["I","ER","B"], [], "lokalita",
   kvant=[kv("I","hodnota","Citace v metodice VÚMOP (zahraniční 📄): pokles infiltrace o 40-80 % v 5-20 cm při utužení; povrchový odtok 53 % srážky na přepaseném svahu vs. 5 % na zatravněném; nepást podél toků a nad 17 % sklonu", rozsah=[5,53], jednotka="% odtoku", zdroj=["fucik2015_pastva"], znacka="citace")],
   vhodnost={"pastviny": True, "sklon_max_pct": 17, "ne_podel_toku": True, "zatizeni_vdj_ha": [0.2,1.5]}, vazby={"potrebuje": [], "synergie": ["L03","L04"], "konflikt": []}, povoleni=0,
   ceny=[cena("pevné oplocení (ohrada)", 138, "Kč/m", 2024, "noo2024")], financovani=["ppk_b","vlastni"], standardy=["sppk_d02_003","fucik2015_pastva"], nedohledano=["české měření extenzivní vs. intenzivní"])

op("L03", "Solitérní stromy a skupiny v pastvině", ["L"], ["V"], 1, ["CH","E","B"], [], "pozemek",
   kvant=[kv("CH","hodnota","Stín -11 až -25 °C povrch (EPA)", rozsah=[11,25], jednotka="°C", zdroj=["epa2008_trees"], znacka="overeno_stare")],
   vhodnost={"vsude": True}, vazby={"potrebuje": [], "synergie": ["L02"], "konflikt": []}, povoleni=0,
   ceny=[cena("strom prostokořenný do 200 cm", 1775, "Kč/ks", 2025, "uur2025_zelen"), cena("tubus individuální ochrana do 170 cm", 176, "Kč/ks", 2024, "noo2024"), cena("oplocenka drátěná 160 cm", 180, "Kč/m", 2024, "noo2024")],
   financovani=["ppk_b","aopk_zmv"], standardy=["sppk_c02_003"], pozn_poctivost="SPPK C02 003: při pastvě povinný ochranný plášť, 3 kůly, ochrana min. 10 let.")

op("L04", "Ochrana pramenišť a mokřin v loukách před sešlapem, obnova", ["L","T"], ["V","O"], 1, ["R","B"], ["I"], "pozemek",
   kvant=[kv("R","kvalitativne","Hydrologická role pramenišť - český zdroj nedohledán", znacka="odhad")],
   vhodnost={"pramenisete_z_dat": "akumulace odtoku + zamokření"}, vazby={"potrebuje": [], "synergie": ["T05","L02"], "konflikt": []}, povoleni=0,
   ceny=[cena("oplocenka drátěná 160 cm", 180, "Kč/m", 2024, "noo2024")], financovani=["ppk_b","vlastni"], nedohledano=["návod k oplocení pramenišť na pastvině"])

# ===== LES
op("LES01", "Lesní tůně a přehrážky v lesních stržích (dřevěné, kamenné)", ["LES","C"], ["SP","V","O"], 2, ["Q","R","ER"], ["I","B"], "lokalita",
   kvant=[kv("R","vzorec","Objem zdrže ~ plocha × výška / 2 (klín) - odhad, retence na přehrážku nedohledána", vzorec="V_m3 = A_zdrze_m2 * h_m / 2", znacka="odhad")],
   vhodnost={"strze_z_dmr": True, "lesni_cesty": True}, vazby={"potrebuje": ["N06"], "synergie": ["C02","LES02"], "konflikt": []}, povoleni=1, povoleni_pozn="souhlas vlastníka/LČR; v korytě § 17 a § 46 vodního zákona",
   ceny=[cena("jednoduchá přehrážka", 10000, "Kč/ks", 2024, "noo2024"), cena("složitá přehrážka (dvojitá, perodrážka)", 38500, "Kč/ks", 2024, "noo2024"), cena("LČR Černý potok ve Strání: 800 m, 8 objektů", 2400000, "Kč bez DPH", 2025, "lcr_strani", pozn="🤔 ~3 000 Kč/m")],
   financovani=["aopk_zmv","opzp_1_3_1"], standardy=["mze2020_bystriny","vyhl239_2017"], nedohledano=["retence m³ na přehrážku"],
   pozn_poctivost="MZe TD 2020: přehrážky běžně 2-5 m; drobné svépomocné prahy jsou pod úrovní normy.")

op("LES02", "Odvodnění lesních cest a svážnic do lesa, ne do strží (svodnice, příčné prahy)", ["LES","C"], ["SP","V"], 1, ["ER","I","Q"], [], "lokalita",
   kvant=[kv("ER","kvalitativne","Svodnice povinné při podélném sklonu >6 %; min. příčný sklon 3-3,5 %; propustek min. 510 mm", znacka="overeno")],
   vhodnost={"svahove_cesty": True, "sklon_min_pct": 6}, vazby={"potrebuje": ["N06"], "synergie": ["LES01"], "konflikt": []}, povoleni=1,
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["vyhl239_2017"], nedohledano=["rozestupy svodnic (ČSN 73 6108)"])

op("LES03", "Druhově pestrý les, přirozená obnova, mrtvé dřevo a humus", ["LES"], ["V","SP"], 3, ["B"], ["I","E","CH"], "uzemi", kontext=True,
   kvant=[kv("I","hodnota","Česká data (Liz, 22 let): v suchých letech smrk propouští do podloží o ~15 % více vody než buk; průměrně se půdní voda pod porosty neliší. Tvrzení 'listnatý les zadrží víc vody' se nepoužije.", hodnota=15, jednotka="% perkolace (smrk > buk)", zdroj=["avcr2023_liz"]),
          kv("I","hodnota","Intercepce: buk 30 %, smíšený buk-dub 21 % srážek (📄 citace)", rozsah=[21,30], jednotka="%", zdroj=["hemr2023"], znacka="citace")],
   vhodnost={"lvs_chriby": "2. LVS 36 %, 3. LVS 60 % (PLO 36)", "vrstva": "NLI OPRL Lesni_vegetacni_stupne"}, vazby={"potrebuje": ["N06"], "synergie": ["LES04"], "konflikt": []}, povoleni=1, povoleni_pozn="LHP",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["avcr2023_liz","czu2011_plo36"], pozn_poctivost="Přínos smíšeného lesa formulovat jako odolnost porostu (kůrovec, vítr), ne jako vodní bilanci.")

op("LES04", "Lesní okraj s keřovým pláštěm (ekoton)", ["LES","P"], ["V","O"], 1, ["E","B","CH"], [], "lokalita",
   kvant=[kv("E","kvalitativne","Mikroklima lesního okraje nekvantifikováno", znacka="odhad")],
   vhodnost={"hranice_les_pole": True}, vazby={"potrebuje": [], "synergie": ["P07"], "konflikt": []}, povoleni=0,
   ceny=[cena("keř prostokořenný do 60 cm", 190, "Kč/ks", 2024, "noo2024")], financovani=["ppk_b","vlastni"], standardy=["sppk_a02_003"])

# ===== T tok, niva, prameniště
op("T01", "Tůň v nivě (bez fólie), soustava tůní, obnova zazemněné tůně", ["T"], ["V","O","SP"], 2, ["R","CH","B"], ["I","Q"], "lokalita",
   kvant=[kv("R","vzorec","Objem = plocha × průměrná hloubka 0,8-1,0 m", vzorec="V_m3 = A_m2 * (0.8..1.0)", zdroj=["sppk_b02_001"])],
   vhodnost={"niva": True, "hladina_pv_melko": True, "hsp": ["C","D"]}, vazby={"potrebuje": [], "synergie": ["T02","T06"], "konflikt": []}, povoleni=1, povoleni_pozn="0-2 podle velikosti a vzdálenosti od toku (§ 15b, § 55)",
   ceny=[cena("tůň strojně, materiál v lokalitě", 330, "Kč/m² hladiny", 2024, "noo2024"), cena("terénní sníženiny v nivě", 330, "Kč/m²", 2024, "noo2024"), cena("odbahnění", 430, "Kč/m³", 2024, "noo2024")],
   financovani=["aopk_zmv","ppk_b","opzp_1_3_1"], standardy=["sppk_b02_001","vz_15b","vz_55"])

op("T02", "Mokřad, zamokření nivy přerušením odvodnění", ["T"], ["V","O"], 2, ["R","CH","B"], ["I","Q"], "lokalita",
   kvant=[kv("R","hodnota","Regulace/eliminace drenáže snižuje odtok o 25-90 %", rozsah=[25,90], jednotka="%", zdroj=["zajicek2021"])],
   vhodnost={"odvodnene_nivy": True}, vazby={"potrebuje": [], "synergie": ["P10","T01"], "konflikt": []}, povoleni=1, povoleni_pozn="1-2",
   ceny=[cena("rušení odvodnění", 1650, "Kč/m²", 2024, "noo2024"), cena("sníženiny v nivě", 330, "Kč/m²", 2024, "noo2024")], financovani=["aopk_zmv","opzp_1_3_1"], standardy=["zajicek2021"])

op("T03", "Mrtvé dřevo a dřevní přehrážky v korytě drobného toku (leaky dams)", ["T"], ["SP","V"], 1, ["Q","R","B"], [], "lokalita",
   kvant=[kv("Q","hodnota","Model (1 přehrážka, povodí 2 km²): průtok -31 % při 6h dešti 1/10 let se sedimentem, -3,1 % bez; empirie 📄: kulminace 1leté povodně nižší v průměru o 10 %, velká variabilita. Zahraniční; český zdroj nedohledán.", rozsah=[3,31], jednotka="% průtoku", zdroj=["wolstenholme2024"]),
          kv("B","kvalitativne","Říční dřevo nutné pro přírodě blízký stav (AOPK 2020)", zdroj=["aopk2020_toky"])],
   vhodnost={"drobne_toky_mimo_intravilan": True, "bez_ohrozeni_staveb": True}, vazby={"potrebuje": ["N06"], "synergie": ["T04"], "konflikt": ["intravilán","mosty a propustky"]},
   povoleni=2, povoleni_pozn="§ 46 zakazuje ukládat do toku předměty ohrožující odtok; § 17 souhlas vodoprávního úřadu; vždy dohoda se správcem toku - nikdy svépomoc bez ptání",
   ceny=[NEOVERENA], financovani=["vlastni","aopk_zmv"], standardy=["aopk2020_toky","vz_17_46_47"], nedohledano=["český kvantifikovaný zdroj"])

op("T04", "Revitalizace drobného toku (odstranění opevnění, rozvlnění, snížení břehů)", ["T"], ["SP","O"], 3, ["Q","R","B","CH"], [], "uzemi", kontext=True,
   kvant=[kv("R","kvalitativne","Měřený efekt na vlnu v ČR nedohledán; AOPK 2020 kvalitativně. Příklad rozsahu: Zdoňovsko (předběžná studie) +697 495 m³ zádrže, +58,8 ha mokřadů, 25,7 km toků", zdroj=["aopk2020_toky","zivavoda2018"], znacka="overeno_stare")],
   vhodnost={"naprimene_useky": "porovnání s II./III. vojenským mapováním"}, vazby={"potrebuje": ["N06"], "synergie": ["T01","T03","T06"], "konflikt": []}, povoleni=2,
   ceny=[cena("revitalizace koryta drobného toku", 1200, "Kč/m²", 2024, "noo2024"), cena("revitalizace významného toku", 1650, "Kč/m²", 2024, "noo2024")],
   financovani=["opzp_1_3_1","aopk_zmv"], standardy=["aopk2020_toky"], nedohledano=["SPPK kód pro revitalizace","měřený efekt (ČR)"])

op("T05", "Obnova prameniště, studánky, ochrana před sešlapem a splachy", ["T","L","LES"], ["J","V","S","O"], 1, ["R","B"], [], "pozemek",
   kvant=[kv("R","kvalitativne","Hydrologická role pramenišť - český zdroj nedohledán", znacka="odhad")],
   vhodnost={"pramenisete_z_dat": True, "teren": True}, vazby={"potrebuje": [], "synergie": ["L04","M04"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1; souhlas vlastníka; studánka typicky není vodní dílo (§ 55 odst. 3, 🤔 výklad)",
   ceny=[NEOVERENA], financovani=["vlastni","ppk_b"], standardy=["studanky2025"], pozn_poctivost="Nezasahovat do jímek; prameniště/mokřad neupravovat na studánku; registr estudanky.eu.")

op("T06", "Břehové porosty podél toku a kolem nádrží", ["T"], ["V","O","SP"], 1, ["CH","E","ER","B"], [], "lokalita",
   kvant=[kv("CH","hodnota","Stíněné úseky: max. teplota vody o 2,2-3,5 °C nižší; nestíněné oteplení až +3,9 °C; denní amplituda až o 4 °C nižší; doporučeno >40 % husté vegetace (Rakousko)", rozsah=[2.2,3.9], jednotka="°C teplota vody", zdroj=["kalny2017","trimmel2018"])],
   vhodnost={"nezastinene_useky": True}, vazby={"potrebuje": ["N06"], "synergie": ["T01"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1; § 47 správce udržuje porosty",
   ceny=[cena("keř prostokořenný do 60 cm", 190, "Kč/ks", 2024, "noo2024"), cena("špičák 80-125 cm", 1055, "Kč/ks", 2024, "noo2024"), cena("strom ok 6-8 prostokořenný", 2245, "Kč/ks", 2024, "noo2024"), cena("následná péče strom", 725, "Kč/ks/rok", 2024, "noo2024")],
   financovani=["aopk_zmv","ppk_b"], standardy=["sppk_a02_001"], nedohledano=["SPPK kód břehové porosty","český zdroj teploty vody"])

op("T07", "Malá vodní nádrž, suchý poldr, rybník", ["T"], ["O","SP"], 3, ["R","Q"], ["B","CH"], "uzemi", kontext=True,
   kvant=[kv("R","vzorec","Objem z DMR při zvolené hrázi (jádro aplikace)", vzorec="V = sum(h_hraz - z_dmr) * dx*dy pro z < h_hraz")],
   vhodnost={"profil_z_dmr": True}, vazby={"potrebuje": ["N06"], "synergie": [], "konflikt": []}, povoleni=2,
   ceny=[NEOVERENA], financovani=["opzp_1_3_1"], standardy=["tnv752415"], nedohledano=["Kč/m³ retence z realizací 2024-2026"], pozn_poctivost="Dřívější údaj o ceně poldru/hráze se nepotvrdil a byl vyřazen.")

# ===== C cesta, svah, strž
op("C01", "Zasakovací příkopy a svodnice u cest, odvedení vody do průlehů místo do toku", ["C"], ["O","V"], 1, ["I","Q","ER"], [], "lokalita",
   kvant=[kv("R","vzorec","Objem = délka × průřez; příkop dno 0,3-0,6 m, hloubka 0,6-1,2 m, svahy 1:1,5-1:2; průleh svahy ≤1:5, jen do 10 % sklonu", vzorec="V_m3 = L_m * S_m2", zdroj=["tpeo2014"], znacka="overeno_stare")],
   vhodnost={"svahove_cesty": True, "sklon_max_pct_pruleh": 10}, vazby={"potrebuje": [], "synergie": ["U03","P08"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[cena("průlehy a meze s terénními úpravami", 200, "Kč/m²", 2024, "noo2024"), {"polozka": "příkop", "hodnota": None, "rozsah": None, "jednotka": "Kč/m", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["kopu","aopk_zmv"], standardy=["tpeo2014"])

op("C02", "Přehrážky v erozních rýhách a stržích (kámen, dřevo, proutí)", ["C","LES"], ["V","O","S"], 1, ["ER","Q"], ["R","I"], "pozemek",
   kvant=[kv("ER","kvalitativne","Efekt drobných přehrážek na sediment nedohledán; příbuzná technika silt-fence zachytí >84 % erodovaného materiálu", hodnota=84, jednotka="% (silt-fence)", zdroj=["vumop2020_siltfence"])],
   vhodnost={"ryhy_z_dmr_a_terenu": True, "mimo_koryto_toku": True}, vazby={"potrebuje": [], "synergie": ["LES01","M06"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1 mimo koryto",
   ceny=[cena("jednoduchá přehrážka", 10000, "Kč/ks", 2024, "noo2024"), cena("silt-fence instalace", 8146, "Kč/100 m", 2020, "vumop2020_siltfence")], financovani=["vlastni","aopk_zmv"], standardy=["mze2020_bystriny"])

op("C03", "Zatravnění a výsadba na svazích, terasování starých úvozů", ["C"], ["V","O"], 2, ["ER","I","E"], [], "lokalita",
   kvant=[kv("ER","vzorec","USLE C 0,01 pro travní porost; terasy stupeň max. 8 m (optimum 6 m), svah 1:1 do 1,5 m", vzorec="A_new/A_old = 0.01 / C_old", zdroj=["kalkulacka_manual","tpeo2014"])],
   vhodnost={"sklon_min_pct": 15}, vazby={"potrebuje": [], "synergie": ["P06"], "konflikt": []}, povoleni=0, povoleni_pozn="0-1",
   ceny=[cena("trávník luční", 40, "Kč/m²", 2025, "uur2025_zelen"), cena("založení trávníku", 33.5, "Kč/m²", 2024, "noo2024"), cena("založení trávníku s modelací", 81.5, "Kč/m²", 2024, "noo2024", pozn="příplatek svah 15-30 % +20 %, >30 % +30 %")],
   financovani=["vlastni","aopk_zmv"], standardy=["tpeo2014"], nedohledano=["hydroosev Kč/m² 2025"])

# ===== M měření (podpůrná)
for mid, nazev, ucel, syn in [
    ("M01","Srážkoměr (jednoduchý, denní odečet)","základ pro bilanci a validaci",["*"]),
    ("M02","Hladina ve studních (měsíční odečet, síť dobrovolníků)","indikátor podzemní vody",[]),
    ("M03","Vlhkost půdy (jednoduché čidlo nebo gravimetricky)","validace účinku opatření",["Z05","P04"]),
    ("M04","Stav drobných toků a pramenišť (fotomonitoring, teče/neteče; registr estudanky.eu)","validace, argumentace",["T05","L04"]),
    ("M05","Teplota povrchů IR teploměrem (asfalt, tráva, tmavá vs. světlá střecha)","ukázka účinku CH",["Z06","S04","Z04"]),
    ("M06","Mapování erozních rýh po přívalu","lokalizace C02, P05",["C02","P05"])]:
    op(mid, nazev, ["U","Z","L","T","C"], ["S","J"], 1, [], [], "pozemek", popis=ucel,
       vazby={"potrebuje": [], "synergie": syn, "konflikt": []}, povoleni=0, povoleni_pozn="souhlas vlastníka pozemku", ceny=[NEOVERENA], financovani=["vlastni","participativni"])

# ===== N nástroje
NASTROJE = [
 {"id":"N01","nazev":"Pachtovní smlouva s půdoochrannými podmínkami","rozhoduje":["V"],"umoznuje":["P03","P04","P12","P01","P09"],
  "parametry":"OZ § 2345 zemědělský pacht; § 2336 pachtýř pečuje jako řádný hospodář; § 2334 změna hospodářského určení jen se souhlasem propachtovatele; pachtovní rok 1. 10. - 30. 9. Půdoochranné podmínky ve smlouvě: OZ dispozitivní, smluvně možné 🤔 (právní výklad neověřen).","zdroj":["oz_pacht"]},
 {"id":"N02","nazev":"Vyjmutí pozemku nebo jeho části z pachtu","rozhoduje":["V"],"umoznuje":["P01","P05","P06","P07","P08","P09","P10","P11"],
  "parametry":"§ 2347: pacht na dobu neurčitou lze vypovědět v 12měsíční výpovědní době; u doby určité podle smlouvy.","zdroj":["oz_pacht"]},
 {"id":"N03","nazev":"Směna nebo koupě pozemku v klíčové poloze (údolnice, niva)","rozhoduje":["V","O"],"umoznuje":["T01","T02","P05"],"parametry":None,"zdroj":[]},
 {"id":"N04","nazev":"Žádost o komplexní pozemkové úpravy","rozhoduje":["V","O"],"umoznuje":["P01","P02","P08","C01"],
  "parametry":"Zák. 139/2002 § 6 odst. 3: pozemkový úřad zahájí řízení vždy, pokud se vysloví vlastníci nadpoloviční výměry zemědělské půdy v k.ú.; formulář SPÚ. KoPÚ v Koryčanech neproběhly.","zdroj":["zak139_2002","spu_kopu_form"]},
 {"id":"N05","nazev":"Dotace a programy","rozhoduje":["J","V","O","S"],"umoznuje":["*"],"parametry":"viz číselník programy","zdroj":[]},
 {"id":"N06","nazev":"Dohoda se správcem toku (Povodí Moravy) nebo lesa (LČR)","rozhoduje":["O","SP"],"umoznuje":["T03","T04","T06","T07","LES01","LES02","LES03"],
  "parametry":"Vodní zákon § 17 (souhlas vodoprávního úřadu), § 46 (zákaz zásahů do koryta), § 47 (povinnosti správce) - ověřit znění v e-Sbírce.","zdroj":["vz_17_46_47"]},
]

CISELNIKY = {
 "misto": {"Z":"zahrada, dvůr","S":"střecha, stavba","U":"veřejný prostor obce","P":"orná půda","L":"louka, pastvina","LES":"les","T":"tok, niva, prameniště","C":"cesta, svah, strž"},
 "rozhoduje": {"J":"jednotlivec na svém pozemku","V":"vlastník půdy (přes pacht N01 nebo vyjmutí N02)","O":"obec","SP":"správce toku/lesa (Povodí Moravy, LČR)","S":"škola","zemedelec":"uživatel DPB (jen pro SZP dotace)"},
 "pracnost": {"1":"víkend a ruce","2":"dny až týdny, malá technika","3":"projekt + firma"},
 "ucinek": {"R":"zadržení objemu","I":"infiltrace do půdy","Q":"zpomalení odtoku","E":"omezení neproduktivního výparu / větru","CH":"ochlazení mikroklimatu","ER":"protierozní","B":"biodiverzita","W":"šetření pitnou vodou"},
 "meritko": {"pozemek":"účinek na pozemku + příspěvek do součtu","lokalita":"ulice, lán, úsek toku","uzemi":"povodí; kontextová opatření"},
 "povoleni": {"0":"nic","1":"ohlášení / souhlas vlastníka či správce","2":"vodoprávní nebo stavební řízení"},
 "znacka": {"overeno":"✅ ověřeno online v uvedený den","overeno_stare":"✅⏳ ověřeno, zdroj starší 12 měsíců","citace":"📄 doložený zdroj, originál nečten","odhad":"🤔 odhad bez zdroje","pamet":"💻 z paměti, neověřeno"},
 "kvantifikace_typ": {"vzorec":"jádro počítá z parametrů","hodnota":"doložená konstanta nebo rozsah","kvalitativne":"bez čísla, zobrazit slovně"},
}

DATA = {
 "meta": {"nazev":"Katalog opatření - Koryčany resilience","verze":"0.4","datum":DNES,"licence_dat":"CC BY 4.0 (vlastní kompilace; citované zdroje mají vlastní licence)",
          "upozorneni":"Zjednodušený osvětový model, ne projektová dokumentace. Každé číslo má zdroj a značku původu. Ceny jen se zdrojem a datem; jinak 'cena neověřena'. Paragrafy vodního zákona ověřit v e-Sbírce.",
          "zdroje_md":["claude/KATALOG.md","claude/KATALOG-Z-S.md","claude/KATALOG-U-P.md","claude/KATALOG-L-LES-T-C.md"]},
 "ciselniky": CISELNIKY, "konstanty": KONSTANTY, "zdroje": Z, "programy": PROGRAMY, "nastroje": NASTROJE, "opatreni": O,
}

# ----------------------------------------------------------------- kontroly
ids = [o["id"] for o in O]
assert len(ids) == len(set(ids)), "duplicitní ID"
for o in O:
    for k in o["kvantifikace"]:
        for zid in (k["zdroj"] or []):
            assert zid in Z, f"{o['id']}: neznámý zdroj {zid}"
    for c in o["ceny"]:
        if c["zdroj"]: assert c["zdroj"] in Z, f"{o['id']}: neznámý zdroj ceny {c['zdroj']}"
    for f in o["financovani"]:
        assert f in PROGRAMY, f"{o['id']}: neznámý program {f}"
    for s in o["standardy"]:
        assert s in Z, f"{o['id']}: neznámý standard {s}"
    for v in o["vazby"]["potrebuje"] + o["vazby"]["synergie"]:
        for alt in v.split("|"):
            assert alt == "*" or alt in ids or alt in [n["id"] for n in NASTROJE] or alt in PROGRAMY, f"{o['id']}: neznámá vazba {alt}"

with open(os.path.join(OUT,"opatreni.json"),"w",encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)

SCHEMA = {
 "$schema":"https://json-schema.org/draft/2020-12/schema","title":"Katalog opatření Koryčany resilience","type":"object",
 "required":["meta","ciselniky","konstanty","zdroje","programy","nastroje","opatreni"],
 "properties":{
  "zdroje":{"type":"object","additionalProperties":{"type":"object","required":["id","nazev","znacka"],"properties":{"id":{"type":"string"},"nazev":{"type":"string"},"url":{"type":["string","null"]},"rok":{"type":["integer","null"]},"znacka":{"enum":["overeno","overeno_stare","citace","odhad","pamet"]},"overeno_dne":{"type":["string","null"]},"pozn":{"type":["string","null"]}}}},
  "programy":{"type":"object","additionalProperties":{"type":"object","required":["nazev","zadatel","stav"],"properties":{"stav":{"enum":["vzdy","otevreno","uzavreno","ukonceno","nastroj","zavisi_na_obci"]}}}},
  "opatreni":{"type":"array","items":{"type":"object",
    "required":["id","nazev","misto","rozhoduje","pracnost","ucinky","meritko","kontext","kvantifikace","vhodnost","vazby","povoleni","ceny","financovani"],
    "properties":{
      "id":{"type":"string","pattern":"^(Z|S|U|P|L|LES|T|C|M)[0-9]{2}$"},
      "misto":{"type":"array","items":{"enum":["Z","S","U","P","L","LES","T","C"]}},
      "rozhoduje":{"type":"array","items":{"enum":["J","V","O","SP","S"]}},
      "pracnost":{"type":"integer","minimum":1,"maximum":3},
      "ucinky":{"type":"object","properties":{"primarni":{"type":"array","items":{"enum":["R","I","Q","E","CH","ER","B","W"]}},"vedlejsi":{"type":"array","items":{"enum":["R","I","Q","E","CH","ER","B","W"]}}}},
      "meritko":{"enum":["pozemek","lokalita","uzemi"]},
      "kvantifikace":{"type":"array","items":{"type":"object","required":["ucinek","typ","popis","znacka"],"properties":{"typ":{"enum":["vzorec","hodnota","kvalitativne"]},"znacka":{"enum":["overeno","overeno_stare","citace","odhad","pamet"]},"zdroj":{"type":["array","null"],"items":{"type":"string"}}}}},
      "povoleni":{"type":["integer","null"],"minimum":0,"maximum":2},
      "ceny":{"type":"array","items":{"type":"object","required":["polozka","jednotka"],"properties":{"hodnota":{"type":["number","null"]},"rozsah":{"type":["array","null"]},"rok":{"type":["integer","null"]},"zdroj":{"type":["string","null"]}}}},
      "vahy_skaly":{"type":["object","null"],"description":"rezervováno: sucho, prival, vedro, vitr_mraz, biodiverzita 0-3 (NAPADY-ROZHRANI.md)"}
    }}}
 }
}
with open(os.path.join(OUT,"opatreni.schema.json"),"w",encoding="utf-8") as f:
    json.dump(SCHEMA, f, ensure_ascii=False, indent=1)

print("opatreni:", len(O), "zdroje:", len(Z), "programy:", len(PROGRAMY))
print("ceny neověřené:", sum(1 for o in O for c in o["ceny"] if c["hodnota"] is None and c["rozsah"] is None))
print("kvantifikace celkem:", sum(len(o["kvantifikace"]) for o in O), "z toho kvalitativně:", sum(1 for o in O for k in o["kvantifikace"] if k["typ"]=="kvalitativne"))
