# -*- coding: utf-8 -*-
"""Sestaví dummy náhled rozhraní (jeden HTML soubor) ze syntetických dat + reálného opatreni.json.
Spustit z libovolné složky: python tools/build_dummy.py -> prototyp/index.html a index.html (GitHub Pages)
"""
import json, re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, "tools", "vendor", "leaflet-1.9.4")

OP = json.load(open(os.path.join(ROOT, "data", "opatreni.json"), encoding="utf-8"))
LEAFLET_CSS = open(os.path.join(VENDOR, "leaflet.css"), encoding="utf-8").read()
LEAFLET_JS = open(os.path.join(VENDOR, "leaflet.js"), encoding="utf-8").read()
# leaflet.css odkazuje na images/ - ikony nahradíme vlastními kruhy, odkazy vyčistíme
LEAFLET_CSS = re.sub(r"url\(images/[^)]+\)", "none", LEAFLET_CSS)

# zúžený JSON pro prohlížeč
data = {
    "meta": OP["meta"], "ciselniky": OP["ciselniky"], "konstanty": OP["konstanty"],
    "zdroje": {k: {"nazev": v["nazev"], "url": v["url"], "rok": v["rok"], "znacka": v["znacka"]} for k, v in OP["zdroje"].items()},
    "programy": OP["programy"], "nastroje": OP["nastroje"],
    "opatreni": [{k: o[k] for k in ("id","nazev","popis","misto","rozhoduje","pracnost","ucinky","meritko","kontext","kvantifikace","vhodnost","vazby","povoleni","povoleni_pozn","ceny","financovani","standardy","nedohledano","pozn_poctivost","priklady","prenositelnost","rizika","hlavni_cislo")} for o in OP["opatreni"]],
}
# skutecna data o uzemi (faze 2): budovy, CN/odtok, povodi, srazky
BUD = json.load(open(os.path.join(ROOT, "data", "budovy_info.json"), encoding="utf-8"))
CNI = json.load(open(os.path.join(ROOT, "data", "cn_info.json"), encoding="utf-8"))
SRA = json.load(open(os.path.join(ROOT, "data", "srazky_chmi.json"), encoding="utf-8"))
kor = SRA["denni"]["0-203-0-41701068002"]
data["uzemi"] = {
    "zdroj": "budovy_info.json (ČÚZK INSPIRE BU), cn_info.json (06_cn.py), srazky_chmi.json (ČHMÚ Koryčany)",
    "plocha_ha": CNI["uzemi_modelu"]["plocha_ha"], "cn_vazene": CNI["uzemi_modelu"]["cn_vazene"],
    "odtok": CNI["uzemi_modelu"]["odtok"],
    "rd_pocet": BUD["podle_ucelu"]["rodinný dům"]["pocet"], "rd_strechy_m2": BUD["podle_ucelu"]["rodinný dům"]["plocha_strech_m2"],
    "budov": BUD["budov_v_uzemi_modelu"], "strechy_m2": BUD["plocha_pudorysu_v_uzemi_m2"],
    "podle_povodi": BUD["podle_povodi"], "podle_ucelu": BUD["podle_ucelu"],
    "srazky": {"normal_mm": kor["normal_1991_2020_mm"], "n_lete_denni_mm": kor["n_lete_denni_mm_gumbel"], "max_denni": [(x["max_denni_datum"], x["max_denni_mm"]) for x in sorted(kor["rocni"].values(), key=lambda x: -x["max_denni_mm"])[:3]], "mesicni_mm": kor["normal_mesicni_mm"]},
}
NS = json.load(open(os.path.join(ROOT, "data", "navrhove_srazky.json"), encoding="utf-8"))
data["navrhove"] = {"uhrny_6h_mm": NS["uhrny_6h_mm"], "podil_tvaru_pct": NS["podil_tvaru_pct"], "qAPI": NS["qAPI"], "tvary_popis": NS["tvary_popis"]}
data["srazky_hist"] = kor.get("histogram_denni_1991_2020")   # None, dokud 07_srazky_chmi.py nebezi znovu
CNT = json.load(open(os.path.join(ROOT, "data", "cn_tabulka.json"), encoding="utf-8"))
data["cn_tabulka"] = {k: {"nazev": v["nazev"], "vychozi": v["vychozi"], "varianty": {n: x["cn"] for n, x in v["varianty"].items()}} for k, v in CNT["tridy"].items()}
# pocasi "Jak bylo" (12_pocasi.py + 13_normaly_pocasi.py); zhustene: den -> [P, zdrojP, T, Tmin, Tmax, ET0]
POC = json.load(open(os.path.join(ROOT, "data", "pocasi", "denni.json"), encoding="utf-8"))
NRM = json.load(open(os.path.join(ROOT, "data", "pocasi", "normaly.json"), encoding="utf-8"))
ZDR_P = {"chmu_korycany": "K", "pmo_korycany": "P", "chmu_nemochovice": "N", None: ""}
data["pocasi"] = {
    "vytvoreno": POC["vytvoreno"], "stanice": POC["stanice"], "metoda": POC["metoda"],
    "dny": {d: [v.get("P"), ZDR_P.get(v.get("zdroj_P"), ""), v.get("T"), v.get("Tmin"), v.get("Tmax"), v.get("ET0")] for d, v in POC["dny"].items()},
    "normaly": {"obdobi": NRM["obdobi"], "rok": NRM["rok"], "mesic": NRM["mesic"], "rekordy": NRM["rekordy"],
                "rocniky": {r: {"P": z.get("P", {}).get("rok"), "Pm": [z.get("P", {}).get(str(m)) for m in range(1, 13)],
                                "T": z.get("T", {}).get("rok"), "ET0": z.get("ET0", {}).get("rok"), "bil": z.get("bil", {}).get("rok"),
                                "d30": z.get("T", {}).get("dni_nad_30"), "d0": z.get("T", {}).get("dni_pod_0"),
                                "Tx": z.get("T", {}).get("max_den"), "d35": z.get("T", {}).get("dni_nad_35"),
                                "tn": z.get("T", {}).get("tropicke_noci"), "lx": z.get("leto", {}).get("Tmax"), "dopl": z.get("dopl")} for r, z in NRM["rocniky"].items()},
                "doplneni": NRM.get("doplneni"),
                "leto_normal": NRM.get("leto_normal")},
}
DATA_JS = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<title>Voda v Koryčanech</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: mapa nahoře (nebo vlevo na širokém), pracovní panel pod ní; čísla v mono, nadpisy serif s charakterem. */
:root{
  --bg:#f6f3ee; --panel:#ffffff; --fg:#1f2a2e; --muted:#5c6b70; --line:#d8d2c7;
  --accent:#1f6f8b; --accent-ink:#ffffff; --soil:#7a5a3a; --water:#2d7fb8; --ok:#3b7a57; --warn:#b5651d; --bad:#a23b3b; --dry:#b8923a; --hot:#6b1d4a;
  --chip:#e9e4da; --mark:#eef4f7;
  --f-display:"Fraunces", Georgia, "Times New Roman", serif;
  --f-body:"IBM Plex Sans", "Segoe UI", Arial, sans-serif;
  --f-mono:"IBM Plex Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#171c1f; --panel:#1f2629; --fg:#e8e4dc; --muted:#a3adb1; --line:#36414a;
  --accent:#5aa9c9; --accent-ink:#0f1a1f; --soil:#c49a6c; --water:#6fb3e0; --ok:#7fc39a; --warn:#e0a060; --bad:#e08080; --dry:#d4b26a; --hot:#f07ac0;
  --chip:#2b353a; --mark:#1b2a31; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#171c1f; --panel:#1f2629; --fg:#e8e4dc; --muted:#a3adb1; --line:#36414a;
  --accent:#5aa9c9; --accent-ink:#0f1a1f; --soil:#c49a6c; --water:#6fb3e0; --ok:#7fc39a; --warn:#e0a060; --bad:#e08080; --dry:#d4b26a; --hot:#f07ac0;
  --chip:#2b353a; --mark:#1b2a31; color-scheme:dark }
html,body{height:100%}
body{background:var(--bg);color:var(--fg);font-family:var(--f-body);font-size:15px;line-height:1.45;margin:0}
*{box-sizing:border-box}
h1,h2,h3{font-family:var(--f-display);font-weight:600;letter-spacing:-.01em;text-wrap:balance;margin:0}
h1{font-size:1.5rem} h2{font-size:1.2rem} h3{font-size:1.05rem}
.num{font-family:var(--f-mono);font-variant-numeric:tabular-nums}
header.top{display:flex;flex-wrap:wrap;gap:.5rem 1rem;align-items:baseline;padding-block:.7rem;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));border-bottom:1px solid var(--line);background:var(--panel)}
header.top .tag{font-size:.75rem;color:var(--muted);letter-spacing:.06em;text-transform:uppercase}
nav.tabs{display:flex;gap:.25rem;flex-wrap:wrap;margin-left:auto}
nav.tabs button{background:none;border:1px solid var(--line);color:var(--fg);padding:.35rem .7rem;border-radius:999px;cursor:pointer;font:inherit;font-size:.9rem}
nav.tabs button[aria-selected="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
nav.tabs button:focus-visible,button:focus-visible,select:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.banner{font-size:.8rem;color:var(--muted);padding:.4rem 0;border-bottom:1px dashed var(--line);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
main{padding-block:1rem 2rem;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));max-width:1200px;margin:0 auto}
.grid{display:grid;grid-template-columns:1fr;gap:1rem}
@media(min-width:900px){.grid.two{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}}
.grid>*{min-width:0}
#map{height:340px;border:1px solid var(--line);border-radius:6px;background:#dfe7ea}
@media(min-width:900px){#map{height:520px}}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:.9rem 1rem}
.panel+.panel{margin-top:1rem}
.kv{display:grid;grid-template-columns:auto 1fr;gap:.25rem .8rem;font-size:.92rem}
.kv dt{color:var(--muted)} .kv dd{margin:0}
label.f{display:grid;gap:.2rem;font-size:.85rem;color:var(--muted)}
label.f input,label.f select{font:inherit;font-size:.95rem;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:4px;padding:.35rem .5rem;width:100%}
.inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.6rem}
.step{margin-top:1rem}
.eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
table.flow{width:100%;border-collapse:collapse;font-size:.92rem;margin-top:.5rem}
table.flow th,table.flow td{text-align:left;padding:.3rem .4rem;border-bottom:1px solid var(--line)}
table.flow td.num,table.flow th.num{text-align:right}
table.flow tr.total td{font-weight:600}
#tab-uzemi table.flow{display:block;overflow-x:auto;max-width:100%}
.cards>*{min-width:0} .card{overflow-wrap:anywhere}
.card .meta .chip{max-width:100%;white-space:normal;min-width:0}
.bars{display:grid;gap:.35rem;margin-top:.6rem}
.bar{display:grid;grid-template-columns:7.5rem 1fr 4.5rem;align-items:center;gap:.5rem;font-size:.85rem}
.bar .track{height:14px;background:var(--chip);border-radius:3px;overflow:hidden;display:flex}
.bar .track i{display:block;height:100%}
.bar .track .away{background:var(--bad)} .bar .track .kept{background:var(--water)}
.legend{font-size:.8rem;color:var(--muted);display:flex;gap:1rem;flex-wrap:wrap}
.legend b{display:inline-block;width:.8rem;height:.8rem;border-radius:2px;vertical-align:-1px;margin-right:.3rem}
.cards{display:grid;gap:.6rem;margin-top:.6rem}
.card{border:1px solid var(--line);border-radius:6px;padding:.7rem .8rem;background:var(--panel)}
.card.on{border-color:var(--accent);background:var(--mark)}
.card header{display:flex;gap:.6rem;align-items:flex-start}
.card header input{margin-top:.3rem;width:1.1rem;height:1.1rem;flex:none}
.card header .t{flex:1;min-width:0}
.card header .t b{font-weight:600}
.card .meta{display:flex;flex-wrap:wrap;gap:.3rem .5rem;font-size:.78rem;color:var(--muted);margin-top:.25rem}
.chip{background:var(--chip);border-radius:999px;padding:.05rem .5rem;white-space:nowrap}
.chip.id{font-family:var(--f-mono)}
.card .eff{font-size:.9rem;margin-top:.4rem}
.card .eff .num{font-weight:500}
.card details{margin-top:.4rem;font-size:.85rem}
.card details summary{cursor:pointer;color:var(--accent)}
.card details ul{margin:.3rem 0 0;padding-left:1.1rem}
.card details.kde summary{font-weight:500}
.card details.kde li{margin-bottom:.25rem}
.card details.kde .note{margin-top:.35rem}
.mark{font-size:.75rem;vertical-align:1px}
.note{font-size:.85rem;color:var(--muted)}
.callout{border-left:3px solid var(--warn);padding:.5rem .8rem;background:var(--mark);border-radius:0 6px 6px 0;font-size:.92rem;margin-top:.8rem}
.callout.ok{border-left-color:var(--ok)}
.motiv{margin-top:1rem;padding:1rem 1.1rem;border-radius:8px;background:var(--water);color:#fff;font-size:1rem}
.motiv p{margin:.35rem 0}
.motiv .mot-h{font-family:var(--f-display);font-size:1.25rem;font-weight:700}
.motiv .mot-a{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem}
.motiv .mot-a a{background:#fff;color:var(--water);font-weight:600;text-decoration:none;padding:.4rem .8rem;border-radius:999px}
.motiv .mot-a a:hover,.motiv .mot-a a:focus-visible{outline:2px solid #fff;outline-offset:2px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .motiv{color:#0f1a1f} :root:not([data-theme="light"]) .motiv .mot-a a{background:#0f1a1f}}
.unfit{margin-top:.8rem;font-size:.88rem}
.unfit li{margin:.15rem 0}
.big{font-family:var(--f-display);font-size:2rem;font-weight:700;line-height:1.1}
.sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem;margin-top:.6rem}
.sum .box{border-top:2px solid var(--water);padding-top:.4rem}
.sum .box small{display:block;color:var(--muted);font-size:.78rem}
input[type=range]{width:100%}
.filters{display:flex;flex-wrap:wrap;gap:.4rem;margin:.6rem 0}
.kde{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.5rem;margin:.6rem 0}
.kde button{font:inherit;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:10px;padding:.6rem .5rem;cursor:pointer;min-height:56px;line-height:1.2}
.kde button b{display:block;font-size:1rem}.kde button span{font-size:.78rem;color:var(--muted)}
.kde button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}.kde button[aria-pressed="true"] span{color:var(--accent-ink);opacity:.85}
.co{display:flex;flex-wrap:wrap;gap:.4rem;margin:.4rem 0 .6rem}
.co button{font:inherit;font-size:.9rem;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:.35rem .8rem;cursor:pointer;min-height:40px}
.co button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.card .one{font-size:.95rem;margin-top:.35rem}.card .one b{font-weight:600}
.card .pr{font-size:.7rem;color:var(--muted);margin-left:.5rem;letter-spacing:.1em;vertical-align:middle;cursor:help}
.card .zivot{font-size:.8rem;color:var(--ok);margin-top:.25rem}
.filters button{font:inherit;font-size:.82rem;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:.2rem .6rem;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.src{font-size:.8rem;color:var(--muted)} .src a{color:var(--accent)}
.hidden-tab{display:none}
/* Jak bylo */
.jb-head{display:flex;flex-wrap:wrap;gap:.6rem 1rem;align-items:end}
.jb-head label.f{min-width:160px}
.jb-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.8rem;margin-top:.8rem}
.jb-card{border:1px solid var(--line);border-radius:6px;padding:.7rem .8rem;background:var(--panel);border-top:3px solid var(--water)}
.jb-card.t{border-top-color:var(--warn)} .jb-card.p{border-top-color:var(--bad)} .jb-card.e{border-top-color:var(--soil)} .jb-card.b{border-top-color:var(--ok)} .jb-card.n{border-top-color:var(--accent)} .jb-card.s{border-top-color:var(--hot)}
.jb-card .big{font-size:1.7rem}
.jb-card .cmp{font-size:.85rem;margin-top:.15rem}
.jb-card .cmp b{font-weight:600}
.jb-card .cmp.plus b{color:var(--water)} .jb-card .cmp.minus b{color:var(--bad)}
.jb-card .src{margin-top:.35rem}
.jb-chart{width:100%;height:auto;margin-top:.6rem;display:block;font-family:var(--f-mono);font-size:10px}
.jb-chart .ax{stroke:var(--line);stroke-width:1}
.jb-chart text{fill:var(--muted)}
.jb-chart .bP{fill:var(--water)} .jb-chart .bPn{fill:var(--water);opacity:.45}
.jb-chart .lT{fill:none;stroke:var(--warn);stroke-width:1.6}
.jb-chart .lE{fill:none;stroke:var(--soil);stroke-width:1.4;stroke-dasharray:3 2}
.jb-chart .lX{fill:none;stroke:var(--bad);stroke-width:1.2}
.jb-chart .thr{stroke:var(--bad);stroke-width:1;stroke-dasharray:5 3} .jb-chart .thr.s{stroke:var(--hot)}
.jb-chart text.thr-t{fill:var(--bad);font-size:9.5px;paint-order:stroke;stroke:var(--panel);stroke-width:3px;stroke-linejoin:round} .jb-chart text.thr-t.s{fill:var(--hot)}
.legend b.ln{background:none;height:0;width:1rem;border-top:2px solid;border-radius:0;vertical-align:3px}
.jb-chart .rY{fill:var(--chip)} .jb-chart .rY.now{fill:var(--accent)} .jb-chart .rY.hi{fill:var(--water)} .jb-chart .rY.lo{fill:var(--bad)} .jb-chart .rY.dry{fill:var(--dry)}
.jb-chart .dmk{fill:var(--muted)}
.jb-chart .nrm{stroke:var(--fg);stroke-width:1;stroke-dasharray:4 3}
.jb-ext{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:.4rem .8rem;font-size:.9rem;margin-top:.5rem}
.jb-ext div{display:flex;justify-content:space-between;gap:.5rem;border-bottom:1px dashed var(--line);padding:.2rem 0}
.jb-ext span:last-child{white-space:nowrap}
.jb-rank{font-size:.92rem;margin-top:.5rem}
footer{font-size:.78rem;color:var(--muted);margin-top:2rem;border-top:1px solid var(--line);padding-top:.6rem}
.leaflet-container{font:inherit}
.leaflet-container a{color:var(--accent)}
.leaflet-control-layers-toggle{width:auto!important;height:auto!important;padding:.2rem .5rem;font-size:.8rem}
.leaflet-control-layers-toggle::after{content:"vrstvy"}
.pin{width:14px;height:14px;border-radius:50%;background:var(--water);border:2px solid #fff;box-shadow:0 0 0 2px var(--water)}
@media (prefers-reduced-motion: no-preference){.card{transition:background .15s,border-color .15s}}

/* ---- Muj pozemek: pruvodce po krocich (varianta A, 21. 10. 2026) ---- */
.pz-prog ol{list-style:none;margin:0 0 .8rem;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px}
.pz-prog button{width:100%;font:inherit;font-size:.78rem;color:var(--muted);background:none;border:0;border-top:5px solid var(--chip);padding:.35rem .1rem 0;text-align:left;cursor:pointer;display:flex;gap:.3rem;align-items:baseline;min-height:40px;line-height:1.2}
.pz-prog button .n{font-family:var(--f-mono);font-weight:500}
.pz-prog button.done{border-top-color:var(--accent);color:var(--fg)}
.pz-prog button[aria-current="step"]{border-top-color:var(--water);color:var(--fg);font-weight:600}
.pz-prog button:disabled{cursor:default;opacity:.7}
.pz-grid{display:grid;grid-template-columns:1fr;gap:1rem}
.pz-grid>*{min-width:0}
.pz-ask{background:var(--mark);border-left:3px solid var(--water);border-radius:0 6px 6px 0;padding:.5rem .7rem;margin-bottom:.5rem;font-size:.95rem}
.pz-mapwrap{position:relative}
.pz #map{height:max(320px,calc(100svh - 330px));transition:height .2s}
.pz-mapcover{display:none;position:absolute;inset:0;z-index:900;width:100%;background:transparent;border:0;cursor:pointer;font:inherit;font-weight:600;color:var(--fg)}
.pz[data-step]:not([data-step="1"]) .pz-mapcover{display:flex;align-items:flex-start;justify-content:flex-end;padding:.5rem}
.pz-mapcover span{background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:999px;padding:.3rem .7rem;font-size:.85rem;box-shadow:0 1px 4px rgba(0,0,0,.15)}
.pz-mapcover:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.pz[data-step]:not([data-step="1"]) #map{height:120px}
.pz[data-step]:not([data-step="1"]) .leaflet-control-container,.pz[data-step]:not([data-step="1"]) #w-parc-x,.pz[data-step]:not([data-step="1"]) .pz-only1,.pz[data-step]:not([data-step="1"]) .pz-ask,.pz[data-step]:not([data-step="1"]) .pz-maphint{display:none}
.pz-sel{font-size:.9rem;margin-top:.45rem}
.pz-maphint{margin:.35rem 0 0}
.linkbtn{font:inherit;background:none;border:0;padding:0;color:var(--accent);text-decoration:underline;cursor:pointer}
.pz-step{display:none}
.pz[data-step="1"] .pz-step[data-s="1"],.pz[data-step="2"] .pz-step[data-s="2"],.pz[data-step="3"] .pz-step[data-s="3"],.pz[data-step="4"] .pz-step[data-s="4"],.pz[data-step="5"] .pz-step[data-s="5"]{display:block}
.pz-step>h2{margin-bottom:.5rem}
.pz-known{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:.6rem .8rem;margin-top:.6rem}
.pz[data-step="1"] .pz-known{display:none}
.pz-known dl{margin:.3rem 0 0}
.pz-known:not(.ukaz) .note,.pz-known:not(.ukaz) .pz-det{display:none}
.pz-known .eyebrow{display:flex;gap:.6rem;align-items:baseline;justify-content:space-between}
.pz-known .eyebrow .linkbtn{text-transform:none;letter-spacing:0;font-size:.8rem}
details.pz-mini{margin-top:.3rem;font-size:.85rem} details.pz-mini>summary{cursor:pointer;color:var(--accent);min-height:36px;display:flex;align-items:center}
.pz-nav{position:sticky;bottom:0;z-index:1100;display:flex;gap:.5rem;justify-content:flex-end;background:var(--bg);border-top:1px solid var(--line);margin-top:1rem;padding-top:.6rem;padding-bottom:calc(.6rem + env(safe-area-inset-bottom,0px))}
.pz-btn{font:inherit;font-weight:600;min-height:46px;padding:.6rem 1.1rem;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
.pz-btn.pri{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.pz-btn:disabled{opacity:.45;cursor:not-allowed}
.pz[data-step="1"] #pz-back{visibility:hidden}
@media(max-width:899px){.pz-btn.pri{flex:1}}
@media(min-width:900px){
  .pz[data-step="1"] .pz-grid{grid-template-columns:minmax(0,7fr) minmax(0,4fr)}
  .pz[data-step="1"] #map{height:max(440px,calc(100vh - 310px))}
  .pz[data-step]:not([data-step="1"]) .pz-grid{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
  .pz[data-step]:not([data-step="1"]) .pz-mapcol{position:sticky;top:.5rem;align-self:start}
  .pz[data-step]:not([data-step="1"]) #map{height:260px}
}
@media (prefers-reduced-motion: reduce){.pz #map{transition:none}}
.pz-search{display:flex;gap:.4rem;margin-bottom:.4rem;flex-wrap:wrap}
.pz-search input{flex:1 1 12rem;min-width:0;font:inherit;font-size:1rem;min-height:46px;padding:.5rem .7rem;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--fg)}
.pz-search .pz-btn{padding:.5rem .8rem}
.pz-sug{display:grid;gap:2px;margin:-.2rem 0 .4rem;border:1px solid var(--line);border-radius:10px;background:var(--panel);overflow:hidden}
.pz-sug button{font:inherit;text-align:left;min-height:44px;padding:.45rem .7rem;border:0;background:none;color:var(--fg);cursor:pointer}
.pz-sug button:hover,.pz-sug button:focus-visible{background:var(--mark)}
.pz-sug small{color:var(--muted)}
.pz-search-n:empty{display:none}
.pz-search-n{margin:0 0 .4rem}
.pz[data-step]:not([data-step="1"]) .pz-search,.pz[data-step]:not([data-step="1"]) .pz-sug,.pz[data-step]:not([data-step="1"]) .pz-search-n{display:none}
.pz-shared{margin-top:.6rem;font-size:.85rem}
.pz-shared input{width:100%;font:inherit;font-size:.8rem;padding:.4rem;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--fg)}
.pz-q{margin:.9rem 0}
#tab-uzemi.u-moje .u-prumer{display:none}
#u-zaklad button:disabled{opacity:.5;cursor:not-allowed}
.pz-q .q{font-weight:600;margin-bottom:.4rem}
.pz-q .note{margin-top:.35rem}
.pz-chips{display:flex;flex-wrap:wrap;gap:.4rem}
.pz-chip{font:inherit;font-size:.92rem;min-height:44px;padding:.5rem .8rem;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer;text-align:left}
.pz-chip[aria-pressed="true"]{border-color:var(--accent);background:var(--mark);box-shadow:inset 0 0 0 1px var(--accent);font-weight:600}
details.pz-more{margin-top:.8rem;border-top:1px solid var(--line);padding-top:.4rem}
details.pz-more>summary{cursor:pointer;color:var(--accent);min-height:40px;display:flex;align-items:center;font-weight:500}
details.pz-more .inputs{margin-top:.5rem}
.pz-teaser{margin-top:1rem;border-top:2px solid var(--water);padding-top:.6rem}
.pz-big{display:grid;gap:.35rem;margin-top:.4rem}
.pz-big p{margin:0}
.pz-track{height:18px;background:var(--chip);border-radius:4px;overflow:hidden;display:flex}
.pz-track i{display:block;height:100%} .pz-track .away{background:var(--bad)} .pz-track .kept{background:var(--water)}
.pz-chosen{font-size:1rem;margin:.2rem 0 .4rem}
.unfit details>summary{cursor:pointer;min-height:40px;display:flex;align-items:center;gap:.4rem}
#summary .motiv{margin-top:0}
#summary .motiv .big{color:inherit;font-size:2.4rem}
/* hlavicka a upozorneni na telefonu na jeden radek */
details.banner>summary{cursor:pointer;list-style:none}
details.banner>summary::-webkit-details-marker{display:none}
details.banner>summary b{font-weight:600;color:var(--fg)}
details.banner>summary .more{color:var(--accent);text-decoration:underline}
details.banner[open]>summary .more{display:none}
@media(max-width:600px){
  header.top{padding-block:.45rem;gap:.3rem}
  header.top h1{font-size:1.2rem}
  header.top .tag{display:none}
  nav.tabs{flex-wrap:nowrap;overflow-x:auto;margin-left:0;width:100%;scrollbar-width:none}
  nav.tabs button{white-space:nowrap;padding:.3rem .6rem;font-size:.85rem}
}
</style>
<style>__LEAFLET_CSS__</style>

<header class="top">
  <div><h1>Voda v Koryčanech</h1><div class="tag">náhled v0.2 - skutečný terén, půda, budovy a srážky; katalog v0.8</div></div>
  <nav class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-tab="jakbylo">Jak bylo</button>
    <button role="tab" aria-selected="false" data-tab="pozemek">Můj pozemek</button>
    <button role="tab" aria-selected="false" data-tab="uzemi">Celé území</button>
    <button role="tab" aria-selected="false" data-tab="katalog">Katalog</button>
    <button role="tab" aria-selected="false" data-tab="model">O modelu</button>
  </nav>
</header>
<details class="banner"><summary><b>Zjednodušený model pro osvětu, ne projekt. Nevalidováno.</b> Nic se neukládá. <span class="more">víc</span></summary>Po kliku do mapy se sklon a půda berou z dat (DMR 5G ČÚZK, BPEJ SPÚ); střechy a výměry z katastru (ČÚZK) po kliknutí na parcely, zpevněné plochy zadáváš sám. Katalog, vzorce, ceny a zdroje: opatreni.json v0.4 (20. 10. 2026). Značky: ✅ ověřený zdroj, ✅⏳ starší než rok, 📄 citace, 🤔 odhad.</details>

<main>
<!-- ======================= JAK BYLO ======================= -->
<section id="tab-jakbylo">
  <div class="panel">
    <h2>Jak bylo v Koryčanech</h2>
    <p class="note" style="margin:.2rem 0 0">Co se tu děje s vodou: kolik naprší, kolik se vypaří a co zbyde. Nejdřív dlouhé řady, protože jeden měsíc trend neukáže.</p>
    <p class="note" style="margin:.2rem 0 0">Data se stahují automaticky každý den; poslední aktualizace <span class="num" id="jb-upd"></span>.</p>
    <h3 style="margin-top:1rem">Dlouhý pohled: srážky Koryčany od roku 1921</h3>
    <p class="note" id="jb-l1-n"></p>
    <svg class="jb-chart" id="jb-l1" viewBox="0 0 720 220" role="img" aria-label="Roční srážky 1921-2025"></svg>
    <div class="legend"><span><b style="background:var(--chip)"></b>roční úhrn</span><span><b style="background:var(--dry)"></b>3 nejsušší roky</span><span><b style="background:var(--water)"></b>3 nejdeštivější roky</span><span><b style="background:var(--dry);opacity:.45"></b>letošek do dneška</span><span><b style="background:var(--muted);border-radius:50%;width:.4rem;height:.4rem;vertical-align:1px"></b>tečka pod rokem = část dní doplněna z okolní stanice</span><span><b style="background:var(--warn)"></b>klouzavý průměr 10 let</span><span><b style="background:var(--fg)"></b>normál 1991-2020</span></div>
    <h3 style="margin-top:1rem">Dlouhý pohled: kolik vody zbyde po výparu (od roku 2001)</h3>
    <p class="note" id="jb-l2-n"></p>
    <svg class="jb-chart" id="jb-l2" viewBox="0 0 720 220" role="img" aria-label="Srážky minus výpar a možný výpar 2001-2025"></svg>
    <div class="legend"><span><b style="background:var(--ok)"></b>srážky minus výpar: voda zbyla</span><span><b style="background:var(--dry)"></b>srážky minus výpar: voda chyběla</span><span><b class="ln" style="border-color:var(--soil);border-top-style:dashed"></b>možný výpar za rok</span><span><b style="background:var(--muted);border-radius:50%;width:.4rem;height:.4rem;vertical-align:1px"></b>tečka pod rokem = část dní doplněna z okolní stanice</span></div>
    <div class="jb-cards" id="jb-trend-v"></div>
    <h3 style="margin-top:1rem">Dlouhý pohled: teplota a horko (od roku 2001)</h3>
    <p class="note" id="jb-l3-n"></p>
    <svg class="jb-chart" id="jb-l3" viewBox="0 0 720 210" role="img" aria-label="Tropické a supertropické dny, tropické noci a letní maxima 2001-2025"></svg>
    <div class="legend" id="jb-l3-leg"><span><b style="background:var(--bad);border-radius:50%"></b>tropické dny (≥ 30 °C)</span><span><b style="background:var(--hot);transform:rotate(45deg) scale(.8)"></b>supertropické dny (≥ 35 °C)</span><span><b style="background:none;border:2px solid var(--accent);border-radius:50%"></b>tropické noci (minimum ≥ 20 °C)</span><span class="jb-leto"><b class="ln" style="border-color:var(--warn)"></b>letní maxima: průměr nejvyšších teplot dne červen-srpen (pravá osa)</span><span><b class="ln" style="border-color:var(--bad);border-top-style:dashed;opacity:.6"></b>trend tropických dní</span><span><b style="background:var(--muted);border-radius:50%;width:.4rem;height:.4rem;vertical-align:1px"></b>tečka pod rokem = část dní doplněna z okolní stanice</span></div>
    <div class="jb-cards" id="jb-trend"></div>
    <div class="motiv" id="jb-l-call"></div>

    <div class="jb-head" style="margin-top:1.4rem">
      <div><h3>Detail: vybrané období</h3><p class="note" style="margin:.2rem 0 0">Denní data jsou od 1. 1. 2026 (ČHMÚ je zveřejňuje jen pro běžící rok); starší roky jsou v řadách nahoře.</p></div>
      <label class="f" style="margin-left:auto">Období<select id="jb-obd"></select></label>
      <label class="f">od<input type="date" id="jb-od"></label>
      <label class="f">do<input type="date" id="jb-do"></label>
    </div>
    <div class="jb-cards" id="jb-cards"></div>
    <svg class="jb-chart" id="jb-graf" viewBox="0 0 720 230" role="img" aria-label="Denní průběh srážek, teploty a výparu"></svg>
    <div class="legend" id="jb-leg"><span><b style="background:var(--water)"></b>srážky mm/den (světlejší = náhradní stanice)</span><span><b class="ln" style="border-color:var(--bad)"></b>nejvyšší teplota dne °C</span><span><b class="ln" style="border-color:var(--warn)"></b>průměrná teplota dne (průměr za 24 h) °C</span><span><b class="ln" style="border-color:var(--soil);border-top-style:dashed"></b>možný výpar mm/den</span><span><b style="background:var(--bad);border-radius:50%"></b>tropický den (≥ 30 °C)</span><span><b style="background:var(--hot);transform:rotate(45deg) scale(.8)"></b>supertropický den (≥ 35 °C)</span></div>
    <h3 style="margin-top:1rem">Extrémy období</h3>
    <div class="jb-ext" id="jb-ext"></div>
    <h3 style="margin-top:1rem" id="jb-roc-h">Srovnání ročníků</h3>
    <p class="note" id="jb-roc-n"></p>
    <svg class="jb-chart" id="jb-roc" viewBox="0 0 720 200" role="img" aria-label="Srovnání ročníků"></svg>
    <div class="legend"><span><b style="background:var(--chip)"></b>úhrn ve vybraných měsících</span><span><b style="background:var(--bad)"></b>pod 60 % normálu</span><span><b style="background:var(--water)"></b>nad 140 % normálu</span><span><b style="background:var(--accent)"></b>letošek</span><span><b class="ln" style="border-color:var(--fg);border-top-style:dashed"></b>normál 1991-2020</span><span><b style="background:var(--muted);border-radius:50%;width:.4rem;height:.4rem;vertical-align:1px"></b>část dní doplněna z okolní stanice</span></div>
    <div class="jb-rank" id="jb-rank"></div>
    <div class="callout" style="margin-top:1rem"><b>Jak to číst.</b> <b>Možný výpar</b> je kolik vody by se vypařilo z trávníku, kdyby jí měl dost (odborně referenční evapotranspirace ET₀, počítaná z teplot metodou Hargreaves-Samani podle FAO-56 📄). Skutečný výpar je v suchém létě menší, protože není z čeho. <b>Srážky minus výpar</b> proto ukazuje, kolik vody krajině chybí a dobírá si ji ze zásoby v půdě a pod zemí (odborně klimatická vodní bilance). Vítr a vlhkost vzduchu metoda nezná; při větru je skutečná ztráta větší. <b>Průměrná teplota</b> je průměr dne i noci; horko líp ukazuje nejvyšší teplota dne. Prahy podle ČHMÚ ✅: tropický den = nejvyšší teplota aspoň 30 °C, supertropický aspoň 35 °C (neoficiální název), tropická noc = teplota neklesne pod 20 °C (<a href="https://intranet.chmi.cz/files/portal/docs/tiskove_zpravy/2025/TI_Leto2025.pdf" target="_blank" rel="noopener">ČHMÚ, Klimatologické léto 2025</a>).</div>
    <p class="src" id="jb-src"></p>
  </div>
</section>

<!-- ======================= MŮJ POZEMEK ======================= -->
<section id="tab-pozemek" class="hidden-tab pz" data-step="1">
  <nav class="pz-prog" aria-label="Postup">
    <ol>
      <li><button type="button" data-go="1" aria-current="step"><span class="n">1</span>Kde</button></li>
      <li><button type="button" data-go="2" disabled><span class="n">2</span>Okapy a půda</button></li>
      <li><button type="button" data-go="3" disabled><span class="n">3</span>Při dešti</button></li>
      <li><button type="button" data-go="4" disabled><span class="n">4</span>Co udělat</button></li>
      <li><button type="button" data-go="5" disabled><span class="n">5</span>Výsledek</button></li>
    </ol>
  </nav>
  <div class="pz-grid">
    <div class="pz-mapcol">
      <div class="pz-ask" id="pz-ask"><b>Najdi svůj dům a klepni na něj.</b> Označ parcely, které chceš řešit (sčítají se).</div>
      <form class="pz-search" id="pz-search" role="search" autocomplete="off">
        <input type="search" id="pz-adr" placeholder="Ulice a číslo domu, nebo číslo parcely" aria-label="Hledat adresu nebo parcelu" enterkeyhint="search">
        <button type="submit" class="pz-btn">Najít</button>
        <button type="button" class="pz-btn" id="pz-gps" title="Najít mě podle polohy telefonu">◎ Jsem tady</button>
      </form>
      <div class="pz-sug" id="pz-sug" hidden></div>
      <div class="note pz-search-n" id="pz-search-n" aria-live="polite"></div>
      <div class="pz-mapwrap">
        <div id="map" aria-label="Mapa Koryčan - klepni na svůj dům"></div>
        <button type="button" class="pz-mapcover" id="pz-mapcover" data-go="1" aria-label="Změnit místo - zpět na výběr pozemku"><span>Změnit místo</span></button>
      </div>
      <div class="pz-sel" id="w-parc">Zatím nic nevybráno.</div>
      <div class="pz-known">
          <div class="eyebrow">Z map víme <button type="button" class="linkbtn" id="pz-known-x" aria-expanded="false">podrobnosti</button></div>
          <dl class="kv" id="where">
            <dt class="pz-det">Místo</dt><dd class="pz-det" id="w-pos">-</dd>
            <dt>Sklon</dt><dd><span class="num" id="w-slope">-</span> % <span class="note" id="w-slope-n">(po kliku z DMR 5G, průměr v okruhu 15 m)</span></dd>
            <dt>Půda</dt><dd id="w-soil">- <span class="note">(po kliku z BPEJ; v lese a zástavbě odhad - ověř zkouškou vsaku)</span></dd>
            <dt>Okolí 30 m</dt><dd id="w-okoli">-</dd>
          </dl>
        </div>
      <p class="note pz-maphint">Katastr a budovy ČÚZK (CC BY 4.0), podklad ZTM a ortofoto ČÚZK. Hledání adresy dělá vyhledávací služba RÚIAN (ČÚZK): hledaný text se pošle jí, u nás se nic neukládá. Poloha telefonu zůstává v telefonu. Vlastníci se nenačítají. <button type="button" class="linkbtn" id="pz-manual">Nechci mapu, zadám plochy ručně</button></p>
    </div>
    <div class="pz-panel">
      <div class="pz-step" data-s="1">
        <h2>Co se děje s vodou na tvém pozemku?</h2>
        <p>Vyber v mapě svůj pozemek.</p>
        <p>Aplikace z map spočítá střechy, sklon a půdu, ty můžeš data upřesnit.</p>
        <p>Ihned uvidíš, kolik vody ti při dešti uteče a co s tím jde udělat.</p>
        <div id="pz-teaser"></div>
      </div>
      <div class="pz-step" data-s="2">
        <h2>Střechy, dlažba a půda</h2>
        <p class="callout" id="pz-manual-n" hidden>Bez mapy počítám s příkladem: střecha 120 m², zahrada 300 m². Oprav to v „Upřesnit čísla“.</p>
        <div class="pz-q"><div class="q">Kam vedou okapy ze střechy?</div><div class="pz-chips" data-for="in-drain"></div></div>
        <div class="pz-q"><div class="q">Kolik máš dlažby, betonu a štěrku?</div><div class="pz-chips" data-for="in-paved"></div><div class="note" id="pz-paved-n"></div></div>
        <details class="pz-more" id="pz-detail"><summary>Upřesnit čísla (plochy v m², sklon, dlažba, zahrada)</summary>
          <div class="inputs">
            <label class="f">Střecha (m²)<input type="number" id="in-roof" value="120" min="0" step="10"></label>
            <label class="f">Zpevněné plochy (m²)<input type="number" id="in-paved" value="0" min="0" step="5"></label>
            <label class="f">Typ zpevnění<select id="in-pavedtype">
          <option value="asfalt_beton_zalita_dlazba">asfalt / beton / zalitá dlažba</option>
          <option value="dlazba_piskove_spary" selected>dlažba s pískovými spárami</option>
          <option value="sterk_upraveny">štěrk</option>
          <option value="zatravnovaci_tvarnice">zatravňovací tvárnice</option></select></label>
            <label class="f">Zelené plochy (m²)<input type="number" id="in-green" value="300" min="0" step="10"></label>
            <label class="f">Co na nich je<select id="in-greentype"><option value="zahrada, trávník > 75 %" selected>hlavně trávník (přes 3/4)</option><option value="zahrada, trávník 50-75 % (záhony, cesty)">trávník s záhony a cestami (1/2 až 3/4)</option></select></label>
            <label class="f">Sklon pozemku (%)<input type="number" id="in-slope" value="4" min="0" max="40" step="1"></label>
            <label class="f">Svody ze střechy<select id="in-drain">
          <option value="kanal" selected>do kanalizace</option><option value="pozemek">na pozemek</option><option value="nevim">nevím</option></select></label>
            <label class="f">Půda (zkouška vsaku, 30 min)<select id="in-soil">
          <option value="A">kleslo přes 8 cm - A, velmi propustná</option>
          <option value="B" selected>kleslo 4-8 cm - B, propustná</option>
          <option value="C">kleslo 2-4 cm - C, málo propustná</option>
          <option value="D">kleslo pod 2 cm - D, jíl, nepropustná</option></select></label>
          </div>
          <p class="note">Střechy jsou půdorysy budov z katastru (ne plocha šikmé střechy). Zeleň = výměra vybraných parcel minus střechy a zpevněné plochy. Převod zkoušky vsaku na skupinu půdy A-D podle brožury Praha 2009 ✅⏳.</p>
        </details>
        <div class="pz-q"><div class="q">Jakou máš půdu?</div><div class="pz-chips" data-for="in-soil"></div>
          <div class="note">Předvybráno z mapy půd, v zástavbě je to odhad.</div>
          <details class="pz-mini"><summary>Jak to zjistit sám</summary><p class="note">Vykopej jámu 30 cm, nalij vodu a po 30 minutách změř, o kolik klesla. Přes 8 cm velmi propustná, 4-8 cm propustná, 2-4 cm spíš těžká, pod 2 cm jíl.</p></details></div>
      </div>
      <div class="pz-step" data-s="3">
        <h2>Co se u tebe děje při dešti</h2>
        <div class="pz-q"><div class="q">Jaký déšť?</div><div class="pz-chips" data-for="in-rain"></div><div class="note">Vzácné přívalové deště (53, 87 a 94 mm) najdeš v „Jak se to počítá“.</div></div>
        <div id="pz-rain-big"></div>
        <p id="pz-year"></p>
        <details class="pz-more"><summary>Jak se to počítá</summary>
          <div class="inputs" style="margin-top:.5rem"><label class="f">Jiný déšť<select id="in-rain">
          <optgroup label="Běžné deště (denní úhrny ČHMÚ Koryčany 1991-2019 ✅)">
            <option value="10" selected>10 mm - běžný déšť, asi 17x za rok</option>
            <option value="20">20 mm - silný déšť, asi 5x za rok</option></optgroup>
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm, 1x za 2 roky</option>
            <option value="53.2" data-n="N10">vzácný - 53 mm, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="26.2">26 mm - 60 min, 1x za 5 let (ČSN 75 9010, Brno)</option>
            <option value="93.5">94 mm - den 12. 6. 2012, 2. největší za 105 let (ČHMÚ Koryčany)</option></optgroup></select></label></div>
          <table class="flow" id="flow"></table>
          <p class="note" id="year"></p>
          <p class="note">Střechy a dlažba: součinitele odtoku ČSN 75 9010, první 1 mm deště zůstane na povrchu. Zahrada: metoda SCS-CN (Janeček a kol. 2012) podle půdy; u velkých dešťů vážený průměr běžně vlhké a nasycené půdy (Kavka a kol. 2023). Srážky: návrhové 6hodinové úhrny pro Koryčany (ČVUT a ČHMÚ 2023 ✅). Víc v záložce O modelu.</p>
        </details>
      </div>
      <div class="pz-step" data-s="4">
        <h2>Co můžeš udělat</h2>
        <p class="pz-chosen" id="pz-chosen"></p>
        <div class="co" id="pz-co"></div>
        <p class="note">Seřazeno: nejvíc vody za nejmíň práce. Zaškrtni, co by u tebe šlo. Čísla platí pro tvoje plochy a zvolený déšť. Podrobnosti (zdroje, kde to funguje, ceny) jsou pod každou kartou.</p>
        <div class="cards" id="cards"></div>
        <div class="unfit" id="unfit"></div>
      </div>
      <div class="pz-step" data-s="5">
        <h2>Výsledek</h2>
        <div id="summary"></div>
        <div class="bars" id="bars"></div>
        <div class="legend"><span><b style="background:var(--bad)"></b>odteče pryč</span><span><b style="background:var(--water)"></b>zůstane u tebe (vsákne se nebo zadrží)</span></div>
        <div class="callout ok" id="scale"></div>
      </div>
    </div>
  </div>
  <div class="pz-nav">
    <button type="button" class="pz-btn" id="pz-back">Zpět</button>
    <button type="button" class="pz-btn pri" id="pz-next" disabled>Dál: okapy a půda</button>
  </div>
</section>

<!-- ======================= CELÉ ÚZEMÍ ======================= -->
<section id="tab-uzemi" class="hidden-tab">
  <div class="panel">
    <h2>Co to udělá, když se zapojí víc lidí</h2>
    <p class="note" id="u-zdroj"></p>
    <div class="filters" id="u-zaklad" role="group" aria-label="Z čeho počítat jednu domácnost">
      <span class="note">Jedna domácnost:</span>
      <button type="button" data-z="prumer" aria-pressed="true">průměrná v obci</button>
      <button type="button" data-z="moje" aria-pressed="false" disabled title="Nejdřív projdi Můj pozemek">jako můj pozemek</button>
    </div>
    <div class="callout ok" id="u-moje-n" hidden></div>
    <div class="inputs" style="margin-top:.6rem">
      <label class="f">Rodinných domů v území<input type="number" id="u-n" value="__RD__" min="0" step="10"></label>
      <label class="f u-prumer">Průměrný půdorys domu (m²)<input type="number" id="u-roof" value="__ROOF__" min="0" step="10"></label>
      <label class="f u-prumer">Průměrně zpevněno (m², odhad 🤔)<input type="number" id="u-paved" value="35" min="0" step="5"></label>
      <label class="f">Déšť k výpočtu<select id="u-rain">
          <optgroup label="Běžné deště (denní úhrny ČHMÚ Koryčany 1991-2019 ✅)">
            <option value="10" selected>10 mm - běžný déšť, asi 17x za rok</option>
            <option value="20">20 mm - silný déšť, asi 5x za rok</option></optgroup>
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm, 1x za 2 roky</option>
            <option value="53.2" data-n="N10">vzácný - 53 mm, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="26.2">26 mm - 60 min, 1x za 5 let (ČSN 75 9010, Brno)</option>
            <option value="93.5">94 mm - den 12. 6. 2012, 2. největší za 105 let (ČHMÚ Koryčany)</option></optgroup></select></label>
    </div>
    <label class="f" style="margin-top:.8rem">Kolik domácností se zapojí: <span class="num" id="u-pct-val">20</span> %
      <input type="range" id="u-pct" min="0" max="100" value="20"></label>
    <div class="filters u-prumer" id="u-pack">
      <button aria-pressed="true" data-m="S02">S02 odpojit svody</button>
      <button aria-pressed="true" data-m="Z01">Z01 dešťová zahrada</button>
      <button aria-pressed="false" data-m="S01">S01 nádrž 1 m³</button>
      <button aria-pressed="false" data-m="Z04">Z04 propustný dvůr</button>
    </div>
    <div class="sum" id="u-sum"></div>
    <table class="flow" id="u-table" style="margin-top:.8rem"></table>
    <div class="callout" id="u-limit"></div>
    <div class="callout ok" id="u-plus"></div>
  </div>
  <div class="panel" style="margin-top:1rem">
    <h3>Velké střechy - kdo rozhoduje o nejvíc vodě</h3>
    <p class="note">Všechny budovy v území modelu podle účelu (ČÚZK INSPIRE BU ✅, účel z RÚIAN, u části budov neuveden). Voda ze střechy při zvoleném dešti = půdorys × úhrn (C = 1,0); průměr střech je 🤔 sklonem a tvarem skutečná plocha ~1,2× půdorys, počítá se půdorys. Jedna velká střecha = desítky zahrad; rozhoduje o ní jeden člověk nebo rada.</p>
    <table class="flow" id="s-table" style="margin-top:.6rem"></table>
    <div class="callout" id="s-limit"></div>
  </div>
  <div class="panel" style="margin-top:1rem">
    <h3>Pole, louky a les - odtok z krajiny</h3>
    <p class="note" id="k-zdroj">Plochy a půdy ze skutečných dat (ZABAGED využití, BPEJ -> HSP, DMR 5G) v mřížce 5 m, území modelu 1 772 ha (Kyjovka k jezu před Mouchnicemi). Posuvníky mění stav hospodaření na části plochy; odtok počítá SCS-CN po buňkách. Je to tabulková změna CN, ne měření - ukazuje řád, ne přesné číslo.</p>
    <div class="inputs" style="margin-top:.6rem">
      <label class="f">Orná: půdoochranné technologie (P04: zbytky na povrchu, bezorebně) <span class="num" id="k-p04-v">0</span> % plochy<input type="range" id="k-p04" min="0" max="100" value="0"></label>
      <label class="f">Orná: vrstevnicově + pásy + zbytky (P01, P03) <span class="num" id="k-p01-v">0</span> % plochy<input type="range" id="k-p01" min="0" max="100" value="0"></label>
      <label class="f">Orná nad 7° (svažitá): zatravnit (P06) <span class="num" id="k-p06-v">0</span> %<input type="range" id="k-p06" min="0" max="100" value="0"></label>
      <label class="f"><input type="checkbox" id="k-p05"> Zatravnit údolnice v orné půdě (P05: buňky, kam stéká ≥ 1 ha)</label>
      <label class="f">Stav lesa (hrabanka, podrost; LES)<select id="k-les"><option value="les, dobrý stav (hrabanka, podrost)">dobrý</option><option value="les, střední stav" selected>střední (výchozí)</option><option value="les, špatný stav (pastva, sešlap, bez hrabanky)">špatný</option></select></label>
      <label class="f">Louky a pastviny (L02)<select id="k-ttp"><option value="pastvina/louka, pokryv > 75 %" selected>pokryv > 75 % (výchozí)</option><option value="pastvina, pokryv 50-75 %">pokryv 50-75 %</option><option value="pastvina přepasená, pokryv < 50 %">přepasená < 50 %</option></select></label>
    </div>
    <table class="flow" id="k-table" style="margin-top:.8rem"></table>
    <div class="callout" id="k-limit"></div>
  </div>
  <div class="panel" style="margin-top:1rem">
    <h3>Hráz na potoce - kolik vody zadrží</h3>
    <p class="note">Klikni do mapy na modrý potok (toky ČÚZK ✅) - na tom místě se postaví hráz kolmo na tok. Spočítá se, kam až by voda vystoupala (terén DMR 5G, buňky 5 m) a kolik by jí nádrž pojala. U malých potoků (povodí pod 0,25 km²) a úzkých roklí terén údolí nerozliší, proto se ukáže jen tůň / poldr v údolnici s objemem jako rozsah. Je to odhad pro osvětu, ne návrh hráze.</p>
    <div class="inputs" style="margin-top:.6rem">
      <label class="f">Výška hráze nad dnem potoka<select id="h-vyska">
        <option value="0.5">0,5 m</option><option value="1" selected>1 m</option><option value="1.5">1,5 m</option><option value="2">2 m</option>
        <option value="2.5">2,5 m (vodní dílo)</option><option value="3">3 m (vodní dílo)</option><option value="4">4 m (vodní dílo)</option></select></label>
      <label class="f">Déšť k výpočtu<select id="h-rain">
          <optgroup label="Běžné deště (denní úhrny ČHMÚ Koryčany 1991-2019 ✅)">
            <option value="10" selected>10 mm - běžný déšť, asi 17x za rok</option>
            <option value="20">20 mm - silný déšť, asi 5x za rok</option></optgroup>
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm za 6 h, 1x za 2 roky</option>
            <option value="53.2" data-n="N10">vzácný - 53 mm za 6 h, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm za 6 h, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="93.5">94 mm - den 12. 6. 2012, 2. největší za 105 let (ČHMÚ Koryčany)</option></optgroup></select></label>
    </div>
    <div id="dam-map" style="height:380px;margin-top:.6rem;border:1px solid var(--line);border-radius:6px;background:#dfe7ea" aria-label="Mapa potoků pro hráz"></div>
    <div class="callout" id="h-vd" style="border-left-color:var(--accent);display:none"></div>
    <div id="h-out" style="margin-top:.6rem"><p class="note">Toky a terén se načtou po otevření mapy (asi 0,8 MB).</p></div>
    <p class="note">Každá hráz na potoce potřebuje povolení vodoprávního úřadu (ORP Kroměříž) a dohodu se správcem toku. Model nepočítá ztráty, bezpečnostní přeliv, těleso hráze ani koryto užší než 5 m. Metoda: docs/JADRO.md, kap. Nádrže.</p>
    <div class="callout ok">🦫 <b>Bobr evropský povolení nepotřebuje.</b> Na Kyjovce žije a jeho hráze jsou místy vysoké skoro 1 m. Bobří hráze zvedají hladinu, zpomalují odtok a kolem nich vznikají mokřady, kde se usazují splaveniny a daří se dalším druhům (Ametyst, metodický list Po stopách bobra ✅). Příroda umí některá opatření udělat sama. Bobr je u nás silně ohrožený druh.</div>
  </div>
  <div class="panel" style="margin-top:1rem">
    <h3>Co musí udělat obec a správci (kontext)</h3>
    <p class="note">Velká opatření z katalogu (kontext = true). Objemy a účinky na vlnu se tu nepočítají: bez DMR a bez doloženého zdroje by to bylo tahání závěrů.</p>
    <div class="cards" id="u-context"></div>
  </div>
</section>

<!-- ======================= KATALOG ======================= -->
<section id="tab-katalog" class="hidden-tab">
  <div class="panel">
    <h2>Katalog opatření</h2>
    <p class="note">Vyber, kde jsi a co tě trápí. Čísla jsou pro vzorový případ (100 m² střechy, 50 m² dvora, běžný déšť 10 mm); přesná čísla pro svůj dům dostaneš v záložce Můj pozemek. Každé číslo má zdroj a značku. Tečky u názvu = pracnost: ●○○ ruce a víkend, ●●○ dny a malá technika, ●●● projekt a firma.</p>
    <div class="kde" id="k-kde"></div>
    <div class="co" id="k-co"></div>
    <p class="note"><span class="num" id="k-count"></span> opatření</p>
    <details class="pz-more"><summary>Podrobné filtry (pro školu a úřad)</summary>
    <div class="filters" id="k-misto"></div>
    <div class="filters" id="k-rozhoduje"></div>
    <div class="filters" id="k-ucinek"></div>
    <div class="filters" id="k-fin"><button aria-pressed="false" data-f="otevreno">jen s otevřenou dotací (k 18. 10. 2026)</button><button aria-pressed="false" data-f="svepomoc">jen svépomoc (pracnost 1, povolení 0)</button></div>
    </details>
    <div class="cards" id="k-cards"></div>
  </div>
</section>

<!-- ======================= O MODELU ======================= -->
<section id="tab-model" class="hidden-tab">
  <div class="panel">
    <h2>O modelu</h2>
    <p>Jedno výpočetní jádro, dvě obálky (občan, škola/expert). Primární ukazatel: kolik vody z přívalu zůstane v území (zasákne, zadrží se, zůstane v půdě) místo odtoku korytem za hodinu. Zploštění povodňové vlny je vedlejší produkt. Výpar je součást bilance: méně neproduktivního výparu, víc vody v půdě a biomase.</p>
    <h3 style="margin-top:.8rem">Co jádro počítá v této verzi</h3>
    <ul>
      <li>Odtok z ploch: V = plocha × srážka × součinitel odtoku C (ČSN 75 9010 / TNV 75 9011 ✅).</li>
      <li>Účinek opatření jen tam, kde má katalog typ "vzorec" nebo doloženou "hodnotu". Odhady a kvalitativní účinky se nesčítají.</li>
      <li>Součet za území = počet domácností × průměrný pozemek × balíček opatření.</li>
    </ul>
    <h3 style="margin-top:.8rem">Co tu chybí a proč</h3>
    <ul>
      <li>Terén, půda, plochy střech: fáze 2 (DMR 5G, VÚMOP, ZABAGED). V náhledu zadáváš ručně.</li>
      <li>Eroze polí (USLE), objem nádrže z DMR, měření školy: další verze.</li>
      <li>Klimatické scénáře 2050/2090: zdroj s licencí zatím nedohledán.</li>
    </ul>
    <h3 style="margin-top:.8rem">Konstanty</h3>
    <div id="konst" class="src"></div>
    <h3 style="margin-top:.8rem">Dotační programy (stav k 18. 10. 2026)</h3>
    <div id="progs" class="src"></div>
  </div>
</section>

<footer>Skautský oddíl Hříběcí hory, Koryčany, s ZŠ Koryčany. Data: ČÚZK (CC BY 4.0), katalog opatření v0.3 (vlastní kompilace, zdroje u každé položky). Náhled 18. 10. 2026.</footer>
</main>

<script>__LEAFLET_JS__</script>
<script>
const D = __DATA__;
const K = D.konstanty;
const C = K.soucinitel_odtoku;
const RAIN_Y = K.srazky_rocni_mm.hodnota/1000; // m
const ZN = {overeno:"✅",overeno_stare:"✅⏳",citace:"📄",odhad:"🤔",pamet:"💻"};
const CZ = D.ciselniky;
const byId = Object.fromEntries(D.opatreni.map(o=>[o.id,o]));
const fmt = (x,d=1)=> (Math.round(x*10**d)/10**d).toLocaleString("cs-CZ",{minimumFractionDigits:d,maximumFractionDigits:d});
const fmt0 = x=> Math.round(x).toLocaleString("cs-CZ");
function cIdx(slope){return slope<1?0:slope<=5?1:2;}
function coef(key,slope){const a=C[key]; return Array.isArray(a)?a[cIdx(slope)]:a;}

// ---------- tabs
document.querySelectorAll('nav.tabs button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('nav.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));
  ['jakbylo','pozemek','uzemi','katalog','model'].forEach(t=>{document.getElementById('tab-'+t).classList.toggle('hidden-tab',t!==b.dataset.tab);});
  if(b.dataset.tab==='pozemek') setTimeout(()=>map.invalidateSize(),50);
  if(b.dataset.tab==='uzemi') setTimeout(hrazInit,50);
  try{localStorage.setItem('kor_tab',b.dataset.tab)}catch(e){}
}));

