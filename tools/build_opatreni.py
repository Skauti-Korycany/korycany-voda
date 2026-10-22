# -*- coding: utf-8 -*-
"""Sestaví data/opatreni.json pro aplikaci Koryčany resilience z katalogu (docs/KATALOG*.md).
Spustit z libovolné složky: python tools/build_opatreni.py  -> data/opatreni.json, data/opatreni.schema.json
Zdroj pravdy je tento skript; MD soubory v projektu jsou dokumentace.
"""
import json, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data")
os.makedirs(OUT, exist_ok=True)

DNES = "2026-10-22"

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

# --- blok B rešerše dobré praxe, 21. 10. 2026 (docs/KATALOG-RESERSE.md)
zdroj("az1911_2021", "University of Arizona Extension AZ1911, Nickel & Brischke: Irrigating with Ollas (5/2021); cituje Ezekiel a kol. 2017", "https://extension.arizona.edu/sites/default/files/2024-08/az1911-2021.pdf", 2021, "overeno", "aridní klima; úspora 60-70 % je citace 📄 z pokusu s kukuřicí")
zdroj("oyas_bxl", "Oyas (Brusel), podklad pro zakázku obce Ixelles, bilance sezóny 2023", "https://environnement.brussels/media/15711/download", 2023, "overeno", "údaje výrobce, studie nejmenovány; pozorování obce po 1 sezóně")
zdroj("roeschwoog2022", "Neozone 24. 5. 2022 (podle France 3): obec Roeschwoog (Alsasko) zkouší oyas v záhonu před radnicí", "https://www.neozone.org/ecologie-planete/un-village-alsacien-utilise-la-technique-ancestrale-des-jarres-enterrees-oyas-pour-economiser-leau-de-ses-jardins", 2022, "overeno", "bez měření úspory vody")
zdroj("felixova2025_olla", "Felixová M., Záhrada.sk 15. 4. 2025: fotopostup výroby olly ze dvou květináčů", "https://www.zahrada.sk/magazine/fotopostup-ako-si-doma-vyrobit-zavlazovacie-nadoby-olla/", 2025, "overeno", "archivní kopie fotek: tools/stahni_zdroje.py (mimo git)")
zdroj("lwg_misch2021", "LWG Veitshöchheim, Staudenmischpflanzungen (vydání 2021)", "https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf", 2021, "overeno")
zdroj("lwg_klimabaeume2019", "LWG Veitshöchheim, Schönfeld: Zukunft Klimabäume, projekt Stadtgrün 2021 (7. 4. 2019)", "https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/zukunft_klimabaeume.pdf", 2019, "overeno_stare")
zdroj("lwg_versickern2010", "LWG Veitshöchheim, Mit Pflanzen versickern, 2. vyd. 2010 (Schwarz, Eppel, Eppel-Hotz)", "https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/merkblatt_mit_pflanzen_versickern.pdf", 2010, "overeno_stare")
zdroj("lfu_mulden2023", "LfU Bayern / TU München / HSWT / Bodeninstitut Prügl: multifunkční vsakovací mulda, závěrečná zpráva (projekt 2020-2023)", "https://www.cee.ed.tum.de/fileadmin/w00cbe/sww/_my_direct_uploads/LfU_Kurzdarstellung_2023_Versickerungsmulden.pdf", 2023, "overeno", "rok vydání v dokumentu neuveden")
zdroj("lakhi2025", "Lakhi N. 2025, Open Universiteit (diplomová práce): ozelenění soukromých zahrad a povodně, Leeuwarden", "https://research.ou.nl/en/studentTheses/the-impact-of-greening-measures-for-private-gardens-on-flood-prev/", 2025, "overeno", "3 zahrady, infiltrometr + Horton; modelované hodnoty")
zdroj("hoyk2024", "Hoyk, Szórát, Farkas 2024: Role of rain gardens in stormwater management (Kecskemét)", "https://regscience.hu/items/3845b111-d508-4224-b71a-1ddfbe631ffe", 2024, "overeno", "jen abstrakt, bez čísel")
zdroj("bratislava_com", "Covenant of Mayors, případová studie Bratislava: dotace domácnostem na hospodaření se srážkovou vodou 2016-2020", "https://eu-mayors.ec.europa.eu/sites/default/files/2022-10/EN_case%20study_Bratislava.pdf", 2022, "overeno", "účinek neměřen")
zdroj("steenbreek_sponstuin", "De Urbanisten / Steenbreek: Sponstuin Rotterdam, zkušební zahrada (leták 2019)", "https://steenbreek.nl//wp-content/uploads/2019/08/20190621-sponstuin-flyer.pdf", 2019, "overeno_stare", "výsledky měření v letáku nejsou")
zdroj("nrw2005_belaege", "MUNLV NRW, FH Bochum + IKT: Prüfung wasserdurchlässiger Flächenbeläge nach mehrjähriger Betriebsdauer (2/2005)", "https://www.lanuk.nrw.de/fileadmin/forschung/wasser/sonstiges/Kurzbericht_wasserdurchl_Flaeche.pdf", 2005, "overeno_stare")
zdroj("bayern2003_entsiegelung", "Bayerischer Landesverband für Gartenbau und Landespflege + LWG: Mehr Grün durch Bodenentsiegelung (2003)", "https://mv.gartenbauvereine.org/wp-content/uploads/2020/05/MehrGruendurchBodenentsiegelung.pdf", 2003, "overeno_stare")
zdroj("hlnug2022", "HLNUG / LGB RLP, Maßnahmensteckbrief 72: Teilentsiegelung, Versickerungsbeläge (12/2022)", "https://www.hlnug.de/fileadmin/dokumente/boden/Planung/Kompboden/msb_072_teilentsiegelung_versickerungsbelaege.pdf", 2022, "overeno")
zdroj("tegelwippen2025", "BNNVARA Vroege Vogels 17. 11. 2025: NK Tegelwippen 2025, téměř 6 mil. dlaždic, celkem 20 mil.", "https://www.bnnvara.nl/vroegevogels/artikelen/nk-tegelwippen-2025-levert-bijna-6-miljoen-nieuwe-plekken-voor-natuur-op", 2025, "overeno")
zdroj("dwd_mulch", "DWD Agrarmeteorologie Lipsko (Böttcher, Schmidt): Wirkung einer Mulchbedeckung auf die Evaporation, pokusy 2012-2014", "https://www.gartenbau.sachsen.de/download/Die_Wirkung_einer_Mulchbedeckung_auf_die_Evaporation.pdf", 2014, "overeno", "rok vydání neuveden")
zdroj("igz_heistermann", "Heistermann K. (IGZ Großbeeren), Wissenschaftstagung Ökologischer Landbau: Streifenbearbeitung, Mulch und Untersaaten (pokusy 2022-2023)", "https://orgprints.org/id/eprint/53926/1/Beitrag_279_final_a.pdf", 2023, "overeno", "rok vydání neuveden")
zdroj("minasny2018", "Minasny B., McBratney A. B. 2018: Limited effect of organic matter on soil available water capacity, Eur. J. Soil Sci. 69(1):39-47 (metaanalýza 60 studií)", "https://agris.fao.org/search/en/records/65df2f3a63b8185d9cab777b", 2018, "overeno", "abstrakt a highlights; plný text neotevřen")
zdroj("blake2021", "Blake M. 2021, Toronto Metropolitan University (diplomová práce): popínavky a letní oteplování fasád", "https://rshare.library.torontomu.ca/articles/thesis/The_Potential_for_Perennial_Vines_to_Mitigate_Summer_Warming_of_an_Urban_Microclimate/14657580", 2021, "overeno", "Toronto, přísavník trojcípý, 6 měsíců")
zdroj("bayika2022", "Edelhäuser K.-J. (Bayerische Ingenieurekammer-Bau), sloupek Bayerische Staatszeitung 29. 7. 2022: Fassadenbegrünung und Stadtklima", "https://www.bayika.de/bayika-wAssets/docs/presse/standpunkte/2022-07-29.Fassadenbegruenung_und_Stadtklima_-_29-07-2022_Klaus_Juergen_Edelhaeuser.pdf", 2022, "overeno", "názorový sloupek, cituje nejmenované studie")
zdroj("byrne2020", "Byrne, Dallas, Anda, Ho 2020: Quantifying the Benefits of Residential Greywater Reuse, Water 12(8):2310", "https://www.mdpi.com/2073-4441/12/8/2310", 2020, "overeno", "3 domy u Fremantle (Austrálie)")
zdroj("nolde2026", "IVV immobilien vermieten & verwalten 5/2026: rozhovor E. Nolde (šedá voda, Berlín)", "https://www.vermieter-ratgeber.de/sites/default/files/public/data-fachartikel/IVV_2026_05_Vier-Fragen-an-Dipl_-Ing_-Erwin-Nolde_40-41.pdf", 2026, "overeno")
zdroj("csn756780", "ČSN 75 6780 Využití šedých a srážkových vod v budovách a na přilehlých pozemcích (9/2021, Z1 10/2022) - anotace tzb-info", "https://www.tzb-info.cz/normy/csn-75-6780-2021-09", 2021, "overeno", "text normy neotevřen")
zdroj("szu2022_seda", "Kožíšek, Bobková, Baudišová, Jeligová (SZÚ) 2022: Zdravotní rizika při využití recyklovaných vod v budovách, část 2 - šedé vody, Hygiena 67(4):125-133", "https://hygiena.szu.cz/pdfs/hyg/2022/04/02.pdf", 2022, "overeno")
zdroj("adapterra2022", "businessinfo.cz 2. 11. 2022: Adapterra Awards 2022 - Český soběstačný dům, ZŠ Českobrodská, Ořechov", "https://www.businessinfo.cz/clanky/adapterra-awards-2022-ocenila-sobestacny-dum-energeticky-pozitivni-skolu-i-protierozni-prvky-v-krajine/", 2022, "overeno", "bez čísel")
zdroj("ceskestavby2022_orechov", "ceskestavby.cz 2. 11. 2022: vítězné projekty Adapterra 2022 (Ořechov: 4 retenční nádrže, 3 tůně, poldr, 7 ha mokřad)", "https://www.ceskestavby.cz/clanky/sobestacny-dum-i-energeticky-pozitivni-skola-podivejte-se-vitezne-projekty-proti-zmenam-klimatu-31347.html", 2022, "overeno", "objemy a využití nádrží neuvedeny")
zdroj("mall2010", "Mall GmbH, studie trhu Regenwassernutzung 2010 (baulinks.de 9/2010)", "https://www.baulinks.de/webplugin/2010/1798.php4", 2010, "overeno_stare", "údaje výrobce, odhady")
zdroj("praha14_voda2022", "MČ Praha 14, leták Voda (2022): spotřeba domácnosti podle činností, Praha 2020", "https://www.praha14.cz/app/uploads/sites/4/2022/06/Letak-Voda-2022.pdf", 2022, "overeno", "zdroj čísel v letáku neuveden")
zdroj("madzia2019", "Madzia M. a kol. 2019: Reduction of Treated Water Use through Application of Rainwater Tanks in Households, J. Ecol. Eng. 20(9):156-161 (Bielsko-Biała)", "https://www.jeeng.net/Reduction-of-Treated-Water-Use-through-Application-of-Rainwater-Tanks-in-Households,112495,0,2.html", 2019, "overeno", "nomogram/výpočet, ne měření; vyšší srážky než Koryčany")
zdroj("csu2024_voda", "ČSÚ 2. 5. 2024: Domácnosti vodou nadále šetří - spotřeba 86,7 l/os/den (2023)", "https://csu.gov.cz/produkty/domacnosti-vodou-nadale-setri-v-prumyslu-jeji-spotreba-mirne-roste", 2024, "overeno")

