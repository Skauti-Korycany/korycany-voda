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
    "opatreni": [{k: o[k] for k in ("id","nazev","popis","misto","rozhoduje","pracnost","ucinky","meritko","kontext","kvantifikace","vhodnost","vazby","povoleni","povoleni_pozn","ceny","financovani","standardy","nedohledano","pozn_poctivost")} for o in OP["opatreni"]],
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
                                "d30": z.get("T", {}).get("dni_nad_30"), "d0": z.get("T", {}).get("dni_pod_0")} for r, z in NRM["rocniky"].items()}},
}
DATA_JS = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<title>Voda v Koryčanech</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: mapa nahoře (nebo vlevo na širokém), pracovní panel pod ní; čísla v mono, nadpisy serif s charakterem. */
:root{
  --bg:#f6f3ee; --panel:#ffffff; --fg:#1f2a2e; --muted:#5c6b70; --line:#d8d2c7;
  --accent:#1f6f8b; --accent-ink:#ffffff; --soil:#7a5a3a; --water:#2d7fb8; --ok:#3b7a57; --warn:#b5651d; --bad:#a23b3b; --dry:#b8923a;
  --chip:#e9e4da; --mark:#eef4f7;
  --f-display:"Fraunces", Georgia, "Times New Roman", serif;
  --f-body:"IBM Plex Sans", "Segoe UI", Arial, sans-serif;
  --f-mono:"IBM Plex Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#171c1f; --panel:#1f2629; --fg:#e8e4dc; --muted:#a3adb1; --line:#36414a;
  --accent:#5aa9c9; --accent-ink:#0f1a1f; --soil:#c49a6c; --water:#6fb3e0; --ok:#7fc39a; --warn:#e0a060; --bad:#e08080; --dry:#d4b26a;
  --chip:#2b353a; --mark:#1b2a31; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#171c1f; --panel:#1f2629; --fg:#e8e4dc; --muted:#a3adb1; --line:#36414a;
  --accent:#5aa9c9; --accent-ink:#0f1a1f; --soil:#c49a6c; --water:#6fb3e0; --ok:#7fc39a; --warn:#e0a060; --bad:#e08080; --dry:#d4b26a;
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
.mark{font-size:.75rem;vertical-align:1px}
.note{font-size:.85rem;color:var(--muted)}
.callout{border-left:3px solid var(--warn);padding:.5rem .8rem;background:var(--mark);border-radius:0 6px 6px 0;font-size:.92rem;margin-top:.8rem}
.callout.ok{border-left-color:var(--ok)}
.unfit{margin-top:.8rem;font-size:.88rem}
.unfit li{margin:.15rem 0}
.big{font-family:var(--f-display);font-size:2rem;font-weight:700;line-height:1.1}
.sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem;margin-top:.6rem}
.sum .box{border-top:2px solid var(--water);padding-top:.4rem}
.sum .box small{display:block;color:var(--muted);font-size:.78rem}
input[type=range]{width:100%}
.filters{display:flex;flex-wrap:wrap;gap:.4rem;margin:.6rem 0}
.filters button{font:inherit;font-size:.82rem;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:999px;padding:.2rem .6rem;cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.src{font-size:.8rem;color:var(--muted)} .src a{color:var(--accent)}
.hidden-tab{display:none}
/* Jak bylo */
.jb-head{display:flex;flex-wrap:wrap;gap:.6rem 1rem;align-items:end}
.jb-head label.f{min-width:160px}
.jb-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.8rem;margin-top:.8rem}
.jb-card{border:1px solid var(--line);border-radius:6px;padding:.7rem .8rem;background:var(--panel);border-top:3px solid var(--water)}
.jb-card.t{border-top-color:var(--warn)} .jb-card.e{border-top-color:var(--soil)} .jb-card.b{border-top-color:var(--ok)}
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
.jb-chart .rY{fill:var(--chip)} .jb-chart .rY.now{fill:var(--accent)} .jb-chart .rY.hi{fill:var(--water)} .jb-chart .rY.lo{fill:var(--bad)} .jb-chart .rY.dry{fill:var(--dry)}
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
</style>
<style>__LEAFLET_CSS__</style>

<header class="top">
  <div><h1>Voda v Koryčanech</h1><div class="tag">náhled v0.2 - skutečný terén, půda, budovy a srážky; katalog v0.4</div></div>
  <nav class="tabs" role="tablist">
    <button role="tab" aria-selected="true" data-tab="jakbylo">Jak bylo</button>
    <button role="tab" aria-selected="false" data-tab="pozemek">Můj pozemek</button>
    <button role="tab" aria-selected="false" data-tab="uzemi">Celé území</button>
    <button role="tab" aria-selected="false" data-tab="katalog">Katalog</button>
    <button role="tab" aria-selected="false" data-tab="model">O modelu</button>
  </nav>
</header>
<div class="banner">Zjednodušený model pro osvětu, ne projekt. Nevalidováno. Po kliku do mapy se sklon a půda berou z dat (DMR 5G ČÚZK, BPEJ SPÚ); střechy a výměry z katastru (ČÚZK) po kliknutí na parcely, zpevněné plochy zadáváš sám. Katalog, vzorce, ceny a zdroje: opatreni.json v0.4 (20. 10. 2026). Značky: ✅ ověřený zdroj, ✅⏳ starší než rok, 📄 citace, 🤔 odhad.</div>

<main>
<!-- ======================= JAK BYLO ======================= -->
<section id="tab-jakbylo">
  <div class="panel">
    <h2>Jak bylo v Koryčanech</h2>
    <p class="note" style="margin:.2rem 0 0">Co se tu děje s vodou: kolik naprší, kolik se vypaří a co zbyde. Nejdřív dlouhé řady, protože jeden měsíc trend neukáže.</p>
    <p class="note" style="margin:.2rem 0 0">Data se stahují automaticky každý den; poslední aktualizace <span class="num" id="jb-upd"></span>.</p>
    <h3 style="margin-top:1rem">Dlouhý pohled: srážky Koryčany 1921-2025</h3>
    <p class="note" id="jb-l1-n"></p>
    <svg class="jb-chart" id="jb-l1" viewBox="0 0 720 220" role="img" aria-label="Roční srážky 1921-2025"></svg>
    <div class="legend"><span><b style="background:var(--chip)"></b>roční úhrn</span><span><b style="background:var(--dry)"></b>3 nejsušší roky</span><span><b style="background:var(--water)"></b>nad 140 % normálu</span><span><b style="background:var(--warn)"></b>klouzavý průměr 10 let</span><span><b style="background:var(--fg)"></b>normál 1991-2020</span></div>
    <h3 style="margin-top:1rem">Dlouhý pohled: teplota, výpar a bilance 2001-2025</h3>
    <p class="note" id="jb-l2-n"></p>
    <svg class="jb-chart" id="jb-l2" viewBox="0 0 720 220" role="img" aria-label="Bilance, výpar a teplota 2001-2025"></svg>
    <div class="legend"><span><b style="background:var(--ok)"></b>bilance P - ET₀ přebytek</span><span><b style="background:var(--dry)"></b>bilance P - ET₀ deficit (mm/rok)</span><span><b style="background:var(--soil)"></b>ET₀ mm/rok</span><span><b style="background:var(--warn)"></b>průměrná teplota °C</span><span><b style="background:var(--bad)"></b>tropické dny</span></div>
    <div class="jb-cards" id="jb-trend"></div>
    <div class="callout" id="jb-l-call" style="margin-top:.8rem"></div>

    <div class="jb-head" style="margin-top:1.4rem">
      <div><h3>Detail: vybrané období</h3><p class="note" style="margin:.2rem 0 0">Denní data jsou od 1. 1. 2026 (ČHMÚ je zveřejňuje jen pro běžící rok); starší roky jsou v řadách nahoře.</p></div>
      <label class="f" style="margin-left:auto">Období<select id="jb-obd"></select></label>
      <label class="f">od<input type="date" id="jb-od"></label>
      <label class="f">do<input type="date" id="jb-do"></label>
    </div>
    <div class="jb-cards" id="jb-cards"></div>
    <svg class="jb-chart" id="jb-graf" viewBox="0 0 720 230" role="img" aria-label="Denní průběh srážek, teploty a výparu"></svg>
    <div class="legend" id="jb-leg"><span><b style="background:var(--water)"></b>srážky mm/den (světlejší = náhradní stanice)</span><span><b style="background:var(--warn)"></b>průměrná teplota °C</span><span><b style="background:var(--soil)"></b>výpar ET₀ mm/den</span></div>
    <h3 style="margin-top:1rem">Extrémy období</h3>
    <div class="jb-ext" id="jb-ext"></div>
    <h3 style="margin-top:1rem" id="jb-roc-h">Srovnání ročníků</h3>
    <p class="note" id="jb-roc-n"></p>
    <svg class="jb-chart" id="jb-roc" viewBox="0 0 720 200" role="img" aria-label="Srovnání ročníků"></svg>
    <div class="jb-rank" id="jb-rank"></div>
    <div class="callout" style="margin-top:1rem"><b>Jak to číst.</b> ET₀ je referenční výpar (kolik by se vypařilo z dobře zavlažené trávy, Hargreaves-Samani podle FAO-56 📄). Skutečný výpar z krajiny je v suchém létě menší, protože není z čeho. Rozdíl srážky - ET₀ je proto <b>klimatický deficit</b>: kolik vody krajině chybí a dobírá si ji ze zásoby v půdě a pod zemí. Vítr a vlhkost vzduchu metoda nezná; při větru je skutečná ztráta větší.</div>
    <p class="src" id="jb-src"></p>
  </div>