// ---------- mapa
const map = L.map('map',{zoomControl:true}).setView([49.1066,17.1650],16);
const ztm = L.tileLayer('https://ags.cuzk.gov.cz/arcgis1/rest/services/ZTM_WM/MapServer/WMTS/tile/1.0.0/ZTM_WM/default/GoogleMapsCompatible/{z}/{y}/{x}',{maxZoom:19,attribution:'ČÚZK - on-line (ZTM)'}).addTo(map);
const orto = L.tileLayer.wms('https://ags.cuzk.gov.cz/arcgis1/services/ORTOFOTO/MapServer/WMSServer',{layers:'0',format:'image/jpeg',maxZoom:19,attribution:'ČÚZK - on-line (Ortofoto)'});
L.control.layers({'ZTM (ČÚZK)':ztm,'Ortofoto (ČÚZK)':orto},null,{collapsed:true}).addTo(map);
let tilesOk=false; ztm.on('load',()=>{tilesOk=true});
setTimeout(()=>{ if(!tilesOk){ const d=document.createElement('div'); d.className='note'; d.style.cssText='position:absolute;inset:auto 8px 8px 8px;background:var(--panel);padding:.4rem .6rem;border-radius:4px;z-index:800'; d.textContent='Podklad ČÚZK se nenačetl (prohlížeč bez sítě, nebo náhled v omezeném prostředí). Mapa je jen kulisa, výpočty fungují.'; document.getElementById('map').appendChild(d);} },6000);
let marker=null;
map.on('click',e=>{
  if(typeof PZ!=='undefined' && PZ.step!==1) return;
  if(marker) marker.remove();
  marker = L.marker(e.latlng,{icon:L.divIcon({className:'',html:'<div class="pin"></div>',iconSize:[14,14],iconAnchor:[7,7]})}).addTo(map);
  document.getElementById('w-pos').innerHTML = '<span class="num">'+e.latlng.lat.toFixed(5)+' N, '+e.latlng.lng.toFixed(5)+' E</span> <span class="note">(nikam se neukládá)</span>';
  vyberParcelu(e.latlng.lng, e.latlng.lat);
  odvodZMapy(e.latlng.lng, e.latlng.lat);
});
// ---------- parcely a budovy (CUZK INSPIRE CP + BU, CC BY 4.0) - vyber klikanim, scita se
const BASE = location.pathname.includes('/prototyp/') ? '../' : '';
const PARC = {feats:[], layer:null, vybrane:new Set(), zvyr:null, budovy:null};
const vBodu = (ring, x, y) => { let inside=false; for(let i=0,j=ring.length-1;i<ring.length;j=i++){ const [xi,yi]=ring[i],[xj,yj]=ring[j]; if((yi>y)!==(yj>y) && x < (xj-xi)*(y-yi)/(yj-yi)+xi) inside=!inside; } return inside; };
const canvasR = L.canvas({padding:0.5});
fetch(BASE+'data/parcely.geojson').then(r=>r.json()).then(gj=>{
  PARC.feats = gj.features.map((f,k)=>{ const ring=f.geometry.coordinates[0]; let a=[Infinity,Infinity,-Infinity,-Infinity]; for(const [x,y] of ring){ if(x<a[0])a[0]=x; if(y<a[1])a[1]=y; if(x>a[2])a[2]=x; if(y>a[3])a[3]=y; } return {k, f, ring, diry:f.geometry.coordinates.slice(1), bbox:a}; });
  PARC.layer = L.geoJSON(gj,{renderer:canvasR, interactive:false, style:{color:'#7a5a3a',weight:0.7,fill:false,opacity:0.8}});
  PARC.zvyr = L.featureGroup().addTo(map);
  const ukaz=()=>{ if(map.getZoom()>=16){ if(!map.hasLayer(PARC.layer)) PARC.layer.addTo(map); } else if(map.hasLayer(PARC.layer)) map.removeLayer(PARC.layer); };
  map.on('zoomend',ukaz); ukaz();
}).catch(err=>{ console.warn('parcely', err); document.getElementById('w-parc').innerHTML='parcely se nenačetly - plochy zadej ručně'; });
fetch(BASE+'data/budovy.geojson').then(r=>r.json()).then(gj=>{
  PARC.budovy = L.geoJSON(gj,{renderer:canvasR, interactive:false, style:{color:'#5c4a3a',weight:0.5,fillColor:'#8a7a6a',fillOpacity:0.5}});
  const ukaz=()=>{ if(map.getZoom()>=16){ if(!map.hasLayer(PARC.budovy)) PARC.budovy.addTo(map); } else if(map.hasLayer(PARC.budovy)) map.removeLayer(PARC.budovy); };
  map.on('zoomend',ukaz); ukaz();
}).catch(()=>{});
function najdiParcelu(lon,lat){
  for(const p of PARC.feats){ if(lon<p.bbox[0]||lon>p.bbox[2]||lat<p.bbox[1]||lat>p.bbox[3]) continue; if(vBodu(p.ring,lon,lat) && !p.diry.some(d=>vBodu(d,lon,lat))) return p; }
  return null;
}
function vyberParcelu(lon,lat){
  if(!PARC.feats.length) return;
  const p = najdiParcelu(lon,lat);
  if(!p){ $('w-parc').innerHTML = 'tady katastr parcelu nemá (mimo stažená k.ú.) - plochy zadej ručně'; return; }
  if(PARC.vybrane.has(p.k)) PARC.vybrane.delete(p.k); else PARC.vybrane.add(p.k);
  prekresliVyber();
}
function prekresliVyber(){
  PARC.zvyr.clearLayers();
  let A=0, roof=0, bud=0, rd=0; const popis=[];
  for(const k of PARC.vybrane){ const p=PARC.feats[k], q=p.f.properties; A+=q.plocha_m2; roof+=q.strechy_m2; bud+=q.budov; rd+=q.rd;
    L.geoJSON(p.f,{style:{color:'#1f6f8b',weight:2.5,fillColor:'#1f6f8b',fillOpacity:0.12}}).addTo(PARC.zvyr);
    popis.push(`${q.cislo} (${fmt0(q.plocha_m2)} m²${q.budov?', '+q.budov+' bud. '+fmt0(q.strechy_m2)+' m²':''})`); }
  if(typeof pzUI==='function') pzUI();
  if(!PARC.vybrane.size){ $('w-parc').innerHTML='Zatím nic nevybráno.'; return; }
  const paved = +$('in-paved').value||0;
  $('in-roof').value = Math.round(roof);
  $('in-green').value = Math.max(0, Math.round(A - roof - paved));
  $('w-parc').innerHTML = `<b>Vybráno: ${fmt0(A)} m², z toho střechy ${fmt0(roof)} m²</b> <span class="note">(parc. č. ${popis.join('; ')})</span> <button type="button" id="w-parc-x" class="linkbtn">zrušit výběr</button>${PARC.vybrane.size===1?'<div class="note pz-only1">Má zahrada vlastní parcelu? Klepni i na ni.</div>':''}`;
  $('w-parc-x').onclick=()=>{ PARC.vybrane.clear(); prekresliVyber(); recalc(); };
  recalc();
}
document.getElementById('in-paved').addEventListener('input',()=>{ if(PARC.vybrane.size){ let A=0,roof=0; for(const k of PARC.vybrane){ const q=PARC.feats[k].f.properties; A+=q.plocha_m2; roof+=q.strechy_m2; } document.getElementById('in-green').value=Math.max(0,Math.round(A-roof-(+document.getElementById('in-paved').value||0))); } });
// ---------- jadro: sklon, puda, okoli z rastru (web/jadro.js + data/web)
let jadroStav = 'nacitam';
const HSPN = {1:'A, velmi propustná',2:'B, propustná',3:'C, málo propustná',4:'D, jíl, nepropustná'};
const LEG = {};
fetch(BASE+'data/vyuziti_pudy.json').then(r=>r.json()).then(j=>Object.assign(LEG,j.legenda)).catch(()=>{});
Jadro.nacti(BASE+'data/web/', {bez:['smer_v'], toky:false}).then(()=>{ jadroStav='ok'; return fetch(BASE+'data/povodi.geojson').then(r=>r.json()); }).then(gj=>{ krajinaHistogram(gj); renderKrajina(); }).catch(err=>{ jadroStav = jadroStav==='ok' ? jadroStav : 'chyba'; console.warn('jadro/krajina', err); $('k-zdroj').textContent='Rastry nebo povodí se nenačetly - tato část nefunguje.'; });
// ---------- krajina: histogram bunek uzemi modelu: trida x HSP x udolnice x svah
const KRAJ = {h:{}, e:{}, n:0};   // e = suma K*LS (USLE) orne pudy na klic
function krajinaHistogram(gj){
  const f = gj.features.find(x=>x.properties.typ==='uzemi_modelu'); if(!f) return;
  const geom = f.geometry.type==='Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  let bunky=[]; for(const poly of geom) bunky = bunky.concat(Jadro.bunkyPolygonu(poly[0], poly.slice(1)));
  const UD = 400; // bunek 5 m = 1 ha
  for(const i of bunky){ const v=Jadro.vyuziti(i), h=Jadro.hsp(i); if(!v||!h) continue; const a=Jadro.p.akumulace[i], ud=(a && Math.pow(10,(a-1)/40)>=UD)?1:0; const sk=Jadro.sklonDeg(i), sv=(sk!=null&&sk>=7)?1:0; const k=v+'|'+h+'|'+ud+'|'+sv; KRAJ.h[k]=(KRAJ.h[k]||0)+1; KRAJ.n++; if(v===1 && Jadro.p.usle_ls && Jadro.p.usle_ls[i]){ KRAJ.e[k]=(KRAJ.e[k]||0)+Jadro.p.usle_ls[i]/10*Jadro.p.usle_k[i]/100; } }
}
const ORNA='1', TTP='3', LES=['4','41','42','43'];
function cnZ(trida, varianta, h){ const t=D.cn_tabulka[trida]; if(!t) return null; const v=t.varianty[varianta]||t.varianty[t.vychozi]; return v ? v['ABCD'[h-1]] : null; }
function qmm(P, cn){ if(!cn) return 0; const S=25400/cn-254, Ia=0.2*S; return P<=Ia?0:(P-Ia)*(P-Ia)/(P-Ia+S); }
// vazeni pres tvary deste a stav nasyceni (Kavka a kol. 2023 tab. 6) - jen pro navrhove deste N2/N10/N100; jinak CN2
function vahaCN3Sel(sel){ const n=sel.selectedOptions[0]?.dataset.n; return n && D.navrhove.podil_tvaru_pct[n] ? Jadro.vahaCN3(D.navrhove.podil_tvaru_pct[n], D.navrhove.qAPI) : 0; }
function qv(P, cn, w3){ return qmm(P,cn)*(1-w3) + qmm(P, Jadro.cnProIPS(cn,3))*w3; }
function renderKrajina(){
  if(!KRAJ.n) return;
  const P = +$('u-rain').value, A=25, W3=vahaCN3Sel($('u-rain')), NKEY=$('u-rain').selectedOptions[0]?.dataset.n;
  const p04=+$('k-p04').value/100, p01=+$('k-p01').value/100, p06=+$('k-p06').value/100, p05=$('k-p05').checked, les=$('k-les').value, ttp=$('k-ttp').value;
  ['p04','p01','p06'].forEach(k=>$('k-'+k+'-v').textContent=$('k-'+k).value);
  const sk = {}; // trida -> {ha, q0, q1}
  const RU=K.usle.R_korycany.orna_prumer, C0=0.2, HA=A/1e4;
  const add=(name, n, cn0, cn1, kls, c1, pf)=>{ const o=sk[name]||(sk[name]={ha:0,q0:0,q1:0,cn0:0,cn1:0,q0s:0,q0n:0,e0:0,e1:0}); if(kls){ o.e0+=RU*kls*C0*HA; o.e1+=RU*kls*(c1==null?C0:c1)*(pf||1)*HA; } o.ha+=n*A/1e4; o.q0+=qv(P,cn0,W3)/1000*n*A; o.q1+=qv(P,cn1,W3)/1000*n*A; o.q0s+=qmm(P,cn0)/1000*n*A; o.q0n+=qmm(P,Jadro.cnProIPS(cn0,3))/1000*n*A; o.cn0+=cn0*n; o.cn1+=cn1*n; };
  for(const [k,n] of Object.entries(KRAJ.h)){
    const [v,hs,ud,sv]=k.split('|'); const h=+hs; const t=D.cn_tabulka[v]; if(!t) continue;
    const cn0=cnZ(v, t.vychozi, h); let cn1=cn0, name=t.nazev;
    if(v===ORNA){ name='orná půda'; const e=KRAJ.e[k]||0, eu=e/n; const Pv = sv==='1'?0.9:0.65;  // P vrstevnicove: Janecek 0,6-0,7 do 6 st., 0,8-1,0 nad
      const cnTTP=cnZ(TTP,'pastvina/louka, pokryv > 75 %',h), cnP04=cnZ(ORNA,'obilniny, zbytky na povrchu, dobrý stav',h), cnP01=cnZ(ORNA,'obilniny, vrstevnicově + pásy + zbytky, dobrý stav',h);
      if(p05 && ud==='1'){ add(name,n,cn0,cnTTP,e,0.01); continue; }
      // podily se skladaji: zatravneni svazite (jen sv=1) -> z ostatku vrstevnicove -> z ostatku pudoochranne -> zbytek vychozi
      let zb=n; if(sv==='1'&&p06>0){ const m=n*p06; add(name,m,cn0,cnTTP,eu*m,0.01); zb-=m; }
      const m1=zb*p01; if(m1>0) add(name,m1,cn0,cnP01,eu*m1,0.1,Pv); zb-=m1;
      const m2=zb*Math.max(0,p04-p01); if(m2>0) add(name,m2,cn0,cnP04,eu*m2,0.1); zb-=m2;
      if(zb>0) add(name,zb,cn0,cn0,eu*zb); continue; }
    if(LES.includes(v)){ name='les'; cn1=cnZ(v,les,h); }
    else if(v===TTP){ name='louky a pastviny'; cn1=cnZ(v,ttp,h); }
    add(name,n,cn0,cn1);
  }
  // male tridy (< 5 ha) sloucit do "ostatni"
  const ost={ha:0,q0:0,q1:0,cn0:0,cn1:0,q0s:0,q0n:0,e0:0,e1:0}; for(const [nm,o] of Object.entries(sk)) if(o.ha<5){ ost.ha+=o.ha; ost.q0+=o.q0; ost.q1+=o.q1; ost.q0s+=o.q0s; ost.q0n+=o.q0n; ost.e0+=o.e0; ost.e1+=o.e1; ost.cn0+=o.cn0; ost.cn1+=o.cn1; delete sk[nm]; }
  if(ost.ha>0) sk['ostatní (třídy pod 5 ha)']=ost;
  const rows=Object.entries(sk).sort((a,b)=>b[1].ha-a[1].ha); let H=0,Q0=0,Q1=0,Q0s=0,Q0n=0,E0=0,E1=0,HO=0; rows.forEach(([nm,o])=>{H+=o.ha;Q0+=o.q0;Q1+=o.q1;Q0s+=o.q0s;Q0n+=o.q0n;E0+=o.e0;E1+=o.e1; if(nm==='orná půda') HO=o.ha;});
  $('k-table').innerHTML=`<tr><th>plocha (území modelu)</th><th class="num">ha</th><th class="num">CN teď</th><th class="num">CN scénář</th><th class="num">odtok teď m³</th><th class="num">scénář m³</th><th class="num">rozdíl</th><th class="num">eroze teď t/rok</th><th class="num">scénář</th></tr>`+
    rows.map(([nm,o])=>`<tr><td>${nm}</td><td class="num">${fmt0(o.ha)}</td><td class="num">${fmt0(o.cn0/(o.ha*1e4/A))}</td><td class="num">${fmt0(o.cn1/(o.ha*1e4/A))}</td><td class="num">${fmt0(o.q0)}</td><td class="num">${fmt0(o.q1)}</td><td class="num">${o.q0-o.q1>0.5?'-'+fmt0(o.q0-o.q1):(o.q1-o.q0>0.5?'+'+fmt0(o.q1-o.q0):'')}</td><td class="num">${o.e0?fmt0(o.e0):'-'}</td><td class="num">${o.e0?fmt0(o.e1):'-'}</td></tr>`).join('')+
    `<tr class="total"><td>celkem při ${fmt0(P)} mm</td><td class="num">${fmt0(H)}</td><td></td><td></td><td class="num">${fmt0(Q0)}</td><td class="num">${fmt0(Q1)}</td><td class="num">${fmt0(Q1-Q0)}</td><td class="num">${fmt0(E0)}</td><td class="num">${fmt0(E1)}</td></tr>`;
  const dQ=Q0-Q1;
  const IA_UZ = 0.2*(25400/D.uzemi.cn_vazene-254);
  const malo = Q0 < 0.005*H*1e4*P/1000 ? `<b>Při ${fmt0(P)} mm se v krajině skoro všechno vsákne</b> nebo zůstane na rostlinách a v prohlubních: povrchový odtok podle SCS-CN začíná u průměrné půdy v území (CN ${D.uzemi.cn_vazene}) až nad zhruba ${fmt0(IA_UZ)} mm. Opatření na polích a loukách se projeví u silnějších dešťů - vyber 20 mm nebo liják. ` : '';
  $('k-limit').innerHTML = malo + `<b>Co to znamená:</b> scénář ${dQ>=0?'sníží':'zvýší'} povrchový odtok z krajiny při dešti ${fmt0(P)} mm o <b>${fmt0(Math.abs(dQ))} m³</b> (${fmt(100*Math.abs(dQ)/Math.max(1,Q0),1)} % z ${fmt0(Q0)} m³). Pro srovnání: déšť ${fmt0(P)} mm na území spadne ${fmt0(H*1e4*P/1000)} m³ - většina se vsákne nebo zůstane na povrchu i teď. ${NKEY?`Jak moc je půda před deštěm nasycená, nevíme - proto se počítá vážený průměr: běžně vlhká půda (CN2) by dala ${fmt0(Q0s)} m³, nasycená (CN3) ${fmt0(Q0n)} m³; váha nasyceného stavu ${fmt(100*W3,0)} % vychází z toho, jaké průběhy deště (tvary A-F) jsou v Koryčanech u deště ${NKEY.replace('N','1x za ')} let typické a jak často jim předchází mokré dny (Kavka a kol. 2023 ✅, tab. 6; data/navrhove_srazky.json). `:`U tohoto deště se počítá jen s běžně vlhkou půdou (CN2); rozpětí vlhká-nasycená ukážou návrhové deště častý / vzácný / extrémní. `}Čísla jsou změna CN podle tabulky Janeček a kol. 2012 (tab. 2.3) ✅⏳ a USDA TR-55, metoda SCS-CN, buňky 5 m; stav pozemků "teď" je výchozí předpoklad tabulky (orná = obilniny, špatný stav; les střední), ne terénní průzkum. Zatravnění údolnic bere buňky orné půdy, kam stéká aspoň 1 ha (akumulace z DMR 5G). ${E0?`<br><b>Eroze orné půdy (USLE, orientačně):</b> teď ${fmt0(E0)} t/rok z ${fmt0(HO)} ha = ${fmt(E0/Math.max(1,HO),1)} t/ha/rok při obilninách (C 0,2), scénář ${fmt0(E1)} t/rok (${fmt(E1/Math.max(1,HO),1)} t/ha). Přípustná ztráta od 1. 7. 2026 je ${K.usle.Gp_t_ha_rok['od_2026-07-01'].ostatni} t/ha/rok ✅ (mělké půdy ${K.usle.Gp_t_ha_rok['od_2026-07-01'].melke}). R faktor ${fmt0(RU)} (VÚMOP/ČHMÚ 2022 ✅), K podle HPJ a LS z DMR (Janeček 2012 ✅⏳), půdoochranné technologie C 0,1, vrstevnice P 0,65 / 0,9 (do / nad 7°), zatravnění C 0,01; délka svahu z terénu nezná meze a cesty, na dlouhých svazích nadsazuje. Závazný výpočet dělá kalkulačka VÚMOP.`:''} Zpomalení vlny a výpar se tu nepočítají.`;
}
['k-p04','k-p01','k-p06','k-p05','k-les','k-ttp','u-rain'].forEach(id=>document.getElementById(id).addEventListener('input',renderKrajina));
function kruh(lon,lat,rM){ const [X,Y]=Jadro.lonLatNaXY(lon,lat); const ring=[]; for(let k=0;k<24;k++){ const a=k/24*2*Math.PI; ring.push(Jadro.xyNaLonLat(X+rM*Math.cos(a), Y+rM*Math.sin(a))); } return ring; }
function odvodZMapy(lon,lat){
  if(jadroStav!=='ok'){ $('w-slope-n').textContent = jadroStav==='nacitam' ? '(rastry se ještě načítají, klikni za chvíli znovu)' : '(rastry se nepodařilo načíst - zadej sklon ručně)'; return; }
  const b = Jadro.lonLatNaBunku(lon,lat);
  if(!b){ $('w-slope-n').textContent='(mimo území dat)'; return; }
  let bunky = Jadro.bunkyPolygonu(kruh(lon,lat,15));
  if(PARC.vybrane.size){ bunky=[]; for(const k of PARC.vybrane){ const p=PARC.feats[k]; bunky=bunky.concat(Jadro.bunkyPolygonu(p.ring,p.diry)); } if(bunky.length<4) bunky=Jadro.bunkyPolygonu(kruh(lon,lat,15)); }
  const s15 = Jadro.statBunek(bunky);
  const s30 = Jadro.statBunek(Jadro.bunkyPolygonu(kruh(lon,lat,30)));
  const sklonPct = s15.sklon_prumer_pct!=null ? Math.round(s15.sklon_prumer_pct) : null;
  if(sklonPct!=null){ $('in-slope').value = sklonPct; $('w-slope').textContent = sklonPct; $('w-slope-n').textContent = PARC.vybrane.size ? `(DMR 5G, průměr vybraných parcel, ${s15.n_platnych} buněk 5 m)` : `(DMR 5G, průměr v okruhu 15 m; v bodě ${fmt(Jadro.sklonDeg(b.i)||0)}°)`; }
  const h = Jadro.hsp(b.i), odhad = Jadro.p.hsp_zdroj[b.i]===2;
  if(h){ $('in-soil').value = 'ABCD'[h-1]; $('w-soil').innerHTML = `skupina ${HSPN[h]} <span class="note">(${odhad?'odhad z nejbližší bonitované plochy - ověř zkouškou vsaku':'z BPEJ (SPÚ) + Janeček 2012'})</span>`; }
  else $('w-soil').innerHTML = '- <span class="note">(bez dat, zadej podle zkoušky vsaku)</span>';
  const A = s30.plocha_ha*1e4 || 1;
  const sum = ks => ks.reduce((t,k)=>t+(s30.vyuziti_ha[k]||0),0)*1e4;
  const bud = sum([30,31]), zpev = sum([10,14,20,21,22,11]), zel = Math.max(0, A - bud - zpev);
  const top = Object.entries(s30.vyuziti_ha).sort((a,b)=>b[1]-a[1]).slice(0,3).map(([k,v])=>`${LEG[k]||k} ${Math.round(100*v*1e4/A)} %`).join(', ');
  $('w-okoli').innerHTML = `budovy ${Math.round(100*bud/A)} %, zpevněné a areály ${Math.round(100*zpev/A)} %, zeleň ${Math.round(100*zel/A)} % <span class="note">(${top}; ZABAGED, mřížka 5 m - jen nápověda)</span>`;
  recalc();
}