# --- blok A rešerše dobré praxe (horko v obci), 21. 10. 2026
zdroj("tacr2021_horko", "TAČR, tisková zpráva 5. 8. 2021: CzechGlobe + UPOL, riziko teplotního stresu ve městech (program ZÉTA; měření Olomouc 24. 7. 2018, Brno, Ostrava, Plzeň)", "https://tacr.gov.cz/wp-content/uploads/2022/08/220805_riziko-teplotniho-stresu-ve-mestech.pdf", 2021, "overeno", "pocitová teplota; samotná metodika a mapy pro města nedohledány")
zdroj("ct24_2022_horko", "ČT24 8. 8. 2022: I trávník pomůže - doporučení CzechGlobe/UPOL pro města", "https://ct24.ceskatelevize.cz/veda/3520774-i-travnik-pomuze-vedci-pripravili-doporuceni-ktera-maji-pomoci-ceskym-mestum-zvladat", 2022, "overeno")
zdroj("zhaw2023_mlzeni", "Suter, Drossaart van Dusseldorp, Anet (ZHAW), EGU 2023: mlžení Turbinenplatz Curych, 180 trysek, měření 12. 7.-26. 9. 2022", "https://meetingorganizer.copernicus.org/EGU23/EGU23-13652.html", 2023, "overeno", "konferenční abstrakt, jedna sezóna")
zdroj("wien_coolspot", "Wien MA 20: Coolspot / Cooling Park Esterházypark (2020, projekt Tröpferlbad 2.0)", "https://www.wien.gv.at/umwelt/energie-projekt-coolspot-im-esterhazypark", 2020, "overeno", "'až 6 °C' bez metodiky")
zdroj("coollife2025_wien", "CoolLIFE / IEECP factsheet 9/2025: Urban Heat Action Plan Vienna (29 opatření, pítka, Coole Zonen, mlžení)", "https://ieecp.org/wp-content/uploads/2025/12/CoolLIFE_GoodPractices_AustriaHeatActionPlanVienna.pdf", 2025, "overeno", "jen počty, účinky neměřeny")
zdroj("rivm2026_nl", "Climate-ADAPT 18. 6. 2026: Evaluating the effectiveness of the Dutch national heatwave plan (RIVM 2024-2025)", "https://climate-adapt.eea.europa.eu/en/metadata/case-studies/evaluating-the-effectiveness-of-the-dutch-national-heatwave-plan", 2026, "overeno")
zdroj("aarau2022", "Stadt Aarau, odpověď na dotaz P. Benze 19. 9. 2022: dočasné stínící plachty", "https://www.aarau.ch/public/upload/assets/18407/2022-51%20Beantwortung%20Anfrage%20Pascal%20Benz%20%28FDP%29%2C%20Einsatz%20tempor%C3%A4rer%20Sonnensegel%20in%20Aarau.pdf", 2022, "overeno")
zdroj("enki_stromy", "Pokorný J. (ENKI Třeboň), Ratajc U.: Jak stromy chladí, poster (bez roku; citace 2001-2013)", "https://mladimyslivci.cmmj.cz/wp-content/uploads/sites/99/2025/03/Jak_stromy_chladi.pdf", None, "overeno", "IR snímky, jednotlivá měření")
zdroj("earthwatch_fr", "Earthwatch Europe / PANORAMA: Measuring the effects of trees on heat mitigation in Northern France (48 000 měření, 2 roky; aktualizace 11/2020)", "https://panorama.solutions/en/solution/measuring-effects-trees-heat-mitigation-northern-france", 2020, "overeno_stare")
zdroj("ct24_2021_eth", "ČT24 25. 11. 2021: Schwaab a kol. (ETH Curych), Nature Communications 2021, DOI 10.1038/s41467-021-26768-w - povrchová teplota se stromy vs. bez, ~300 evropských měst", "https://ct24.ceskatelevize.cz/veda/3405168-stromy-vyrazne-ochlazuji-mestske-plochy-ubrat-mohou-az-12-stupnu-ukazuje-studie", 2021, "citace", "originál neotevřen; povrch, ne vzduch")
zdroj("dach2019_lee", "Lee H. (Stuttgart), Mayer H. (Freiburg), DACH 2019: ENVI-met simulace stromů v ulicích a parcích", "https://meetingorganizer.copernicus.org/DACH2019/DACH2019-24.pdf", 2019, "overeno_stare", "model, bez čísel")
zdroj("koeniz2025", "Grolimund + Partner / ASTRA / BFH 2025: pilot světlého asfaltu Waldeggstrasse, Köniz (faktenblatt 22. 4. 2026)", "https://www.koeniz.ch/public/upload/assets/24417/260422%20faktenblatt_auswertung_pilotprojekt_waldeggstrasse.pdf", 2026, "overeno")
zdroj("stz2026_kornwestheim", "Stuttgarter Zeitung 7. 10. 2026: Kornwestheim, Silcherschule - 56,2 °C na školním dvoře, přestavba za 37 000 €", "https://www.stuttgarter-zeitung.de/lokales/ludwigsburg/hitze-in-kornwestheim-562-grad-auf-schulhof-gemessen-so-reagiert-die-stadt-jetzt-79527198.html", 2026, "overeno")
zdroj("dresden_huckepack", "ReKIS / Sachsen EuK: Montessorischule Huckepack Dresden, stavební ochrana před horkem 2025-2027", "https://rekis.hydro.tu-dresden.de/wp-content/uploads/2026/07/GPB_Steckbrief_FRL-EuK_Montessori-Huckepack_Formatvorlage-Fachbeitrag.pdf", 2026, "overeno", "v běhu, bez měření")
zdroj("adapterra2026", "businessinfo.cz 26. 8. 2026: finalisté Adapterra Awards 2026 (mj. školní zahrada Červená Voda 2 000 m²)", "https://www.businessinfo.cz/clanky/ziska-cenu-mokrad-pole-nebo-zachranarske-zakladny-o-vitezi-adapterra-awards-2026-rozhodne-i-verejnost/", 2026, "overeno")
zdroj("adapterra2023", "businessinfo.cz 2. 11. 2023: vítězové Adapterra Awards 2023 (zvl. ocenění Obnova údolní nivy řeky Kyjovky)", "https://www.businessinfo.cz/clanky/adapterra-awards-soutez-zna-viteze-ocenila-nejlepsi-ekologicke-projekty/", 2023, "overeno")
zdroj("pmo2009_korycany_cov", "Plán oblasti povodí Dyje 2009, list opatření DY100033 Koryčany - rekonstrukce ČOV (jednotná kanalizace s OK, 4 100 EO)", "https://avd.pmo.cz/pop/2009/Dyje/end/c-stav/listyopatreni/c4_06/2_ostatni/dy100033.pdf", 2009, "overeno_stare", "stav po rekonstrukci neověřen")

# --- blok C rešerše dobré praxe (veřejný prostor, škola), 22. 10. 2026
zdroj("taucha2024", "Grüner Ring Leipzig / město Taucha / IWS / KWL, 5/2024: Versickerung von Regenwasser - Untersuchungen von langjährig genutzten Mulden-Rigolen-Systemen in Taucha (BMBF StadtLandNavi)", "https://gruenerring-leipzig.de/wp-content/uploads/2024/08/broschuere-final-leseansicht-finale-26-06-2024.pdf", 2024, "overeno")
zdroj("iws2024_taucha", "IWS Leipzig (Milke), Abschlussbericht Messprogramm Mulden-Rigolen-Monitoring Taucha, 22. 1. 2024", "https://gruenerring-leipzig.de/wp-content/uploads/2024/08/eb-mrs-monitoring-taucha.pdf", 2024, "overeno", "výsledky z brožury; závěry zprávy neotevřeny celé")
zdroj("werther2005", "FH Bielefeld / I.W.A. Minden 2005: Dezentrale Versickerung in Lehmböden - Mulden-Rigolen-System im Lößlehm, Werther (2000-2005)", "https://www.lanuk.nrw.de/fileadmin/forschung/wasser/niederschlag/Abschlussberichtdezentraleversickerung.pdf", 2005, "overeno_stare")
zdroj("portico2026_jilove", "Portico / European Urban Initiative 17. 5. 2026: Nature-based rainwater retention for climate-resilient small towns (Jílové u Prahy)", "https://portico.urban-initiative.eu/urban-matchmaker/nature-based-rainwater-retention-climate-resilient-small-towns", 2026, "overeno")
zdroj("vrv2020_mocovice", "VRV a.s. 2/2020: Koncepce rozvoje vodních ploch obce Močovice (návesní rybník, jez, náhon)", "https://www.mocovice.cz/mocovice/rozvoj-obce/koncepce-rozvoje-vodnich-ploch/koncepce-rozvoje-vodnich-ploch.pdf", 2020, "overeno")
zdroj("embren2015", "Embrén B. (město Stockholm), The Stockholm System, prezentace TDAG 2015", "https://www.tdag.org.uk/uploads/4/2/8/0/4280686/22.06.15_the_stockholm_system_bjorn_embren.pdf", 2015, "overeno_stare", "bez kontrolního srovnání")
zdroj("mufuwu2024", "Zimmermann a kol. (3:0 Landschaftsarchitektur, Landschafft Wasser, BAW, Bundesgärten), MUFUWU-Stadtbaum, BMK Berichte 39/2024: Schwammstadt pro stromy, Leonhardgürtel Graz", "https://nachhaltigwirtschaften.at/resources/sdz_pdf/schriftenreihe-2024-39-mufuwu.pdf", 2024, "overeno", "kapitoly o chlazení a retenci neotevřeny celé")
zdroj("dafne_schwammstadt", "HBLFA Schönbrunn (Roth), DaFNE projekt 101466 Schwammstadt: Struktursubstrate, lysimetry a Fahrbahnnebenflächen (2019-2024)", "https://dafne.at/projekte/schwammstadt", 2024, "overeno", "jen abstrakt")
zdroj("saluz2022", "Saluz, Bleuler, Krähenbühl, Schönborn (ZHAW) 2022: Quality and suitability of fecal biochar in structurally stable urban tree substrates, Sci. Total Environ. 838:156236", "https://srv-clst-301-data66.zhaw.ch/bitstream/11475/25111/2/2022_Gion-Saluz-et-al_Science-of-the-total-enviroment.pdf", 2022, "overeno", "nádobový pokus, ne ulice")
zdroj("zelenakova_trebisov", "Zeleňáková M., Junáková N. (TU Košice): Water retention measures ... in the city of Trebišov, Slovakia (sborník MENDELU, cca 2021-2022)", "https://doi.mendelu.cz/pdfs/doi/9900/02/00.pdf", 2022, "overeno", "rok neuveden; bez měření")
zdroj("berlin_tk2023", "Berlin Treptow-Köpenick, Straßen- und Grünflächenamt: Projektsteckbrief Schulhöfe entsiegeln (stav 2/2023)", "https://berlin.de/ba-treptow-koepenick/ueber-den-bezirk/nachhaltigkeit/2023-02-13-projektsteckbrief-schulhoefe-entsiegeln.pdf", 2023, "overeno", "bez měření")
zdroj("wiesenena2009", "Sasko, Ländlicher Raum: Dorfteich Wiesenena (Gemeinde Wiedemar), renaturace požární nádrže 2008-2009", "https://www.laendlicher-raum.sachsen.de/download/Dorfteich_Wiesenena.pdf", 2018, "overeno_stare", "bez měření a nákladů")
zdroj("smocr_cehnice", "SMO ČR, příklad dobré praxe: Cehnice - retenční nádrž Třtí na Cehnickém potoce (OPŽP)", "https://www.smocr.cz/Shared/Clanky/10359/sosnova-1-retencni-nadrz-trti-na-cehnickem-potoce.pdf", None, "overeno", "rok stavby neuveden")
zdroj("kujavy2026", "Zpravodaj obce Kujavy 2/2026: Voda pro krajinu - obnova 3 tůní (nadace Hyundai, OSF); finalista Adapterra 2026", "https://pv.svkos.cz/Zpravodaj_obce_Kujavy/Zpravodaj_obce_Kujavy_2026/Zpravodaj_obce_Kujavy_2026_2.pdf", 2026, "overeno")

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
       kvant=None, vhodnost=None, vazby=None, povoleni=None, povoleni_pozn=None, ceny=None, financovani=None, standardy=None, nedohledano=None, pozn_poctivost=None,
       priklady=None, prenositelnost=None, rizika=None):
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
        "priklady": priklady or [],          # "Kde to funguje": [{kde, kdy, kdo, co, mereno, zdroj, znacka}]
        "prenositelnost": prenositelnost,    # text: kdy to v Koryčanech dává smysl a kdy ne
        "rizika": rizika,                    # text: rizika a co z opatření neplyne
        "vahy_skaly": None,  # rezervováno: {"sucho":0-3,"prival":0-3,"vedro":0-3,"vitr_mraz":0-3,"biodiverzita":0-3}
    })