</section>

<!-- ======================= MŮJ POZEMEK ======================= -->
<section id="tab-pozemek" class="grid two hidden-tab">
  <div>
    <div id="map" aria-label="Mapa Koryčan"></div>
    <p class="note" style="margin:.4rem 0 0">Podklad ČÚZK ZTM (WMTS) a ortofoto (WMS), živě ze serverů ČÚZK. Klikni do mapy = vyber místo. Klik vybere parcelu z katastru (ČÚZK, CC BY 4.0) - klikni postupně na dům, zahradu a dvůr, výměry a půdorysy budov se sečtou a předvyplní. Sklon a půda se odvodí z mřížky 5 m (DMR 5G, BPEJ). Zpevněné plochy v datech nejsou, ty zadej sám. Nic se neukládá, vlastníci se nenačítají.</p>
    <div class="panel" style="margin-top:.8rem">
      <div class="eyebrow">Krok 1 - kde</div>
      <dl class="kv" id="where">
        <dt>Parcely</dt><dd id="w-parc">klikni do mapy na dům, pak na zahradu a dvůr - každá parcela zvlášť, sčítá se <span class="note">(katastr má dům a zahradu jako dvě parcely)</span></dd>
        <dt>Místo</dt><dd id="w-pos">-</dd>
        <dt>Sklon</dt><dd><span class="num" id="w-slope">-</span> % <span class="note" id="w-slope-n">(po kliku z DMR 5G, průměr v okruhu 15 m)</span></dd>
        <dt>Půda</dt><dd id="w-soil">- <span class="note">(po kliku z BPEJ; v lese a zástavbě odhad - ověř zkouškou vsaku)</span></dd>
        <dt>Okolí 30 m</dt><dd id="w-okoli">-</dd>
        <dt>Podzemní voda</dt><dd>hlouběji než 1 m <span class="note">(zástupně)</span></dd>
        <dt>Intravilán</dt><dd>ano <span class="note">(zástupně)</span></dd>
      </dl>
    </div>
  </div>
  <div>
    <div class="panel">
      <div class="eyebrow">Krok 2 - co tu je (uprav podle sebe)</div>
      <div class="inputs" style="margin-top:.5rem">
        <label class="f">Střecha (m²)<input type="number" id="in-roof" value="120" min="0" step="10"></label>
        <label class="f">Zpevněné plochy (m²)<input type="number" id="in-paved" value="40" min="0" step="5"></label>
        <label class="f">Typ zpevnění<select id="in-pavedtype">
          <option value="asfalt_beton_zalita_dlazba">asfalt / beton / zalitá dlažba</option>
          <option value="dlazba_piskove_spary" selected>dlažba s pískovými spárami</option>
          <option value="sterk_upraveny">štěrk</option>
          <option value="zatravnovaci_tvarnice">zatravňovací tvárnice</option></select></label>
        <label class="f">Zelené plochy (m²)<input type="number" id="in-green" value="300" min="0" step="10"></label>
        <label class="f">Co na nich je<select id="in-greentype"><option value="zahrada, trávník > 75 %" selected>hlavně trávník (přes 3/4)</option><option value="zahrada, trávník 50-75 % (záhony, cesty)">trávník s záhony a cestami (1/2 až 3/4)</option></select></label>
        <label class="f">Svody ze střechy<select id="in-drain">
          <option value="kanal" selected>do kanalizace</option><option value="pozemek">na pozemek</option><option value="nevim">nevím</option></select></label>
        <label class="f">Sklon pozemku (%)<input type="number" id="in-slope" value="4" min="0" max="40" step="1"></label>
        <label class="f">Půda (zkouška vsaku, 30 min)<select id="in-soil">
          <option value="A">kleslo přes 8 cm - A, velmi propustná</option>
          <option value="B" selected>kleslo 4-8 cm - B, propustná</option>
          <option value="C">kleslo 2-4 cm - C, málo propustná</option>
          <option value="D">kleslo pod 2 cm - D, jíl, nepropustná</option></select></label>
        <label class="f">Déšť k výpočtu<select id="in-rain">
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm, 1x za 2 roky</option>
            <option value="53.2" data-n="N10" selected>vzácný - 53 mm, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="20">20 mm - běžný letní liják</option>
            <option value="26.2">26 mm - 60 min, 1x za 5 let (ČSN 75 9010, Brno)</option>
            <option value="93.5">94 mm - den 12. 6. 2012, 2. největší za 105 let (ČHMÚ Koryčany)</option></optgroup></select></label>
      </div>
      <p class="note" style="margin:.5rem 0 0">Zkouška vsaku: vykopej jámu 30 cm, nalij vodu, po 30 minutách změř pokles. Převod podle brožury Praha 2009 ✅⏳. Nahrazuje mapu půd, dokud nejsou data VÚMOP; i potom je přesnější než mapa.</p>
    </div>

    <div class="panel step">
      <div class="eyebrow">Krok 3 - co se u tebe děje při dešti</div>
      <table class="flow" id="flow"></table>
      <div class="bars" id="bars"></div>
      <div class="legend"><span><b style="background:var(--bad)"></b>odteče pryč</span><span><b style="background:var(--water)"></b>zůstane u tebe (zasákne nebo zadrženo)</span></div>
      <p class="note" id="year"></p>
    </div>

    <div class="panel step">
      <div class="eyebrow">Krok 4 - co můžeš udělat (zaškrtni, přepočítá se)</div>
      <p class="note">Seřazeno: nejvíc vody za nejmíň práce. Čísla u opatření platí pro tvoje plochy a zvolený déšť.</p>
      <div class="cards" id="cards"></div>
      <div class="unfit" id="unfit"></div>
    </div>

    <div class="panel step">
      <div class="eyebrow">Krok 5 - shrnutí</div>
      <div class="sum" id="summary"></div>
      <div class="callout" id="scale"></div>
    </div>
  </div>
</section>