// ---------- Muj pozemek: pruvodce po krocich (varianta A)
const PZ = {step:1, manual:false};
const PZ_NEXT = ['', 'Dál: okapy a půda', 'Dál: co se děje při dešti', 'Dál: co můžu udělat', 'Dál: výsledek', 'Vybrat jiný pozemek'];
function pzReady(){ return PZ.manual || PARC.vybrane.size>0; }
function pzGo(n){
  n = Math.max(1, Math.min(5, n));
  if(n>1 && !pzReady()) return;
  const sec = document.getElementById('tab-pozemek'); const prev = PZ.step; PZ.step = n; sec.dataset.step = n;
  pzUI(); pzStav();
  setTimeout(()=>{ map.invalidateSize(); if(PARC.vybrane.size && PARC.zvyr){ try{ map.fitBounds(PARC.zvyr.getBounds(), {padding:[20,20], maxZoom:19}); }catch(e){} } }, 230);
  if(prev!==n){ const top = sec.getBoundingClientRect().top + scrollY - 8; if(scrollY>top) window.scrollTo({top, behavior:'auto'}); }
}
function pzUI(){
  const ok = pzReady();
  document.querySelectorAll('.pz-prog button').forEach(b=>{ const k=+b.dataset.go; b.disabled = k>1 && !ok; b.classList.toggle('done', k<PZ.step); if(k===PZ.step) b.setAttribute('aria-current','step'); else b.removeAttribute('aria-current'); });
  const nx = document.getElementById('pz-next'); nx.textContent = PZ_NEXT[PZ.step]; nx.disabled = PZ.step===1 && !ok;
}
document.getElementById('tab-pozemek').addEventListener('click', e=>{ const g=e.target.closest('[data-go]'); if(g && !g.disabled) pzGo(+g.dataset.go); });
document.getElementById('pz-next').addEventListener('click', ()=>{ if(PZ.step===5){ PARC.vybrane.clear(); prekresliVyber(); PZ.manual=false; pzGo(1); } else pzGo(PZ.step+1); });
document.getElementById('pz-back').addEventListener('click', ()=>pzGo(PZ.step-1));
document.getElementById('pz-manual').addEventListener('click', ()=>{ PZ.manual=true; document.getElementById('pz-detail').open=true; pzGo(2); recalc(); });