def kv(ucinek, typ, popis, hodnota=None, jednotka=None, rozsah=None, vzorec=None, zdroj=None, znacka="overeno"):
    """typ: 'vzorec' (jádro počítá), 'hodnota' (doložená konstanta/rozsah), 'kvalitativne' (bez čísla)."""
    return {"ucinek": ucinek, "typ": typ, "popis": popis, "hodnota": hodnota, "jednotka": jednotka, "rozsah": rozsah, "vzorec": vzorec, "zdroj": zdroj, "znacka": znacka}

def pr(kde, co, kdy=None, kdo=None, mereno=None, zdroj=None, znacka="overeno"):
    """Příklad dobré praxe pro kartu 'Kde to funguje'. mereno: co bylo změřeno (text), None = bez měření."""
    return {"kde": kde, "kdy": kdy, "kdo": kdo, "co": co, "mereno": mereno, "zdroj": zdroj or [], "znacka": znacka}

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

op("Z12", "Zalévací hliněné nádoby v záhonu (olla, oya)", ["Z"], ["J","S"], 1, ["W","E"], ["I"], "pozemek",
   popis="Neglazovaná hliněná nádoba zakopaná po hrdlo mezi rostliny; naplní se vodou (nejlépe dešťovou z S01) a voda prosakuje stěnou přímo ke kořenům. Z povrchu půdy se nic neodpařuje, zalévá se jednou za několik dní. Středomořský princip, svépomocně ze dvou květináčů.",
   kvant=[kv("W","hodnota","Úspora vody 60-70 % proti zálivce konví (pokus s kukuřicí, aridní klima; citace v AZ1911)", rozsah=[60,70], jednotka="% vody na zálivku", zdroj=["az1911_2021"], znacka="citace"),
          kv("W","hodnota","Výrobce: úspora 50-70 %, zálivka 3x řidší (studie nejmenovány); obec Ixelles po 1. sezóně: čas zálivky zhruba poloviční", rozsah=[50,70], jednotka="% vody na zálivku", zdroj=["oyas_bxl"], znacka="citace"),
          kv("E","kvalitativne","Voda jde pod povrch, neproduktivní výpar z půdy odpadá; proti kapkové závlaze úspora zhruba nulová (AZ1911)", zdroj=["az1911_2021"], znacka="overeno")],
   vhodnost={"vsude": True, "misto_typ": ["zeleninový záhon","trvalkový záhon","truhlík","školní zahrada"], "vyloucit": ["pod dřevinami (kořeny rozbijí nádobu)","velké plochy"]},
   vazby={"potrebuje": [], "synergie": ["S01","Z05","U07"], "konflikt": []}, povoleni=0,
   ceny=[cena("svépomocně ze 2 květináčů Ø 16-18 cm + silikon", None, "Kč", 2025, None, pozn="cena neověřena; 🤔 desítky až stovky Kč")],
   financovani=["vlastni"], standardy=["felixova2025_olla"],
   priklady=[pr("Roeschwoog, Alsasko (Francie)", "pilotní záhon 12 m² před radnicí, 11 nádob po 6,5 l (cca 1 ks/m²), bez jiné zálivky; úspora času: dosud 3 půldny zálivky týdně", kdy="2022", kdo="obec", mereno=None, zdroj=["roeschwoog2022"]),
             pr("Ixelles, Brusel (Belgie)", "300 nádob ve veřejných záhonech; po sezóně 2023 čas zálivky zhruba poloviční, menší úhyn trvalek a keřů; sousední Watermael-Boitsfort dotuje domácnostem 75 % ceny do 100 €", kdy="2023", kdo="obec, parky", mereno="čas zálivky (pozorování obce, nezávisle neověřeno)", zdroj=["oyas_bxl"]),
             pr("Fotopostup výroby ze dvou květináčů (Záhrada.sk)", "2 terakotové květináče Ø 16-18 cm, otvor zalepit střepem a sanitárním silikonem, slepit okraji, zakopat 2 cm nad zem, 3-4 sazenice kolem, zakrýt miskou, namulčovat; na zimu vyjmout", kdy="2025", kdo="M. Felixová", zdroj=["felixova2025_olla"])],
   prenositelnost="Ano pro zeleninové a trvalkové záhony, školní zahradu (U07) a truhlíky; nezávisí na půdě ani sklonu. Nehodí se pod stromy a keře a na velké plochy.",
   rizika="Úspora platí proti zálivce na povrch, ne proti kapkové závlaze. Póry se zanášejí solemi z tvrdé vody; sazenice prvních cca 4 týdny zalévat navíc; na zimu vyprázdnit nebo vyjmout 🤔. Neřeší vsak ani odtok, jen šetří vodu.",
   nedohledano=["měření v ČR nebo střední Evropě","interval dolévání (l/den) pro naše klima","trvanlivost přes zimu"],
   pozn_poctivost="Čísla úspory jsou z aridního pokusu a od výrobce; v našem klimatu neměřeno. Zobrazovat jako citaci, ne jako jistotu.")

op("Z13", "Suchomilný záhon (stepní, štěrkový): trvalky místo zalévaného trávníku a letniček", ["Z","U"], ["J","O","S"], 2, ["W","E","B"], ["CH"], "pozemek",
   popis="Záhon trvalek a trav ze stepních a suchých stanovišť v propustném substrátu s minerálním mulčem (štěrk 8-16 mm, 5-7 cm), který po zapojení nepotřebuje zálivku ani hnojení. Náhrada za zalévaný trávník nebo letničky - rostliny snášející sucho místo dodávání vody.",
   kvant=[kv("W","kvalitativne","Po roce zapojení bez zálivky (směs Blütensaum výslovně bez dozálivky); úspora v litrech ve zdroji není", zdroj=["lwg_misch2021"], znacka="overeno"),
          kv("E","hodnota","Údržba 2-6 min/m²/rok (podle směsi), kompost ani kůra se nepoužívají; minerální mulč 5-7 cm", rozsah=[2,6], jednotka="min/m²/rok", zdroj=["lwg_misch2021"], znacka="overeno"),
          kv("B","kvalitativne","Kvetoucí směsi 10-35 druhů, písek jako hnízdiště samotářských včel", zdroj=["lwg_misch2021"], znacka="overeno")],
   vhodnost={"misto_typ": ["slunné suché místo","jižní svah","pás u chodníku","okolí školy"], "vyloucit": ["zamokřené místo","stín"], "pozn": "na těžké půdě (HSP C/D) zlehčit štěrkem 2-16 mm nebo vyměnit substrát"},
   vazby={"potrebuje": [], "synergie": ["Z06","U06"], "konflikt": ["Z08 na stejné ploše"]}, povoleni=0,
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["lwg_misch2021"],
   priklady=[pr("Veitshöchheim, Bavorsko (LWG)", "zkušební a ukázkové plochy trvalkových směsí od 1993 (Silbersommer a nástupci), standard pro obce v Bavorsku; podobné srážky jako Koryčany 💻", kdy="1993-2021", kdo="Bayerische Landesanstalt für Weinbau und Gartenbau", mereno="pracnost údržby min/m²/rok", zdroj=["lwg_misch2021"])],
   prenositelnost="Dobrá na slunná, suchá místa: jižní svahy, pásy u chodníků, předzahrádky, okolí školy. Na pelozemích nutná výměna nebo zlehčení substrátu. Nehodí se na zamokřená a stinná místa (LWG má zvlášť stínové směsi).",
   rizika="První rok zálivka a pletí; štěrkový mulč se v létě ohřívá (ochlazení jen z transpirace, nepřehánět). V ČR se prodávají směsi pod jinými názvy; cizí druhy volit s ohledem na invaznost 🤔.",
   nedohledano=["české srovnání spotřeby vody trávník vs. stepní záhon","cena založení 2025-2026"])

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

