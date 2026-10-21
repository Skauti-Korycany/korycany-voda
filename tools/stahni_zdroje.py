# -*- coding: utf-8 -*-
"""Stáhne archivní kopie podkladů ke katalogu opatření (fotky, PDF) do složky
..\\zdroje-archiv\\<id> vedle složky repo. Složka je MIMO git: fotky a PDF
jsou autorské, do veřejného repozitáře nepatří. Spouští se poklepáním
na tools\\stahni_zdroje.bat nebo: python tools/stahni_zdroje.py

Seznam ZDROJE doplňovat po blocích rešerše (docs/KATALOG-RESERSE.md).
"""
import os, sys, urllib.request, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # ...\repo
ARCHIV = os.path.join(os.path.dirname(ROOT), "zdroje-archiv")                # ...\zdroje-archiv

ZDROJE = {
    # id opatření / zdroje : (popis, [url, ...])
    "Z12_olla_felixova2025": ("Felixová M., Záhrada.sk 15. 4. 2025, fotopostup výroby olly ze dvou květináčů (17 fotografií + úvodní)",
        ["https://www.zahrada.sk/wp-content/uploads/2025/04/ako-vyrobit-zavlazovacie-nadoby-olla.jpg"]
        + [f"https://www.zahrada.sk/wp-content/uploads/2025/04/{i}_olla_DIY_felixova.jpg" for i in (1,2,3,4,5)]
        + ["https://www.zahrada.sk/wp-content/uploads/2025/04/6__olla_DIY_felixova.jpg"]
        + [f"https://www.zahrada.sk/wp-content/uploads/2025/04/{i}_olla_DIY_felixova.jpg" for i in (7,8,9)]
        + [f"https://www.zahrada.sk/wp-content/uploads/2025/04/{i}_ola_DIY_felixova.jpg" for i in range(10,17)]
        + ["https://www.zahrada.sk/wp-content/uploads/2025/04/17_TIP_ola_DIY_felixova.jpg"]),
    "Z12_olla_arizona2021": ("University of Arizona Extension AZ1911, Irrigating with Ollas (Nickel, Brischke, 5/2021)",
        ["https://extension.arizona.edu/sites/default/files/2024-08/az1911-2021.pdf"]),
    "Z13_lwg_mischpflanzungen2021": ("LWG Veitshöchheim, Staudenmischpflanzungen (2021)",
        ["https://lwg.bayern.de/mam/cms06/landespflege/dateien/mischpflanzen_bf.pdf"]),
    "Z01_lwg_versickern2010": ("LWG Veitshöchheim, Mit Pflanzen versickern (2010)",
        ["https://www.lwg.bayern.de/mam/cms06/landespflege/dateien/merkblatt_mit_pflanzen_versickern.pdf"]),
    "Z04_nrw2005_belaege": ("MUNLV NRW 2005, Prüfung wasserdurchlässiger Flächenbeläge nach mehrjähriger Betriebsdauer",
        ["https://www.lanuk.nrw.de/fileadmin/forschung/wasser/sonstiges/Kurzbericht_wasserdurchl_Flaeche.pdf"]),
    "Z04_bayern2003_entsiegelung": ("Bayerischer Landesverband für Gartenbau 2003, Mehr Grün durch Bodenentsiegelung",
        ["https://mv.gartenbauvereine.org/wp-content/uploads/2020/05/MehrGruendurchBodenentsiegelung.pdf"]),
    "Z05_dwd_mulch": ("DWD Agrarmeteorologie, Wirkung einer Mulchbedeckung auf die Evaporation (pokusy 2012-2014)",
        ["https://www.gartenbau.sachsen.de/download/Die_Wirkung_einer_Mulchbedeckung_auf_die_Evaporation.pdf"]),
    "S05_szu2022_seda": ("SZÚ, Kožíšek a kol. 2022, Hygiena 67(4), zdravotní rizika šedých vod",
        ["https://hygiena.szu.cz/pdfs/hyg/2022/04/02.pdf"]),
    "S05_nolde2026": ("IVV 5/2026, rozhovor E. Nolde, šedá voda Berlín",
        ["https://www.vermieter-ratgeber.de/sites/default/files/public/data-fachartikel/IVV_2026_05_Vier-Fragen-an-Dipl_-Ing_-Erwin-Nolde_40-41.pdf"]),
    "S06_praha14_2022": ("MČ Praha 14, leták Voda 2022 (spotřeba podle činností)",
        ["https://www.praha14.cz/app/uploads/sites/4/2022/06/Letak-Voda-2022.pdf"]),
    "D_cyprus_terasy_egu2017": ("Camera a kol., EGU 2017, suché kamenné terasy Troodos (pro blok D)",
        ["https://meetingorganizer.copernicus.org/EGU2017/EGU2017-7404.pdf?pdf"]),
}

HDR = {"User-Agent": "Mozilla/5.0 (archiv podkladu korycany-voda; nekomercni)"}

def main():
    os.makedirs(ARCHIV, exist_ok=True)
    ok = chyby = preskoceno = 0
    for sid, (popis, urls) in ZDROJE.items():
        slozka = os.path.join(ARCHIV, sid)
        os.makedirs(slozka, exist_ok=True)
        with open(os.path.join(slozka, "ZDROJ.txt"), "w", encoding="utf-8") as f:
            f.write(popis + "\n\nStaženo: " + time.strftime("%Y-%m-%d") + "\nURL:\n" + "\n".join(urls) + "\n")
        for url in urls:
            jmeno = url.split("/")[-1].split("?")[0]
            cil = os.path.join(slozka, jmeno)
            if os.path.exists(cil) and os.path.getsize(cil) > 0:
                preskoceno += 1; continue
            try:
                req = urllib.request.Request(url, headers=HDR)
                with urllib.request.urlopen(req, timeout=60) as r, open(cil, "wb") as f:
                    f.write(r.read())
                ok += 1; print("OK ", sid, jmeno)
            except Exception as e:
                chyby += 1; print("CHYBA", sid, jmeno, e)
                if os.path.exists(cil): os.remove(cil)
    print(f"\nHotovo: staženo {ok}, přeskočeno (už bylo) {preskoceno}, chyby {chyby}\nSložka: {ARCHIV}")

if __name__ == "__main__":
    main()