// ---------- Muj pozemek: otazky s tlacitky (nastavuji puvodni vstupy, vypocet beze zmeny)
const PZ_CHIPS = {
  'in-drain':[['kanal','do kanalizace'],['pozemek','na zahradu'],['nevim','nevím']],
  'in-paved':[['0','skoro nic'],['20','cesta, malý dvůr (~20 m²)'],['60','dvůr a příjezd (~60 m²)'],['150','velký dvůr (~150 m²)']],
  'in-soil':[['A','velmi propustná, písek'],['B','propustná'],['C','spíš těžká'],['D','jíl, voda stojí']],
  'in-rain':[['10','běžný, 10 mm'],['20','silný, 20 mm'],['32.2','liják, 32 mm']],
};
document.querySelectorAll('.pz-chips').forEach(box=>{ const id=box.dataset.for;
  box.innerHTML = PZ_CHIPS[id].map(([v,l])=>`<button type="button" class="pz-chip" data-v="${v}" aria-pressed="false">${l}</button>`).join('');
  box.addEventListener('click', e=>{ const b=e.target.closest('.pz-chip'); if(!b) return; const el=document.getElementById(id); el.value=b.dataset.v; el.dispatchEvent(new Event('input',{bubbles:true})); });
});
function pzChipsSync(){ document.querySelectorAll('.pz-chips').forEach(box=>{ const v=String(document.getElementById(box.dataset.for).value); box.querySelectorAll('.pz-chip').forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.v===v || (+b.dataset.v===+v && v!=='')))); }); }
document.getElementById('tab-pozemek').addEventListener('click', e=>{ const u=e.target.closest('[data-uz-moje]'); if(!u) return; e.preventDefault(); UZ.moje=true; const ur=document.getElementById('u-rain'); ur.value=document.getElementById('in-rain').value; document.querySelector('nav.tabs button[data-tab="uzemi"]').click(); ur.dispatchEvent(new Event('input')); window.scrollTo({top:0}); });
document.getElementById('tab-pozemek').addEventListener('click', e=>{ const t=e.target.closest('[data-tab-go]'); if(!t) return; e.preventDefault(); document.querySelector(`nav.tabs button[data-tab="${t.dataset.tabGo}"]`).click(); window.scrollTo({top:0}); });
const VANA_L = 150; // plna vana ~150 l - odhad pro predstavu
const vany = m3 => fmt0(m3*1000/VANA_L);
// cetnost: kolik dni za rok ma vic nez P mm (histogram dennich uhrnu CHMU Korycany 1991-2019)
const cetnost = P => { const H=D.srazky_hist; if(!H) return null; let n=0; for(let k=0;k<H.bin_mm.length;k++) if(H.bin_mm[k]-1>=P) n+=H.dni_za_rok[k]; return n; };
const RAIN_TXT = {'10':'běžný déšť, asi '+fmt0(cetnost(10)||17)+'x za rok','20':'silný déšť, asi '+fmt0(cetnost(20)||5)+'x za rok','32.2':'liják, jednou za 2 roky','53.2':'vzácný liják, jednou za 10 let','87':'extrémní liják, jednou za 100 let','26.2':'krátká bouřka, jednou za 5 let','93.5':'jako 12. 6. 2012 v Koryčanech'};
function pzRender(i, r, kept, keptYear, n){
  const $=id=>document.getElementById(id);
  pzChipsSync();
  const P = Math.round(i.rain*1000), rt = RAIN_TXT[$('in-rain').value] || '';
  // krok 1: prvni cislo hned po vyberu
  $('pz-teaser').innerHTML = !PARC.vybrane.size ? '' : (i.roof>0
    ? `<div class="pz-teaser"><div class="note">Při dešti ${P} mm (${rt}) odteče ze střech na vybraných parcelách (${fmt0(i.roof)} m²)</div><div class="big num">${fmt(r.roofOut)} m³</div><div class="note">to je asi ${vany(r.roofOut)} plných van 🤔. Co se děje se zbytkem pozemku a co s tím jde udělat, ukážou další kroky.</div></div>`
    : `<div class="pz-teaser note">Na vybraných parcelách nejsou budovy. Klepni i na svůj dům, nebo pokračuj se zahradou.</div>`);
  // krok 2
  $('pz-manual-n').hidden = !(PZ.manual && !PARC.vybrane.size);
  $('pz-paved-n').textContent = `Zpevněné plochy v mapách nejsou, odhadni je. Teď počítám s ${fmt0(i.paved)} m², přesně v „Upřesnit čísla“.`;
  // krok 3: kolik spadne, kolik odtece, odkud
  const fall = r.total, pct = fall>0 ? Math.round(100*r.out/fall) : 0;
  const src = [['ze střechy',r.roofOut],['z dlažby a betonu',r.pavedOut],['ze zahrady',r.greenOut]].sort((a,b)=>b[1]-a[1])[0];
  const dest = i.drain==='kanal' ? 'Voda z okapů teče do kanalizace a dál do potoka.' : i.drain==='pozemek' ? 'Okapy už vedou na zahradu, to je dobrý začátek - v kroku 4 uvidíš, jak tu vodu udržet.' : 'Kam vedou okapy, poznáš u paty svodu: když mizí v trubce v zemi, většinou je to kanalizace 🤔.';
  $('pz-rain-big').innerHTML = `<div class="pz-big"><div class="note">Při dešti ${P} mm (${rt}) spadne na tvůj pozemek (${fmt0(i.roof+i.paved+i.green)} m²)</div>
    <div><span class="big num">${fmt(fall)} m³</span> <span class="note">= asi ${vany(fall)} van 🤔</span></div>
    <p>Z toho <b>${fmt(r.out)} m³ odteče</b> (${pct} %), zbytek se vsákne do zahrady.</p>
    <div class="pz-track" role="img" aria-label="odteče ${pct} %"><i class="away" style="width:${pct}%"></i><i class="kept" style="width:${100-pct}%"></i></div>
    <div class="legend"><span><b style="background:var(--bad)"></b>odteče</span><span><b style="background:var(--water)"></b>vsákne se</span></div>
    <p>${src[1]>0.05?`Nejvíc odteče ${src[0]} (${fmt(src[1])} m³). `:''}${dest} ${i.green>0?`Trávník při dešti do ${fmt0(r.g.Ia_mm)} mm vsákne všechno.`:''}</p></div>`;
  $('pz-year').innerHTML = `Za celý rok (průměrně ${fmt0(K.srazky_rocni_mm.hodnota)} mm, ČHMÚ Koryčany ✅) odteče ze střech a dlažby asi <b>${fmt0(r.yearRoof+r.yearPaved)} m³</b>${r.yearGreen!=null?`, ze zahrady ${fmt0(r.yearGreen)} m³`:''}.`;
  // krok 4: prubezny soucet
  $('pz-chosen').innerHTML = kept>0.05 ? `Zaškrtnutá opatření udrží <b>${fmt(kept)} m³</b> z ${fmt(r.out)} m³, které teď při tomto dešti odtečou.` : `Zatím nic, co by vodu zadrželo. Teď při tomto dešti odteče ${fmt(r.out)} m³.`;
  // krok 5: motivacni vysledek
  $('scale').hidden = !(kept>0.05);
  setTimeout(pzStav, 0);
  $('summary').innerHTML = kept>0.05
    ? `<div class="motiv"><div>Tvoje volba udrží doma</div><div class="big num">${fmt(kept)} m³</div><p>z každého deště ${P} mm (${rt}), to je asi ${vany(kept)} van 🤔, které neodtečou ${i.drain==='kanal'?'do kanalizace':'pryč'}. Za rok ${fmt0(keptYear)} m³.</p><div class="mot-a"><a href="#" data-uz-moje="1">Co kdyby to udělali i ostatní? →</a><a href="#" data-tab-go="uzemi">Co může obec a celé území →</a><a href="#" data-tab-go="katalog">Všechna opatření →</a><a href="#" data-share="1">Poslat odkaz</a></div></div><div class="pz-shared note" id="pz-shared">Odkaz obsahuje čísla vybraných parcel a tvoje odpovědi. Nikam se neukládá, pošleš ho jen ty.</div>`
    : `<div class="callout">Zatím jsi nevybral žádné opatření, které vodu zadrží. Vrať se <button type="button" class="linkbtn" data-go="4">ke kroku 4</button>.</div>`;
}

// ---------- hledani adresy nebo parcely: vyhledavaci sluzba RUIAN (CUZK, GeocodeSOE; overeno 21. 10. 2026)
const RUIAN = 'https://ags.cuzk.gov.cz/arcgis/rest/services/RUIAN/Vyhledavaci_sluzba_nad_daty_RUIAN/MapServer/exts/GeocodeSOE';
const MISTNI = ['Koryčany','Blišice','Jestřabice','Lískovec','Mouchnice'];
const pzMsg = t => { document.getElementById('pz-search-n').textContent = t; };
let pzSugT = null, pzSugN = 0, pzSugList = [];
async function pzHledej(q){
  const qs = [q]; if(!MISTNI.some(m=>q.toLowerCase().includes(m.toLowerCase().slice(0,4)))) qs.push(q+' Koryčany');
  const out = [];
  for(const t of qs){
    const j = await (await fetch(RUIAN+'/suggest?text='+encodeURIComponent(t)+'&f=json')).json();
    (j.suggestions||[]).forEach(x=>{
      if(!['AdresniMisto','ParcelaDefinicniBod','Ulice'].includes(x.type)) return;
      if(!MISTNI.some(m=>x.text.includes(m))) return;
      if(x.type==='AdresniMisto' && !/76805|68333/.test(x.text)) return;   // PSC Korycan a Mouchnic (jine Liskovce pryc)
      if(!out.some(y=>y.magicKey===x.magicKey)) out.push(x);
    });
  }
  return out.slice(0,6);
}
function pzSugRender(list){
  pzSugList = list; const box = document.getElementById('pz-sug');
  const typ = {AdresniMisto:'adresa', ParcelaDefinicniBod:'parcela (k. ú. a číslo)', Ulice:'ulice'};
  box.innerHTML = list.map((x,k)=>`<button type="button" data-sug="${k}">${x.text} <small>${typ[x.type]||''}</small></button>`).join('');
  box.hidden = !list.length;
}
document.getElementById('pz-adr').addEventListener('input', e=>{
  const q = e.target.value.trim(); clearTimeout(pzSugT);
  if(q.length<3){ pzSugRender([]); pzMsg(''); return; }
  pzSugT = setTimeout(async()=>{ const n=++pzSugN; try{ const l=await pzHledej(q); if(n!==pzSugN) return; pzSugRender(l); pzMsg(l.length?'':'Nic nenalezeno v Koryčanech a okolí. Zkus ulici a číslo domu, nebo najdi dům v mapě.'); }catch(err){ pzMsg('Vyhledávání ČÚZK teď neodpovídá. Najdi dům přímo v mapě.'); } }, 350);
});
async function pzNajdi(x){
  pzSugRender([]); document.getElementById('pz-adr').value = x.text;
  try{
    const j = await (await fetch(RUIAN+'/findAddressCandidates?SingleLine='+encodeURIComponent(x.text)+'&magicKey='+encodeURIComponent(x.magicKey)+'&outSR=4326&maxLocations=1&f=json')).json();
    const c = (j.candidates||[])[0]; if(!c){ pzMsg('Místo se nepodařilo najít. Najdi dům v mapě.'); return; }
    const lat=c.location.y, lon=c.location.x;
    if(x.type==='Ulice'){ map.setView([lat,lon],18); pzMsg('Ulice nalezena. Klepni v mapě na svůj dům.'); return; }
    const p = najdiParcelu(lon,lat);
    if(!p){ map.setView([lat,lon],17); pzMsg('Tohle místo je mimo území modelu (povodí Kyjovky a Stříbrníku v Koryčanech po jez před Mouchnicemi).'); return; }
    map.setView([lat,lon],19);
    if(!PARC.vybrane.has(p.k)) map.fire('click',{latlng:L.latLng(lat,lon)});
    pzMsg(PARC.vybrane.size===1 ? 'Našel jsem to. Má zahrada vlastní parcelu? Klepni i na ni.' : '');
  }catch(err){ pzMsg('Vyhledávání ČÚZK teď neodpovídá. Najdi dům přímo v mapě.'); }
}
document.getElementById('pz-sug').addEventListener('click', e=>{ const b=e.target.closest('[data-sug]'); if(b) pzNajdi(pzSugList[+b.dataset.sug]); });
document.getElementById('pz-search').addEventListener('submit', async e=>{ e.preventDefault(); const q=document.getElementById('pz-adr').value.trim(); if(q.length<3) return;
  try{ const l = pzSugList.length ? pzSugList : await pzHledej(q); if(l.length) pzNajdi(l[0]); else pzMsg('Nic nenalezeno v Koryčanech a okolí. Najdi dům v mapě.'); }catch(err){ pzMsg('Vyhledávání ČÚZK teď neodpovídá. Najdi dům přímo v mapě.'); } });