op("S05", "Šedá voda ze sprchy a umyvadel na zálivku (a WC)", ["S","Z"], ["J"], 3, ["W"], ["R"], "pozemek",
   popis="Lehce znečištěná voda ze sprchy, vany a umyvadel se jímá, přefiltruje (u WC se čistí) a použije na zálivku okrasné zeleně nebo splachování. V létě je to jediná 'dešťová voda', která teče každý den, i když neprší.",
   kvant=[kv("W","hodnota","Úspora pitné vody na zahradu 33-59 % (32-39 m³/rok na dům); 3 rodinné domy, podzemní kapková závlaha trvalek a ovocných stromů, max. 10 mm/den, v zimě vypnuto", rozsah=[33,59], jednotka="% pitné vody na zálivku", zdroj=["byrne2020"], znacka="overeno"),
          kv("W","hodnota","Bytové domy Berlín: recyklace šedé vody snižuje spotřebu pitné vody o cca 30 %, s pračkou, zálivkou a chlazením až 60 %", rozsah=[30,60], jednotka="% spotřeby pitné vody", zdroj=["nolde2026"], znacka="overeno")],
   vhodnost={"podminka": "oddělený odpad z koupelny (rekonstrukce) a místo na nádrž s filtrem", "vyloucit": ["zálivka zeleniny a jedlých částí","kropení na list","každodenní zálivka těžké půdy 🤔 (zasolení)"]},
   vazby={"potrebuje": [], "synergie": ["Z11","S06","Z12"], "konflikt": []}, povoleni=1,
   povoleni_pozn="🤔 1-2: změna vnitřní kanalizace; u WC nepitný rozvod podle ČSN 75 6780; ověřit u stavebního a vodoprávního úřadu",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=["csn756780","szu2022_seda"],
   priklady=[pr("Fremantle, Západní Austrálie", "3 rodinné domy, přímé odklonění šedé vody do podzemní kapkové závlahy; 12 měsíců monitoringu", kdy="2020", kdo="Byrne a kol. (Murdoch University)", mereno="úspora pitné vody na zahradu 33-59 %", zdroj=["byrne2020"]),
             pr("Berlín-Pankow", "2 novostavby bytového družstva EWG s recyklací šedé vody (sprcha, vana; v jedné i pračka + rekuperace tepla); úspora 600 a 1 200 m³ pitné vody za rok 2025", kdy="2025", kdo="EWG Pankow, Nolde & Partner", mereno="spotřeba pitné vody", zdroj=["nolde2026"]),
             pr("Praha 9, ZŠ Českobrodská", "voda z umyvadel a sprch po úpravě na splachování WC, dešťová voda v retenčních nádržích na zálivku (Adapterra Awards 2022)", kdy="2022", kdo="MČ Praha 9", mereno=None, zdroj=["adapterra2022"])],
   prenositelnost="Technicky ano u rodinného domu při rekonstrukci koupelny; smysl hlavně tam, kde v létě vyschne dešťová nádrž. Ekonomicky slabé na úrovni jednoho domu (Austrálie: 4-5x dražší než pitná voda).",
   rizika="V ČR zatím bez závazných hygienických limitů (SZÚ 2022); k zálivce jen lehká šedá voda bez kuchyně a pračky; soli a tenzidy degradují půdu, mikroplasty z pračky, patogeny přežívají ve skladované vodě. Nešetří vodu v krajině, jen pitnou. Filtr vyžaduje údržbu.",
   nedohledano=["měření na rodinném domě ve střední Evropě","množství šedé vody z RD (l/os/den) z primárního zdroje","cena technologie pro RD 2026"],
   pozn_poctivost="Austrálie má středomořské klima a jinou cenu vody; čísla brát jako rozsah, ne jako předpověď pro Koryčany.")

op("S06", "Dešťová voda na splachování WC (nepitný rozvod v domě nebo škole)", ["S"], ["J","O","S"], 3, ["W","R"], ["Q"], "pozemek",
   popis="Podzemní nádrž (S01) napojená přes filtr a čerpadlo na oddělený rozvod k WC (případně pračce) s automatickým dopouštěním pitné vody. Na rozdíl od zálivky bere vodu každý den celý rok, takže nádrž má smysl i v zimě a při každém dešti má volný objem.",
   kvant=[kv("W","hodnota","WC = cca 20-30 % spotřeby domácnosti: Praha 2020 splachování 26 l ze 112 l/os/den; Bielsko-Biała cca 30 %; ČR 2023 celkem 86,7 l/os/den", rozsah=[20,30], jednotka="% spotřeby pitné vody", zdroj=["praha14_voda2022","madzia2019","csu2024_voda"], znacka="overeno"),
          kv("W","vzorec","Úspora pitné vody = osoby × 17-26 l/den = 6-9,5 m³/os/rok; 4 osoby 25-38 m³/rok 🤔 odvozeno", vzorec="V_rok_m3 = osoby * (0.017..0.026) * 365", zdroj=["praha14_voda2022","csu2024_voda"], znacka="odhad"),
          kv("W","hodnota","Nádrž 0,25 m³/os a střecha 30 m²/os nahradí téměř 80 % vody na splachování (přes 10 m³/os/rok); nomogram, Bielsko-Biała (vlhčí klima než Koryčany)", hodnota=80, jednotka="% vody na splachování", zdroj=["madzia2019"], znacka="overeno"),
          kv("R","vzorec","Jako S01; nádrž se průběžně vyprazdňuje, při dešti má volný objem", vzorec="V_zachyceno_m3 = min(V_nadrz_m3 - V_naplneno_m3, A_strechy_m2 * P_m)", zdroj=["tab_c"])],
   vhodnost={"kazda_strecha": True, "podminka": "místo na podzemní nádrž a oddělený rozvod; nejlépe novostavba, rekonstrukce, veřejná budova (U04)", "vyloucit": ["malá střecha + velká domácnost (nádrž vyschne)"]},
   vazby={"potrebuje": ["S01"], "synergie": ["S02","U04","S05"], "konflikt": ["přepad do kanalizace"]}, povoleni=1,
   povoleni_pozn="nepitný rozvod označený podle ČSN 75 6780, ochrana proti zpětnému toku; ohlášení 🤔; souhlas provozovatele vodovodu 💻",
   ceny=[cena("podzemní nádrž 5000 l vč. šachty, bez montáže (viz S01)", 50830, "Kč", 2026, "hornbach_nadrz"), {"polozka": "čerpadlo, filtr, nepitný rozvod, montáž", "hodnota": None, "rozsah": None, "jednotka": "Kč", "rok": None, "zdroj": None, "pozn": "cena neověřena"}],
   financovani=["vlastni","nzu_rd_2026","opzp_1_3_4"], standardy=["csn756780","csn759010"],
   priklady=[pr("Kyselov u Vyššího Brodu (Český soběstačný dům)", "dům bez přípojek; zachycená dešťová voda po úpravě na sprchu a WC (Adapterra Awards 2022, Náš domov)", kdy="2022", kdo="soukromý stavebník + 40 odborníků", mereno=None, zdroj=["adapterra2022"]),
             pr("Ořechov u Brna", "obec: 4 retenční nádrže na dešťovou vodu, 3 tůně, suchý poldr, 7 ha mokřad (Adapterra Awards 2022, Volná krajina); využití nádrží na WC a objemy ve zdroji neuvedeny", kdy="2022", kdo="obec Ořechov", mereno=None, zdroj=["ceskestavby2022_orechov"]),
             pr("Německo (celá země)", "cca 1,8 mil. instalovaných nádrží na dešťovou vodu, 60-65 tis. ročně, 40 % do stávajících domů (studie trhu výrobce)", kdy="2010", kdo="Mall GmbH", mereno="odhad výrobce, ne měření", zdroj=["mall2010"], znacka="overeno_stare")],
   prenositelnost="Ano u novostaveb a rekonstrukcí RD; u veřejných budov (škola, úřad) ještě lépe, protože WC je tam hlavní spotřeba 🤔. Nehodí se tam, kde není místo na nádrž, nebo malá střecha + velká domácnost.",
   rizika="V suchém létě 5 m³ nádrž pro 4 osoby bez deště dojde za 1-3 týdny 🤔, pak dopouští pitná voda. Nešetří vodu v krajině, šetří pitnou a odlehčí kanalizaci. NZÚ 2026 podporuje jen v kombinaci se zateplením nebo zdrojem energie.",
   nedohledano=["měření na RD ve střední Evropě","podíl WC na spotřebě v ČR z primárního zdroje (SOVAK/ČSÚ)","cena technologie 2026"],
   pozn_poctivost="Podíl WC 20-30 % je z letáku bez uvedeného zdroje a z polského výpočtu; 80 % náhrady platí pro vlhčí Beskydy, pro Koryčany spíš méně 🤔.")

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

op("U09", "Studie a plán hospodaření s dešťovou vodou obce (kam teče voda z veřejných ploch, kdo se stará)", ["U","H"], ["O","S"], 2, ["R","I","Q"], [], "uzemi", kontext=True,
   popis="Obec si nechá zpracovat (nebo se školou udělá) přehled, kam teče voda ze střech veřejných budov, silnic a náměstí, kde jsou místa pro průlehy, rabátka a nádrže, a kdo se o ně bude starat. Bez toho se opatření staví nahodile a po letech chátrají. V Koryčanech tuto roli z velké části plní tato aplikace.",
   kvant=[kv("Q","kvalitativne","Taucha (Sasko): u 25-30 let starých průlehů selhávaly správa a údržba (ucpané vtoky, chybějící spád, zrušené soukromé průlehy, zásahy sítí), ne princip; doporučení: vlastnictví a údržbu určit smluvně, provozní řád, kontrola vsaku každých 10 let, cedule pro obyvatele", zdroj=["taucha2024"], znacka="overeno")],
   vhodnost={"vsude": True},
   vazby={"potrebuje": [], "synergie": ["U01","U03","U04","U05","U07","M01","M05"], "konflikt": []}, povoleni=0,
   ceny=[NEOVERENA], financovani=["vlastni","opzp_1_3_4"], standardy=["taucha2024"],
   priklady=[pr("Taucha (Sasko)", "vyhodnocení 3 soustav průleh-rýha po 25-30 letech provozu; obecné pokyny pro obce (plánování, vlastnictví, provoz, údržba, monitoring)", kdy="2023-2024", kdo="město Taucha, Grüner Ring Leipzig, IWS, KWL", mereno="k_f, vyprázdnění do 24 h, těžké kovy v půdě", zdroj=["taucha2024","iws2024_taucha"]),
             pr("Jílové u Prahy", "malé město má studii retenční kapacity (vsak, malé nádrže, krajinná opatření) a hledá partnery, jak přejít 'od analýzy k realizaci'", kdy="2026", kdo="město Jílové u Prahy", mereno=None, zdroj=["portico2026_jilove"]),
             pr("Močovice (Středočeský kraj)", "koncepce rozvoje vodních ploch obce: návesní rybník 0,65 ha (4 530 m² hladiny), odbahnění 906 m³, varianty 2,5-2,8 mil. Kč bez DPH, jez 7,6-16,6 mil. Kč", kdy="2020", kdo="obec, VRV a.s.", mereno=None, zdroj=["vrv2020_mocovice"])],
   prenositelnost="Plně. Pro Koryčany: tato aplikace + pasport svodů veřejných budov (škola, úřad, sokolovna, hasičárna) + dohoda, kdo seče a čistí průlehy. Školní projekt 'kam teče voda ze školy' (M01, M05) jako vstup.",
   rizika="Studie bez realizace (Jílové). Náklady studie nedohledány. Dolní Rakousko dotuje obcím 'Regenwasserpläne' 📄 (web 22. 10. offline).",
   nedohledano=["cena studie HDV pro obec do 3 000 obyvatel","NÖ Regenwasserpläne (web offline)"])