<!-- ======================= CELÉ ÚZEMÍ ======================= -->
<section id="tab-uzemi" class="hidden-tab">
  <div class="panel">
    <h2>Co to udělá, když se zapojí víc lidí</h2>
    <p class="note" id="u-zdroj"></p>
    <div class="inputs" style="margin-top:.6rem">
      <label class="f">Rodinných domů v území<input type="number" id="u-n" value="__RD__" min="0" step="10"></label>
      <label class="f">Průměrný půdorys domu (m²)<input type="number" id="u-roof" value="__ROOF__" min="0" step="10"></label>
      <label class="f">Průměrně zpevněno (m², odhad 🤔)<input type="number" id="u-paved" value="35" min="0" step="5"></label>
      <label class="f">Déšť k výpočtu<select id="u-rain">
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm, 1x za 2 roky</option>
            <option value="53.2" data-n="N10">vzácný - 53 mm, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="20" selected>20 mm - běžný letní liják</option>
            <option value="26.2">26 mm - 60 min, 1x za 5 let (ČSN 75 9010, Brno)</option>
            <option value="93.5">94 mm - den 12. 6. 2012, 2. největší za 105 let (ČHMÚ Koryčany)</option></optgroup></select></label>
    </div>
    <label class="f" style="margin-top:.8rem">Kolik domácností se zapojí: <span class="num" id="u-pct-val">20</span> %
      <input type="range" id="u-pct" min="0" max="100" value="20"></label>
    <div class="filters" id="u-pack">
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
          <optgroup label="Návrhový déšť Koryčany, 6 hodin (ČVUT/ČHMÚ 2023 ✅)">
            <option value="32.2" data-n="N2">častý - 32 mm za 6 h, 1x za 2 roky</option>
            <option value="53.2" data-n="N10">vzácný - 53 mm za 6 h, 1x za 10 let</option>
            <option value="87" data-n="N100">extrémní - 87 mm za 6 h, 1x za 100 let</option></optgroup>
          <optgroup label="Další">
            <option value="20" selected>20 mm - běžný letní liják</option>
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
    <p class="note"><span class="num" id="k-count"></span> položek z opatreni.json. Filtry se sčítají. Každé číslo má zdroj a značku.</p>
    <div class="filters" id="k-misto"></div>
    <div class="filters" id="k-rozhoduje"></div>
    <div class="filters" id="k-ucinek"></div>
    <div class="filters" id="k-fin"><button aria-pressed="false" data-f="otevreno">jen s otevřenou dotací (k 18. 10. 2026)</button><button aria-pressed="false" data-f="svepomoc">jen svépomoc (pracnost 1, povolení 0)</button></div>
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
const map = L.map('map',{zoomControl:true}).setView([49.106,17.165],15);
const ztm = L.tileLayer('https://ags.cuzk.gov.cz/arcgis1/rest/services/ZTM_WM/MapServer/WMTS/tile/1.0.0/ZTM_WM/default/GoogleMapsCompatible/{z}/{y}/{x}',{maxZoom:19,attribution:'ČÚZK - on-line (ZTM)'}).addTo(map);
const orto = L.tileLayer.wms('https://ags.cuzk.gov.cz/arcgis1/services/ORTOFOTO/MapServer/WMSServer',{layers:'0',format:'image/jpeg',maxZoom:19,attribution:'ČÚZK - on-line (Ortofoto)'});
L.control.layers({'ZTM (ČÚZK)':ztm,'Ortofoto (ČÚZK)':orto},null,{collapsed:true}).addTo(map);
let tilesOk=false; ztm.on('load',()=>{tilesOk=true});
setTimeout(()=>{ if(!tilesOk){ const d=document.createElement('div'); d.className='note'; d.style.cssText='position:absolute;inset:auto 8px 8px 8px;background:var(--panel);padding:.4rem .6rem;border-radius:4px;z-index:800'; d.textContent='Podklad ČÚZK se nenačetl (prohlížeč bez sítě, nebo náhled v omezeném prostředí). Mapa je jen kulisa, výpočty fungují.'; document.getElementById('map').appendChild(d);} },6000);
let marker=null;
map.on('click',e=>{
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
  PARC.zvyr = L.layerGroup().addTo(map);
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
  if(!PARC.vybrane.size){ $('w-parc').innerHTML='klikni do mapy na dům, pak na zahradu a dvůr - každá parcela zvlášť, sčítá se'; return; }
  const paved = +$('in-paved').value||0;
  $('in-roof').value = Math.round(roof);
  $('in-green').value = Math.max(0, Math.round(A - roof - paved));
  $('w-parc').innerHTML = `${popis.join('; ')} <b>= ${fmt0(A)} m², střechy ${fmt0(roof)} m²</b> <span class="note">(ČÚZK katastr + budovy, CC BY 4.0; plocha půdorysů, ne šikmých střech; zpevněné plochy v datech nejsou - zadej sám, zeleň = zbytek)</span> <button type="button" id="w-parc-x" style="font:inherit;font-size:.8rem">zrušit výběr</button>`;
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
  $('k-limit').innerHTML = `<b>Co to znamená:</b> scénář ${dQ>=0?'sníží':'zvýší'} povrchový odtok z krajiny při dešti ${fmt0(P)} mm o <b>${fmt0(Math.abs(dQ))} m³</b> (${fmt(100*Math.abs(dQ)/Math.max(1,Q0),1)} % z ${fmt0(Q0)} m³). Pro srovnání: déšť ${fmt0(P)} mm na území spadne ${fmt0(H*1e4*P/1000)} m³ - většina se vsákne nebo zůstane na povrchu i teď. ${NKEY?`Jak moc je půda před deštěm nasycená, nevíme - proto se počítá vážený průměr: běžně vlhká půda (CN2) by dala ${fmt0(Q0s)} m³, nasycená (CN3) ${fmt0(Q0n)} m³; váha nasyceného stavu ${fmt(100*W3,0)} % vychází z toho, jaké průběhy deště (tvary A-F) jsou v Koryčanech u deště ${NKEY.replace('N','1x za ')} let typické a jak často jim předchází mokré dny (Kavka a kol. 2023 ✅, tab. 6; data/navrhove_srazky.json). `:`U tohoto deště se počítá jen s běžně vlhkou půdou (CN2); rozpětí vlhká-nasycená ukážou návrhové deště častý / vzácný / extrémní. `}Čísla jsou změna CN podle tabulky Janeček a kol. 2012 (tab. 2.3) ✅⏳ a USDA TR-55, metoda SCS-CN, buňky 5 m; stav pozemků "teď" je výchozí předpoklad tabulky (orná = obilniny, špatný stav; les střední), ne terénní průzkum. Zatravnění údolnic bere buňky orné půdy, kam stéká aspoň 1 ha (akumulace z DMR 5G). ${E0?`<br><b>Eroze orné půdy (USLE, orientačně):</b> teď ${fmt0(E0)} t/rok z ${fmt0(HO)} ha = ${fmt(E0/Math.max(1,HO),1)} t/ha/rok při obilninách (C 0,2), scénář ${fmt0(E1)} t/rok (${fmt(E1/Math.max(1,HO),1)} t/ha). Přípustná ztráta od 1. 7. 2026 je ${K.usle.Gp_t_ha_rok['od_2026-07-01'].ostatni} t/ha/rok ✅ (mělké půdy ${K.usle.Gp_t_ha_rok['od_2026-07-01'].melke}). R faktor ${fmt0(RU)} (VÚMOP/ČHMÚ 2022 ✅), K podle HPJ a LS z DMR (Janeček 2012 ✅⏳), půdoochranné technologie C 0,1, vrstevnice P 0,65 / 0,9 (do / nad 7°), zatravnění C 0,01; délka svahu z terénu nezná meze a cesty, na dlouhých svazích nadsazuje. Závazný výpočet dělá kalkulačka VÚMOP.`:''} Zpomalení vlny a výpar se tu nepočítají.`;
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
  Z06(i,r){ return {dV:0,dYear:0,fit:true,text:`Voda: nic měřitelného. Horko: stín snižuje teplotu stěny o 11-25 °C ✅⏳ EPA 2008; vzduch ve skupině stromů až o 5 °C. Strom 1 775-6 100 Kč ✅ ÚÚR 2025. Pozor na sítě a odstup od plotu.`}; },
  Z05(i,r){ return {dV:0,dYear:0,fit:true,text:`Výpar z půdy nižší o cca třetinu (17-79 % podle plodiny a materiálu ✅ Irrigation Science 2024). Do součtu vody za obec se nepočítá, na záhonech to poznáš.`}; },
  Z07(i,r){ return {dV:0,dYear:0,fit:true,text:`Vítr za plotem nižší o ~70 % do vzdálenosti 5 výšek, o 50 % do 10 výšek ✅⏳ UNL. Živý plot 2 m chrání pás 20-40 m. Výpar v mm nedohledán - ukazujeme plochu, ne litry.`}; },
  Z08(i,r){ return {dV:0,dYear:0,fit:true,text:`Vlhkost půdy nekvantifikována 🤔. Druhová pestrost: fázovaná seč ponechá 10-20 % neposečeno (SPPK D02 004 📄); nepravidelně kosené plochy o 20 % chudší ✅ Chytrá 2024. 0 Kč.`}; },
  Z09(i,r){ return {dV:0,dYear:0,fit:true,text:`Stín na fasádě: povrch až o 11-25 °C chladnější ✅⏳ (hodnota pro stín stromů). Pro fasády samostatný zdroj nedohledán.`}; },
  Z11(i,r){ return {dV:0,dYear:0,fit:true,needs:['S01'],text:`Šetří pitnou vodu; úspora nekvantifikována 🤔.`}; },
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
function finText(o){ return o.financovani.map(f=>{const p=D.programy[f]; return p? (p.stav==='otevreno'&&f!=='vlastni'?'● ':'')+p.nazev.split(' - ')[0].split(' (')[0] : f}).join('; '); }
function povText(o){ return (CZ.povoleni[String(o.povoleni)]||'?')+(o.povoleni_pozn?' ('+o.povoleni_pozn+')':''); }
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
  const ev = evalMeasures(i,r);
  let kept=0, keptYear=0, hasS02 = chosen.has('S02') || i.drain==='pozemek';
  ev.fit.forEach(x=>{ if(chosen.has(x.o.id)){ const needsOK = !(x.needs||[]).length || (x.needs||[]).every(n=>chosen.has(n) || (n==='S02'&&i.drain==='pozemek')); if(needsOK){ kept+=x.dV; keptYear+= (x.dYear||0);} } });
  kept=Math.min(kept,r.out); const yearOut=r.yearRoof+r.yearPaved+(r.yearGreen||0); keptYear=Math.min(keptYear,yearOut);
  const pct=(x)=> r.out>0? 100*x/r.out:0;
  $('bars').innerHTML = `<div class="bar"><span>teď</span><div class="track"><i class="away" style="width:100%"></i></div><span class="num">${fmt(r.out)} m³</span></div>
    <div class="bar"><span>s opatřeními</span><div class="track"><i class="kept" style="width:${pct(kept)}%"></i><i class="away" style="width:${100-pct(kept)}%"></i></div><span class="num">${fmt(r.out-kept)} m³</span></div>`;
  $('year').textContent = `Za rok (${fmt0(K.srazky_rocni_mm.hodnota)} mm, stanice ČHMÚ Koryčany 1991-2020 ✅) odteče ze střechy a zpevněných ploch zhruba ${fmt0(r.yearRoof+r.yearPaved)} m³ (po odečtení 1 mm z každého deště: ${fmt0(RAIN_Y_NEPR*1000)} mm z ${fmt0(K.srazky_rocni_mm.hodnota)})${r.yearGreen!=null?`, ze zelených ploch ${fmt0(r.yearGreen)} m³ (SCS-CN po dnech z řady denních úhrnů ČHMÚ)`:'; ze zelených ploch zatím nepočítáno (čeká na rozdělení denních úhrnů ze stanice ČHMÚ - vyrob_srazky.bat)'}. Se zvolenými opatřeními zůstane u tebe až ${fmt0(keptYear)} m³.`;
  // karty
  $('cards').innerHTML = ev.fit.map(x=>{const o=x.o; const on=chosen.has(o.id); const needs=(x.needs||[]).filter(n=>!(chosen.has(n)||(n==='S02'&&i.drain==='pozemek')));
    return `<div class="card ${on?'on':''}"><header><input type="checkbox" id="c-${o.id}" data-id="${o.id}" ${on?'checked':''}><div class="t"><b>${o.nazev}</b>
      <div class="meta"><span class="chip id">${o.id}</span><span class="chip">${CZ.pracnost[String(o.pracnost)]}</span><span class="chip">${cenaText(o)}</span><span class="chip">povolení: ${CZ.povoleni[String(o.povoleni)]}</span>${x.enabler?'<span class="chip">předpoklad pro další</span>':(x.dV>0?`<span class="chip num">+${fmt(x.dV)} m³ teď</span>`:'')}</div></div></header>
      <div class="eff">${x.text}</div>
      ${needs.length?`<div class="note">Doporučujeme nejdřív: ${needs.join(', ')}</div>`:''}
      <details><summary>zdroje, financování, co chybí</summary><ul>
        <li>Financování: ${finText(o)}</li>
        <li>Povolení: ${povText(o)}</li>
        ${o.kvantifikace.map(k=>`<li>${CZ.ucinek[k.ucinek]||k.ucinek}: ${k.popis} ${ZN[k.znacka]||''}${(k.zdroj||[]).map(z=>D.zdroje[z]?` <a class="src" href="${D.zdroje[z].url||'#'}" target="_blank" rel="noopener">${D.zdroje[z].nazev.split(':')[0].slice(0,60)}</a>`:'').join(';')}</li>`).join('')}
        ${o.nedohledano&&o.nedohledano.length?`<li>Nedohledáno: ${o.nedohledano.join('; ')}</li>`:''}
        ${o.pozn_poctivost?`<li>${o.pozn_poctivost}</li>`:''}
      </ul></details></div>`;}).join('');
  $('cards').querySelectorAll('input[type=checkbox]').forEach(cb=>cb.addEventListener('change',()=>{ if(cb.checked) chosen.add(cb.dataset.id); else chosen.delete(cb.dataset.id); recalc(); }));
  $('unfit').innerHTML = ev.unfit.length? `<b>Nehodí se sem:</b><ul>${ev.unfit.map(x=>`<li>${x.o.nazev} (${x.o.id}) - ${x.fit}</li>`).join('')}</ul>` : '';
  // krok 5
  const n=200;
  $('summary').innerHTML = `<div class="box"><div class="big num">${fmt(kept)} m³</div><small>zůstane u tebe z deště ${rainmm} mm (z ${fmt(r.out)} m³)</small></div>
    <div class="box"><div class="big num">${fmt0(keptYear)} m³</div><small>za rok místo kanalizace a potoka</small></div>
    <div class="box"><div class="big num">${fmt0(kept*n)} m³</div><small>kdyby to samé udělalo ${n} domácností, na jeden déšť</small></div>`;
  $('scale').innerHTML = `<b>Na co to nestačí:</b> ${fmt0(kept*n)} m³ od ${n} domácností je při dešti ${rainmm} mm zhruba ${fmt(100*kept*n/(D.uzemi.plocha_ha*1e4*i.rain),2)} % objemu, který spadne na území modelu ${fmt0(D.uzemi.plocha_ha)} ha (${fmt0(D.uzemi.plocha_ha*1e4*i.rain)} m³; plocha z rozvodnice DMR 5G ✅). Na povodeň na Kyjovce drobná opatření nestačí a aplikace to neřekne. Je to ale ${fmt0(kept*n)} m³ vody v půdě a zahradách místo v kanálu, při každém lijáku, zdarma. To je rozdíl mezi "proteklo" a "zůstalo".`;
  renderUzemi();
}
['in-roof','in-paved','in-pavedtype','in-green','in-greentype','in-drain','in-slope','in-soil','in-rain'].forEach(id=>$(id).addEventListener('input',recalc));

// ---------- území
function renderUzemi(){
  const n=+$('u-n').value||0, roof=+$('u-roof').value||0, paved=+$('u-paved').value||0, rain=+$('u-rain').value/1000, pct=+$('u-pct').value/100;
  $('u-pct-val').textContent=Math.round(pct*100);
  const pack=[...document.querySelectorAll('#u-pack button[aria-pressed="true"]')].map(b=>b.dataset.m);
  const i={roof,paved,pavedType:'dlazba_piskove_spary',green:250,drain:'kanal',slope:3,soil:'B',rain};
  const r=runoff(i); let per=0, perY=0;
  if(pack.includes('S02')){ if(pack.includes('Z01')){const e=EFF.Z01(i,r); per+=e.dV; perY+=e.dYear;} if(pack.includes('S01')){const e=EFF.S01(i,r); per+=e.dV; perY+=e.dYear;} }
  if(pack.includes('Z04')){const e=EFF.Z04(i,r); per+=e.dV; perY+=e.dYear;}
  per=Math.min(per,r.roofOut+r.pavedOut); perY=Math.min(perY,r.yearRoof+r.yearPaved);
  const hh=Math.round(n*pct), tot=per*hh, totY=perY*hh;
  const allOut=(r.roofOut+r.pavedOut)*n;
  $('u-sum').innerHTML=`<div class="box"><div class="big num">${hh}</div><small>domácností se zapojí</small></div>
    <div class="box"><div class="big num">${fmt0(tot)} m³</div><small>zůstane v území na jeden déšť ${Math.round(rain*1000)} mm (ze ${fmt0(allOut)} m³ ze střech a dvorů všech domácností)</small></div>
    <div class="box"><div class="big num">${fmt0(totY)} m³</div><small>za rok</small></div>`;
  // podíly podle počtu budov v dílčích povodích (ČÚZK INSPIRE BU)
  const U=D.uzemi; const celk=Object.values(U.podle_povodi).reduce((t,x)=>t+x.pocet,0);
  const sidla=Object.entries(U.podle_povodi).map(([k,x])=>[k.replace('Koryčany (','').replace(')',''), x.pocet/celk]);
  $('u-table').innerHTML=`<tr><th>dílčí povodí (podíl podle počtu budov)</th><th class="num">domácností</th><th class="num">zapojí se</th><th class="num">m³ na déšť</th><th class="num">m³/rok</th></tr>`+
    sidla.map(([s,p])=>`<tr><td>${s}</td><td class="num">${fmt0(n*p)}</td><td class="num">${fmt0(n*p*pct)}</td><td class="num">${fmt0(tot*p)}</td><td class="num">${fmt0(totY*p)}</td></tr>`).join('')+
    `<tr class="total"><td>profil na Kyjovce pod Koryčany</td><td class="num">${n}</td><td class="num">${hh}</td><td class="num">${fmt0(tot)}</td><td class="num">${fmt0(totY)}</td></tr>`;
  if(!pack.includes('S02') && (pack.includes('Z01')||pack.includes('S01'))) $('u-limit').innerHTML='<b>Pozor:</b> dešťová zahrada a nádrž bez odpojení svodů (S02) nic nezadrží - voda se k nim nedostane. Balíček to respektuje.';
  else { const key='P'+Math.round(rain*1000)+'mm', od=U.odtok[key]; const spadne=U.plocha_ha*1e4*rain;
    $('u-limit').innerHTML=`<b>Na co to nestačí:</b> ${fmt0(tot)} m³ je ${fmt(100*tot/spadne,2)} % deště, který při ${Math.round(rain*1000)} mm spadne na území modelu (${fmt0(U.plocha_ha)} ha = ${fmt0(spadne)} m³)${od?`, a ${fmt(100*tot/od.objem_m3,1)} % povrchového odtoku z celého území (${fmt0(od.objem_m3)} m³ podle SCS-CN, CN ${U.cn_vazene}, IPS II)`:''}. Povodňovou vlnu na Kyjovce to nezmění. Součet platí pro vodu ze střech a dvorů; pole, louky a les jsou samostatná kapitola (USLE, pásy, průlehy) a v tomto náhledu se nepočítají.`; }
  $('u-plus').innerHTML=`<b>Co to ale je:</b> ${fmt0(totY)} m³ vody za rok v půdě a zahradách místo v kanálu. Pro srovnání: nákladní cisterna má 🤔 10 m³, tohle je ${fmt0(totY/10)} cisteren ročně, bez jediné stavby. A na každý liják o ${fmt0(tot)} m³ pomalejší odtok z intravilánu do potoka.`;
  // kontext
  $('u-context').innerHTML = D.opatreni.filter(o=>o.kontext).map(o=>`<div class="card"><header><div class="t"><b>${o.nazev}</b><div class="meta"><span class="chip id">${o.id}</span><span class="chip">rozhoduje: ${o.rozhoduje.map(r=>CZ.rozhoduje[r].split(' ')[0]).join(', ')}</span><span class="chip">${cenaText(o)}</span><span class="chip">povolení: ${CZ.povoleni[String(o.povoleni)]}</span></div></div></header>
    <div class="eff">${o.kvantifikace.map(k=>k.popis+' '+(ZN[k.znacka]||'')).join(' ')}</div>${o.pozn_poctivost?`<div class="note">${o.pozn_poctivost}</div>`:''}<div class="note">Financování: ${finText(o)}</div></div>`).join('');
}
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
    n.varovani.map(v=>`<p class="note" style="color:var(--warn)">! ${v}</p>`).join('');
}
$('h-vyska').addEventListener('input',hrazSpocti); $('h-rain').addEventListener('input',hrazSpocti);