// ---------- Jsem tady: poloha telefonu, jen pro posun mapy (nikam se neposila)
let pzGpsKruh = null;
document.getElementById('pz-gps').addEventListener('click', ()=>{
  if(!navigator.geolocation){ pzMsg('Tenhle prohlížeč polohu neumí. Najdi dům v mapě.'); return; }
  pzMsg('Zjišťuji polohu...');
  navigator.geolocation.getCurrentPosition(pos=>{
    const {latitude:lat, longitude:lon, accuracy:acc} = pos.coords;
    if(pzGpsKruh) pzGpsKruh.remove(); pzGpsKruh = L.circle([lat,lon],{radius:Math.max(acc,5),color:'#2d7fb8',weight:1,fillOpacity:.1,interactive:false}).addTo(map);
    map.setView([lat,lon],19);
    pzMsg(najdiParcelu(lon,lat) ? `Jsi tady zhruba (přesnost ±${Math.round(acc)} m). Klepni na svůj dům.` : 'Podle polohy jsi mimo území modelu. Najdi dům v mapě nebo podle adresy.');
  }, ()=>pzMsg('Polohu se nepodařilo zjistit (prohlížeč ji nepovolil nebo nemá signál). Najdi dům v mapě nebo podle adresy.'), {enableHighAccuracy:true, timeout:12000, maximumAge:60000});
});
// ---------- stav v odkazu (#pozemek?...): parcely (k. u. + cislo), odpovedi, opatreni, krok. Nic se neuklada.
function pzStav(){
  if(PZ.restoring || document.getElementById('tab-pozemek').classList.contains('hidden-tab')) return;
  const $=id=>document.getElementById(id), q=new URLSearchParams();
  q.set('k', PZ.step);
  const p=[...PARC.vybrane].map(k=>{ const x=PARC.feats[k].f.properties; return x.ku_kod+':'+x.cislo; });
  if(p.length) q.set('p', p.join(',')); else if(PZ.manual){ q.set('r',$('in-roof').value); q.set('g',$('in-green').value); }
  else { if(location.hash.startsWith('#pozemek?')) try{ history.replaceState(null,'','#pozemek'); }catch(e){} return; }
  q.set('o',$('in-drain').value); q.set('z',$('in-paved').value); q.set('s',$('in-soil').value); q.set('d',$('in-rain').value); q.set('m',[...chosen].join('.'));
  try{ history.replaceState(null,'','#pozemek?'+q.toString()); }catch(e){}
}
async function pzObnov(){
  const h = location.hash; if(!h.startsWith('#pozemek')) return;
  document.querySelector('nav.tabs button[data-tab="pozemek"]').click();
  const q = new URLSearchParams(h.split('?')[1]||''); if(![...q.keys()].length) return;
  const $=id=>document.getElementById(id); PZ.restoring = true;
  for(let t=0; t<150 && (!PARC.feats.length || jadroStav==='nacitam'); t++) await new Promise(r=>setTimeout(r,100));
  (q.get('p')||'').split(',').filter(Boolean).forEach(id=>{ const i=id.indexOf(':'), ku=id.slice(0,i), c=id.slice(i+1); const p=PARC.feats.find(p=>p.f.properties.ku_kod===ku && p.f.properties.cislo===c); if(p) PARC.vybrane.add(p.k); });
  if(PARC.vybrane.size){ prekresliVyber(); const c=PARC.zvyr.getBounds().getCenter(); odvodZMapy(c.lng,c.lat); $('w-pos').innerHTML='<span class="note">podle vybraných parcel</span>'; }
  else if(q.get('r')!=null){ PZ.manual=true; $('in-roof').value=q.get('r'); $('in-green').value=q.get('g')||0; }
  if(q.get('o')) $('in-drain').value=q.get('o'); if(q.get('s')) $('in-soil').value=q.get('s'); if(q.get('d')) $('in-rain').value=q.get('d');
  if(q.get('z')!=null){ $('in-paved').value=q.get('z'); $('in-paved').dispatchEvent(new Event('input')); }
  if(q.has('m')) chosen = new Set(q.get('m').split('.').filter(Boolean));
  PZ.restoring = false; recalc(); pzGo(+q.get('k')||1);
}
document.querySelectorAll('nav.tabs button').forEach(b=>b.addEventListener('click',()=>{ if(b.dataset.tab!=='pozemek' && location.hash.startsWith('#pozemek')){ try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){} } }));
document.getElementById('tab-pozemek').addEventListener('click', async e=>{ const a=e.target.closest('[data-share]'); if(!a) return; e.preventDefault(); pzStav(); const url=location.href, box=document.getElementById('pz-shared');
  try{ if(navigator.share){ await navigator.share({title:'Voda na mém pozemku - Koryčany', url}); return; } }catch(err){ if(err && err.name==='AbortError') return; }
  try{ await navigator.clipboard.writeText(url); box.textContent='Odkaz je zkopírovaný, vlož ho do zprávy. Obsahuje čísla vybraných parcel a tvoje odpovědi.'; }
  catch(err){ box.innerHTML='Zkopíruj si odkaz: <input readonly value="'+url.replace(/"/g,'&quot;')+'" aria-label="Odkaz">'; box.querySelector('input').select(); } });

document.getElementById('pz-known-x').addEventListener('click', e=>{ const k=e.target.closest('.pz-known'); const on=k.classList.toggle('ukaz'); e.target.setAttribute('aria-expanded', String(on)); e.target.textContent = on ? 'skrýt' : 'podrobnosti'; });
// ---------- vstupy
const $ = id=>document.getElementById(id);
function inputs(){
  return {roof:+$('in-roof').value||0, paved:+$('in-paved').value||0, pavedType:$('in-pavedtype').value, green:+$('in-green').value||0,
          drain:$('in-drain').value, slope:+$('in-slope').value||0, soil:$('in-soil').value, rain:+$('in-rain').value/1000, greenType:$('in-greentype').value, nkey:$('in-rain').selectedOptions[0]?.dataset.n||null};
}
// ---------- jádro: odtok
// zelena plocha: SCS-CN (ne soucinitel) - mala srazka se vsakne cela (Ia = 0,2 S), vetsi odteka podle pudy (HSP A-D) a sklonu
// CN2 podle Janecek 2012 / TR-55 (cn_tabulka, trida zahrada). Sklon do CN nevstupuje (ceske metodiky ho nemaji; zahranicni upravy
// Sharpley & Williams 1990, Huang 2006 jsou kalibrovane jinde a v CR neoverene) - rozhodnuti 21. 10. 2026; sklon se resi jen u vhodnosti opatreni.
function cnZahrada(i){ const t=D.cn_tabulka['7']; const v=t.varianty[i.greenType]||t.varianty[t.vychozi]; const cn2=v[i.soil]; return {cn2, cn2s:cn2, cn3s:Jadro.cnProIPS(cn2,3)}; }
function qmmP(P, cn){ if(!cn) return 0; const S=25400/cn-254, Ia=0.2*S; return P<=Ia?0:(P-Ia)*(P-Ia)/(P-Ia+S); }
function greenRunoff(i){ const c=cnZahrada(i); const P=i.rain*1000; const w3 = i.nkey && D.navrhove.podil_tvaru_pct[i.nkey] ? Jadro.vahaCN3(D.navrhove.podil_tvaru_pct[i.nkey], D.navrhove.qAPI) : 0;
  const q2=qmmP(P,c.cn2s), q3=qmmP(P,c.cn3s), q=q2*(1-w3)+q3*w3; const Ia=0.2*(25400/c.cn2s-254);
  let year=null; const H=D.srazky_hist; if(H){ let mm=0; for(let k=0;k<H.bin_mm.length;k++){ mm+=H.dni_za_rok[k]*qmmP(H.bin_mm[k]-0.5,c.cn2s); } year=i.green*mm/1000; }
  return {...c, w3, q_mm:q, q2_mm:q2, q3_mm:q3, Ia_mm:Ia, out:i.green*q/1000, year}; }
// nepropustne plochy: soucinitel C (CSN 75 9010) x (P - 1 mm); 1 mm = pocatecni ztrata smacenim a prohlubnemi, odpovida Ia pri CN 98 (TR-55: 0,2 S = 1,04 mm)
const IA_NEPROPUSTNE_MM = 1.0;
function rocniNepropustne(){ const H=D.srazky_hist; if(!H) return RAIN_Y; let mm=0; for(let k=0;k<H.bin_mm.length;k++) mm+=H.dni_za_rok[k]*Math.max(0,H.bin_mm[k]-0.5-IA_NEPROPUSTNE_MM); return mm/1000; }
const RAIN_Y_NEPR = rocniNepropustne(); // m/rok, co z nepropustne plochy opravdu odtece (cca 510 mm z 632)
function runoff(i){
  const cR=1.0, cP=coef(i.pavedType,i.slope), g=greenRunoff(i);
  const Pef=Math.max(0, i.rain-IA_NEPROPUSTNE_MM/1000);
  const roofOut = i.roof*Pef*cR, pavedOut=i.paved*Pef*cP, greenOut=g.out;
  const total=(i.roof+i.paved+i.green)*i.rain;
  return {cR,cP,cG:g.q_mm/(i.rain*1000||1),g,roofOut,pavedOut,greenOut,out:roofOut+pavedOut+greenOut,total,
          yearRoof:i.roof*RAIN_Y_NEPR*cR, yearPaved:i.paved*RAIN_Y_NEPR*cP, yearGreen:g.year};
}
// ---------- jádro: účinky opatření (jen typ vzorec/hodnota; zbytek kvalitativně)
// vrací {dV: m³ zadržené při zvoleném dešti, dYear: m³/rok, text, fit:true|string důvod nevhodnosti, needs:[]}
const EFF = {
  S02(i,r){ const fit = i.drain==='pozemek' ? 'svody už vedou na pozemek' : (i.drain==='nevim' ? true : true);
    return {dV:0,dYear:0,enabler:true,fit, text:`Sám nezadrží nic, ale otevře cestu pro zahradu a nádrž: ze střechy jde ${fmt(r.roofOut)} m³ na jeden déšť (${fmt0(r.yearRoof)} m³/rok) ${i.drain==='kanal'?'do kanalizace':'někam'}.`}; },
  Z01(i,r){ const fit = (i.soil==='D') ? 'půda D (jíl) - voda by stála, zvaž tůň Z02' : (i.slope>5 ? 'sklon nad 5 % - zvaž průleh Z03' : true);
    const A=(i.roof+i.paved); const lo=0.10*A, hi=0.20*A; const V=hi*0.25; // vzdutí 0,25 m
    const dV=Math.min(V, r.roofOut+r.pavedOut); const dYear=Math.min(hi*0.25*20, r.yearRoof+r.yearPaved); // 🤔 kapacita za rok ~ 20 naplnění
    return {dV,dYear:r.yearRoof+r.yearPaved,fit,needs:['S02'],
      text:`Záhon ${fmt0(lo)}-${fmt0(hi)} m² (10-20 % napojené plochy ✅⏳ Praha 2009, MENDELU 2022), vzdutí do 25 cm = pojme ${fmt(V)} m³ najednou. Zadrží ${fmt(dV)} m³ z tohoto deště; za rok zasákne až ${fmt0(r.yearRoof+r.yearPaved)} m³ místo kanalizace.`}; },
  Z10(i,r){ const fit = (i.soil==='C'||i.soil==='D') ? 'půda '+i.soil+' - vsak příliš pomalý (ČSN: kf > 1e-5 m/s)' : true;
    return {dV:r.roofOut,dYear:r.yearRoof,fit,needs:['S02'],text:`Štěrkové těleso nebo bloky na déšť 1x za 5 let: ${fmt(i.roof*0.0442)} m³ návrhový objem; zasákne celý odtok ze střechy (${fmt(r.roofOut)} m³ teď, ${fmt0(r.yearRoof)} m³/rok). Prázdné do 72 h, 1 m nad podzemní vodou, 5 m od domu ✅ ČSN 75 9010.`}; },
  S01(i,r){ const V=1.0; const dV=Math.min(V,r.roofOut); return {dV,dYear:Math.min(V*25, r.yearRoof),fit:true,needs:['S02'],
      text:`Nádrž 1 m³ (IBC 7 250 Kč ✅ Hornbach 18. 10. 2026) pojme ${fmt0(1000/Math.max(i.roof,1))} mm deště z tvé střechy; z tohoto deště zadrží ${fmt(dV)} m³. Nádrž 5 m³ (50 830 Kč bez montáže ✅) pojme ${fmt0(5000/Math.max(i.roof,1))} mm. Za rok využiješ jen to, co mezi dešti spotřebuješ (🤔 odhad ${fmt0(Math.min(V*25,r.yearRoof))} m³). Přepad veď do zahrady, ne do kanálu.`}; },
  Z04(i,r){ const cNew=coef('zatravnovaci_tvarnice',i.slope); const dV=i.paved*Math.max(0,i.rain-IA_NEPROPUSTNE_MM/1000)*(r.cP-cNew); const dYear=i.paved*RAIN_Y_NEPR*(r.cP-cNew);
    const fit = i.paved<=0 ? 'žádné zpevněné plochy' : (i.soil==='D' ? 'půda D - pod dlažbou se nevsákne' : true);
    return {dV,dYear,fit,text:`${fmt0(i.paved)} m² ${i.pavedType==='zatravnovaci_tvarnice'?'už jsou tvárnice':'-> zatravňovací tvárnice (C '+r.cP+' -> '+cNew+')'}: zasákne o ${fmt(dV)} m³ víc na tento déšť, o ${fmt0(dYear)} m³ za rok. Tráva je o 1-2 °C chladnější než dlažba ✅⏳ EPA 2008. Tvárnice 1 136 Kč/m² ✅ ÚÚR 2025.`}; },
  Z03(i,r){ const fit = i.slope<3 ? 'sklon pod 3 % - průleh nemá co zachytávat' : (i.slope>15 ? 'sklon nad 15 % - riziko eroze, raději terasa' : (i.soil==='D'?'půda D - nevsákne':true));
    const V=Math.min(10*0.3, r.greenOut); return {dV:V,dYear:Math.min(10*0.3*20,r.yearGreen||0),fit,text:`Průleh 10 m × 0,3 m² zadrží ${fmt(10*0.3)} m³ povrchového odtoku z vlastní zelené plochy (odtéká z ní ${fmt(r.greenOut)} m³). Vliv na vlhkost půdy nekvantifikován 🤔.`}; },
  Z02(i,r){ const fit = (i.soil==='A'||i.soil==='B') ? 'půda '+i.soil+' propustná - tůň bez fólie neudrží vodu' : true;
    return {dV:1.0,dYear:null,fit,text:`Tůň 2×1 m, 0,5 m = 1 m³ (SPPK B02 001 ✅: hloubka 0,8-1 m, mělčiny ≥ polovina, břehy ≤ 1:3). Hlavní přínos je život v zahradě 🤔; část vody se odpaří (bez čísla). Bez hráze a mimo potok není vodní dílo ✅ § 55; do 300 m² ověřit na úřadě ORP.`}; },
  S03(i,r){ return {dV:r.roofOut*0.75,dYear:r.yearRoof*0.75,fit:'jen ploché a mírně šikmé střechy s nosností - ověřit statikem',
      text:`Zadrží ~75 % běžného deště, u přívalu >30 mm sníží odtok o 77-83 % ✅ Žilina 2024. Povrch o 5-7 °C chladnější než fólie. 1 000-2 500 Kč/m² ✅⏳ UJEP 2023. NZÚ 2026: 2 000 Kč/m² jen jako úvěr a jen se zateplením ✅.`}; },
  S04(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda: nic. Horko: povrch střechy o 28-33 °C chladnější, uvnitř o 1,2-3,3 °C ✅⏳ EPA. Na vzduch v obci skoro bez vlivu (0,2-0,3 °C při 50 % střech) - do součtu za území se nepočítá.`}; },
  Z06(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda: nic měřitelného. Horko: ve stínu stromu je pocitově o 8-11 °C chladněji, vzduch jen o 0,4-2 °C ✅ CzechGlobe/UPOL 2018; povrch stěny ve stínu o 11-25 °C ✅⏳ EPA. Strom 1 775-6 100 Kč ✅ ÚÚR 2025. Pozor na sítě a odstup od plotu.`}; },
  Z05(i,r){ return {dV:0,dYear:0,fit:true,text:`Výpar z půdy nižší o cca třetinu až polovinu (17-79 % ✅ Irrigation Science 2024; slámový mulč ≥ 50 % ✅ DWD Lipsko 2012-2014, mokrý mulč nepomáhá). Organická hmota zvýší zásobu vody jen o 1,2 mm/100 mm na 1 % uhlíku ✅ metaanalýza 2018, na jílu nejméně. Do součtu vody za obec se nepočítá, na záhonech to poznáš.`}; },
  Z07(i,r){ return {dV:0,dYear:0,fit:true,text:`Vítr za plotem nižší o ~70 % do vzdálenosti 5 výšek, o 50 % do 10 výšek ✅⏳ UNL. Živý plot 2 m chrání pás 20-40 m. Výpar v mm nedohledán - ukazujeme plochu, ne litry.`}; },
  Z08(i,r){ return {dV:0,dYear:0,fit:true,text:`Vlhkost půdy nekvantifikována 🤔. Druhová pestrost: fázovaná seč ponechá 10-20 % neposečeno (SPPK D02 004 📄); nepravidelně kosené plochy o 20 % chudší ✅ Chytrá 2024. 0 Kč.`}; },
  Z09(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda: nic. Horko: stěna pod popínavkou o 6,5-7 °C chladnější (jih, západ) ✅ Toronto 2021, při husté zeleni až o 15 °C 📄. Ochladí zeď a pokoj, ne ulici.`}; },
  Z11(i,r){ return {dV:0,dYear:0,fit:true,needs:['S01'],text:`Šetří pitnou vodu; úspora kapkové závlahy proti postřiku pro naše zahrady nedohledána 🤔. Olla (Z12) je podle AZ1911 zhruba rovnocenná kapce.`}; },
  Z12(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda ke kořenům pod povrchem: úspora 50-70 % proti zálivce konví 📄 (aridní pokus, výrobce); u nás neměřeno. Ze dvou květináčů a silikonu za víkend. Roeschwoog 2022, Ixelles 2023 ✅. Vsak ani odtok neřeší.`}; },
  Z13(i,r){ return {dV:0,dYear:0,fit:(i.soil==='D'?'půda D - jen s výměnou substrátu, zvaž Z08':true),text:`Trvalky ze stepi místo zalévaného trávníku: po zapojení bez zálivky, údržba 2-6 min/m²/rok ✅ LWG Veitshöchheim 2021. Úspora v litrech nedohledána. Štěrk se v létě hřeje - stín to nenahradí.`}; },
  S05(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda ze sprchy na trvalky a stromy: úspora pitné vody na zahradu 33-59 % ✅ Austrálie 2020 (3 domy). V ČR bez závazných limitů ✅ SZÚ 2022: ne na zeleninu, ne z pračky a kuchyně. Vodu v krajině nepřidá.`}; },
  S06(i,r){ const osoby=4, V=5.0, rok=osoby*0.022*365; const dV=Math.max(0,Math.min(V,r.roofOut)-1.0); const dYear=Math.min(rok,r.yearRoof);
    return {dV,dYear,fit:(i.roof<40?'střecha pod 40 m² - nádrž na WC se nenaplní':true),needs:['S01','S02'],text:`Nádrž 5 m³ na WC bere vodu každý den (🤔 4 osoby × 17-26 l = ${fmt0(osoby*0.017*365)}-${fmt0(osoby*0.026*365)} m³/rok; WC je 20-30 % spotřeby ✅ Praha 14, Bielsko-Biała 2019). Proti nádrži 1 m³ zadrží navíc ${fmt(dV)} m³ z tohoto deště, za rok nahradí až ${fmt0(dYear)} m³ pitné vody. V suchém létě dojde za 1-3 týdny 🤔.`}; },
};
const ORDER_FALLBACK = 99;
function evalMeasures(i,r){
  const list = D.opatreni.filter(o=>o.misto.some(m=>['Z','S'].includes(m)) && EFF[o.id]).map(o=>{
    const e = EFF[o.id](i,r);
    return Object.assign({o},e);
  });
  const fit = list.filter(x=>x.fit===true), unfit=list.filter(x=>x.fit!==true);
  fit.sort((a,b)=> (b.enabler?1e9:(b.dV/ b.o.pracnost)) - (a.enabler?1e9:(a.dV/a.o.pracnost)) );
  return {fit,unfit};
}
let chosen = new Set(['S02','Z01']);
function cenaText(o){
  const c = o.ceny.filter(c=>c.hodnota!=null||c.rozsah); if(!c.length) return 'cena neověřena';
  const x=c[0]; const v = x.rozsah? `${fmt0(x.rozsah[0])}-${fmt0(x.rozsah[1])}` : fmt0(x.hodnota);
  const z = x.zdroj && D.zdroje[x.zdroj]; return `${v} ${x.jednotka}${x.rok?' ('+x.rok+(z?', '+ZN[z.znacka]:'')+')':''}`;
}
function kdeText(o){
  const pr=(o.priklady||[]); if(!pr.length && !o.prenositelnost && !o.rizika) return '';
  const li=pr.map(p=>`<li><b>${p.kde}</b>${p.kdy?' ('+p.kdy+')':''}: ${p.co}${p.mereno?`. <span class="note">Měřeno: ${p.mereno}.</span>`:'. <span class="note">Bez měření.</span>'} ${ZN[p.znacka]||''}${(p.zdroj||[]).map(z=>D.zdroje[z]?` <a class="src" href="${D.zdroje[z].url||'#'}" target="_blank" rel="noopener">[${D.zdroje[z].nazev.split(',')[0].split(':')[0].slice(0,50)}]</a>`:'').join('')}</li>`).join('');
  return `<details class="kde"><summary>${pr.length?'Kde to funguje ('+pr.length+')':'Přenositelnost a rizika'}</summary>${li?`<ul>${li}</ul>`:''}${o.prenositelnost?`<div class="note"><b>Přenositelnost do Koryčan:</b> ${o.prenositelnost}</div>`:''}${o.rizika?`<div class="note"><b>Rizika, co z toho neplyne:</b> ${o.rizika}</div>`:''}</details>`;
}

// ---------- výběr podle oblastí (OPATRENI-UX-ZADANI.md, 22. 10. 2026)
const KDE = {zahrada:{n:'Zahrada',d:'záhon, dvůr, sad',m:['Z']}, dum:{n:'Dům a střecha',d:'okapy, nádrž, fasáda',m:['S']}, obec:{n:'Obec a škola',d:'náměstí, ulice, veřejné budovy',m:['U','H']}, krajina:{n:'Krajina',d:'pole, louky, les, potok',m:['P','L','LES','T','C']}, mereni:{n:'Měř s námi',d:'škola, dobrovolníci',m:['M']}};
const CO = {sucho:{n:'Sucho',u:['I','R','W','E']}, prival:{n:'Příval a voda do kanálu',u:['Q','R','I','ER']}, horko:{n:'Horko',u:['CH','E']}, zivot:{n:'Život a voda v krajině',u:['B']}};
const PRAC = {1:'ruce a víkend',2:'dny, malá technika',3:'projekt a firma'};
const oblastiOp = o=>{const u=new Set([...o.ucinky.primarni,...o.ucinky.vedlejsi]); const r=new Set(); Object.entries(CO).forEach(([k,c])=>{if(c.u.some(x=>u.has(x))) r.add(k);}); if(o.misto.some(m=>['T','L','LES'].includes(m))) r.add('zivot'); return r;};
const kdeOp = o=> Object.keys(KDE).filter(k=>o.misto.some(m=>KDE[k].m.includes(m)));
// vzorový pozemek pro katalog: 100 m² střecha, 50 m² dvůr, 250 m² zahrada, HSP B, 10 mm, svody do kanálu
const VZOR = {roof:100,paved:50,pavedType:'dlazba_piskove_spary',green:250,drain:'kanal',slope:3,soil:'B',rain:0.010,greenType:'zahrada',nkey:null};
const fmtN = x=> Number.isInteger(+x) ? (+x).toLocaleString("cs-CZ") : (+x).toLocaleString("cs-CZ",{maximumFractionDigits:1});
const SLOVO = {E:'snížení výparu o', CH:'ochlazení o', W:'úspora pitné vody', ER:'méně eroze o', I:'vsak', R:'zadrží', Q:'zpomalení odtoku', B:''};
function jednoCislo(o, co, i, r){
  // 1) spočtené z EFF (pozemek nebo vzor) - jen když vyjde víc než nula
  if(EFF[o.id] && i){ const e=EFF[o.id](i,r); const y=e.dYear||0, v=e.dV||0;
    if(co==='sucho' && Math.round(y)>=1) return {t:`<b>za rok zůstane až ${fmt0(y)} m³</b> vody`, vzor:true};
    if(v>=0.05) return {t:`<b>z tohoto deště zadrží ${fmt(v)} m³</b>`, vzor:true};
    if(Math.round(y)>=1) return {t:`<b>za rok zůstane až ${fmt0(y)} m³</b> vody`, vzor:true}; }
  // 2) ručně napsaná hlavní věta z katalogu (build_opatreni.py HLAVNI_CISLO)
  const h=o.hlavni_cislo; if(h) return {t:(h.znacka?`<b>${h.text}</b> ${ZN[h.znacka]||''}`:`<span class="note">${h.text}</span>`), vzor:false};
  return {t:`<span class="note">účinek doložen slovně, bez čísla</span>`, vzor:false};
}
const PRAC_IK = {1:'<span class="pr" title="ruce a víkend">●○○</span>',2:'<span class="pr" title="dny, malá technika">●●○</span>',3:'<span class="pr" title="projekt a firma">●●●</span>'};
function kdeButtons(id, state, cb){ $(id).innerHTML=Object.entries(KDE).map(([k,v])=>`<button aria-pressed="${state.has(k)}" data-k="${k}"><b>${v.n}</b><span>${v.d}</span></button>`).join('');
  $(id).querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?state.add(b.dataset.k):state.delete(b.dataset.k); cb();})); }
function coButtons(id, state, cb){ $(id).innerHTML=Object.entries(CO).map(([k,v])=>`<button aria-pressed="${state.has(k)}" data-k="${k}">${v.n}</button>`).join('');
  $(id).querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?state.add(b.dataset.k):state.delete(b.dataset.k); cb();})); }
const PZCO = new Set();
function coMatch(o, state){ if(!state.size) return true; const ob=oblastiOp(o); return [...state].some(k=>ob.has(k)); }
function finText(o){ return o.financovani.map(f=>{const p=D.programy[f]; return p? (p.stav==='otevreno'&&f!=='vlastni'?'● ':'')+p.nazev.split(' - ')[0].split(' (')[0] : f}).join('; '); }
function povText(o){ return (CZ.povoleni[String(o.povoleni)]||'?')+(o.povoleni_pozn?' ('+o.povoleni_pozn+')':''); }
// zadrzeni vody na jednom pozemku pri zvolenych opatrenich (pouziva Muj pozemek i Cele uzemi v rezimu "jako muj pozemek")
function zadrzeni(i, r, ch){
  const ev = evalMeasures(i,r);
  let kept=0, keptYear=0;
  ev.fit.forEach(x=>{ if(ch.has(x.o.id)){ const needsOK = !(x.needs||[]).length || (x.needs||[]).every(n=>ch.has(n) || (n==='S02'&&i.drain==='pozemek')); if(needsOK){ kept+=x.dV; keptYear+= (x.dYear||0);} } });
  kept=Math.min(kept,r.out); const yearOut=r.yearRoof+r.yearPaved+(r.yearGreen||0); keptYear=Math.min(keptYear,yearOut);
  return {ev, kept, keptYear};
}
function recalc(){
  const i=inputs(), r=runoff(i);
  const rainmm=Math.round(i.rain*1000);
  // krok 3
  $('flow').innerHTML = `<tr><th>plocha</th><th class="num">m²</th><th class="num">C</th><th class="num">odteče m³</th></tr>
    <tr><td>střecha <span class="note">(první 1 mm zůstane na střeše)</span></td><td class="num">${fmt0(i.roof)}</td><td class="num">${r.cR}</td><td class="num">${fmt(r.roofOut)}</td></tr>
    <tr><td>zpevněné plochy</td><td class="num">${fmt0(i.paved)}</td><td class="num">${r.cP}</td><td class="num">${fmt(r.pavedOut)}</td></tr>
    <tr><td>zelené plochy <span class="note">(CN ${fmt0(r.g.cn2s)}${r.g.w3?` / nasycená ${fmt0(r.g.cn3s)}, váha ${fmt0(100*r.g.w3)} %`:''}; déšť do ${fmt0(r.g.Ia_mm)} mm se vsákne celý)</span></td><td class="num">${fmt0(i.green)}</td><td class="num">${fmt(r.cG,2)}</td><td class="num">${fmt(r.greenOut)}</td></tr>
    <tr class="total"><td>celkem pryč z pozemku při ${rainmm} mm</td><td class="num">${fmt0(i.roof+i.paved+i.green)}</td><td></td><td class="num">${fmt(r.out)} m³</td></tr>`;
  // účinky zvolených
  const z = zadrzeni(i, r, chosen); const ev = z.ev; let kept = z.kept, keptYear = z.keptYear;
  const pct=(x)=> r.out>0? 100*x/r.out:0;
  $('bars').innerHTML = `<div class="bar"><span>teď</span><div class="track"><i class="away" style="width:100%"></i></div><span class="num">${fmt(r.out)} m³</span></div>
    <div class="bar"><span>s opatřeními</span><div class="track"><i class="kept" style="width:${pct(kept)}%"></i><i class="away" style="width:${100-pct(kept)}%"></i></div><span class="num">${fmt(r.out-kept)} m³</span></div>`;
  $('year').textContent = `Za rok (${fmt0(K.srazky_rocni_mm.hodnota)} mm, stanice ČHMÚ Koryčany 1991-2020 ✅) odteče ze střechy a zpevněných ploch zhruba ${fmt0(r.yearRoof+r.yearPaved)} m³ (po odečtení 1 mm z každého deště: ${fmt0(RAIN_Y_NEPR*1000)} mm z ${fmt0(K.srazky_rocni_mm.hodnota)})${r.yearGreen!=null?`, ze zelených ploch ${fmt0(r.yearGreen)} m³ (SCS-CN po dnech z řady denních úhrnů ČHMÚ)`:'; ze zelených ploch zatím nepočítáno (čeká na rozdělení denních úhrnů ze stanice ČHMÚ - vyrob_srazky.bat)'}. Se zvolenými opatřeními zůstane u tebe až ${fmt0(keptYear)} m³.`;
  // karty
  if(!$('pz-co').children.length) coButtons('pz-co', PZCO, recalc);
  const cardHTML = x=>{const o=x.o; const on=chosen.has(o.id); const needs=(x.needs||[]).filter(n=>!(chosen.has(n)||(n==='S02'&&i.drain==='pozemek')));
    return `<div class="card ${on?'on':''}"><header><input type="checkbox" id="c-${o.id}" data-id="${o.id}" ${on?'checked':''}><div class="t"><b>${o.nazev}</b>${PRAC_IK[o.pracnost]||''}${x.enabler?'<span class="chip">předpoklad pro další</span>':(x.dV>0?`<span class="chip num">+${fmt(x.dV)} m³ teď</span>`:'')}</div></header>
      ${o.popis?`<div class="eff">${o.popis}</div>`:''}
      <div class="one">${x.text}</div>
      ${oblastiOp(o).has('zivot')&&o.ucinky.primarni.includes('B')?'<div class="zivot">+ život v zahradě</div>':''}
      ${needs.length?`<div class="note">Nejdřív je potřeba: ${needs.map(n=>byId[n]?byId[n].nazev:n).join(', ')}</div>`:''}
      ${kdeText(o)}
      <details><summary>zdroje, cena, povolení, financování</summary><ul>
        <li>Cena: ${cenaText(o)}</li><li>Financování: ${finText(o)}</li>
        <li>Povolení: ${povText(o)}</li>
        ${o.kvantifikace.map(k=>`<li>${CZ.ucinek[k.ucinek]||k.ucinek}: ${k.popis} ${ZN[k.znacka]||''}${(k.zdroj||[]).map(z=>D.zdroje[z]?` <a class="src" href="${D.zdroje[z].url||'#'}" target="_blank" rel="noopener">${D.zdroje[z].nazev.split(':')[0].slice(0,60)}</a>`:'').join(';')}</li>`).join('')}
        ${o.nedohledano&&o.nedohledano.length?`<li>Nedohledáno: ${o.nedohledano.join('; ')}</li>`:''}
        ${o.pozn_poctivost?`<li>${o.pozn_poctivost}</li>`:''}
      </ul></details></div>`;};
  const fitCo=ev.fit.filter(x=>coMatch(x.o,PZCO)); const top3=fitCo.slice(0,3), dalsi=fitCo.slice(3);
  $('cards').innerHTML = top3.map(cardHTML).join('') + (dalsi.length?`<details class="pz-more"><summary>Další možnosti (${dalsi.length})</summary><div class="cards">${dalsi.map(cardHTML).join('')}</div></details>`:'');
  $('cards').querySelectorAll('input[type=checkbox]').forEach(cb=>cb.addEventListener('change',()=>{ if(cb.checked) chosen.add(cb.dataset.id); else chosen.delete(cb.dataset.id); recalc(); }));
  $('unfit').innerHTML = ev.unfit.length? `<details><summary><b>Nehodí se sem (${ev.unfit.length})</b> <span class="note">- proč</span></summary><ul>${ev.unfit.map(x=>`<li>${x.o.nazev} (${x.o.id}) - ${x.fit}</li>`).join('')}</ul></details>` : '';
  // krok 5
  const n=200;
  pzRender(i, r, kept, keptYear, n);
  const dest_adj={'10':'běžném dešti','20':'silném dešti','32.2':'lijáku'}[$('in-rain').value]||'dešti';
  $('scale').innerHTML = `Při ${n} domácnostech srovnatelné velikosti zůstane při jednom ${dest_adj} (${rainmm} mm) zhruba <b>${fmt0(kept*n)} m³</b> vody v půdě a zahradách místo v kanálu. To je rozdíl mezi „odteklo“ a „zůstalo“, který může měnit poušť v oázu.`;
  renderUzemi();
}
['in-roof','in-paved','in-pavedtype','in-green','in-greentype','in-drain','in-slope','in-soil','in-rain'].forEach(id=>$(id).addEventListener('input',recalc));

// ---------- území
function renderUzemi(){
  const n=+$('u-n').value||0, roof=+$('u-roof').value||0, paved=+$('u-paved').value||0, rain=+$('u-rain').value/1000, pct=+$('u-pct').value/100;
  $('u-pct-val').textContent=Math.round(pct*100);
  const pack=[...document.querySelectorAll('#u-pack button[aria-pressed="true"]')].map(b=>b.dataset.m);
  const moje = UZ.moje && pzReady();
  document.getElementById('tab-uzemi').classList.toggle('u-moje', moje);
  $('u-zaklad').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed', String((b.dataset.z==='moje')===moje)));
  $('u-zaklad').querySelector('[data-z="moje"]').disabled = !pzReady();
  const i = moje ? Object.assign(inputs(), {rain, nkey: $('u-rain').selectedOptions[0]?.dataset.n||null}) : {roof,paved,pavedType:'dlazba_piskove_spary',green:250,drain:'kanal',slope:3,soil:'B',rain};
  const r=runoff(i); let per=0, perY=0;
  if(moje){ const z=zadrzeni(i, r, chosen); per=z.kept; perY=z.keptYear;
    const nazvy=[...chosen].filter(id=>byId[id] && z.ev.fit.some(x=>x.o.id===id)).map(id=>byId[id].nazev.split(' (')[0].toLowerCase());
    $('u-moje-n').hidden=false;
    $('u-moje-n').innerHTML=`<b>Počítám, jako by každá zapojená domácnost měla pozemek jako ty:</b> střecha ${fmt0(i.roof)} m², dlažba ${fmt0(i.paved)} m², zahrada ${fmt0(i.green)} m², okapy ${i.drain==='kanal'?'do kanalizace':i.drain==='pozemek'?'na zahradu':'nevíš kam'}; opatření: ${nazvy.length?nazvy.join(', '):'zatím žádné, které zadrží vodu'}. Jedna domácnost tak udrží ${fmt(per)} m³ z deště ${Math.round(rain*1000)} mm. <button type="button" class="linkbtn" data-tab-go2="pozemek">Změnit v Můj pozemek</button><br><span class="note">Domy v obci mají různé střechy a půdy, je to „co kdyby“, ne odhad pro obec 🤔. Průměrný dům v území má půdorys __ROOF__ m² (ČÚZK ✅).</span>`;
  } else $('u-moje-n').hidden=true;
  if(!moje && pack.includes('S02')){ if(pack.includes('Z01')){const e=EFF.Z01(i,r); per+=e.dV; perY+=e.dYear;} if(pack.includes('S01')){const e=EFF.S01(i,r); per+=e.dV; perY+=e.dYear;} }
  if(!moje){ if(pack.includes('Z04')){const e=EFF.Z04(i,r); per+=e.dV; perY+=e.dYear;}
  per=Math.min(per,r.roofOut+r.pavedOut); perY=Math.min(perY,r.yearRoof+r.yearPaved); }
  const hh=Math.round(n*pct), tot=per*hh, totY=perY*hh;
  const allOut=(moje ? r.out : r.roofOut+r.pavedOut)*n;
  $('u-sum').innerHTML=`<div class="box"><div class="big num">${hh}</div><small>domácností se zapojí</small></div>
    <div class="box"><div class="big num">${fmt0(tot)} m³</div><small>zůstane v území na jeden déšť ${Math.round(rain*1000)} mm (ze ${fmt0(allOut)} m³ ${moje?'z pozemků':'ze střech a dvorů'} všech domácností)</small></div>
    <div class="box"><div class="big num">${fmt0(totY)} m³</div><small>za rok</small></div>`;
  // podíly podle počtu budov v dílčích povodích (ČÚZK INSPIRE BU)
  const U=D.uzemi; const celk=Object.values(U.podle_povodi).reduce((t,x)=>t+x.pocet,0);
  const sidla=Object.entries(U.podle_povodi).map(([k,x])=>[k.replace('Koryčany (','').replace(')',''), x.pocet/celk]);
  $('u-table').innerHTML=`<tr><th>dílčí povodí (podíl podle počtu budov)</th><th class="num">domácností</th><th class="num">zapojí se</th><th class="num">m³ na déšť</th><th class="num">m³/rok</th></tr>`+
    sidla.map(([s,p])=>`<tr><td>${s}</td><td class="num">${fmt0(n*p)}</td><td class="num">${fmt0(n*p*pct)}</td><td class="num">${fmt0(tot*p)}</td><td class="num">${fmt0(totY*p)}</td></tr>`).join('')+
    `<tr class="total"><td>profil na Kyjovce pod Koryčany</td><td class="num">${n}</td><td class="num">${hh}</td><td class="num">${fmt0(tot)}</td><td class="num">${fmt0(totY)}</td></tr>`;
  if(!moje && !pack.includes('S02') && (pack.includes('Z01')||pack.includes('S01'))) $('u-limit').innerHTML='<b>Pozor:</b> dešťová zahrada a nádrž bez odpojení svodů (S02) nic nezadrží - voda se k nim nedostane. Balíček to respektuje.';
  else { const key='P'+Math.round(rain*1000)+'mm', od=U.odtok[key]; const spadne=U.plocha_ha*1e4*rain;
    $('u-limit').innerHTML=`<b>Na co to nestačí:</b> ${fmt0(tot)} m³ je ${fmt(100*tot/spadne,2)} % deště, který při ${Math.round(rain*1000)} mm spadne na území modelu (${fmt0(U.plocha_ha)} ha = ${fmt0(spadne)} m³)${od?`, a ${fmt(100*tot/od.objem_m3,1)} % povrchového odtoku z celého území (${fmt0(od.objem_m3)} m³ podle SCS-CN, CN ${U.cn_vazene}, IPS II)`:''}. Povodňovou vlnu na Kyjovce to nezmění. Součet platí pro vodu ze střech a dvorů; pole, louky a les jsou samostatná kapitola (USLE, pásy, průlehy) a v tomto náhledu se nepočítají.`; }
  $('u-plus').innerHTML=`<b>Co to ale je:</b> ${fmt0(totY)} m³ vody za rok v půdě a zahradách místo v kanálu. Pro srovnání: nákladní cisterna má 🤔 10 m³, tohle je ${fmt0(totY/10)} cisteren ročně, bez jediné stavby. A na každý liják o ${fmt0(tot)} m³ pomalejší odtok z intravilánu do potoka.`;
  // kontext
  $('u-context').innerHTML = D.opatreni.filter(o=>o.kontext).map(o=>`<div class="card"><header><div class="t"><b>${o.nazev}</b><div class="meta"><span class="chip id">${o.id}</span><span class="chip">rozhoduje: ${o.rozhoduje.map(r=>CZ.rozhoduje[r].split(' ')[0]).join(', ')}</span><span class="chip">${cenaText(o)}</span><span class="chip">povolení: ${CZ.povoleni[String(o.povoleni)]}</span></div></div></header>
    <div class="eff">${o.kvantifikace.map(k=>k.popis+' '+(ZN[k.znacka]||'')).join(' ')}</div>${o.pozn_poctivost?`<div class="note">${o.pozn_poctivost}</div>`:''}${kdeText(o)}<div class="note">Financování: ${finText(o)}</div></div>`).join('');
}
const UZ = {moje:false};
document.getElementById('u-zaklad').addEventListener('click', e=>{ const b=e.target.closest('button[data-z]'); if(!b || b.disabled) return; UZ.moje = b.dataset.z==='moje'; renderUzemi(); });
document.getElementById('tab-uzemi').addEventListener('click', e=>{ const b=e.target.closest('[data-tab-go2]'); if(!b) return; document.querySelector('nav.tabs button[data-tab="pozemek"]').click(); window.scrollTo({top:0}); });
// ---------- velke strechy podle ucelu
const UCEL_KDO = {'rodinný dům':['domácnosti','S02, S01, Z01, Z10 (NZÚ, vlastní)'], 'průmysl':['firmy (areály)','S02 + vsak/nádrž na areálu, S03 zelená střecha (OPŽP 1.3.4), U02 propustné plochy'],
  'zemědělství':['zemědělské podniky','S02 + nádrž na závlahu, vsak; U02'], 'vedlejší stavba (garáž, kůlna)':['domácnosti','S01 sud/IBC u kůlny'], 'veřejná služba':['obec, škola, kraj','U04 retence z veřejných budov (OPŽP 1.3.4), U02, S03'],
  'bytový dům':['SVJ, družstva, obec','S02 + vsak/nádrž, S03 (NZÚ bytové domy 💻 ověřit)'], 'obchod':['firmy','S02, U02'], 'kancelář':['firmy','S02, U02'], 'obchod a služby':['firmy','S02, U02'], 'bydlení':['domácnosti','S02, S01'], 'neuvedeno':['?',''],
  'domácnosti':['domácnosti','S02, S01, Z01, Z10 (NZÚ, vlastní)'], 'obchody a služby':['firmy','S02, U02']};
// sloučení účelů RÚIAN do skupin pro tabulku (rozhodnutí uživatele 21. 10. 2026)
const UCEL_SKUPINA = {'rodinný dům':'domácnosti', 'bydlení':'domácnosti', 'kancelář':'obchody a služby', 'obchod':'obchody a služby', 'obchod a služby':'obchody a služby'};
function renderStrechy(){
  const rain=+$('u-rain').value/1000; const U={};
  for(const [u,x] of Object.entries(D.uzemi.podle_ucelu)){ const g=UCEL_SKUPINA[u]||u; U[g]=U[g]||{pocet:0,plocha_strech_m2:0}; U[g].pocet+=x.pocet; U[g].plocha_strech_m2+=x.plocha_strech_m2; }
  const rows=Object.entries(U).map(([u,x])=>({u,n:x.pocet,a:x.plocha_strech_m2,v:x.plocha_strech_m2*rain})).sort((a,b)=>b.a-a.a);
  const tot=rows.reduce((t,r)=>t+r.v,0), totA=rows.reduce((t,r)=>t+r.a,0);
  $('s-table').innerHTML=`<tr><th>účel budov</th><th class="num">budov</th><th class="num">střechy ha</th><th class="num">m³ na déšť ${Math.round(rain*1000)} mm</th><th class="num">prům. m³/budovu</th><th>kdo rozhoduje</th><th>opatření z katalogu</th></tr>`+
    rows.map(r=>`<tr><td>${r.u}</td><td class="num">${fmt0(r.n)}</td><td class="num">${fmt(r.a/1e4)}</td><td class="num">${fmt0(r.v)}</td><td class="num">${fmt(r.v/r.n)}</td><td>${(UCEL_KDO[r.u]||['',''])[0]}</td><td>${(UCEL_KDO[r.u]||['',''])[1]}</td></tr>`).join('')+
    `<tr class="total"><td>všechny budovy v území</td><td class="num">${fmt0(rows.reduce((t,r)=>t+r.n,0))}</td><td class="num">${fmt(totA/1e4)}</td><td class="num">${fmt0(tot)}</td><td></td><td></td><td></td></tr>`;
  const rd=U['domácnosti'], pr=U['průmysl'], ve=U['veřejná služba'], ze=U['zemědělství'];
  $('s-limit').innerHTML=`<b>Co z toho plyne:</b> ${fmt0(pr.pocet)} průmyslových budov má ${fmt(pr.plocha_strech_m2/1e4)} ha střech = ${fmt0(100*pr.plocha_strech_m2/rd.plocha_strech_m2)} % plochy střech všech ${fmt0(rd.pocet)} domů domácností; průměrná průmyslová střecha (${fmt0(pr.plocha_strech_m2/pr.pocet)} m²) dá na jeden déšť tolik vody jako ${fmt0(pr.plocha_strech_m2/pr.pocet/(rd.plocha_strech_m2/rd.pocet))} domů. Veřejné budovy (${ve.pocet}, ${fmt(ve.plocha_strech_m2/1e4)} ha) a zemědělské (${ze.pocet}, ${fmt(ze.plocha_strech_m2/1e4)} ha) jsou v rukou obce, kraje a pár podniků - tam má smysl začít jednáním, ne letákem. Kam ty střechy dnes odvádějí vodu (kanalizace / vsak / potok), v datech není - zjistit u provozovatelů (otázka pro město: kanalizace jednotná nebo oddílná?).`;
}
renderStrechy(); $('u-rain').addEventListener('input',renderStrechy);
// ---------- hraz na potoce (jadro.js nadrz v0.3; toky.json a smer_v se dotahuji az tady)
let damMap=null, damVrstva=null, damStav='nic';
function hrazInit(){
  if(damMap){ damMap.invalidateSize(); return; }
  damMap = L.map('dam-map',{zoomControl:true}).setView([49.108,17.17],14);
  L.tileLayer('https://ags.cuzk.gov.cz/arcgis1/rest/services/ZTM_WM/MapServer/WMTS/tile/1.0.0/ZTM_WM/default/GoogleMapsCompatible/{z}/{y}/{x}',{maxZoom:19,attribution:'ČÚZK - on-line (ZTM)'}).addTo(damMap);
  damStav='nacitam'; $('h-out').innerHTML='<p class="note">Načítám toky a terén...</p>';
  const cekej = ()=> jadroStav==='ok' ? Promise.resolve() : (jadroStav==='chyba' ? Promise.reject('rastry') : new Promise(r=>setTimeout(r,300)).then(cekej));
  cekej().then(()=>Jadro.nactiProNadrze(BASE+'data/web/')).then(()=>{
    damStav='ok';
    L.layerGroup(Jadro.toky.linie.map(l=>L.polyline(l.x.map((X,k)=>{const q=Jadro.xyNaLonLat(X,l.y[k]); return [q[1],q[0]];}),{color:'#1a7fd6',weight:3,opacity:.85}))).addTo(damMap);
    $('h-out').innerHTML='<p class="note">Klikni na modrý potok.</p>';
  }).catch(err=>{ damStav='chyba'; console.warn('nadrze',err); $('h-out').innerHTML='<p class="note">Toky nebo terén se nenačetly - tato část nefunguje.</p>'; });
  damMap.on('click',e=>{ hrazPosledni=[e.latlng.lng,e.latlng.lat]; hrazSpocti(); });
}
let hrazPosledni=null;
function hrazSpocti(){
  const h=+$('h-vyska').value;
  const vd=$('h-vd');
  if(!hrazPosledni || damStav!=='ok'){ vd.style.display='none'; return; }
  if(damVrstva){ damVrstva.remove(); damVrstva=null; }
  const n=Jadro.nadrz(hrazPosledni[0],hrazPosledni[1],h,{polomerM:60});
  vd.style.display = n && n.info && n.info.length ? '' : 'none';
  if(n && n.info) vd.innerHTML = '<b>Pro informaci:</b> ' + n.info.join(' ');
  if(!n){ $('h-out').innerHTML='<p class="note">Mimo data modelu.</p>'; return; }
  if(n.chyba==='daleko_od_toku'){ $('h-out').innerHTML=`<p class="note">Hráz se staví jen na potoce (modré čáry). Nejbližší je ${fmt0(n.vzdalenost_m)} m od kliku - klikni blíž.</p>`; return; }
  damVrstva=L.layerGroup().addTo(damMap);
  if(n.maska){ const bb=Jadro.obalMasky(n.maska,30); if(bb){ const im=Jadro.obrazek(i=>n.maska[i]?[30,110,220,170]:null,bb,900); const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; c.getContext('2d').putImageData(new ImageData(im.data,im.width,im.height),0,0); L.imageOverlay(c.toDataURL(),im.bounds,{opacity:.75,interactive:false}).addTo(damVrstva);} }
  if(n.obrys_lonlat) L.polygon(n.obrys_lonlat.map(([lo,la])=>[la,lo]),{color:'#1e6ec8',weight:1,dashArray:'4 3',fillOpacity:.35}).addTo(damVrstva);
  L.polyline(n.hraz_lonlat.map(([lo,la])=>[la,lo]),{color:'#a23b3b',weight:5}).addTo(damVrstva);
  const P=+$('h-rain').value, W3=vahaCN3Sel($('h-rain'));
  const st=Jadro.statBunek(n.povodi_bunky,P,2).odtok;
  const odt = st ? st.objem_m3*(1-W3)+st.objem_m3_cn3*W3 : 0;
  const tun=n.typ==='tun_udolnice', V=n.objem_m3, rz=a=>`${fmt0(a[0])} - ${fmt0(a[1])}`;
  const pod=Math.min(100,100*V/Math.max(1,odt));
  $('h-out').innerHTML = `<div class="sum">`+
    `<div><div class="eyebrow">${tun?'tůň / poldr v údolnici (orientačně)':'nádrž za hrází'}</div><div class="num" style="font-size:1.4rem">${tun?rz(n.objem_rozsah_m3):fmt0(V)} m³</div><div class="note">${tun?'rozsah: údolí tvaru V až ploché dno 🤔':'zatopí '+fmt0(n.plocha_ha*1e4)+' m², hloubka max '+fmt(n.hloubka_max_m,1)+' m'}</div></div>`+
    `<div><div class="eyebrow">odteče z povodí při dešti ${fmt0(P)} mm</div><div class="num" style="font-size:1.4rem">${fmt0(odt)} m³</div><div class="note">povodí k hrázi ${fmt(n.povodi_km2,2)} km² (SCS-CN)</div></div>`+
    `<div><div class="eyebrow">nádrž pojme</div><div class="num" style="font-size:1.4rem">${pod<1?"pod 1":fmt0(pod)} %</div><div class="note">prázdná nádrž, bez ztrát</div></div></div>`+
    `<p class="note">Hráz ${fmt0(n.delka_hraze_m)} m dlouhá kolmo na tok${n.hraz_uzavira?'':' - <b>údolí neuzavře</b>'}, dno ${fmt(n.kota_dna,1)} m n. m., hladina ${fmt(n.hladina,1)} m n. m.`+
    `${tun?`, sklon dna ${fmt(100*n.profil_odhad.sklon_dna,1)} %, voda vystoupá ${fmt0(n.profil_odhad.delka_vzduti_m)} m proti proudu`:`; kontrola z příčného profilu ${rz(n.profil_odhad.objem_m3)} m³`}.</p>`+
    (odt<1?`<p class="note">Při dešti ${fmt0(P)} mm z povodí po povrchu skoro nic neodteče, vsákne se. Nádrž plní hlavně silnější deště a průtok v potoce (ten model nepočítá) - pro posouzení hráze vyber silnější déšť.</p>`:'')+
    n.varovani.map(v=>`<p class="note" style="color:var(--warn)">! ${v}</p>`).join('');
}
$('h-vyska').addEventListener('input',hrazSpocti); $('h-rain').addEventListener('input',hrazSpocti);

$('u-zdroj').innerHTML=`V území modelu (${fmt0(D.uzemi.plocha_ha)} ha, povodí Kyjovky k jezu před Mouchnicemi bez povodí nad přehradou) je ${fmt0(D.uzemi.budov)} budov s půdorysem ${fmt0(D.uzemi.strechy_m2/1e4*10)/10} ha, z toho ${fmt0(D.uzemi.rd_pocet)} rodinných domů (${fmt0(D.uzemi.rd_strechy_m2/1e4*10)/10} ha) ✅ ČÚZK INSPIRE BU, 19. 10. 2026. Zpevněné plochy u domů nejsou v datech - odhad. Počítá se jen voda ze střech a dvorů rodinných domů; průmysl, bytové domy a veřejné budovy zatím ne.`;
['u-n','u-roof','u-paved','u-rain','u-pct'].forEach(id=>$(id).addEventListener('input',renderUzemi));
document.querySelectorAll('#u-pack button').forEach(b=>b.addEventListener('click',()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true');renderUzemi();}));

// ---------- katalog
const KF={misto:new Set(),rozhoduje:new Set(),ucinek:new Set(),fin:new Set(),kde:new Set(),co:new Set()};
kdeButtons('k-kde',KF.kde,()=>renderKatalog()); coButtons('k-co',KF.co,()=>renderKatalog());
const VZOR_R = runoff(VZOR);
function chips(id,obj,key){ $(id).innerHTML=Object.entries(obj).map(([k,v])=>`<button aria-pressed="false" data-k="${k}">${k} ${v.split(' (')[0]}</button>`).join('');
  $(id).querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?KF[key].add(b.dataset.k):KF[key].delete(b.dataset.k); renderKatalog();})); }
chips('k-misto',CZ.misto,'misto'); chips('k-rozhoduje',Object.fromEntries(Object.entries(CZ.rozhoduje).filter(([k])=>k!=='zemedelec')),'rozhoduje'); chips('k-ucinek',CZ.ucinek,'ucinek');
$('k-fin').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?KF.fin.add(b.dataset.f):KF.fin.delete(b.dataset.f); renderKatalog();}));
function renderKatalog(){
  const list=D.opatreni.filter(o=> (!KF.kde.size||kdeOp(o).some(k=>KF.kde.has(k))) && coMatch(o,KF.co) && (!KF.misto.size||o.misto.some(m=>KF.misto.has(m))) && (!KF.rozhoduje.size||o.rozhoduje.some(m=>KF.rozhoduje.has(m)))
    && (!KF.ucinek.size||[...o.ucinky.primarni,...o.ucinky.vedlejsi].some(u=>KF.ucinek.has(u)))
    && (!KF.fin.has('otevreno')||o.financovani.some(f=>D.programy[f]&&D.programy[f].stav==='otevreno'&&f!=='vlastni'))
    && (!KF.fin.has('svepomoc')||(o.pracnost===1&&o.povoleni===0)));
  $('k-count').textContent=list.length+' / '+D.opatreni.length;
  const co1=[...KF.co][0]||null; const jeVzor=o=>o.misto.some(m=>['Z','S'].includes(m));
  list.sort((a,b)=>(a.pracnost-b.pracnost)||(a.kontext-b.kontext));
  $('k-cards').innerHTML=list.map(o=>`<div class="card"><header><div class="t"><b>${o.nazev}</b>${PRAC_IK[o.pracnost]||''}${o.kontext?'<span class="chip">obec / správce</span>':''}</div></header>
    ${o.popis?`<div class="eff">${o.popis}</div>`:''}
    <div class="one">${(()=>{const j=jednoCislo(o, co1, jeVzor(o)?VZOR:null, VZOR_R); return j.t+(j.vzor?' <span class="note">(vzor: 100 m² střechy, 10 mm)</span>':'');})()}</div>
    ${o.ucinky.primarni.includes('B')?'<div class="zivot">+ život a pestrost</div>':''}
    ${kdeText(o)}
    <details><summary>účinek, zdroje, ceny, financování</summary><ul>
      <li>${o.id} - kde: ${o.misto.map(m=>CZ.misto[m]).join(', ')}; rozhoduje: ${o.rozhoduje.map(r=>CZ.rozhoduje[r]?CZ.rozhoduje[r].split(' (')[0]:r).join(', ')}; účinky: ${o.ucinky.primarni.map(u=>CZ.ucinek[u]).join(', ')}${o.ucinky.vedlejsi.length?' (vedlejší: '+o.ucinky.vedlejsi.map(u=>CZ.ucinek[u]).join(', ')+')':''}</li>
      ${o.kvantifikace.map(k=>`<li><b>${CZ.ucinek[k.ucinek]||k.ucinek}</b> (${k.typ}) ${ZN[k.znacka]||''}: ${k.popis}${(k.zdroj||[]).map(z=>D.zdroje[z]?` <a class="src" href="${D.zdroje[z].url||'#'}" target="_blank" rel="noopener">[${D.zdroje[z].nazev.split(',')[0].slice(0,50)}]</a>`:'').join('')}</li>`).join('')}
      ${o.ceny.map(c=>`<li>Cena: ${c.polozka} - ${c.hodnota!=null?fmt0(c.hodnota):(c.rozsah?fmt0(c.rozsah[0])+'-'+fmt0(c.rozsah[1]):'cena neověřena')} ${c.jednotka}${c.rok?' ('+c.rok+')':''}${c.pozn?' - '+c.pozn:''}</li>`).join('')}
      <li>Financování: ${finText(o)}</li><li>Povolení: ${povText(o)}</li>
      ${o.vazby.potrebuje.length?`<li>Potřebuje: ${o.vazby.potrebuje.join(', ')}</li>`:''}${o.vazby.synergie.length?`<li>Hodí se k: ${o.vazby.synergie.join(', ')}</li>`:''}
      ${o.nedohledano&&o.nedohledano.length?`<li>Nedohledáno: ${o.nedohledano.join('; ')}</li>`:''}${o.pozn_poctivost?`<li>${o.pozn_poctivost}</li>`:''}
    </ul></details></div>`).join('');
}
renderKatalog();

// ---------- o modelu
$('konst').innerHTML = `<ul><li>Srážky: ${K.srazky_rocni_mm.hodnota} mm/rok ✅ (${K.srazky_rocni_mm.pozn}); měsíčně I-XII: ${Object.values(D.uzemi.srazky.mesicni_mm).join(', ')} mm; největší denní úhrny ${D.uzemi.srazky.max_denni.map(x=>x[1]+' mm ('+x[0]+')').join(', ')}</li>
<li>Návrhové 6hodinové úhrny Koryčany ✅ (ČVUT/ČHMÚ metodika 2023, rastr 1 km): N2 ${K.navrhovy_dest_6h_korycany.N2_mm}, N5 ${K.navrhovy_dest_6h_korycany.N5_mm}, N10 ${K.navrhovy_dest_6h_korycany.N10_mm}, N20 ${K.navrhovy_dest_6h_korycany.N20_mm}, N50 ${K.navrhovy_dest_6h_korycany.N50_mm}, N100 ${K.navrhovy_dest_6h_korycany.N100_mm} mm; nejčastější průběh C (dva vrcholy, 35 %), přívalový A jen 9 %</li>
<li>N-leté denní úhrny Koryčany (Gumbel 1921-2025, odhad 🤔, jen pro srovnání): N2 ${K.navrhovy_dest_denni_korycany.N2_mm}, N10 ${K.navrhovy_dest_denni_korycany.N10_mm}, N100 ${K.navrhovy_dest_denni_korycany.N100_mm} mm</li>
<li>Území modelu: ${fmt0(D.uzemi.plocha_ha)} ha, CN vážené ${D.uzemi.cn_vazene} (HSP z BPEJ, v lese a zástavbě odhad), odtok při 20/40/60 mm: ${fmt0(D.uzemi.odtok.P20mm.objem_m3)} / ${fmt0(D.uzemi.odtok.P40mm.objem_m3)} / ${fmt0(D.uzemi.odtok.P60mm.objem_m3)} m³ (SCS-CN, IPS II) ✅ 06_cn.py</li>
<li>Terén a půda po kliku: DMR 5G ČÚZK (5 m), BPEJ SPÚ -> HSP podle Janeček 2012; jádro web/jadro.js (docs/JADRO.md)</li>
<li>Návrhový déšť p=0,2: 15 min ${K.navrhovy_dest_p02['15min_mm']} mm, 60 min ${K.navrhovy_dest_p02['60min_mm']} mm, 24 h ${K.navrhovy_dest_p02['24h_mm']} mm ✅ (${K.navrhovy_dest_p02.pozn})</li>
<li>Zelené plochy pozemku: SCS-CN, CN zahrady podle půdy A-D (Janeček 2012 / TR-55 ✅⏳: trávník 39/61/74/80), bez úpravy na sklon (české metodiky ji nemají); u návrhových dešťů vážení CN2/CN3 jako v krajině; roční odtok po dnech z histogramu denních úhrnů ČHMÚ Koryčany 1991-2019. Střechy a zpevněné plochy: součinitel ČSN × (déšť - 1 mm), 1 mm = ztráta smáčením (Ia pro CN 98 podle TR-55 ✅⏳)</li>
<li>Součinitele odtoku C (střechy, zpevněné; sklon &lt;1 / 1-5 / &gt;5 %): ${Object.entries(C).filter(([k,v])=>Array.isArray(v)).map(([k,v])=>k.replaceAll('_',' ')+' '+v.join('/')).join('; ')} ✅</li>
<li>Vsak: prázdné do ${K.vsak.vyprazdneni_max_h} h, ${K.vsak.nad_hladinou_pv_min_m} m nad podzemní vodou, ${K.vsak.odstup_budova_nehydroizolovana_m} m od budovy ✅</li>
<li>USLE: přípustná ztráta půdy od 1. 7. 2026 ${K.usle.Gp_t_ha_rok['od_2026-07-01'].melke}/${K.usle.Gp_t_ha_rok['od_2026-07-01'].ostatni} t/ha/rok ✅ (v náhledu se nepočítá)</li></ul>`;
$('progs').innerHTML='<ul>'+Object.values(D.programy).map(p=>`<li><b>${p.nazev}</b> - ${p.stav}${p.do?' do '+p.do:''}${p.pozn?': '+p.pozn:''}</li>`).join('')+'</ul>';

// ---------- Jak bylo
(function(){
const W=D.pocasi, N=W.normaly, DNY=Object.keys(W.dny).sort();
if(!DNY.length) return;
const MES=['leden','únor','březen','duben','květen','červen','červenec','srpen','září','říjen','listopad','prosinec'];
const dim=(y,m)=>new Date(y,m,0).getDate();
const csd=s=>{const [y,m,d]=s.split('-');return `${+d}. ${+m}. ${y}`;};
const iso=d=>d.toISOString().slice(0,10);
const addD=(s,n)=>{const d=new Date(s+'T00:00:00Z'); d.setUTCDate(d.getUTCDate()+n); return iso(d);};
const dni=n=>n+' '+(n===1?'den':n>=2&&n<=4?'dny':'dní');
const ZDR={K:'ČHMÚ Koryčany',P:'KS Koryčany (Povodí Moravy)',N:'ČHMÚ Nemochovice'};
const R=N.rocniky, LAST=DNY[DNY.length-1], ROK=+LAST.slice(0,4);
$('jb-upd').textContent=W.vytvoreno.replace('T',' ').replace('Z',' UTC');
const mean=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;
function lin(xs,ys){const n=xs.length,mx=mean(xs),my=mean(ys);let sxy=0,sxx=0;for(let i=0;i<n;i++){sxy+=(xs[i]-mx)*(ys[i]-my);sxx+=(xs[i]-mx)**2;}return sxx?sxy/sxx:0;}
// osy s kulatými hodnotami (0, 250, 500...): dílek 1/2/2,5/5 x 10^k, aby čáry nevypadaly jako konkrétní hodnota
function nice(lo,hi,n){const raw=((hi-lo)||1)/n, p=10**Math.floor(Math.log10(raw)), st=[1,2,2.5,5,10].map(k=>k*p).find(s=>s>=raw-1e-9);
  const a=Math.floor(lo/st+1e-9)*st, b=Math.ceil(hi/st-1e-9)*st, t=[]; for(let v=a;v<=b+st/2;v+=st) t.push(+v.toFixed(6)); return {lo:a,hi:b,t};}
const osy=(L,w,T,h,s,o_)=>{const {right,suf='',col}=o_||{}; let o=''; s.t.forEach(v=>{const y=(T+h-h*(v-s.lo)/(s.hi-s.lo)).toFixed(1);
  if(!right) o+=`<line class="ax" x1="${L}" x2="${L+w}" y1="${y}" y2="${y}"/>`;
  o+=`<text x="${right?L+w+4:L-4}" y="${+y+3}"${right?'':' text-anchor="end"'}${col?` style="fill:var(${col})"`:''}>${fmtN(v)}${suf}</text>`;}); return o;};

// doplněné dny z okolních stanic (13_normaly_pocasi.py): rok se zesvětlí od DOPL_MIN dní, v popisku je vždy
const DOPL_MIN=10, DMK=(cx,y)=>`<circle class="dmk" cx="${(+cx).toFixed(1)}" cy="${(+y).toFixed(1)}" r="1.8"/>`, DOPL=(r,k)=>(R[r]&&R[r].dopl&&R[r].dopl[k])?R[r].dopl[k].dni:0;
const DOPL_T=(r,...ks)=>ks.map(k=>DOPL(r,k)?`; v roce doplněno ${DOPL(r,k)} ${DOPL(r,k)===1?'den':DOPL(r,k)<5?'dny':'dní'} ${k==='P'?'srážek':'teploty'} ze stanice ${R[r].dopl[k].stanice.join(', ')}`:'').join('');
// doplněné dny srážek v konkrétních měsících (pro srovnání ročníků); [[rok, měsíc], ...] -> počet dní
const DOPL_M=list=>list.reduce((a,[r,m])=>a+(((R[r]||{}).dopl||{}).P&&R[r].dopl.P.mesice?(R[r].dopl.P.mesice[m]||0):0),0);
// seznam let jako rozsahy: 1945-1953, 1980, 2010
const roky_=a=>{const o=[];a.forEach(r=>{const l=o[o.length-1]; if(l&&l[1]===r-1) l[1]=r; else o.push([r,r]);}); return o.map(([a,b])=>a===b?a:a+'-'+b).join(', ');};

// ---------- dlouhy pohled 1: rocni srazky 1921-2025 + letosni necely rok
(function(){
  const body=Object.entries(R).filter(([r,z])=>z.P!=null).map(([r,z])=>[+r,z.P]).sort((a,b)=>a[0]-b[0]);
  // letošní neúplný rok: součet denních srážek (zdroj podle zdroj_P) a normál za stejné dny (měsíční normál poměrně)
  let cur=null;
  if(!R[ROK]){ const dd=DNY.filter(d=>d.startsWith(ROK+'-')); let P=0,nP=0,Pn=0; dd.forEach(d=>{const p=W.dny[d][0], m=+d.slice(5,7); Pn+=N.mesic[m].P/dim(ROK,m); if(p!=null){P+=p;nP++;}});
    if(nP>60) cur={r:ROK,P,Pn,do:dd[dd.length-1],n:nP,dni:dd.length}; }
  // osa x po letech: chybějící rok = mezera (ne posun ostatních)
  const R0=body[0][0], n=(cur?cur.r:body[body.length-1][0])-R0+1;
  const norm=N.rok.P, Wd=720,Hd=220,L=40,Rr=6,T=12,B=24,w=Wd-L-Rr,h=Hd-T-B, sc=nice(0,Math.max(...body.map(b=>b[1])),4), vmax=sc.hi, bw=w/n, y=v=>T+h-h*v/vmax, X=r=>L+(r-R0)*bw;
  let o=osy(L,w,T,h,sc)+`<text x="${L}" y="${T-3}">mm za rok</text>`;
  const srt=[...body].sort((a,b)=>a[1]-b[1]), nejsussi=new Set(srt.slice(0,3).map(z=>z[0])), nejmokrejsi=new Set(srt.slice(-3).map(z=>z[0]));
  body.forEach(([r,v])=>{const cls=nejsussi.has(r)?'dry':nejmokrejsi.has(r)?'hi':'', dp=DOPL(r,'P');
    if(dp>=DOPL_MIN) o+=DMK(X(r)+bw/2,T+h+4);
    o+=`<rect class="rY ${cls}" x="${X(r).toFixed(1)}" y="${y(v)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${T+h-y(v)}"><title>${r}: ${fmt(v,0)} mm${DOPL_T(r,'P')}</title></rect>`;
    if(r%10===0&&!(cur&&r>=cur.r-6))o+=`<text x="${X(r)+bw/2}" y="${Hd-8}" text-anchor="middle">${r}</text>`;});
  // klouzavý průměr 10 let jen přes 10 po sobě jdoucích let
  const P_=Object.fromEntries(body); let p='',prev=null;
  body.forEach(([r])=>{const okno=[]; for(let k=r-9;k<=r;k++) if(P_[k]!=null) okno.push(P_[k]); if(okno.length<10){prev=null;return;}
    p+=(prev===r-1?'L':'M')+(X(r)+bw/2).toFixed(1)+' '+y(mean(okno)).toFixed(1)+' '; prev=r;});
  const dt=cur?cur.do.slice(8,10).replace(/^0/,'')+'. '+cur.do.slice(5,7).replace(/^0/,'')+'.':'';
  if(cur){ const xx=X(cur.r);
    o+=`<rect x="${xx.toFixed(1)}" y="${y(cur.P)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${T+h-y(cur.P)}" style="fill:var(--dry);opacity:.45;stroke:var(--dry);stroke-dasharray:2 2"><title>${cur.r} do ${dt}: ${fmt(cur.P,0)} mm (normál za stejné období ${fmt(cur.Pn,0)} mm)</title></rect>`+
      `<line x1="${xx.toFixed(1)}" x2="${(xx+bw).toFixed(1)}" y1="${y(cur.Pn)}" y2="${y(cur.Pn)}" style="stroke:var(--fg);stroke-width:1.5"><title>normál do ${dt}: ${fmt(cur.Pn,0)} mm</title></line>`+
      `<text x="${xx+bw/2}" y="${Hd-8}" text-anchor="end">${cur.r}*</text>`; }
  o+=`<path class="lT" d="${p}"/><line class="nrm" x1="${L}" x2="${L+w}" y1="${y(norm)}" y2="${y(norm)}"/><text x="${L+w}" y="${y(norm)-3}" text-anchor="end">normál ${fmt(norm,0)} mm</text>`;
  $('jb-l1').innerHTML=o;
  const p10=mean(body.filter(b=>b[0]>=ROK-10).map(b=>b[1])), p30=mean(body.filter(b=>b[0]>=1961&&b[0]<=1990).map(b=>b[1]));
  const sucha=body.filter(b=>b[1]<norm*0.75).map(b=>b[0]+(DOPL(b[0],'P')>=DOPL_MIN?' (doplněný)':''));
  const doplR=body.filter(b=>DOPL(b[0],'P')>=DOPL_MIN).map(b=>b[0]), chybi=[]; for(let r=R0;r<=body[body.length-1][0];r++) if(P_[r]==null) chybi.push(r);
  $('jb-l1-n').innerHTML=`${body.length} úplných let, ČHMÚ Koryčany ✅`+(doplR.length?`; roky ${roky_(doplR)} mají chybějící dny doplněné z nejbližší okolní stanice (tečka pod rokem, podrobnosti po najetí na sloupec)`:'')+(chybi.length?`; chybí ${roky_(chybi)}`:'')+`. Průměr ${ROK-10}-${ROK-1}: <b class="num">${fmt(p10,0)} mm</b>, normál 1991-2020 ${fmt(norm,0)} mm, 1961-1990 ${fmt(p30,0)} mm. Roční úhrn se dlouhodobě drží; roky pod 75 % normálu: ${sucha.length?sucha.join(', '):'žádné'}.`+
    (cur?` <b>${cur.r}*</b> = neúplný rok do ${dt} (předběžná data, dny bez stanice Koryčany doplněny z KS Koryčany a Nemochovic): <b class="num">${fmt(cur.P,0)} mm</b>, normál za stejné období ${fmt(cur.Pn,0)} mm (černá čárka u sloupce) = ${fmt(100*cur.P/cur.Pn,0)} %.`:'');
})();

// ---------- dlouhy pohled 2: srazky minus vypar a mozny vypar; 3: horko (tropicke a supertropicke dny, tropicke noci, letni maxima) 2001-2025
(function(){
  const body=Object.entries(R).filter(([r,z])=>z.T!=null&&z.bil!=null).map(([r,z])=>({r:+r,T:z.T,E:z.ET0,b:z.bil,d30:z.d30||0,Tx:z.Tx,d35:z.d35,tn:z.tn,lx:z.lx})).sort((a,b)=>a.r-b.r);
  if(!body.length) return;
  // horko nepotřebuje srážky: rok s úplnou teplotou se kreslí, i když chybí bilance (např. 2020)
  const bodyT=Object.entries(R).filter(([r,z])=>z.T!=null).map(([r,z])=>({r:+r,T:z.T,d30:z.d30||0,Tx:z.Tx,d35:z.d35,tn:z.tn,lx:z.lx})).sort((a,b)=>a.r-b.r);
  const LN=N.leto_normal, maH=bodyT.some(b=>b.d35!=null);   // nová pole z 13_normaly_pocasi.py (22. 10. 2026); dokud neproběhne, kreslí se jen tropické dny
  // letošní neúplný rok z denních dat (1. 1. až poslední den): srážky minus výpar a výpar jako součet do data; horko z denních maxim a minim
  let cur=null;
  if(!R[ROK]){ const dd=DNY.filter(d=>d.startsWith(ROK+'-')); let P=0,E=0,nb=0,d30=0,d35=0,tn=0,tx=null,lx=[]; dd.forEach(d=>{const [p,z,T_,Tn,Tx,e]=W.dny[d]; const m=+d.slice(5,7); if(p!=null&&e!=null){P+=p;E+=e;nb++;} if(Tx!=null){if(Tx>=30)d30++; if(Tx>=35)d35++; if(!tx||Tx>tx[1])tx=[d,Tx]; if(m>=6&&m<=8)lx.push(Tx);} if(Tn!=null&&Tn>=20)tn++;});
    if(nb>60) cur={r:ROK,b:P-E,E,d30,d35,tn,Tx:tx,lx:lx.length>=89?mean(lx):null,do:dd[dd.length-1],n:nb}; }
  const dt=cur?cur.do.slice(8,10).replace(/^0/,'')+'. '+cur.do.slice(5,7).replace(/^0/,'')+'.':'';
  // osa x po letech (chybějící rok = mezera, ne posun); I(b) = pořadí roku od prvního
  const R0=body[0].r, I=b=>b.r-R0, n=(cur?cur.r:body[body.length-1].r)-R0+1, Wd=720, L=40, Rr=40, w=Wd-L-Rr, bw=w/n, x=i=>L+(i+.5)*bw;
  const roky=(Hd)=>body.map(b=>b.r%5===0&&!(cur&&b.r>=cur.r-2)?`<text x="${x(I(b))}" y="${Hd-8}" text-anchor="middle">${b.r}</text>`:'').join('')+(cur?`<text x="${x(I(cur))}" y="${Hd-8}" text-anchor="middle">${cur.r}*</text>`:'');
  const txt=t=>t?`, nejteplejší den ${csd(t[0])} ${fmt(t[1],1)} °C`:'';
  // --- voda: sloupce srážky minus výpar, čára možný výpar
  { const Hd=220,T=12,B=24,h=Hd-T-B;
    const sc=nice(Math.min(0,...body.map(b=>b.b),cur?cur.b:0), Math.max(...body.map(b=>b.E),cur?cur.E:0), 7), y=v=>T+h-h*(v-sc.lo)/(sc.hi-sc.lo);
    let o=osy(L,w,T,h,sc)+`<line class="ax" x1="${L}" x2="${L+w}" y1="${y(0)}" y2="${y(0)}" style="stroke:var(--fg)"/>`;
    body.forEach(b=>{const dp=Math.max(DOPL(b.r,'P'),DOPL(b.r,'T'))>=DOPL_MIN; if(dp) o+=DMK(L+(I(b)+.5)*bw,T+h+4); o+=`<rect x="${(L+I(b)*bw).toFixed(1)}" y="${Math.min(y(0),y(b.b))}" width="${Math.max(1,bw-1).toFixed(1)}" height="${Math.abs(y(0)-y(b.b))}" style="fill:var(${b.b<0?'--dry':'--ok'});opacity:.8"><title>${b.r}: ${b.b<0?'chybělo':'zbylo'} ${fmt(Math.abs(b.b),0)} mm (možný výpar ${fmt(b.E,0)} mm)${DOPL_T(b.r,'P','T')}</title></rect>`;});
    o+=`<path class="lE" d="${body.map((b,i)=>(i&&b.r-body[i-1].r===1?'L':'M')+x(I(b)).toFixed(1)+' '+y(b.E).toFixed(1)).join(' ')}"/>`;
    if(cur){ const i=I(cur);
      o+=`<rect x="${(L+i*bw).toFixed(1)}" y="${Math.min(y(0),y(cur.b))}" width="${Math.max(1,bw-1).toFixed(1)}" height="${Math.abs(y(0)-y(cur.b))}" style="fill:var(--dry);opacity:.45;stroke:var(--dry);stroke-dasharray:2 2"><title>${cur.r} do ${dt}: chybí ${fmt(-cur.b,0)} mm, možný výpar ${fmt(cur.E,0)} mm (neúplný rok)</title></rect>`+
        `<circle cx="${x(i)}" cy="${y(cur.E)}" r="3" style="fill:none;stroke:var(--soil);stroke-width:1.4"><title>možný výpar ${cur.r} do ${dt}: ${fmt(cur.E,0)} mm</title></circle>`; }
    $('jb-l2').innerHTML=o+roky(Hd)+`<text x="${L}" y="${T-3}">mm za rok</text>`;
  }
  // --- horko: počty dní jako body (levá osa), letní maxima jako čára (pravá osa)
  { const Hd=210,T=12,B=24,h=Hd-T-B, body=bodyT;
    const all=body.concat(cur?[cur]:[]), lxs=body.some(b=>b.lx!=null)?all.map(b=>b.lx).filter(v=>v!=null):[];   // čára letních maxim jen s historií
    const sd=nice(0,Math.max(...all.map(b=>b.d30)),4), yd=v=>T+h-h*v/sd.hi;
    const st=lxs.length?nice(Math.min(...lxs)-.5,Math.max(...lxs)+.5,4):null, yt=v=>T+h-h*(v-st.lo)/(st.hi-st.lo);
    let o=osy(L,w,T,h,sd,{col:'--bad'})+(st?osy(L,w,T,h,st,{right:true,col:'--warn',suf:'°'}):'');
    const k=lin(body.map(b=>b.r),body.map(b=>b.d30)), q=mean(body.map(b=>b.d30))-k*mean(body.map(b=>b.r));
    o+=`<line x1="${x(I(body[0]))}" x2="${x(I(body[body.length-1]))}" y1="${yd(q+k*body[0].r)}" y2="${yd(q+k*body[body.length-1].r)}" style="stroke:var(--bad);stroke-width:1.2;stroke-dasharray:5 3;opacity:.5"><title>trend ${k>0?'+':''}${fmt(k*10,1)} tropického dne za 10 let</title></line>`;
    if(st){ let p='',on=null; all.forEach(b=>{ if(b.lx==null){on=null;return;} p+=(on===b.r-1?'L':'M')+x(I(b)).toFixed(1)+' '+yt(b.lx).toFixed(1)+' '; on=b.r;}); o+=`<path class="lT" d="${p}"/>`;
      all.forEach(b=>{ if(b.lx!=null) o+=`<circle cx="${x(I(b))}" cy="${yt(b.lx)}" r="6" style="fill:transparent"><title>${b.r}${b===cur?'*':''}: průměr nejvyšších teplot dne v létě ${fmt(b.lx,1)} °C${LN&&LN.Tmax!=null?' (průměr 2001-2025: '+fmt(LN.Tmax,1)+' °C)':''}</title></circle>`;}); }
    const tip=b=>`${b.r}${b===cur?'* do '+dt:''}: ${b.d30} tropických dní${b.d35!=null?', '+b.d35+' supertropických':''}${b.tn!=null?', '+b.tn+' tropických nocí':''}${txt(b.Tx)}${b===cur?'':DOPL_T(b.r,'T')}`;
    all.forEach(b=>{const op=b===cur?';opacity:.5':'', cx=x(I(b)); if(b!==cur&&DOPL(b.r,'T')>=DOPL_MIN) o+=DMK(cx,T+h+5);
      o+=`<circle cx="${cx}" cy="${yd(b.d30)}" r="3.6" style="fill:var(--bad)${op}"><title>${tip(b)}</title></circle>`;
      if(b.d35!=null){const y=yd(b.d35); o+=`<path d="M${cx} ${y-4}L${cx+4} ${y}L${cx} ${y+4}L${cx-4} ${y}Z" style="fill:var(--hot)${op}"><title>${tip(b)}</title></path>`;}
      if(b.tn!=null) o+=`<circle cx="${cx}" cy="${yd(b.tn)}" r="3" style="fill:none;stroke:var(--accent);stroke-width:1.6${op}"><title>${tip(b)}</title></circle>`;});
    $('jb-l3').innerHTML=o+roky(Hd)+`<text x="${L}" y="${T-3}" style="fill:var(--bad)">počet dní za rok</text>`+(st?`<text x="${L+w}" y="${T-3}" text-anchor="end" style="fill:var(--warn)">°C</text>`:'');
    if(!maH) $('jb-l3-leg').querySelectorAll('span').forEach((s,i)=>{ if(i===1||i===2||s.classList.contains('jb-leto')) s.style.display='none'; });
  }
  const xs=body.map(b=>b.r), tr=k=>lin(xs,body.map(b=>b[k]))*10;
  const prv=body.filter(b=>b.r<=2010), pos=body.filter(b=>b.r>=ROK-10);
  const kar=(cls,n,a,b,j,d)=>`<div class="jb-card ${cls}"><div class="eyebrow">${n}</div><div class="big num">${a}<small style="font-size:.9rem;font-weight:400"> ${j}</small></div><div class="cmp">${b}</div><div class="src">${d}</div></div>`;
  const nejt=bodyT.filter(b=>b.Tx).reduce((a,b)=>b.Tx[1]>a.Tx[1]?b:a);
  const trS=(v,d,j)=>`trend <b>${v>0?'+':''}${fmt(v,d)} ${j} za 10 let</b>`, srv=(k,d,j,dt)=>`2001-2010: ${fmt(mean(prv.map(b=>b[k])),d)} ${j}; ${trS(tr(k),dt,j)}`;
  $('jb-trend-v').innerHTML=
    kar('e','Možný výpar',fmt(mean(pos.map(b=>b.E)),0),srv('E',0,'mm',0),'mm/rok',`průměr ${ROK-10}-${ROK-1}`)+
    kar('b','Srážky minus výpar',fmt(mean(pos.map(b=>b.b)),0),srv('b',0,'mm',0),'mm/rok',`průměr ${ROK-10}-${ROK-1}; záporné = voda chybí`);
  const xsT=bodyT.map(b=>b.r), trT=k=>lin(xsT,bodyT.map(b=>b[k]))*10, prvT=bodyT.filter(b=>b.r<=2010), posT=bodyT.filter(b=>b.r>=ROK-10);
  const srvT=(k,d,j,dt)=>`2001-2010: ${fmt(mean(prvT.map(b=>b[k])),d)} ${j}; ${trS(trT(k),dt,j)}`;
  const posH=posT.filter(b=>b.d35!=null), prvH=prvT.filter(b=>b.d35!=null), bodyH=bodyT.filter(b=>b.d35!=null), trH=k=>lin(bodyH.map(b=>b.r),bodyH.map(b=>b[k]))*10;
  const srvH=(k,d,j)=>`2001-2010: ${fmt(mean(prvH.map(b=>b[k])),d)} ${j}; ${trS(trH(k),d+1,j)}`;
  const posL=posT.filter(b=>b.lx!=null), bodyL=bodyT.filter(b=>b.lx!=null);
  $('jb-trend').innerHTML=
    kar('t','Průměrná teplota',fmt(mean(posT.map(b=>b.T)),1),srvT('T',1,'°C',2),'°C',`průměr dne i noci za celý rok, ${ROK-10}-${ROK-1}`)+
    (posL.length?kar('t','Letní maxima',fmt(mean(posL.map(b=>b.lx)),1),`2001-2010: ${fmt(mean(prvT.filter(b=>b.lx!=null).map(b=>b.lx)),1)} °C; ${trS(lin(bodyL.map(b=>b.r),bodyL.map(b=>b.lx))*10,2,'°C')}`,'°C',`průměr nejvyšších teplot dne VI-VIII, ${ROK-10}-${ROK-1}`+(cur&&cur.lx!=null?`; léto ${ROK} ${fmt(cur.lx,1)} °C`:'')):'')+
    kar('p','Tropické dny',fmt(mean(posT.map(b=>b.d30)),0),srvT('d30',0,'dní',1),'za rok',`nejvíc ${bodyT.reduce((a,b)=>b.d30>a.d30?b:a).r} (${bodyT.reduce((a,b)=>b.d30>a.d30?b:a).d30}); nejteplejší den ${csd(nejt.Tx[0])} ${fmt(nejt.Tx[1],1)} °C`)+
    (posH.length?kar('s','Supertropické dny',fmt(mean(posH.map(b=>b.d35)),1),srvH('d35',1,'dne'),'za rok',`≥ 35 °C; nejvíc ${bodyH.reduce((a,b)=>b.d35>a.d35?b:a).r} (${bodyH.reduce((a,b)=>b.d35>a.d35?b:a).d35})`+(cur?`; ${ROK}: ${cur.d35}`:''))+
      kar('n','Tropické noci',fmt(mean(posH.map(b=>b.tn)),1),srvH('tn',1,'noci'),'za rok',`minimum ≥ 20 °C; nejvíc ${bodyH.reduce((a,b)=>b.tn>a.tn?b:a).r} (${bodyH.reduce((a,b)=>b.tn>a.tn?b:a).tn})`+(cur?`; ${ROK}: ${cur.tn}`:'')):'');
  const w10=body.filter(b=>b.b<0).length;
  const nejh=body.reduce((a,b)=>b.b<a.b?b:a);
  const dV=body.filter(b=>Math.max(DOPL(b.r,'P'),DOPL(b.r,'T'))>=DOPL_MIN).map(b=>b.r), dH=bodyT.filter(b=>DOPL(b.r,'T')>=DOPL_MIN).map(b=>b.r);
  const dTxt=a=>a.length?` Roky ${roky_(a)} mají chybějící dny doplněné z okolní stanice (tečka pod rokem, podrobnosti po najetí).`:'';
  $('jb-l2-n').innerHTML=`Srážky Koryčany minus možný výpar spočítaný z teplot Nemochovic, ${body[0].r}-${body[body.length-1].r} (ČHMÚ ✅, výpočet výparu 📄).`+dTxt(dV)+` Srážky nepokryly výpar ${w10===body.length?'ani v jednom':'ve '+w10} z ${body.length} úplných let; nejvíc chybělo ${nejh.r} (${fmt(-nejh.b,0)} mm).`+
    (cur?` <b>${cur.r}*</b> = neúplný rok do ${dt} (předběžná data): chybí už ${fmt(-cur.b,0)} mm${cur.b<nejh.b?' - víc než za celý rok '+nejh.r:''}, možný výpar ${fmt(cur.E,0)} mm (kroužek).`:'');
  $('jb-l3-n').innerHTML=`ČHMÚ Nemochovice (8 km) ✅, ${bodyT[0].r}-${bodyT[bodyT.length-1].r} (${bodyT.length} úplných let). Tropický den = nejvyšší teplota dne aspoň 30 °C, supertropický aspoň 35 °C, tropická noc = teplota neklesne pod 20 °C (prahy ČHMÚ ✅).${dTxt(dH)} Letní maxima = průměr nejvyšších teplot dne v červnu až srpnu; líp ukazují horko než průměrná teplota, ve které je i noc a zima. Najetím na bod uvidíš podrobnosti a nejteplejší den roku.`+
    (cur?` <b>${cur.r}*</b> = předběžná data do ${dt}: ${cur.d30} tropických, ${cur.d35} supertropických dní, ${cur.tn} tropických nocí${txt(cur.Tx)}${cur.lx!=null?', letní maxima '+fmt(cur.lx,1)+' °C':''}.`+
      (()=>{const rek=[], mx=k=>Math.max(...bodyT.filter(b=>b[k]!=null).map(b=>b[k]));
        if(maH&&cur.d35>mx('d35')) rek.push(`supertropických dní víc než v kterémkoli roce od ${bodyT[0].r} (dosud nejvíc ${mx('d35')})`);
        if(maH&&cur.d30>mx('d30')) rek.push(`tropických dní víc než v kterémkoli roce od ${bodyT[0].r}`);
        if(cur.lx!=null&&bodyT.some(b=>b.lx!=null)&&cur.lx>mx('lx')) rek.push(`nejteplejší léto řady (dosud ${fmt(mx('lx'),1)} °C)`);
        return rek.length?` <b>Rekord: ${rek.join('; ')}.</b>`:'';})():'')+
    (maH?'':' <i>Supertropické dny, tropické noci a letní maxima za minulé roky se právě přepočítávají.</i>');
  $('jb-l-call').innerHTML=`<div class="mot-h">Co z toho plyne pro pozemek</div><p>Déšť přijde v epizodách a mezi nimi je krajina v deficitu - srážky ročně zhruba stejné, výpar roste. Co z deště nezůstane na pozemku, odteče během hodin.</p><p><b>Proto má smysl zadržet vodu tam, kde spadne.</b></p><div class="mot-a"><a href="#" data-go="pozemek">Spočítej to na svém pozemku →</a><a href="#" data-go="katalog">Co se dá udělat (katalog) →</a></div>`;
  $('jb-l-call').querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault(); document.querySelector(`nav.tabs button[data-tab="${a.dataset.go}"]`).click(); window.scrollTo({top:0,behavior:'smooth'});}));
})();

// ---------- detail: obdobi
const sel=$('jb-obd'), inOd=$('jb-od'), inDo=$('jb-do');
const roky=[...new Set(DNY.map(d=>d.slice(0,4)))].sort().reverse();
const mesice=[...new Set(DNY.map(d=>d.slice(0,7)))].sort().reverse();
const SEZ=[['zima','12-01','02-28',-1],['jaro','03-01','05-31',0],['léto','06-01','08-31',0],['podzim','09-01','11-30',0]];
let opts=[['p30',`posledních 30 dní`],['p42',`posledních 6 týdnů`],['p90',`posledních 90 dní`],['ytd',`od začátku roku ${ROK}`]];
roky.forEach(r=>SEZ.forEach(([n,a,b,off])=>{const od=`${+r+off}-${a}`, do_=`${r}-${b}`; if(DNY.some(d=>d>=od&&d<=do_)) opts.push([`r:${od}:${do_}`,`${n} ${r}`]);}));
mesice.forEach(k=>opts.push([`m:${k}`,`${MES[+k.slice(5)-1]} ${k.slice(0,4)}`]));
roky.forEach(r=>opts.push([`y:${r}`,`rok ${r} (zatím)`]));
opts.push(['vl','vlastní od - do']);
sel.innerHTML=opts.map(([v,t])=>`<option value="${v}">${t}</option>`).join(''); sel.value='p90';
inOd.min=inDo.min=DNY[0]; inOd.max=inDo.max=LAST;
function rozsah(){const v=sel.value; if(v==='vl') return [inOd.value||DNY[0],inDo.value||LAST];
  if(v[0]==='p') return [addD(LAST,1-parseInt(v.slice(1))),LAST]; if(v==='ytd') return [ROK+'-01-01',LAST];
  if(v.startsWith('m:')) {const k=v.slice(2); return [k+'-01',k+'-'+dim(+k.slice(0,4),+k.slice(5))];}
  if(v.startsWith('y:')) return [v.slice(2)+'-01-01',v.slice(2)+'-12-31'];
  const [,a,b]=v.split(':'); return [a,b];}
function stat(od,do_){
  const dd=DNY.filter(d=>d>=od&&d<=do_); const r={dd,dni:dd.length,P:0,nP:0,E:0,nE:0,Ts:0,nT:0,tmax:null,tmin:null,pmax:null,d1:0,d30:0,d35:0,tn:0,Txs:0,nTx:0,d0:0,suchoMax:0,zdr:{},nP_:0,nE_:0,nT_:0,posl:null};
  let sucho=0;
  dd.forEach(d=>{const [P,z,T,Tn,Tx,E]=W.dny[d]; const m=+d.slice(5,7), y=+d.slice(0,4), n=N.mesic[m];
    if(P!=null){r.P+=P;r.nP++;r.nP_+=n.P/dim(y,m);r.zdr[z]=(r.zdr[z]||0)+1; if(P>=1){r.d1++;r.posl=d;} if(!r.pmax||P>r.pmax[0])r.pmax=[P,d]; if(P<0.1){sucho++; if(sucho>r.suchoMax)r.suchoMax=sucho;} else sucho=0;}
    if(E!=null){r.E+=E;r.nE++;r.nE_+=n.ET0/dim(y,m);}
    if(T!=null){r.Ts+=T;r.nT++;r.nT_+=n.T;}
    if(Tx!=null){ if(!r.tmax||Tx>r.tmax[0])r.tmax=[Tx,d]; if(Tx>=30)r.d30++; if(Tx>=35)r.d35++; r.Txs+=Tx; r.nTx++; }
    if(Tn!=null){ if(!r.tmin||Tn<r.tmin[0])r.tmin=[Tn,d]; if(Tn<0)r.d0++; if(Tn>=20)r.tn++; }
  });
  r.T=r.nT?r.Ts/r.nT:null; r.Tn=r.nT?r.nT_/r.nT:null; r.bil=r.P-r.E; r.biln=r.nP_-r.nE_;
  return r;
}
function karta(cls,nazev,hod,jedn,cmp,src){return `<div class="jb-card ${cls}"><div class="eyebrow">${nazev}</div><div class="big num">${hod}<small style="font-size:.9rem;font-weight:400"> ${jedn}</small></div><div class="cmp ${cmp.k}">${cmp.t}</div><div class="src">${src}</div></div>`;}
function pct(a,b){return b?Math.round(100*a/b):null;}
function render(){
  const [od,do_]=rozsah(); const s=stat(od,do_); const vl=sel.value==='vl'; inOd.parentElement.style.display=inDo.parentElement.style.display=vl?'':'none';
  if(!vl){inOd.value=od;inDo.value=Math.min(do_,LAST)===do_?do_:LAST;}
  if(!s.dni){$('jb-cards').innerHTML='<p class="note">Pro toto období nejsou denní data.</p>';$('jb-graf').innerHTML='';$('jb-ext').innerHTML='';$('jb-roc').innerHTML='';$('jb-rank').innerHTML='';$('jb-roc-n').textContent='';return;}
  const pP=pct(s.P,s.nP_), pE=pct(s.E,s.nE_);
  const zd=Object.entries(s.zdr).map(([z,n])=>`${ZDR[z]||z} ${n} d`).join(', ');
  const obd=`${csd(s.dd[0])} - ${csd(s.dd[s.dd.length-1])}, ${dni(s.dni)}`;
  $('jb-cards').innerHTML=
    karta('p','Srážky',fmt(s.P,0),'mm',{k:pP>=100?'plus':'minus',t:`<b>${pP}&nbsp;%</b> normálu (${fmt(s.nP_,0)} mm za stejné dny, 1991-2020)`},`${obd}; ${zd}; ${dni(s.d1)} s deštěm ≥ 1 mm${s.posl?', naposledy '+csd(s.posl):''}`)+
    karta('t','Teplota',s.T==null?'-':fmt(s.T,1),'°C',{k:s.T>=s.Tn?'minus':'plus',t:`<b>${s.T>=s.Tn?'+':''}${fmt(s.T-s.Tn,1)}&nbsp;°C</b> proti průměru ${fmt(s.Tn,1)} °C (2001-2025)`},`průměr dne i noci; průměr nejvyšších teplot dne ${s.nTx?fmt(s.Txs/s.nTx,1)+' °C':'-'}, nejvýš ${s.tmax?fmt(s.tmax[0],1)+' °C '+csd(s.tmax[1]):'-'}; ČHMÚ Nemochovice, 8 km`)+
    karta('e','Možný výpar',fmt(s.E,0),'mm',{k:pE<=100?'plus':'minus',t:`<b>${pE}&nbsp;%</b> průměru (${fmt(s.nE_,0)} mm, 2001-2025)`},`z teplot Nemochovice (Hargreaves-Samani 📄)`)+
    karta('b','Srážky minus výpar',(s.bil>0?'+':'')+fmt(s.bil,0),'mm',{k:s.bil>=s.biln?'plus':'minus',t:`průměr ${s.biln>0?'+':''}${fmt(s.biln,0)} mm; ${s.bil<0?'krajině chybí':'voda zbývá'} <b>${fmt(Math.abs(s.bil),0)} mm</b>`},`kolik chybí nebo zbývá; není to odtok`);
  $('jb-ext').innerHTML=[
    ['Nejvíc za den',s.pmax?`<span class="num">${fmt(s.pmax[0],1)} mm</span> ${csd(s.pmax[1])}`:'-'],
    ['Nejdelší období bez deště',`<span class="num">${s.suchoMax}</span> ${s.suchoMax===1?'den':s.suchoMax<5?'dny':'dní'}`],
    ['Nejtepleji',s.tmax?`<span class="num">${fmt(s.tmax[0],1)} °C</span> ${csd(s.tmax[1])}`:'-'],
    ['Nejchladněji',s.tmin?`<span class="num">${fmt(s.tmin[0],1)} °C</span> ${csd(s.tmin[1])}`:'-'],
    ['Tropické dny (≥ 30 °C)',`<span class="num">${s.d30}</span>`],
    ['Supertropické dny (≥ 35 °C)',`<span class="num">${s.d35}</span>`],
    ['Tropické noci (min ≥ 20 °C)',`<span class="num">${s.tn}</span>`],
    ['Mrazové dny (min < 0 °C)',`<span class="num">${s.d0}</span>`],
  ].map(([a,b])=>`<div><span>${a}</span><span>${b}</span></div>`).join('');
  grafDenni(s.dd); rocniky(od,do_,s);
  $('jb-src').innerHTML=`Zdroje: ${W.stanice.chmu_korycany.nazev} (${W.stanice.chmu_korycany.typ}, ${W.stanice.chmu_korycany.km} km) a ${W.stanice.chmu_nemochovice.nazev} (${W.stanice.chmu_nemochovice.typ}, ${W.stanice.chmu_nemochovice.km} km, +22 m): ČHMÚ otevřená data, <a href="https://opendata.chmi.cz/" target="_blank" rel="noopener">opendata.chmi.cz</a> ✅, letošek = předběžná data (po kontrole ČHMÚ se mohou změnit; srážky Koryčany chodí se zpožděním, do té doby KS Koryčany Povodí Moravy nebo Nemochovice - zdroj je u karty). Normály: srážky Koryčany 1991-2020 (${N.rok.P} mm/rok), teplota a ET₀ Nemochovice 2001-2025 (stanice měří od 12/2000, 30letý normál nemá). ET₀ FAO-56 rov. 52 📄. Skripty tools/12_pocasi.py, tools/13_normaly_pocasi.py; trend = lineární regrese přes roky 2001-2025.`;
}
function grafDenni(dd){
  const svg=$('jb-graf'); const Wd=720,Hd=230,L=34,R_=34,T=12,B=26; const w=Wd-L-R_,h=Hd-T-B;
  const sP=nice(0,Math.max(10,...dd.map(d=>W.dny[d][0]||0),...dd.map(d=>W.dny[d][5]||0)),4);
  const Ts=dd.flatMap(d=>[W.dny[d][2],W.dny[d][4]]).filter(x=>x!=null);
  const sT=nice(Math.min(0,...Ts),Math.max(30,...Ts),4);
  const x=i=>L+w*(i+.5)/dd.length, yP=v=>T+h-h*v/sP.hi, yT=v=>T+h-h*(v-sT.lo)/(sT.hi-sT.lo), bw=Math.max(1,w/dd.length-1);
  let o=osy(L,w,T,h,sP)+osy(L,w,T,h,sT,{right:true,suf:'°'});
  // prahy horka (ČHMÚ): čára s popiskem přímo v grafu, aby nesplynula s mřížkou; 35 °C jen když se v období vyskytlo
  const thr=[[30,'','30 °C tropický den']].concat(Math.max(...Ts)>=34?[[35,'s','35 °C supertropický den']]:[]);
  thr.forEach(([t,cls,lab])=>{o+=`<line class="thr ${cls}" x1="${L}" x2="${L+w}" y1="${yT(t)}" y2="${yT(t)}"><title>${lab}</title></line>`;});
  dd.forEach((d,i)=>{const [P,z,Tm,,Tx,E]=W.dny[d]; if(P!=null) o+=`<rect class="${z==='K'?'bP':'bPn'}" x="${x(i)-bw/2}" y="${yP(P)}" width="${bw}" height="${T+h-yP(P)}"><title>${csd(d)}: ${fmt(P,1)} mm (${ZDR[z]||'?'})${Tm!=null?', průměr '+fmt(Tm,1)+' °C':''}${Tx!=null?', nejvýš '+fmt(Tx,1)+' °C':''}${E!=null?', možný výpar '+fmt(E,1)+' mm':''}</title></rect>`;});
  const path=(idx,fy)=>{let p='',on=false;dd.forEach((d,i)=>{const v=W.dny[d][idx]; if(v==null){on=false;return;} p+=(on?'L':'M')+x(i).toFixed(1)+' '+fy(v).toFixed(1)+' '; on=true;}); return p;};
  o+=`<path class="lE" d="${path(5,yP)}"/><path class="lT" d="${path(2,yT)}"/><path class="lX" d="${path(4,yT)}"/>`;
  // dny nad prahem: bod na čáře nejvyšší teploty (tropický kruh, supertropický kosočtverec)
  dd.forEach((d,i)=>{const Tx=W.dny[d][4]; if(Tx==null||Tx<30) return; const cx=x(i), cy=yT(Tx), r=dd.length>120?2.2:3;
    o+= Tx>=35 ? `<path d="M${cx} ${cy-r-1.5}L${cx+r+1.5} ${cy}L${cx} ${cy+r+1.5}L${cx-r-1.5} ${cy}Z" style="fill:var(--hot)"><title>${csd(d)}: ${fmt(Tx,1)} °C, supertropický den</title></path>`
               : `<circle cx="${cx}" cy="${cy}" r="${r}" style="fill:var(--bad)"><title>${csd(d)}: ${fmt(Tx,1)} °C, tropický den</title></circle>`;});
  const krok=dd.length>40?Math.ceil(dd.length/12):dd.length>12?5:1;
  dd.forEach((d,i)=>{if(i%krok===0) o+=`<text x="${x(i)}" y="${Hd-8}" text-anchor="middle">${dd.length>40?(+d.slice(8))+'.'+(+d.slice(5,7))+'.':+d.slice(8)}</text>`;});
  thr.forEach(([t,cls,lab])=>{o+=`<text class="thr-t ${cls}" x="${L+w-4}" y="${yT(t)-3}" text-anchor="end">${lab}</text>`;});   // popisky až nad daty
  o+=`<text x="${L}" y="${T-3}">mm</text><text x="${L+w}" y="${T-3}" text-anchor="end">°C</text>`;
  svg.innerHTML=o;
}
function rocniky(od,do_,s){
  // porovnava se soucet celych kalendarnich mesicu uvnitr obdobi se stejnymi mesici v minulosti (jedine poctive srovnani pri mesicnich historickych datech)
  const mm=[]; for(let d=od.slice(0,7);d<=do_.slice(0,7);){const y=+d.slice(0,4),m=+d.slice(5); const a=d+'-01',b=d+'-'+dim(y,m); if(a>=od&&b<=do_&&DNY.filter(x=>x>=a&&x<=b).length>=dim(y,m)) mm.push([y,m]); d=m===12?`${y+1}-01`:`${y}-${String(m+1).padStart(2,'0')}`;}
  if(!mm.length){ $('jb-roc').innerHTML=''; $('jb-roc-h').textContent='Srovnání ročníků'; $('jb-roc-n').textContent='Období neobsahuje žádný uzavřený celý měsíc, srovnání s minulými roky tu nejde udělat (historická data ČHMÚ jsou po měsících). Pro srovnání vyber delší období, např. posledních 90 dní, od začátku roku nebo celý měsíc.'; $('jb-rank').innerHTML=''; return; }
  const rokRef=mm[mm.length-1][0], ofs=mm.map(([y,m])=>[y-rokRef,m]);
  const body=[]; Object.keys(R).map(Number).forEach(r=>{ if(r===rokRef) return; const vs=ofs.map(([o,m])=>R[r+o]?R[r+o].Pm[m-1]:null); if(vs.every(v=>v!=null)) body.push([r,vs.reduce((a,b)=>a+b,0)]);});
  const letos=mm.map(([y,m])=>stat(`${y}-${String(m).padStart(2,'0')}-01`,`${y}-${String(m).padStart(2,'0')}-${dim(y,m)}`).P).reduce((a,b)=>a+b,0);
  body.push([rokRef,letos]); body.sort((a,b)=>a[0]-b[0]);
  const norm=mm.reduce((a,[y,m])=>a+N.mesic[m].P,0);
  const nazev=mm.length===1?`${MES[mm[0][1]-1]}`:`${MES[mm[0][1]-1]} až ${MES[mm[mm.length-1][1]-1]}`;
  const svg=$('jb-roc'); const Wd=720,Hd=200,L=34,Rr=6,T=12,B=24,w=Wd-L-Rr,h=Hd-T-B; const sc=nice(0,Math.max(norm*1.2,...body.map(b=>b[1])),4), vmax=sc.hi;
  // osa x po letech: chybějící rok = mezera, ostatní se neposouvají
  const R0=body[0][0], bw=w/(rokRef-R0+1), X=r=>L+(r-R0)*bw, y=v=>T+h-h*v/vmax; let o=osy(L,w,T,h,sc)+`<text x="${L}" y="${T-3}">mm</text>`;
  body.forEach(([r,v])=>{const cls=r===rokRef?'now':v<norm*0.6?'lo':v>norm*1.4?'hi':''; const dm=r===rokRef?0:DOPL_M(ofs.map(([q,m])=>[r+q,m])); if(dm>=DOPL_MIN) o+=DMK(X(r)+bw/2,T+h+4); o+=`<rect class="rY ${cls}" x="${X(r).toFixed(1)}" y="${y(v)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${T+h-y(v)}"><title>${r}: ${fmt(v,0)} mm (${fmt(100*v/norm,0)} % normálu)${r===rokRef?', předběžně':dm?`; v těchto měsících doplněno ${dm} ${dm===1?'den':dm<5?'dny':'dní'} z okolní stanice`:''}</title></rect>`; if((r%10===0&&r<rokRef-5)||r===rokRef) o+=`<text x="${X(r)+bw/2}" y="${Hd-8}" text-anchor="middle">${r}</text>`;});
  o+=`<line class="nrm" x1="${L}" x2="${L+w}" y1="${y(norm)}" y2="${y(norm)}"/><text x="${L+w}" y="${y(norm)-3}" text-anchor="end">normál ${fmt(norm,0)} mm</text>`;
  svg.innerHTML=o;
  $('jb-roc-h').textContent=`Srovnání ročníků: srážky ${nazev}`;
  $('jb-roc-n').textContent=`Uzavřené měsíce v období (${nazev} ${rokRef}) proti stejným měsícům v letech ${body[0][0]}-${body[body.length-2][0]}. Měsíční úhrny z denních dat ČHMÚ Koryčany (dny bez měření doplněné z okolních stanic, tečka pod rokem), letošek předběžně (dny bez stanice Koryčany z KS Koryčany a Nemochovic).`;
  const sorted=[...body].sort((a,b)=>a[1]-b[1]); const i=sorted.findIndex(b=>b[0]===rokRef);
  let rank=`<b>${rokRef}: ${fmt(letos,0)} mm</b> je <b>${i+1}. nejsušší</b> z ${sorted.length} let. Nejsušší ${sorted[0][0]} (${fmt(sorted[0][1],0)} mm), nejvlhčí ${sorted[sorted.length-1][0]} (${fmt(sorted[sorted.length-1][1],0)} mm).`;
  if(mm.length===1){const rk=N.rekordy[mm[0][1]]; if(rk) rank+=` Rekordy měsíce: nejvíc za den ${fmt(rk.P_den_max[1],0)} mm (${csd(rk.P_den_max[0])}); teplota max ${fmt(rk.TMA_max[1],1)} °C (${csd(rk.TMA_max[0])}), min ${fmt(rk.TMI_min[1],1)} °C (${csd(rk.TMI_min[0])}) v řadě Nemochovic 2001-2025.`;}
  $('jb-rank').innerHTML=rank;
}
sel.addEventListener('change',render); inOd.addEventListener('change',render); inDo.addEventListener('change',render); render();
})();

// hacek pro automaticke testy (tools: headless kontrola); v aplikaci se nevola
window.TEST_HOOK = async ()=>{ for(let t=0;t<40 && !PARC.feats.length;t++) await new Promise(r=>setTimeout(r,100)); const p=PARC.feats.find(p=>p.f.properties.rd>0 && p.f.properties.plocha_m2>150); if(!p) return {hook:'bez parcel'}; let x=0,y=0; p.ring.forEach(([a,b])=>{x+=a;y+=b}); x/=p.ring.length; y/=p.ring.length; map.setView([y,x],18); map.fire('click',{latlng:L.latLng(y,x)}); await new Promise(r=>setTimeout(r,600)); return {hook:'ok', parc:p.f.properties.cislo}; };
// start
try{const t=localStorage.getItem('kor_tab'); if(t){document.querySelector(`nav.tabs button[data-tab="${t}"]`)?.click();}}catch(e){}
recalc();
pzObnov();
</script>
"""
JADRO_JS = open(os.path.join(ROOT, "web", "jadro.js"), encoding="utf-8").read()
html = (HTML.replace("__LEAFLET_CSS__", LEAFLET_CSS).replace("__LEAFLET_JS__", LEAFLET_JS + "\n" + JADRO_JS).replace("__DATA__", DATA_JS)
        .replace("__RD__", str(data["uzemi"]["rd_pocet"])).replace("__ROOF__", str(round(data["uzemi"]["rd_strechy_m2"] / data["uzemi"]["rd_pocet"]))))
pre = '<!doctype html>\n<html lang="cs">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
i = html.index('<header class="top">')
html = pre + html[:i] + '</head>\n<body>\n' + html[i:] + '\n</body>\n</html>\n'
for out in (os.path.join(ROOT, "prototyp", "index.html"), os.path.join(ROOT, "index.html")):
    open(out, "w", encoding="utf-8").write(html)
print("ok", len(html)//1024, "KB ->", "prototyp/index.html, index.html")