# ===== H organizační opatření obce při vedrech + U08 (blok A, 21. 10. 2026)
op("U08", "Mlžení a kropení při letních hromadných akcích (mlžná brána, tryska na hydrantu)", ["U","H"], ["O","S"], 1, ["CH"], [], "lokalita",
   popis="Mlžná brána nebo tryska na hydrantu na hodech, táboře, sportovním dni nebo trhu v horkém dni. Pomůže lidem, kteří stojí přímo u ní; ulici ani obec neochladí. Jako trvalý prvek nemá smysl (rozhodnutí 21. 10. 2026), jen pro akce.",
   kvant=[kv("CH","hodnota","Vzduch v průměru -0,7 °C, max. -2,5 °C (Curych 2022, 180 trysek, jen za provozu, nejvíc při nízké vlhkosti po větru); autoři účinek označují za slabý", rozsah=[0.7,2.5], jednotka="°C vzduch", zdroj=["zhaw2023_mlzeni"], znacka="overeno"),
          kv("CH","hodnota","Vodní prvky (trysky, mlžné brány) vzduch cca -1,2 °C jen v bezprostředním okolí; kropení ploch -1,3 až -3,1 °C pocitově na max. ~20 min; kašny na náměstí minimální účinek (CzechGlobe/UPOL)", rozsah=[1.2,3.1], jednotka="°C", zdroj=["tacr2021_horko","ct24_2022_horko"], znacka="overeno")],
   vhodnost={"misto_typ": ["náměstí při akci","hřiště","tábořiště","školní dvůr"], "podminka": "jen v horkém dni za provozu; přístup k hydrantu nebo nádrži"},
   vazby={"potrebuje": [], "synergie": ["H01","H02","Z06"], "konflikt": []}, povoleni=1, povoleni_pozn="souhlas provozovatele vodovodu (hydrant) 💻; hygiena vody v mlžení ověřit s KHS 💻",
   ceny=[NEOVERENA], financovani=["vlastni"], standardy=[],
   priklady=[pr("Curych, Turbinenplatz", "kruh 180 vysokotlakých trysek na náměstí, měření ZHAW celé léto 2022; mimo provoz nulový rozdíl", kdy="2022", kdo="město Curych, ZHAW", mereno="teplota vzduchu vs. referenční stanice", zdroj=["zhaw2023_mlzeni"]),
             pr("Vídeň", "100 mlžných sprch 'Sommerspritzer' a 75 mobilních 'Brunnhilde' na hydrantech při výstraze; Cooling Park Esterházypark (2020) uvádí 'až 6 °C' bez metodiky", kdy="2020-2025", kdo="město Vídeň", mereno=None, zdroj=["coollife2025_wien","wien_coolspot"])],
   prenositelnost="Pro Koryčany jen jako vybavení letních akcí (hody, tábor, sportovní den): tryska na hydrant nebo IBC s čerpadlem 🤔. Trvalé mlžení na náměstí ne - účinek do 2,5 °C jen za provozu a spotřeba pitné vody v suchu.",
   rizika="Ochladí místo, ne obec; kašna sama nic. Spotřeba pitné vody v suchu; hygiena rozprašované vody (legionely 💻). Vídeňské 'až 6 °C' nemá metodiku, nepřebírat.",
   nedohledano=["cena a spotřeba vody mlžné brány (l/h)","hygienické podmínky KHS pro mlžení"],
   pozn_poctivost="Účinek je malý a jen za provozu; v aplikaci se do součtů nepočítá.")

op("H01", "Chladná místa, pitná voda a varování při vlně veder (organizační plán obce)", ["H","U"], ["O","S"], 1, ["CH"], [], "uzemi", kontext=True,
   popis="Obec před létem určí a zveřejní chladná místa (knihovna, kostel, úřad, škola), zajistí pitnou vodu (pítko, kohoutek na náměstí), při výstraze ČHMÚ rozešle varování seniorům a pečovatelům (rozhlas, SMS), posune časy akcí a prací. Nic se nestaví, jde o domluvu. Nemění teplotu v obci, snižuje riziko pro lidi.",
   kvant=[kv("CH","hodnota","Nizozemský národní plán vedra (od 2007): odhad úmrtí z vedra v aktivačních dnech cca 4 200 (2000-2009) -> 2 400 (2010-2019); u 90+ podíl z úmrtí 2,0 -> 1,3 %; plán 'mohl přispět' (pokles začal už 2007-2011 po vlnách 2003/2006)", rozsah=[2400,4200], jednotka="úmrtí za dekádu (NL)", zdroj=["rivm2026_nl"], znacka="overeno"),
          kv("CH","kvalitativne","Vídeň: 29 opatření, ~1 600 pítek, 22 chladných zón VI-IX, kaskáda varování nemocnicím, pečovatelům a školám; účinky neměřeny, jen počty", zdroj=["coollife2025_wien"], znacka="overeno")],
   vhodnost={"vsude": True},
   vazby={"potrebuje": [], "synergie": ["U08","H02","Z06","U01"], "konflikt": []}, povoleni=0, povoleni_pozn="usnesení rady/zastupitelstva, dohoda s pečovatelskou službou a školou",
   ceny=[cena("pítko, hlášení rozhlasem, seznam míst", None, "Kč", 2026, None, pozn="cena neověřena; 🤔 řádově tisíce až desetitisíce Kč")], financovani=["vlastni"], standardy=[],
   priklady=[pr("Nizozemsko (celá země)", "národní plán vedra: varování + rady pro seniory, pečovatele a zdravotníky; 20 aktivací 2010-2026; vyhodnoceno RIVM 2024-2025 (epidemiologie, průzkum 804 seniorů, 586 pečujících, 405 zdravotníků)", kdy="2007-2025", kdo="RIVM, ministerstvo zdravotnictví, KNMI, Červený kříž", mereno="úmrtnost z vedra po dekádách; 9 z 10 lidí si rady v létě 2025 vybavilo; 1 ze 3 seniorů si myslí, že se ho netýkají", zdroj=["rivm2026_nl"]),
             pr("Vídeň", "Hitzeaktionsplan 2022, roční vyhodnocení po sezóně; výstraha při >= 3 dnech pocitově >= 35 °C a nocích >= 20 °C; 10 ohrožených skupin", kdy="2022-2025", kdo="město Vídeň", mereno=None, zdroj=["coollife2025_wien"])],
   prenositelnost="Plně. Pro Koryčany: seznam chladných míst na webu a rozhlasem, pítko na náměstí, dohoda s pečovatelskou službou, škola (posun tělocviku, voda ve třídách). Práh varování převzít z výstrah ČHMÚ (SIVS), ne vídeňský 🤔.",
   rizika="Účinek doložen jen pro celostátní systém a 'mohl přispět'; lokální efekt v obci neměřitelný. 'Chladná zóna' bez klimatizace nebo masivní stavby chladná není 🤔. Nemění mikroklima.",
   nedohledano=["české vyhodnocení účinku výstrah ČHMÚ/MZ","vzor plánu vedra pro obec do 3 000 obyvatel"],
   pozn_poctivost="Opatření pro lidi, ne pro krajinu; v aplikaci bez čísla v součtech.")

op("H02", "Stínění veřejných míst plachtami, pergolami s popínavkami, přístřešky (zastávka, hřiště, školní dvůr)", ["U","H"], ["O","S"], 2, ["CH"], [], "lokalita",
   popis="Tam, kde strom nevyroste dost rychle nebo nejde zasadit (sítě, dlažba, zastávka, hřiště), zastínit plachtou, pergolou s popínavkou nebo přístřeškem. Strom zůstává první volba (stín + výpar); plachta je náhrada na dobu, než strom doroste.",
   kvant=[kv("CH","hodnota","Ve stínu (stromu) pocitová teplota o 8,3-10,9 °C nižší než na osluněné dlažbě (CzechGlobe/UPOL); pro plachty samostatné měření nedohledáno", rozsah=[8.3,10.9], jednotka="°C pocitově (stín stromu)", zdroj=["tacr2021_horko"], znacka="overeno"),
          kv("CH","hodnota","Slunečník povrch 51,3 °C vs. koruna stromu 32,7 °C (IR snímek, ENKI): plachta se sama ohřívá a sálá", rozsah=[32.7,51.3], jednotka="°C povrch", zdroj=["enki_stromy"], znacka="overeno"),
          kv("CH","kvalitativne","Aarau 2022: město odmítlo uvést paušální číslo; pevné plachty brání nočnímu chladnutí, stíní, ale neodpařují; preferuje zeleň", zdroj=["aarau2022"], znacka="overeno")],
   vhodnost={"misto_typ": ["zastávka","hřiště","školní dvůr","tribuna","trh"], "vyloucit": ["místo, kde lze zasadit strom"]},
   vazby={"potrebuje": [], "synergie": ["Z06","Z09","U07","H01"], "konflikt": []}, povoleni=1, povoleni_pozn="konstrukce: ohlášení nebo stavební povolení podle velikosti 🤔; sítě",
   ceny=[NEOVERENA], financovani=["vlastni","opzp_1_3_4"], standardy=[],
   priklady=[pr("Solothurn, Amtsplatz", "lanková pergola s popínavkami nad náměstím (zmíněno v odpovědi města Aarau jako vzor rostlinného stínění)", kdy=None, kdo="město Solothurn", mereno=None, zdroj=["aarau2022"], znacka="citace"),
             pr("Kornwestheim, Silcherschule", "asfalt školního dvora 56,2 °C ve 13:30, ve stínu 29,7 °C (termokamera města, červenec 2026); řešení stromy a štěpka, ne plachty", kdy="2026", kdo="město Kornwestheim", mereno="povrch termokamerou", zdroj=["stz2026_kornwestheim"])],
   prenositelnost="Zastávky, hřiště, školní dvůr, tribuna, trh. Pergola s popínavkou (Z09) spojuje stín a výpar a je lepší než holá plachta.",
   rizika="Plachta se ohřívá a sálá; stíní jen pod sebou; pevná konstrukce blokuje noční vychladnutí; vítr a sníh (demontáž na zimu). Neřeší vodu.",
   nedohledano=["měření teploty pod plachtou vs. pod stromem ve střední Evropě","cena"])

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
 "misto": {"Z":"zahrada, dvůr","S":"střecha, stavba","U":"veřejný prostor obce","P":"orná půda","L":"louka, pastvina","LES":"les","T":"tok, niva, prameniště","C":"cesta, svah, strž","H":"organizační opatření obce při vedrech"},
 "rozhoduje": {"J":"jednotlivec na svém pozemku","V":"vlastník půdy (přes pacht N01 nebo vyjmutí N02)","O":"obec","SP":"správce toku/lesa (Povodí Moravy, LČR)","S":"škola","zemedelec":"uživatel DPB (jen pro SZP dotace)"},
 "pracnost": {"1":"víkend a ruce","2":"dny až týdny, malá technika","3":"projekt + firma"},
 "ucinek": {"R":"zadržení objemu","I":"infiltrace do půdy","Q":"zpomalení odtoku","E":"omezení neproduktivního výparu / větru","CH":"ochlazení mikroklimatu","ER":"protierozní","B":"biodiverzita","W":"šetření pitnou vodou"},
 "meritko": {"pozemek":"účinek na pozemku + příspěvek do součtu","lokalita":"ulice, lán, úsek toku","uzemi":"povodí; kontextová opatření"},
 "povoleni": {"0":"nic","1":"ohlášení / souhlas vlastníka či správce","2":"vodoprávní nebo stavební řízení"},
 "znacka": {"overeno":"✅ ověřeno online v uvedený den","overeno_stare":"✅⏳ ověřeno, zdroj starší 12 měsíců","citace":"📄 doložený zdroj, originál nečten","odhad":"🤔 odhad bez zdroje","pamet":"💻 z paměti, neověřeno"},
 "kvantifikace_typ": {"vzorec":"jádro počítá z parametrů","hodnota":"doložená konstanta nebo rozsah","kvalitativne":"bez čísla, zobrazit slovně"},
}