$('u-zdroj').innerHTML=`V území modelu (${fmt0(D.uzemi.plocha_ha)} ha, povodí Kyjovky k jezu před Mouchnicemi bez povodí nad přehradou) je ${fmt0(D.uzemi.budov)} budov s půdorysem ${fmt0(D.uzemi.strechy_m2/1e4*10)/10} ha, z toho ${fmt0(D.uzemi.rd_pocet)} rodinných domů (${fmt0(D.uzemi.rd_strechy_m2/1e4*10)/10} ha) ✅ ČÚZK INSPIRE BU, 19. 10. 2026. Zpevněné plochy u domů nejsou v datech - odhad. Počítá se jen voda ze střech a dvorů rodinných domů; průmysl, bytové domy a veřejné budovy zatím ne.`;
['u-n','u-roof','u-paved','u-rain','u-pct'].forEach(id=>$(id).addEventListener('input',renderUzemi));
document.querySelectorAll('#u-pack button').forEach(b=>b.addEventListener('click',()=>{b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')!=='true');renderUzemi();}));

// ---------- katalog
const KF={misto:new Set(),rozhoduje:new Set(),ucinek:new Set(),fin:new Set()};
function chips(id,obj,key){ $(id).innerHTML=Object.entries(obj).map(([k,v])=>`<button aria-pressed="false" data-k="${k}">${k} ${v.split(' (')[0]}</button>`).join('');
  $(id).querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?KF[key].add(b.dataset.k):KF[key].delete(b.dataset.k); renderKatalog();})); }
