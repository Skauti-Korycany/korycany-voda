# -*- coding: utf-8 -*-
"""Doplní docs/KATALOG-Z-S.md, KATALOG-U-P.md, KATALOG-L-LES-T-C.md o sekci
"Doplnění z rešerše dobré praxe" generovanou z data/opatreni.json (zdroj pravdy
tools/build_opatreni.py). Sekce se při každém spuštění přepíše celá (mezi značkami),
takže se MD soubory nemohou rozejít s JSON. Spustit po build_opatreni.py:
    python tools/build_katalog_md.py
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "opatreni.json"), encoding="utf-8"))
ZN = D["ciselniky"]["znacka"]; ZNS = {k: v.split(" ")[0] for k, v in ZN.items()}
UC = D["ciselniky"]["ucinek"]; Z = D["zdroje"]

# zdroje přidané rešerší = definované za značkou "# --- blok" v build_opatreni.py
src = open(os.path.join(ROOT, "tools", "build_opatreni.py"), encoding="utf-8").read()
NOVE_ZDROJE = set(re.findall(r'^zdroj\("([^"]+)"', src[src.index("# --- blok B"):], re.M))
NOVA_ID = {"Z12","Z13","S05","S06","U08","U09","H01","H02"}

SOUBORY = {
    "KATALOG-Z-S.md": ("Z","S"),
    "KATALOG-U-P.md": ("U","H","P"),
    "KATALOG-L-LES-T-C.md": ("L","LES","T","C"),
}
ZAC = "<!-- RESERSE-START (generováno tools/build_katalog_md.py, needitovat ručně) -->"
KON = "<!-- RESERSE-END -->"

def zdr(ids):
    out = []
    for i in ids or []:
        z = Z.get(i)
        if not z: continue
        nm = z["nazev"].split(":")[0][:70]
        out.append(f"[{nm}]({z['url']})" if z.get("url") else nm)
    return "; ".join(out)

def blok(o):
    nove_kv = [k for k in o["kvantifikace"] if set(k.get("zdroj") or []) & NOVE_ZDROJE]
    if o["id"] in NOVA_ID: nove_kv = o["kvantifikace"]
    if not (nove_kv or o["priklady"] or o.get("prenositelnost") or o.get("rizika")): return ""
    L = [f"### {o['id']} {o['nazev']}" + (" (nové)" if o["id"] in NOVA_ID else " (doplněno)")]
    if o["id"] in NOVA_ID and o.get("popis"): L.append(f"- Co to je: {o['popis']}")
    for k in nove_kv:
        r = ""
        if k.get("rozsah"): r = f" [{k['rozsah'][0]}-{k['rozsah'][1]} {k.get('jednotka') or ''}]"
        elif k.get("hodnota") is not None: r = f" [{k['hodnota']} {k.get('jednotka') or ''}]"
        L.append(f"- Účinek {UC.get(k['ucinek'], k['ucinek'])} ({k['typ']}) {ZNS.get(k['znacka'],'')}: {k['popis']}{r}. Zdroj: {zdr(k.get('zdroj'))}")
    for p in o["priklady"]:
        L.append(f"- Kde to funguje: **{p['kde']}**" + (f" ({p['kdy']})" if p.get("kdy") else "") + f": {p['co'].rstrip('.')}. " + (f"Měřeno: {p['mereno'].rstrip('.')}." if p.get("mereno") else "Bez měření.") + f" {ZNS.get(p['znacka'],'')} {zdr(p.get('zdroj'))}")
    if o.get("prenositelnost"): L.append(f"- Přenositelnost do Koryčan: {o['prenositelnost']}")
    if o.get("rizika"): L.append(f"- Rizika, co z toho neplyne: {o['rizika']}")
    if o["id"] in NOVA_ID:
        c = [f"{x['polozka']}: " + (f"{x['hodnota']} {x['jednotka']}" if x.get("hodnota") is not None else (f"{x['rozsah'][0]}-{x['rozsah'][1]} {x['jednotka']}" if x.get("rozsah") else "cena neověřena")) for x in o["ceny"]]
        if c: L.append("- Kč: " + "; ".join(c))
        L.append(f"- Povolení: {o.get('povoleni')}" + (f" ({o['povoleni_pozn']})" if o.get("povoleni_pozn") else ""))
    if o.get("nedohledano"): L.append("- Nedohledáno: " + "; ".join(o["nedohledano"]))
    return "\n".join(L) + "\n"

for fn, kat in SOUBORY.items():
    p = os.path.join(ROOT, "docs", fn)
    s = open(p, encoding="utf-8").read()
    bloky = [blok(o) for o in D["opatreni"] if o["id"].rstrip("0123456789") in kat]
    bloky = [b for b in bloky if b]
    sekce = (f"{ZAC}\n## Doplnění z rešerše dobré praxe (bloky B, A, C, D, 21.-22. 10. 2026)\n\n"
             f"Generováno z `data/opatreni.json` v{D['meta']['verze']} ({D['meta']['datum']}); podrobný rozbor a odkazy: `docs/KATALOG-RESERSE.md`. "
             f"Uvedeny jen nové položky a kvantifikace, příklady, přenositelnost a rizika doplněné rešerší; původní text výše platí dál. "
             f"Značky: ✅ ověřeno online, ✅⏳ zdroj starší 12 měsíců, 📄 citace, 🤔 odhad.\n\n" + "\n".join(bloky) + KON)
    if ZAC in s:
        s = s[:s.index(ZAC)] + sekce + s[s.index(KON)+len(KON):]
    else:
        s = s.rstrip("\n") + "\n\n---\n\n" + sekce + "\n"
    open(p, "w", encoding="utf-8").write(s)
    print(fn, "bloků:", len(bloky))