DATA = {
 "meta": {"nazev":"Katalog opatření - Koryčany resilience","verze":"0.7","datum":DNES,"licence_dat":"CC BY 4.0 (vlastní kompilace; citované zdroje mají vlastní licence)",
          "upozorneni":"Zjednodušený osvětový model, ne projektová dokumentace. Každé číslo má zdroj a značku původu. Ceny jen se zdrojem a datem; jinak 'cena neověřena'. Paragrafy vodního zákona ověřit v e-Sbírce.",
          "zdroje_md":["claude/KATALOG.md","claude/KATALOG-Z-S.md","claude/KATALOG-U-P.md","claude/KATALOG-L-LES-T-C.md","claude/KATALOG-RESERSE.md"]},
 "ciselniky": CISELNIKY, "konstanty": KONSTANTY, "zdroje": Z, "programy": PROGRAMY, "nastroje": NASTROJE, "opatreni": O,
}

# ------------------------------------------------ doplňky z rešerše dobré praxe (blok B, 21. 10. 2026)
def doplnit(id, kvant=(), priklady=(), prenositelnost=None, rizika=None, standardy=(), nedohledano_odstranit=(), nedohledano=(), pozn_poctivost=None, synergie=()):
    o = next(x for x in O if x["id"] == id)
    o["kvantifikace"] += list(kvant); o["priklady"] += list(priklady); o["standardy"] += [s_ for s_ in standardy if s_ not in o["standardy"]]
    o["nedohledano"] = [n for n in o["nedohledano"] if n not in nedohledano_odstranit] + list(nedohledano)
    o["vazby"]["synergie"] += [v for v in synergie if v not in o["vazby"]["synergie"]]
    if prenositelnost: o["prenositelnost"] = prenositelnost
    if rizika: o["rizika"] = rizika
    if pozn_poctivost: o["pozn_poctivost"] = ((o["pozn_poctivost"] + " ") if o["pozn_poctivost"] else "") + pozn_poctivost

doplnit("Z01",
   kvant=[kv("I","hodnota","Osázená mulda při vytrvalém dešti pojala a předala do podloží až o třetinu více vody než trávník (LWG); návrh: nádrž max. 30 cm, vyprázdnění do 24 h, k_f >= 1e-5 m/s", hodnota=33, jednotka="% více vody než trávník", zdroj=["lwg_versickern2010"], znacka="overeno_stare"),
          kv("I","kvalitativne","Pilot Mnichov: po dobu sledování žádný pokles propustnosti ani při odtoku z komunikací; 57 ze 73 druhů trvalek obstálo", zdroj=["lfu_mulden2023"], znacka="overeno"),
          kv("Q","kvalitativne","Ozelenění zahrad snižuje odtok hlavně při dlouhých mírných deštích; při přívalu málo, na jílové vrstvě téměř nic (3 zahrady, Leeuwarden)", zdroj=["lakhi2025"], znacka="overeno")],
   priklady=[pr("Mnichov (Bavorsko)", "pilotní multifunkční vsakovací mulda s trvalkami, projekt LfU/TU München/HSWT; sledována propustnost, zadržení znečištění z komunikací a hmyz", kdy="2020-2023", kdo="LfU Bayern, TU München, HSWT", mereno="propustnost v čase (bez poklesu), zadržení Zn, Cu a biocidů", zdroj=["lfu_mulden2023"]),
             pr("Kecskemét (Maďarsko)", "experimentální dešťová zahrada napájená ze střechy rodinného domu, různě tolerantní druhy; město ohrožené suchem", kdy="2024", kdo="Hoyk a kol.", mereno="v abstraktu bez čísel", zdroj=["hoyk2024"]),
             pr("Bratislava", "dotace domácnostem a firmám na nádrže, dešťové zahrady, propustné povrchy a zelené střechy: 50 % nákladů do 1 000 €; 2016: 16 žádostí, 6 dokončeno; účinek neměřen, zájem malý", kdy="2016-2020", kdo="hl. město Bratislava", mereno=None, zdroj=["bratislava_com"]),
             pr("Rotterdam, Sponstuin", "zkušební 'houbová zahrada': vlnitá mulda do 80 cm, 4 typy půdy s příměsemi, 2 roky měření", kdy="2019", kdo="De Urbanisten, Voedseltuin, město", mereno="výsledky v letáku nejsou", zdroj=["steenbreek_sponstuin"], znacka="overeno_stare")],
   prenositelnost="V Koryčanech (HSP C/D, těžké půdy) pomáhá běžnému dešti 10 mm a mírným dešťům, ne N10 přívalu; na jílu počítat s rýhou nebo štěrkovým tělesem (Z10) a odstupy od domu.",
   rizika="Účinek na přívaly je malý, aplikace to musí říkat. Stromy ne do vsakovací zóny. Trvalky volit podle tolerance k zaplavení i suchu.",
   standardy=["lwg_versickern2010"])

doplnit("Z04",
   kvant=[kv("I","hodnota","Po 4-7 letech provozu cca 90 % propustných ploch stále nad návrhem 270 l/(s·ha); čisté plochy 1 200-3 200, ucpaná místa 0-100 l/(s·ha) (jen 5-10 % plochy); mokrý povrch 210-260", rozsah=[1200,3200], jednotka="l/(s·ha)", zdroj=["nrw2005_belaege"], znacka="overeno_stare"),
          kv("I","hodnota","Odtok podle povrchu: štěrkový trávník a zatravňovací tvárnice 30-40 %, dlažba s travní spárou 40-50 %, dlažba s propustnou spárou, pórovitá dlažba a štěrkopísková cesta 0-20 %", rozsah=[0,50], jednotka="% srážky", zdroj=["bayern2003_entsiegelung","hlnug2022"], znacka="overeno_stare")],
   priklady=[pr("Severní Porýní-Vestfálsko", "24 objektů 4-7 let po odstranění asfaltu, 49 měření infiltrometrem; svépomocná pokládka bez měřitelného zhoršení, chyby firem (písek v pórech) propustnost srazily", kdy="2005", kdo="MUNLV NRW, FH Bochum, IKT", mereno="infiltrace l/(s·ha) na stárnoucích plochách", zdroj=["nrw2005_belaege"], znacka="overeno_stare"),
             pr("Nizozemsko, NK Tegelwippen", "celostátní soutěž obcí ve 'vydlabávání dlaždic': 2025 téměř 6 mil. ks, od začátku 20 mil. (360 fotbalových hřišť); Utrecht 437 467 ks; přenositelné jako akce školy nebo oddílu", kdy="2021-2025", kdo="obce, školy, obyvatelé", mereno="počet odstraněných dlaždic", zdroj=["tegelwippen2025"])],
   prenositelnost="Dvory, vjezdy, parkovací stání a cesty s malým provozem; sklon 2-3 % a odtok vést do zeleně. Na HSP D jen s podkladní vrstvou a bezpečnostním přepadem.",
   rizika="Propustnost klesá ve stínu, pod mechem a u provozu; spáry čistit s odsáváním dřív, než se zanesou. Při pokládce nezametat písek do pórovité dlažby.",
   standardy=["nrw2005_belaege"])

doplnit("Z05",
   kvant=[kv("E","hodnota","Slámový mulč (hořčice, svazenka, pšenice) snižuje výpar z půdy nejméně o 50 % proti holé půdě; mokrý mulč se odpařuje jako holá půda (DWD, vážené nádoby, 2012-2014)", hodnota=50, jednotka="% výparu z půdy", zdroj=["dwd_mulch"], znacka="overeno"),
          kv("I","hodnota","+1 % organického uhlíku = +1,16 mm vody na 100 mm půdy (75 % studií 0,7-2 mm); nejvíc v píscích, nejméně v jílech; pro pelozemě Koryčan malý účinek (🤔 cca 3,5 mm v 30 cm ornice)", hodnota=1.16, rozsah=[0.7,2.0], jednotka="mm/100 mm půdy na 1 % C", zdroj=["minasny2018"], znacka="overeno"),
          kv("I","hodnota","Mulč z žita a hrachu v celeru (písek, Braniborsko 2023): vlhkost v 25 cm 15 % vs. 14 % holá půda; podsev jetele půdu vysušuje víc než holá půda", rozsah=[14,15], jednotka="% obj. vlhkosti", zdroj=["igz_heistermann"], znacka="overeno")],
   priklady=[pr("Lipsko (DWD Agrarmeteorologie)", "vážené Mitscherlichovy nádoby pod širým nebem, holá půda vs. mulč vs. porost, 2012-2014", kdy="2012-2014", kdo="DWD", mereno="aktuální evapotranspirace denním vážením", zdroj=["dwd_mulch"])],
   nedohledano_odstranit=["retence půdy podle organické hmoty (český zdroj)"],
   nedohledano=["retence půdy podle organické hmoty - český zdroj (zahraniční metaanalýza doplněna)"],
   pozn_poctivost="Organická hmota zvyšuje retenci jen málo (1,16 mm/100 mm na 1 % C, na jílu nejméně); hlavní účinek mulče je výpar, ne zásoba vody.")

doplnit("Z06",
   kvant=[kv("CH","kvalitativne","Výběr druhů do horka a sucha: LWG Stadtgrün 2021 (3 lokality Bavorska vč. Würzburgu, 30 druhů, 2009-2021): m. j. dub cer, dub uherský, jasan zimnář, habrovec, habr 'Frans Fontaine', lípa stříbrná; 15 ze 43 doporučených druhů ze stepních a suchých lesů", zdroj=["lwg_klimabaeume2019"], znacka="overeno_stare")],
   priklady=[pr("Würzburg, Kempten, Hof (Bavorsko)", "zkušební výsadby 30 druhů 'klimastromů' ve třech klimaticky odlišných městech, projekt Stadtgrün 2021", kdy="2009-2021", kdo="LWG Veitshöchheim", mereno="vitalita a růst po letech; skóre horko/sucho zdroj neuvádí", zdroj=["lwg_klimabaeume2019"], znacka="overeno_stare")],
   pozn_poctivost="Do zahrad přednostně ovocné a domácí druhy (SPPK); cizí 'klimastromy' spíš do ulic a na výsušná místa 🤔.")