chips('k-misto',CZ.misto,'misto'); chips('k-rozhoduje',Object.fromEntries(Object.entries(CZ.rozhoduje).filter(([k])=>k!=='zemedelec')),'rozhoduje'); chips('k-ucinek',CZ.ucinek,'ucinek');
$('k-fin').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{const on=b.getAttribute('aria-pressed')!=='true'; b.setAttribute('aria-pressed',on); on?KF.fin.add(b.dataset.f):KF.fin.delete(b.dataset.f); renderKatalog();}));
function renderKatalog(){
  const list=D.opatreni.filter(o=> (!KF.misto.size||o.misto.some(m=>KF.misto.has(m))) && (!KF.rozhoduje.size||o.rozhoduje.some(m=>KF.rozhoduje.has(m)))
    && (!KF.ucinek.size||[...o.ucinky.primarni,...o.ucinky.vedlejsi].some(u=>KF.ucinek.has(u)))
    && (!KF.fin.has('otevreno')||o.financovani.some(f=>D.programy[f]&&D.programy[f].stav==='otevreno'&&f!=='vlastni'))
    && (!KF.fin.has('svepomoc')||(o.pracnost===1&&o.povoleni===0)));
  $('k-count').textContent=list.length+' / '+D.opatreni.length;
  $('k-cards').innerHTML=list.map(o=>`<div class="card"><header><div class="t"><b>${o.nazev}</b>
    <div class="meta"><span class="chip id">${o.id}</span><span class="chip">${o.misto.map(m=>CZ.misto[m]).join(', ')}</span><span class="chip">rozhoduje: ${o.rozhoduje.join(', ')}</span><span class="chip">${CZ.pracnost[String(o.pracnost)]}</span><span class="chip">${cenaText(o)}</span><span class="chip">povolení ${o.povoleni??'?'}</span>${o.kontext?'<span class="chip">kontext - obec/správce</span>':''}</div>
    <div class="meta">účinky: ${o.ucinky.primarni.map(u=>'<b>'+CZ.ucinek[u]+'</b>').join(', ')}${o.ucinky.vedlejsi.length?'; vedlejší: '+o.ucinky.vedlejsi.map(u=>CZ.ucinek[u]).join(', '):''}</div></div></header>
    ${o.popis?`<div class="eff">${o.popis}</div>`:''}
    <details><summary>účinek, zdroje, ceny, financování</summary><ul>
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
const osy=(L,w,T,h,vmin,vmax,jedn,right)=>{let o='';[0,.5,1].forEach(f=>{const y=T+h-h*f;o+=`<line class="ax" x1="${L}" x2="${L+w}" y1="${y}" y2="${y}"/>`+(right?`<text x="${L+w+4}" y="${y+3}">${Math.round(vmin+(vmax-vmin)*f)}${jedn}</text>`:`<text x="${L-4}" y="${y+3}" text-anchor="end">${Math.round(vmin+(vmax-vmin)*f)}${jedn}</text>`);});return o;};

// ---------- dlouhy pohled 1: rocni srazky 1921-2025
(function(){
  const body=Object.entries(R).filter(([r,z])=>z.P!=null).map(([r,z])=>[+r,z.P]).sort((a,b)=>a[0]-b[0]);
  const norm=N.rok.P, Wd=720,Hd=220,L=36,Rr=6,T=10,B=24,w=Wd-L-Rr,h=Hd-T-B, vmax=Math.max(...body.map(b=>b[1]))*1.05, bw=w/body.length, y=v=>T+h-h*v/vmax;
  let o=osy(L,w,T,h,0,vmax,'');
  const nejsussi=new Set([...body].sort((a,b)=>a[1]-b[1]).slice(0,3).map(z=>z[0]));
  body.forEach(([r,v],i)=>{const cls=nejsussi.has(r)?'dry':v>norm*1.4?'hi':'';o+=`<rect class="rY ${cls}" x="${(L+i*bw).toFixed(1)}" y="${y(v)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${T+h-y(v)}"><title>${r}: ${fmt(v,0)} mm</title></rect>`;if(r%10===0)o+=`<text x="${L+(i+.5)*bw}" y="${Hd-8}" text-anchor="middle">${r}</text>`;});
  let p='';body.forEach(([r,v],i)=>{if(i<9)return;const k=mean(body.slice(i-9,i+1).map(b=>b[1]));p+=(p?'L':'M')+(L+(i+.5)*bw).toFixed(1)+' '+y(k).toFixed(1)+' ';});
  o+=`<path class="lT" d="${p}"/><line class="nrm" x1="${L}" x2="${L+w}" y1="${y(norm)}" y2="${y(norm)}"/><text x="${L+w}" y="${y(norm)-3}" text-anchor="end">normál ${fmt(norm,0)} mm</text>`;
  $('jb-l1').innerHTML=o;
  const p10=mean(body.filter(b=>b[0]>=ROK-10).map(b=>b[1])), p30=mean(body.filter(b=>b[0]>=1961&&b[0]<=1990).map(b=>b[1]));
  const sucha=body.filter(b=>b[1]<norm*0.75).map(b=>b[0]);
  $('jb-l1-n').innerHTML=`${body.length} úplných let, ČHMÚ Koryčany ✅. Průměr ${ROK-10}-${ROK-1}: <b class="num">${fmt(p10,0)} mm</b>, normál 1991-2020 ${fmt(norm,0)} mm, 1961-1990 ${fmt(p30,0)} mm. Roční úhrn se dlouhodobě drží; roky pod 75 % normálu: ${sucha.join(', ')}.`;
})();

// ---------- dlouhy pohled 2: T, ET0, bilance, tropicke dny 2001-2025
(function(){
  const body=Object.entries(R).filter(([r,z])=>z.T!=null&&z.bil!=null).map(([r,z])=>({r:+r,T:z.T,E:z.ET0,b:z.bil,d30:z.d30||0})).sort((a,b)=>a.r-b.r);
  if(!body.length) return;
  const Wd=720,Hd=220,L=40,Rr=40,T=10,B=24,w=Wd-L-Rr,h=Hd-T-B;
  const bmin=Math.min(0,...body.map(b=>b.b))*1.1, bmax=Math.max(...body.map(b=>b.E))*1.05;
  const yL=v=>T+h-h*(v-bmin)/(bmax-bmin), tmin=Math.min(0,...body.map(b=>b.T))-1, tmax=Math.max(...body.map(b=>b.T),...body.map(b=>b.d30))+2, yR=v=>T+h-h*(v-tmin)/(tmax-tmin);
  const bw=w/body.length, x=i=>L+(i+.5)*bw;
  let o=osy(L,w,T,h,bmin,bmax,'')+osy(L,w,T,h,tmin,tmax,'',true);
  o+=`<line class="ax" x1="${L}" x2="${L+w}" y1="${yL(0)}" y2="${yL(0)}" style="stroke:var(--fg)"/>`;
  body.forEach((b,i)=>{o+=`<rect x="${(L+i*bw).toFixed(1)}" y="${Math.min(yL(0),yL(b.b))}" width="${Math.max(1,bw-1).toFixed(1)}" height="${Math.abs(yL(0)-yL(b.b))}" style="fill:var(${b.b<0?'--dry':'--ok'});opacity:.8"><title>${b.r}: bilance ${fmt(b.b,0)} mm, ET₀ ${fmt(b.E,0)} mm, ${fmt(b.T,1)} °C, ${b.d30} tropických dní</title></rect>`;if(b.r%5===0)o+=`<text x="${x(i)}" y="${Hd-8}" text-anchor="middle">${b.r}</text>`;});
  const path=(f,fy,cls)=>`<path class="${cls}" d="${body.map((b,i)=>(i?'L':'M')+x(i).toFixed(1)+' '+fy(f(b)).toFixed(1)).join(' ')}"/>`;
  o+=path(b=>b.E,yL,'lE')+path(b=>b.T,yR,'lT')+`<path d="${body.map((b,i)=>(i?'L':'M')+x(i).toFixed(1)+' '+yR(b.d30).toFixed(1)).join(' ')}" style="fill:none;stroke:var(--bad);stroke-width:1.2"/>`;
  o+=`<text x="${L}" y="${T-2}">mm</text><text x="${L+w}" y="${T-2}" text-anchor="end">°C / dny</text>`;
  $('jb-l2').innerHTML=o;
  const xs=body.map(b=>b.r), tr=k=>lin(xs,body.map(b=>b[k]))*10;
  const prv=body.filter(b=>b.r<=2010), pos=body.filter(b=>b.r>=ROK-10);
  const kar=(cls,n,a,b,j,d)=>`<div class="jb-card ${cls}"><div class="eyebrow">${n}</div><div class="big num">${a}<small style="font-size:.9rem;font-weight:400"> ${j}</small></div><div class="cmp">${b}</div><div class="src">${d}</div></div>`;
  $('jb-trend').innerHTML=
    kar('t','Teplota',fmt(mean(pos.map(b=>b.T)),1),`2001-2010: ${fmt(mean(prv.map(b=>b.T)),1)} °C; trend <b>${tr('T')>0?'+':''}${fmt(tr('T'),2)} °C za 10 let</b>`,'°C',`průměr ${ROK-10}-${ROK-1}`)+
    kar('e','Výpar ET₀',fmt(mean(pos.map(b=>b.E)),0),`2001-2010: ${fmt(mean(prv.map(b=>b.E)),0)} mm; trend <b>${tr('E')>0?'+':''}${fmt(tr('E'),0)} mm za 10 let</b>`,'mm/rok',`průměr ${ROK-10}-${ROK-1}`)+
    kar('b','Bilance P - ET₀',fmt(mean(pos.map(b=>b.b)),0),`2001-2010: ${fmt(mean(prv.map(b=>b.b)),0)} mm; trend <b>${tr('b')>0?'+':''}${fmt(tr('b'),0)} mm za 10 let</b>`,'mm/rok',`průměr ${ROK-10}-${ROK-1}`)+
    kar('p','Tropické dny',fmt(mean(pos.map(b=>b.d30)),0),`2001-2010: ${fmt(mean(prv.map(b=>b.d30)),0)} za rok; trend <b>${tr('d30')>0?'+':''}${fmt(tr('d30'),1)} dní za 10 let</b>`,'za rok',`max ${body.reduce((a,b)=>b.d30>a.d30?b:a).r} (${body.reduce((a,b)=>b.d30>a.d30?b:a).d30})`);
  const w10=body.filter(b=>b.b<0).length;
  $('jb-l2-n').innerHTML=`Nemochovice 2001-2025 (25 let, ČHMÚ ✅), ET₀ Hargreaves-Samani 📄. Bilance byla záporná ve všech ${w10} úplných letech; nejhůř ${body.reduce((a,b)=>b.b<a.b?b:a).r} (${fmt(body.reduce((a,b)=>b.b<a.b?b:a).b,0)} mm).`;
  $('jb-l-call').innerHTML=`<b>Co z toho plyne pro pozemek.</b> Déšť přijde v epizodách a mezi nimi je krajina v deficitu - srážky ročně zhruba stejné, výpar roste. Co z deště nezůstane na pozemku, odteče během hodin. Proto má smysl zadržet vodu tam, kde spadne: viz Můj pozemek a Katalog.`;
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
sel.innerHTML=opts.map(([v,t])=>`<option value="${v}">${t}</option>`).join(''); sel.value='p42';
inOd.min=inDo.min=DNY[0]; inOd.max=inDo.max=LAST;
function rozsah(){const v=sel.value; if(v==='vl') return [inOd.value||DNY[0],inDo.value||LAST];
  if(v[0]==='p') return [addD(LAST,1-parseInt(v.slice(1))),LAST]; if(v==='ytd') return [ROK+'-01-01',LAST];
  if(v.startsWith('m:')) {const k=v.slice(2); return [k+'-01',k+'-'+dim(+k.slice(0,4),+k.slice(5))];}
  if(v.startsWith('y:')) return [v.slice(2)+'-01-01',v.slice(2)+'-12-31'];
  const [,a,b]=v.split(':'); return [a,b];}
function stat(od,do_){
  const dd=DNY.filter(d=>d>=od&&d<=do_); const r={dd,dni:dd.length,P:0,nP:0,E:0,nE:0,Ts:0,nT:0,tmax:null,tmin:null,pmax:null,d1:0,d30:0,d0:0,suchoMax:0,zdr:{},nP_:0,nE_:0,nT_:0,posl:null};
  let sucho=0;
  dd.forEach(d=>{const [P,z,T,Tn,Tx,E]=W.dny[d]; const m=+d.slice(5,7), y=+d.slice(0,4), n=N.mesic[m];
    if(P!=null){r.P+=P;r.nP++;r.nP_+=n.P/dim(y,m);r.zdr[z]=(r.zdr[z]||0)+1; if(P>=1){r.d1++;r.posl=d;} if(!r.pmax||P>r.pmax[0])r.pmax=[P,d]; if(P<0.1){sucho++; if(sucho>r.suchoMax)r.suchoMax=sucho;} else sucho=0;}
    if(E!=null){r.E+=E;r.nE++;r.nE_+=n.ET0/dim(y,m);}
    if(T!=null){r.Ts+=T;r.nT++;r.nT_+=n.T;}
    if(Tx!=null){ if(!r.tmax||Tx>r.tmax[0])r.tmax=[Tx,d]; if(Tx>=30)r.d30++; }
    if(Tn!=null){ if(!r.tmin||Tn<r.tmin[0])r.tmin=[Tn,d]; if(Tn<0)r.d0++; }
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
    karta('t','Teplota',s.T==null?'-':fmt(s.T,1),'°C',{k:s.T>=s.Tn?'minus':'plus',t:`<b>${s.T>=s.Tn?'+':''}${fmt(s.T-s.Tn,1)}&nbsp;°C</b> proti průměru ${fmt(s.Tn,1)} °C (2001-2025)`},`ČHMÚ Nemochovice, 8 km; max ${s.tmax?fmt(s.tmax[0],1)+' °C '+csd(s.tmax[1]):'-'}`)+
    karta('e','Výpar ET₀',fmt(s.E,0),'mm',{k:pE<=100?'plus':'minus',t:`<b>${pE}&nbsp;%</b> průměru (${fmt(s.nE_,0)} mm, 2001-2025)`},`Hargreaves-Samani z teplot Nemochovice 📄`)+
    karta('b','Bilance P - ET₀',(s.bil>0?'+':'')+fmt(s.bil,0),'mm',{k:s.bil>=s.biln?'plus':'minus',t:`průměr ${s.biln>0?'+':''}${fmt(s.biln,0)} mm; ${s.bil<0?'krajině chybí':'přebytek'} <b>${fmt(Math.abs(s.bil),0)} mm</b>`},`klimatický deficit, ne odtok`);
  $('jb-ext').innerHTML=[
    ['Nejvíc za den',s.pmax?`<span class="num">${fmt(s.pmax[0],1)} mm</span> ${csd(s.pmax[1])}`:'-'],
    ['Nejdelší období bez deště',`<span class="num">${s.suchoMax}</span> ${s.suchoMax===1?'den':s.suchoMax<5?'dny':'dní'}`],
    ['Nejtepleji',s.tmax?`<span class="num">${fmt(s.tmax[0],1)} °C</span> ${csd(s.tmax[1])}`:'-'],
    ['Nejchladněji',s.tmin?`<span class="num">${fmt(s.tmin[0],1)} °C</span> ${csd(s.tmin[1])}`:'-'],
    ['Tropické dny (≥ 30 °C)',`<span class="num">${s.d30}</span>`],
    ['Mrazové dny (min < 0 °C)',`<span class="num">${s.d0}</span>`],
  ].map(([a,b])=>`<div><span>${a}</span><span>${b}</span></div>`).join('');
  grafDenni(s.dd); rocniky(od,do_,s);
  $('jb-src').innerHTML=`Zdroje: ${W.stanice.chmu_korycany.nazev} (${W.stanice.chmu_korycany.typ}, ${W.stanice.chmu_korycany.km} km) a ${W.stanice.chmu_nemochovice.nazev} (${W.stanice.chmu_nemochovice.typ}, ${W.stanice.chmu_nemochovice.km} km, +22 m): ČHMÚ otevřená data, <a href="https://opendata.chmi.cz/" target="_blank" rel="noopener">opendata.chmi.cz</a> ✅, letošek = předběžná data (po kontrole ČHMÚ se mohou změnit; srážky Koryčany chodí se zpožděním, do té doby KS Koryčany Povodí Moravy nebo Nemochovice - zdroj je u karty). Normály: srážky Koryčany 1991-2020 (${N.rok.P} mm/rok), teplota a ET₀ Nemochovice 2001-2025 (stanice měří od 12/2000, 30letý normál nemá). ET₀ FAO-56 rov. 52 📄. Skripty tools/12_pocasi.py, tools/13_normaly_pocasi.py; trend = lineární regrese přes roky 2001-2025.`;
}
function grafDenni(dd){
  const svg=$('jb-graf'); const Wd=720,Hd=230,L=34,R_=34,T=12,B=26; const w=Wd-L-R_,h=Hd-T-B;
  const Pmax=Math.max(10,...dd.map(d=>W.dny[d][0]||0),...dd.map(d=>W.dny[d][5]||0)); const Ts=dd.map(d=>W.dny[d][2]).filter(x=>x!=null);
  const Tlo=Math.min(-5,...Ts), Thi=Math.max(25,...Ts);
  const x=i=>L+w*(i+.5)/dd.length, yP=v=>T+h-h*v/Pmax, yT=v=>T+h-h*(v-Tlo)/(Thi-Tlo), bw=Math.max(1,w/dd.length-1);
  let o='';
  [0,.5,1].forEach(f=>{o+=`<line class="ax" x1="${L}" x2="${L+w}" y1="${T+h-h*f}" y2="${T+h-h*f}"/><text x="${L-4}" y="${T+h-h*f+3}" text-anchor="end">${Math.round(Pmax*f)}</text><text x="${L+w+4}" y="${T+h-h*f+3}">${Math.round(Tlo+(Thi-Tlo)*f)}°</text>`;});
  dd.forEach((d,i)=>{const [P,z,Tm,,,E]=W.dny[d]; if(P!=null) o+=`<rect class="${z==='K'?'bP':'bPn'}" x="${x(i)-bw/2}" y="${yP(P)}" width="${bw}" height="${T+h-yP(P)}"><title>${csd(d)}: ${fmt(P,1)} mm (${ZDR[z]||'?'})${Tm!=null?', '+fmt(Tm,1)+' °C':''}${E!=null?', ET₀ '+fmt(E,1)+' mm':''}</title></rect>`;});
  const path=(idx,fy)=>{let p='',on=false;dd.forEach((d,i)=>{const v=W.dny[d][idx]; if(v==null){on=false;return;} p+=(on?'L':'M')+x(i).toFixed(1)+' '+fy(v).toFixed(1)+' '; on=true;}); return p;};
  o+=`<path class="lE" d="${path(5,yP)}"/><path class="lT" d="${path(2,yT)}"/>`;
  const krok=dd.length>40?Math.ceil(dd.length/12):dd.length>12?5:1;
  dd.forEach((d,i)=>{if(i%krok===0) o+=`<text x="${x(i)}" y="${Hd-8}" text-anchor="middle">${dd.length>40?(+d.slice(8))+'.'+(+d.slice(5,7))+'.':+d.slice(8)}</text>`;});
  o+=`<text x="${L}" y="${T-3}">mm</text><text x="${L+w}" y="${T-3}" text-anchor="end">°C</text>`;
  svg.innerHTML=o;
}
function rocniky(od,do_,s){
  // porovnava se soucet celych kalendarnich mesicu uvnitr obdobi se stejnymi mesici v minulosti (jedine poctive srovnani pri mesicnich historickych datech)
  const mm=[]; for(let d=od.slice(0,7);d<=do_.slice(0,7);){const y=+d.slice(0,4),m=+d.slice(5); const a=d+'-01',b=d+'-'+dim(y,m); if(a>=od&&b<=do_&&DNY.filter(x=>x>=a&&x<=b).length>=dim(y,m)) mm.push([y,m]); d=m===12?`${y+1}-01`:`${y}-${String(m+1).padStart(2,'0')}`;}
  if(!mm.length){ $('jb-roc').innerHTML=''; $('jb-roc-h').textContent='Srovnání ročníků'; $('jb-roc-n').textContent='Období neobsahuje žádný uzavřený celý měsíc, srovnání s minulými roky tu nejde udělat (historická data ČHMÚ jsou po měsících).'; $('jb-rank').innerHTML=''; return; }
  const rokRef=mm[mm.length-1][0], ofs=mm.map(([y,m])=>[y-rokRef,m]);
  const body=[]; Object.keys(R).map(Number).forEach(r=>{ if(r===rokRef) return; const vs=ofs.map(([o,m])=>R[r+o]?R[r+o].Pm[m-1]:null); if(vs.every(v=>v!=null)) body.push([r,vs.reduce((a,b)=>a+b,0)]);});
  const letos=mm.map(([y,m])=>stat(`${y}-${String(m).padStart(2,'0')}-01`,`${y}-${String(m).padStart(2,'0')}-${dim(y,m)}`).P).reduce((a,b)=>a+b,0);
  body.push([rokRef,letos]); body.sort((a,b)=>a[0]-b[0]);
  const norm=mm.reduce((a,[y,m])=>a+N.mesic[m].P,0);
  const nazev=mm.length===1?`${MES[mm[0][1]-1]}`:`${MES[mm[0][1]-1]} až ${MES[mm[mm.length-1][1]-1]}`;
  const svg=$('jb-roc'); const Wd=720,Hd=200,L=34,Rr=6,T=10,B=24,w=Wd-L-Rr,h=Hd-T-B; const vmax=Math.max(norm*1.2,...body.map(b=>b[1]));
  const bw=w/body.length, y=v=>T+h-h*v/vmax; let o=osy(L,w,T,h,0,vmax,'');
  body.forEach(([r,v],i)=>{const cls=r===rokRef?'now':v<norm*0.6?'lo':v>norm*1.4?'hi':''; o+=`<rect class="rY ${cls}" x="${(L+i*bw).toFixed(1)}" y="${y(v)}" width="${Math.max(1,bw-1).toFixed(1)}" height="${T+h-y(v)}"><title>${r}: ${fmt(v,0)} mm</title></rect>`; if(r%10===0||r===rokRef) o+=`<text x="${L+(i+.5)*bw}" y="${Hd-8}" text-anchor="middle">${r}</text>`;});
  o+=`<line class="nrm" x1="${L}" x2="${L+w}" y1="${y(norm)}" y2="${y(norm)}"/><text x="${L+w}" y="${y(norm)-3}" text-anchor="end">normál ${fmt(norm,0)} mm</text>`;
  svg.innerHTML=o;
  $('jb-roc-h').textContent=`Srovnání ročníků: srážky ${nazev}`;
  $('jb-roc-n').textContent=`Uzavřené měsíce v období (${nazev} ${rokRef}) proti stejným měsícům v letech ${body[0][0]}-${body[body.length-2][0]}; ČHMÚ Koryčany, letošek předběžně.`;
  const sorted=[...body].sort((a,b)=>a[1]-b[1]); const i=sorted.findIndex(b=>b[0]===rokRef);
  let rank=`<b>${rokRef}: ${fmt(letos,0)} mm</b> je <b>${i+1}. nejsušší</b> z ${sorted.length} let. Nejsušší ${sorted[0][0]} (${fmt(sorted[0][1],0)} mm), nejvlhčí ${sorted[sorted.length-1][0]} (${fmt(sorted[sorted.length-1][1],0)} mm).`;
  if(mm.length===1){const rk=N.rekordy[mm[0][1]]; if(rk) rank+=` Rekordy měsíce: nejvíc za den ${fmt(rk.P_den_max[1],0)} mm (${csd(rk.P_den_max[0])}); teplota max ${fmt(rk.TMA_max[1],1)} °C (${csd(rk.TMA_max[0])}), min ${fmt(rk.TMI_min[1],1)} °C (${csd(rk.TMI_min[0])}) v řadě Nemochovic 2001-2025.`;}
  $('jb-rank').innerHTML=rank;
}
sel.addEventListener('change',render); inOd.addEventListener('change',render); inDo.addEventListener('change',render); render();
})();

// start
try{const t=localStorage.getItem('kor_tab'); if(t){document.querySelector(`nav.tabs button[data-tab="${t}"]`)?.click();}}catch(e){}
recalc();
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