doplnit("Z09",
   kvant=[kv("CH","hodnota","Stěna pod přísavníkem trojcípým v průměru o 6,5 °C (jih) a 7,0 °C (západ) chladnější v době plného oslunění; účinek roste s teplotou nad 22 °C (Toronto, 6 měsíců)", rozsah=[6.5,7.0], jednotka="°C povrch stěny", zdroj=["blake2021"], znacka="overeno"),
          kv("CH","hodnota","Pod hustou popínavkou dopadá na zeď cca 20 % záření, povrch o cca 15 °C chladnější (sloupek inženýrské komory, studie nejmenovány)", hodnota=15, jednotka="°C povrch stěny", zdroj=["bayika2022"], znacka="citace")],
   priklady=[pr("Toronto (Kanada)", "přísavník trojcípý na jižní a západní stěně městské budovy, teplotní loggery 6 měsíců", kdy="2021", kdo="Blake M. (diplomová práce)", mereno="rozdíl povrchové teploty stěny", zdroj=["blake2021"])],
   prenositelnost="Jižní a západní stěny domů, garáží, kůlen, školy; samopnoucí druhy (přísavník) na zdravou omítku, jinak lanková konstrukce. Nehodí se na zateplené fasády bez konstrukce 🤔.",
   rizika="Ochladí stěnu a interiér, ne ulici. Vídeňský údaj 'výkon 45 klimatizací' nemá doložený zdroj, nepřebírat. Údržba řezu u oken a okapů.",
   nedohledano_odstranit=["kvantifikace pro zelené fasády"])

doplnit("Z11",
   nedohledano=["měření úspory kapkové závlahy proti postřiku v zahradách střední Evropy"],
   pozn_poctivost="Olla (Z12) je podle AZ1911 zhruba rovnocenná kapkové závlaze.", synergie=["Z12"])

doplnit("S01",
   priklady=[pr("Kyselov u Vyššího Brodu (Český soběstačný dům)", "zachycená dešťová voda po úpravě na sprchu a WC; Adapterra Awards 2022", kdy="2022", kdo="soukromý stavebník", mereno=None, zdroj=["adapterra2022"]),
             pr("Německo", "cca 1,8 mil. instalovaných nádrží, 60-65 tis. ročně (2009), 40 % do stávajících domů; 'úspora 110 mil. m³ pitné vody' je odhad výrobce", kdy="2010", kdo="Mall GmbH (studie trhu)", mereno="odhad, ne měření", zdroj=["mall2010"], znacka="overeno_stare")],
   synergie=["S06"])

doplnit("S02",
   kvant=[kv("Q","hodnota","Svedení ze zpevněných ploch na zeleň snížilo modelovaný odtok ze zpevněných ploch o 30 % (3 zahrady, Leeuwarden); na jílu se voda hromadí na povrchu", hodnota=30, jednotka="% odtoku ze zpevněných ploch", zdroj=["lakhi2025"], znacka="overeno")],
   rizika="Na jílu (HSP D) se voda u domu hromadí; dodržet odstupy z ČSN 75 9010 a vést vodu do Z01/Z10.")

doplnit("Z02",
   rizika="V suchém létě je výpar z hladiny větší než srážky (vlastní data projektu, sekce Počasí): malá tůň bez přítoku na HSP C/D vyschne nebo žádá dolévání 🤔. Nepočítat ji jako zdroj zálivky.",
   nedohledano=["výpar zahradní tůně l/den (jen bazénové tabulky a diskuse)"])

# --- doplňky blok A (horko v obci), 21. 10. 2026
doplnit("Z06",
   kvant=[kv("CH","hodnota","ČR (CzechGlobe/UPOL, Olomouc 2018): ve stínu stromu na otevřené ploše pocitová teplota -8,3 až -10,9 °C, v ulici -2,8 až -7,6 °C; vzduch -0,4 až -2,1 °C podle denní doby; v noci +0,1 až +1,3 °C", rozsah=[0.4,2.1], jednotka="°C vzduch (ČR)", zdroj=["tacr2021_horko","ct24_2022_horko"], znacka="overeno"),
          kv("CH","hodnota","Pod stromem vs. u jižní stěny až -11,5 °C v poledne (šedý globe teploměr, 48 000 měření, 2 roky, severní Francie)", hodnota=11.5, jednotka="°C globe", zdroj=["earthwatch_fr"], znacka="overeno_stare"),
          kv("CH","hodnota","Povrch zástavby se stromy o 8-12 °C chladnější než bez stromů (satelit, ~300 evropských měst, střední Evropa); tráva 2-4x slabší; rozdíl ve vzduchu menší", rozsah=[8,12], jednotka="°C povrch", zdroj=["ct24_2021_eth"], znacka="citace")],
   priklady=[pr("Olomouc (a Brno, Ostrava, Plzeň)", "terénní měření pocitové teploty ve stínu stromů, v ulicích, u vodních prvků a na trávnících, 24. 7. 2018; doporučení a mapy horkých míst pro 4 města", kdy="2018-2022", kdo="CzechGlobe, UPOL (TAČR ZÉTA)", mereno="pocitová a vzduchová teplota, stín vs. osluněná dlažba", zdroj=["tacr2021_horko","ct24_2022_horko"]),
             pr("Severní Francie", "občanská věda Earthwatch: 48 000 měření u stromů vs. u zdí a asfaltu, 2 roky", kdy="2018-2020", kdo="Earthwatch Europe", mereno="globe teplota", zdroj=["earthwatch_fr"], znacka="overeno_stare")],
   pozn_poctivost="Tři různá čísla: povrch pod stromem 8-25 °C, pocitová teplota ve stínu 3-11 °C, vzduch 0,4-2 °C (ČR). EPA 'až 5 °C vzduch' platí pro velké skupiny stromů; pro jeden strom v Koryčanech počítat s CzechGlobe 0,4-2,1 °C.")

doplnit("U01",
   kvant=[kv("CH","hodnota","Stromy v ulici: pocitová teplota -2,8 až -7,6 °C ve dne, +0,1 až +1,3 °C v noci; vzduch -0,4 až -2,1 °C (CzechGlobe/UPOL); stromy na jižním chodníku ulice V-Z důležitější než na severním (model Lee & Mayer 2019)", rozsah=[2.8,7.6], jednotka="°C pocitově", zdroj=["tacr2021_horko","dach2019_lee"], znacka="overeno")],
   priklady=[pr("Olomouc", "měření v ulicích, CzechGlobe/UPOL 2018", kdy="2018", kdo="CzechGlobe, UPOL", mereno="pocitová teplota v uličním kaňonu", zdroj=["tacr2021_horko"])],
   rizika="V noci stromy mírně zadržují teplo (+0,1 až +1,3 °C pocitově). Umisťovat podle map horkých míst, ne nahodile (CzechGlobe).")

doplnit("S04",
   kvant=[kv("CH","hodnota","Světlý asfalt (albedo 0,12-0,16 vs. 0,08): povrch o 4-5,5 °C chladnější v nejteplejší fázi dne; radiační teplota pro chodce o 0,6 °C vyšší (v rámci nejistoty) - pro lidi na ulici bez zlepšení (Köniz 2025)", rozsah=[4,5.5], jednotka="°C povrch vozovky", zdroj=["koeniz2025"], znacka="overeno")],
   priklady=[pr("Köniz (Bern), Waldeggstrasse", "pilot ASTRA: světlé kamenivo v asfaltu, měření povrchu, vzduchu a globe teploty červen-červenec 2025", kdy="2025", kdo="ASTRA, Grolimund + Partner, BFH", mereno="povrch -4 až -5,5 °C; globe +0,6 °C", zdroj=["koeniz2025"]),
             pr("Aarau", "město světlé vozovky odmítlo z finančních a ekologických důvodů, preferuje zeleň", kdy="2022", kdo="město Aarau", mereno=None, zdroj=["aarau2022"])],
   rizika="Na střeše ano; na chodníku a náměstí odraz vadí chodcům a povrch chladí jen sebe. Není náhrada stromů.")

doplnit("U02",
   kvant=[kv("CH","hodnota","Světlý asfalt: povrch -4 až -5,5 °C, pro chodce bez zlepšení (Köniz 2025); trávník v centru vzduch -0,9 °C proti dlažbě (CzechGlobe)", rozsah=[0.9,5.5], jednotka="°C", zdroj=["koeniz2025","tacr2021_horko"], znacka="overeno")],
   rizika="Propustná dlažba chladí jen tehdy, když je v ní voda nebo tráva s kontaktem s podložím; suchá dlažba se chová jako asfalt 🤔.")

doplnit("U06",
   kvant=[kv("CH","hodnota","Trávník v centru: vzduch -0,9 °C proti osluněné dlažbě; zalévaný trávník povrch až o 20 °C chladnější než nezalévaný; trávník bez kontaktu s podložím má povrch jako beton (CzechGlobe/UPOL)", rozsah=[0.9,20], jednotka="°C (vzduch / povrch)", zdroj=["tacr2021_horko","ct24_2022_horko"], znacka="overeno")],
   rizika="V suchu bez závlahy účinek trávníku na horko mizí (suchý trávník ~ dlažba 🤔 odvozeno).")

doplnit("U07",
   priklady=[pr("Kornwestheim (Bádensko-Württembersko), Silcherschule", "termokamera města: asfalt dvora 56,2 °C ve 13:30, stín 29,7 °C; odstranění asfaltu, 2 stromové mísy se štěpkou, stromy, cesty z kůry, sezení z kamene a kmenů; 37 000 € (15 000 € dotace Klimopass), městské zahradnictví 3-4 týdny", kdy="2026", kdo="město Kornwestheim", mereno="povrch termokamerou před úpravou", zdroj=["stz2026_kornwestheim"]),
             pr("Drážďany, Montessorischule Huckepack", "fólie na okna, markýzy, noční provětrávání, odstranění asfaltu, stromy, plachty, nádrž na dešťovou vodu; 2025-2027, EFRE", kdy="2025-2027", kdo="škola + Sasko (EuK)", mereno=None, zdroj=["dresden_huckepack"]),
             pr("Červená Voda", "školní zahrada 2 000 m² (koloběh vody, včely, energie, mikroklima), finalista Adapterra Awards 2026", kdy="2026", kdo="ZŠ Červená Voda", mereno=None, zdroj=["adapterra2026"])],
   prenositelnost="Pro ZŠ Koryčany je prvním krokem změřit dvůr IR teploměrem v létě (M05): asfalt vs. stín vs. tráva. Pak odstranění části asfaltu, stromové mísy, štěpka.",
   synergie=["M05","H02"])

# --- doplňky blok C (veřejný prostor, škola), 22. 10. 2026
doplnit("U01",
   kvant=[kv("R","vzorec","Voda ze střech a chodníků do rabátka: V = napojená plocha × srážka, strop = objem substrátu × pórovitost (~30 % 🤔); Stockholm: 4 600 m² × 600 mm = 2,3 mil. l/rok", vzorec="V_m3 = min(A_napojena_m2 * P_m, V_substrat_m3 * 0.3)", zdroj=["embren2015"], znacka="overeno_stare"),
          kv("B","kvalitativne","Stockholm: stromy vysazené s obvodem 30-35 cm měly po 8 letech 70-83 cm (bez kontrolního srovnání); Graz MUFUWU: střešní voda doplňuje zásobu i při malých deštích, zálivka v prvních letech nutná, retence vs. klasické rabátko nevyčíslena", zdroj=["embren2015","mufuwu2024"], znacka="overeno")],
   priklady=[pr("Stockholm", "cca 2 000 stromových míst přestavěno na strukturální substrát (drcená žula 90-150 mm, od 2013 biouhel), voda ze střech a chodníků vedena do rabátek", kdy="2002-2015", kdo="město Stockholm (Embrén)", mereno="obvod kmene po 8 letech; objem vody do systému", zdroj=["embren2015"], znacka="overeno_stare"),
             pr("Graz, Leonhardgürtel", "7 nových stromů + 4 sanované kaštany v tělesech 60 cm; měření půdní vody, toku mízy, přírůstu a přítoku/odtoku 2022-2023 (projekt MUFUWU, BMK)", kdy="2021-2024", kdo="3:0 Landschaftsarchitektur, BAW, Bundesgärten, město Graz", mereno="půdní voda, tok mízy, přírůst kmene", zdroj=["mufuwu2024"]),
             pr("Vídeň Schönbrunn (HBLFA) + Graz Gradnerstraße + Seestadt", "lysimetry a dva uliční pokusy se strukturálními substráty 2019-2024; závěr: chyby při stavbě výrazně snižují hydrologický výkon, zásobování stromu plánovat spolu s retencí", kdy="2019-2024", kdo="HBLFA Schönbrunn", mereno="lysimetr (čísla v abstraktu nejsou)", zdroj=["dafne_schwammstadt"])],
   prenositelnost="Náměstí a hlavní ulice při rekonstrukci chodníků. Pod rabátkem jsou v Koryčanech pelozemě (HSP C/D): nutný bezpečnostní přepad a drenáž, jinak strom stojí ve vodě.",
   rizika="Retence proti běžnému rabátku není změřena; chyby stavby (zhutnění, jemné frakce v substrátu) výkon zničí; zálivka první 2-3 roky.")

doplnit("U03",
   kvant=[kv("I","hodnota","Taucha: 3 soustavy průleh-rýha po 25-30 letech: k_f 3e-6 až 9e-5 m/s (infiltrometr), 1e-5 až 1e-4 m/s (zaplavení celého průlehu); vyprázdnění do 24 h (DWA-A 138) splněno; návrh 10 % napojené plochy na písku, 20 % na hlíně; odstup od budov 1,5× hloubka výkopu", rozsah=[3e-6,1e-4], jednotka="m/s", zdroj=["taucha2024","iws2024_taucha"], znacka="overeno"),
          kv("Q","kvalitativne","Werther (sprašová hlína, k_f ~1e-7 m/s jako HSP D), 6,5 ha od 2000: odtok rozložen v čase místo špiček, ale rýhy v zimě dlouho zaplavené, lokální zamokření; v suchých létech prázdné - pro HSP C/D průleh s rýhou a regulovaným odtokem, ne čistý vsak", zdroj=["werther2005"], znacka="overeno_stare")],
   priklady=[pr("Taucha (Sasko)", "soustavy průleh-rýha v obytných ulicích z let 1994-1999, vyhodnocení 2023; měď a zinek z měděných okapů nad limity do 25 cm půdy (nepoužívat měď)", kdy="1994-2024", kdo="město Taucha, IWS Leipzig", mereno="k_f, doba vyprázdnění, těžké kovy", zdroj=["taucha2024"]),
             pr("Werther u Bielefeldu (NRW)", "průleh-rýha v nové zástavbě 6,5 ha na sprašové hlíně, měření 2000-2005 (hladiny v rýhách, vlhkost, podzemní voda, lysimetr)", kdy="2000-2005", kdo="FH Bielefeld, I.W.A. Minden", mereno="vsak, hladiny, podzemní voda", zdroj=["werther2005"], znacka="overeno_stare")],
   rizika="Na HSP D se voda v rýze drží týdny; bez regulovaného odtoku hrozí zamokření sousedních pozemků. Měděné okapy kontaminují půdu průlehu. Údržba: vtoky, spád, travní drn.",
   nedohledano=["cena průlehu v ČR 2025-2026 kromě NOO"])
# náklady Taucha jako cenová položka U03
next(x for x in O if x["id"]=="U03")["ceny"].append(cena("stavba průlehu / průleh + rýha (Sasko, literatura upravená)", None, "EUR/m² napojené plochy", 2024, "taucha2024", rozsah=[35,45], pozn="provoz 1-2 EUR/m² průlehu/rok; odvádění do kanalizace cca 20 EUR/m²/rok"))

doplnit("U04",
   priklady=[pr("Trebišov (SK), střední odborná škola", "dešťová zahrada 19 m², nádrž 1,5 m³ s přepadem, vsakovací rýhy 9 + 10 m², zatravňovací dlažba, zelená stěna 7,5 m s kapkovou závlahou z nádrže; účinek nevyčíslen", kdy="2021", kdo="TU Košice, škola", mereno=None, zdroj=["zelenakova_trebisov"]),
             pr("Berlín Treptow-Köpenick, školní dvory", "6 škol + hotová Schule am Altglienicker Wasserturm (2019/20): částečné odstranění asfaltu, výsadby, zasakovací průlehy; úspora poplatku za srážkovou vodu cca 1,80 EUR/m² napojené plochy/rok; měření žádné", kdy="2019-2023", kdo="Straßen- und Grünflächenamt", mereno=None, zdroj=["berlin_tk2023"])],
   prenositelnost="ZŠ, úřad, sokolovna, hasičárna = největší jednotlivé střechy v obci; nejdřív pasport svodů (U09), pak S02 + Z01/Z10/S06.")

doplnit("U05",
   priklady=[pr("Wiesenena (Sasko, obec Wiedemar)", "renaturace betonové požární nádrže: cca 1 000 m² hladiny, mělké břehy, litorál, hnízdiště břehulí, lavičky; náklady a měření neuvedeny", kdy="2008-2009", kdo="obec Wiedemar", mereno=None, zdroj=["wiesenena2009"], znacka="overeno_stare"),
             pr("Močovice", "koncepce: návesní rybník 4 530 m² hladiny, odbahnění 906 m³ (ponechat 10 cm pro těsnění), litorál, oprava hráze a výpusti; 2,5-2,8 mil. Kč bez DPH", kdy="2020", kdo="obec, VRV a.s.", mereno=None, zdroj=["vrv2020_mocovice"]),
             pr("Cehnice (Jihočeský kraj)", "retenční nádrž Třtí na Cehnickém potoce: stálá hladina 11 401 m³ + retenční prostor 50 363 m³, revitalizace přítoku s tůněmi a mokřadem; 15,95 mil. Kč (OPŽP 13,56 mil.) - spíš T07", kdy=None, kdo="obec Cehnice", mereno=None, zdroj=["smocr_cehnice"]),
             pr("Kujavy (Novojičínsko)", "'Voda pro krajinu': obnova 3 tůní svépomocí (myslivci, mladí myslivci), nadace Hyundai a OSF; rozpracováno; finalista Adapterra 2026", kdy="2025-2026", kdo="obec a spolky", mereno=None, zdroj=["kujavy2026","adapterra2026"])],
   rizika="Mikroklima návesní nádrže neměřeno; podle CzechGlobe malé vodní plochy vzduch skoro neochladí - hodnota je retence a biodiverzita.",
   nedohledano=["mikroklima návesní nádrže"])

doplnit("U07",
   priklady=[pr("Trebišov (SK)", "školní atria: dešťová zahrada, nádrž, vsakovací rýhy, zelená stěna (viz U04)", kdy="2021", kdo="TU Košice", mereno=None, zdroj=["zelenakova_trebisov"])],
   synergie=["U09"])

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
    for p in o["priklady"]:
        for zid in p["zdroj"]:
            assert zid in Z, f"{o['id']}: neznámý zdroj příkladu {zid}"
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
      "id":{"type":"string","pattern":"^(Z|S|U|P|L|LES|T|C|M|H)[0-9]{2}$"},
      "misto":{"type":"array","items":{"enum":["Z","S","U","P","L","LES","T","C","H"]}},
      "rozhoduje":{"type":"array","items":{"enum":["J","V","O","SP","S"]}},
      "pracnost":{"type":"integer","minimum":1,"maximum":3},
      "ucinky":{"type":"object","properties":{"primarni":{"type":"array","items":{"enum":["R","I","Q","E","CH","ER","B","W"]}},"vedlejsi":{"type":"array","items":{"enum":["R","I","Q","E","CH","ER","B","W"]}}}},
      "meritko":{"enum":["pozemek","lokalita","uzemi"]},
      "kvantifikace":{"type":"array","items":{"type":"object","required":["ucinek","typ","popis","znacka"],"properties":{"typ":{"enum":["vzorec","hodnota","kvalitativne"]},"znacka":{"enum":["overeno","overeno_stare","citace","odhad","pamet"]},"zdroj":{"type":["array","null"],"items":{"type":"string"}}}}},
      "povoleni":{"type":["integer","null"],"minimum":0,"maximum":2},
      "ceny":{"type":"array","items":{"type":"object","required":["polozka","jednotka"],"properties":{"hodnota":{"type":["number","null"]},"rozsah":{"type":["array","null"]},"rok":{"type":["integer","null"]},"zdroj":{"type":["string","null"]}}}},
      "priklady":{"type":"array","items":{"type":"object","required":["kde","co","zdroj","znacka"],"properties":{"kde":{"type":"string"},"kdy":{"type":["string","null"]},"kdo":{"type":["string","null"]},"co":{"type":"string"},"mereno":{"type":["string","null"]},"zdroj":{"type":"array","items":{"type":"string"}},"znacka":{"enum":["overeno","overeno_stare","citace","odhad","pamet"]}}}},
      "prenositelnost":{"type":["string","null"]},
      "rizika":{"type":["string","null"]},
      "vahy_skaly":{"type":["object","null"],"description":"rezervováno: sucho, prival, vedro, vitr_mraz, biodiverzita 0-3 (NAPADY-ROZHRANI.md)"}
    }}}
 }
}
with open(os.path.join(OUT,"opatreni.schema.json"),"w",encoding="utf-8") as f:
    json.dump(SCHEMA, f, ensure_ascii=False, indent=1)

print("opatreni:", len(O), "zdroje:", len(Z), "programy:", len(PROGRAMY))
print("ceny neověřené:", sum(1 for o in O for c in o["ceny"] if c["hodnota"] is None and c["rozsah"] is None))
print("priklady:", sum(len(o["priklady"]) for o in O), "opatreni s priklady:", sum(1 for o in O if o["priklady"]))
print("kvantifikace celkem:", sum(len(o["kvantifikace"]) for o in O), "z toho kvalitativně:", sum(1 for o in O for k in o["kvantifikace"] if k["typ"]=="kvalitativne"))
