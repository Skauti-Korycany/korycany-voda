# -*- coding: utf-8 -*-
"""
Blok D: reakce Stříbrníku u Kachníku na déšť, léto 2026.
Vstupy:
  data/kachnik_2026_rle.txt  - hladina čidla "Čid5 Koryčany ul. U Rybníka, stavidlo" (VOX, hlásný profil C),
                               krok 20 min, místní čas, zapsány jen změny hodnoty a výpadky (GAP); staženo 21. 10. 2026
                               z http://hladiny-vox.pwsplus.eu/Senzors/Details/5157 (export CSV bez přihlášení)
  data/chmi/recent/1h-*.json - hodinové úhrny SRA1H Nemochovice (0-203-0-41503035001) a Staré Hutě (0-203-0-41701068003),
                               UTC (skript přepočítá na místní čas CEST = UTC+2); stahuje 08_srazky_recent.py
  data/chmi/recent/dly-0-203-0-41701068002-*.json - denní úhrny Koryčany (klimatologický den od 06 UTC)
Výstup: data/kachnik_2026.json, docs/img/kachnik_nahled.png
Spuštění: python tools/build_kachnik.py [cesta k data/chmi/recent]
"""
import json, re, os, sys, csv, datetime as dt, statistics

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
RECENT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "chmi", "recent")
LOCAL = dt.timedelta(hours=2)   # CEST; celé období 10. 7. - 21. 10. je v letním čase

# ------------------------------------------------------------ hladina
txt = open(os.path.join(ROOT, "data", "kachnik_2026_rle.txt"), encoding="utf-8").read()
pts, gaps = [], []
for m in re.finditer(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d),GAP,(\d+)|(\d\d-\d\d \d\d:\d\d),(\d+)', txt):
    if m.group(1): gaps.append({"od": m.group(1)[:16], "minut": int(m.group(2))})
    else: pts.append((dt.datetime.strptime('2026-' + m.group(3), '%Y-%m-%d %H:%M'), int(m.group(4))))
ser = []
for i, (t, v) in enumerate(pts):
    t2 = pts[i + 1][0] if i + 1 < len(pts) else t + dt.timedelta(minutes=20)
    while t < t2:
        ser.append((t, v)); t += dt.timedelta(minutes=20)
lvl = dict(ser)

# ------------------------------------------------------------ srážky (parser jako 08_srazky_recent.py)
def zaznamy(cesta):
    with open(cesta, encoding="utf-8-sig") as f: j = json.load(f)
    out = []
    def projdi(x):
        if isinstance(x, dict):
            if "header" in x and "values" in x and isinstance(x["values"], list):
                h = x["header"]; h = h.split(",") if isinstance(h, str) else list(h)
                h = [{"VAL": "VALUE", "VTYPE": "TIMEFUNC"}.get(str(c).strip().upper(), str(c).strip().upper()) for c in h]
                for row in x["values"]:
                    if isinstance(row, (list, tuple)): out.append(dict(zip(h, row)))
                return
            for v in x.values(): projdi(v)
        elif isinstance(x, list):
            for v in x: projdi(v)
    projdi(j); return out

def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def serie(cesty, element):
    s = {}
    for c in cesty:
        if not os.path.exists(c): continue
        for r in zaznamy(c):
            if str(r.get("ELEMENT", "")).upper() != element: continue
            v, q = fl(r.get("VALUE")), fl(r.get("QUALITY"))
            if v is None or (q is not None and q >= 4): continue
            s[dt.datetime.fromisoformat(str(r.get("DT", ""))[:16]) + LOCAL] = v
    return s

STANICE = {"Nemochovice": "0-203-0-41503035001", "Staré Hutě": "0-203-0-41701068003"}
H = {n: serie([os.path.join(RECENT, f"1h-{w}-2026{m:02d}.json") for m in range(6, 11)], "SRA1H") for n, w in STANICE.items()}
KD = serie([os.path.join(RECENT, f"dly-0-203-0-41701068002-2026{m:02d}.json") for m in range(6, 11)], "SRA")
KD = {(t - LOCAL).date().isoformat(): v for t, v in KD.items()}
if not any(H.values()):
    sys.exit("chybí hodinová data ČHMÚ (data/chmi/recent) - spusť nejdřív vyrob_srazky_2026.bat")

# ------------------------------------------------------------ události hladiny (ručně vymezené po prohlídce řady)
# start = poslední bod na základní hladině před vzestupem; vrchol; base = hladina před vzestupem
UDALOSTI = [
    ("2026-07-14 21:19", "2026-07-15 06:39", "bouřka 14. 7. večer + déšť 15. 7. ráno"),
    ("2026-07-18 14:19", "2026-07-18 16:39", "místní přeháňka (jen Koryčany 6,7 mm/den)"),
    ("2026-07-23 11:59", "2026-07-23 12:19", "krátká přeháňka v poledne"),
    ("2026-08-01 19:19", "2026-08-01 22:59", "bouřka 1. 8. večer (Nemochovice 21 mm/h)"),
    ("2026-08-20 16:39", "2026-08-21 01:39", "déšť 20. 8. večer"),
    ("2026-08-28 22:19", "2026-08-29 08:19", "déšť 29. 8. v noci"),
    ("2026-09-09 21:19", "2026-09-10 04:59", "trvalý déšť 9.-10. 9."),
    ("2026-09-11 07:19", "2026-09-11 14:47", "trvalý slabý déšť 11. 9."),
    ("2026-09-16 21:39", "2026-09-17 03:39", "déšť 16.-17. 9. v noci"),
]
ARTEFAKTY = {
    "8. 9. 17:59-19:59": "hodnoty 50/56 střídané 45/46 po 20 min, bez deště na obou stanicích - šum čidla, ne voda (dřív otevřená otázka)",
    "propady pod 30 cm kolem 16:40-17:20": "15. 7., 23. 7. (17:59), 11. 9., 17. 9., 24. 9. - vždy pozdní odpoledne, návrat do 1 h: optický artefakt (pravděpodobně slunce)",
    "27.-28. 7. a 21.-23. 8.": "pokles na 4-16 cm a pomalý návrat 1 cm za 20-40 min přes 15 h = manipulace stavidlem (vypuštění a opětovné plnění), ne déšť; 23. 8. 09:39 znovu",
}

def okno(h, a, b): return {t: v for t, v in h.items() if a < t <= b}
vys = []
for s, p, pop in UDALOSTI:
    s = dt.datetime.fromisoformat(s); p = dt.datetime.fromisoformat(p)
    base = statistics.median([v for t, v in ser if s - dt.timedelta(hours=6) <= t <= s and v >= 30])
    peak = max(v for t, v in ser if s <= t <= p)
    # konec = první bod po vrcholu s hladinou <= base + 2 (ignoruje propady < 30)
    konec = next((t for t, v in ser if t > p and 30 <= v <= base + 2), None)
    r = {}
    for n, h in H.items():
        w = okno(h, s - dt.timedelta(hours=12), p)
        mx = max(w.items(), key=lambda kv: kv[1]) if w else (None, 0)
        r[n] = {"uhrn_12h_pred_az_vrchol_mm": round(sum(w.values()), 1), "max_1h_mm": mx[1],
                "max_1h_cas": mx[0].strftime("%d.%m. %H:%M") if mx[0] else None,
                "zpozdeni_vrcholu_h": round((p - mx[0]).total_seconds() / 3600, 1) if mx[0] and mx[1] > 0 else None}
    vys.append({"popis": pop, "start": s.strftime("%d.%m. %H:%M"), "vrchol": p.strftime("%d.%m. %H:%M"), "vrchol_cm": peak,
                "zaklad_cm": base, "vzestup_cm": peak - base, "doba_vzestupu_h": round((p - s).total_seconds() / 3600, 1),
                "navrat_k_zakladu": konec.strftime("%d.%m. %H:%M") if konec else None,
                "doba_navratu_h": round((konec - p).total_seconds() / 3600, 1) if konec else None,
                "korycany_denni_mm": {d: KD.get(d) for d in sorted({(s - dt.timedelta(days=1)).date().isoformat(), s.date().isoformat(), p.date().isoformat()})},
                "stanice": r})

# déšť bez odezvy: hodinové události >= 5 mm, u kterých hladina do 12 h nevzrostla o >= 3 cm
def dest_udalosti(h):
    ev, cur = [], None
    for t in sorted(h):
        v = h[t]
        if v >= 0.3:
            if cur and (t - cur["end"]) <= dt.timedelta(hours=6): cur["end"] = t; cur["sum"] += v; cur["max"] = max(cur["max"], v)
            else:
                if cur: ev.append(cur)
                cur = {"start": t, "end": t, "sum": v, "max": v}
    if cur: ev.append(cur)
    return [e for e in ev if e["sum"] >= 5]
bez_odezvy = []
for n, h in H.items():
    for e in dest_udalosti(h):
        if e["start"] < ser[0][0]: continue
        w = [v for t, v in ser if e["start"] <= t <= e["end"] + dt.timedelta(hours=12) and v >= 30]
        b = statistics.median([v for t, v in ser if e["start"] - dt.timedelta(hours=6) <= t <= e["start"] and v >= 30] or [0])
        if w and max(w) - b < 3:
            bez_odezvy.append({"stanice": n, "od": e["start"].strftime("%d.%m. %H:%M"), "do": e["end"].strftime("%d.%m. %H:%M"), "uhrn_mm": round(e["sum"], 1), "max_1h_mm": e["max"], "hladina_zmena_cm": max(w) - b})

out = {
    "zdroj_hladina": "VOX varovné systémy, čidlo 5157 'Čid5 Koryčany ul. U Rybníka, stavidlo' (pomocný hlásný profil C, Stříbrník u rybníka Kachník), SPA 100/120/140 cm; export CSV z hladiny-vox.pwsplus.eu 21. 10. 2026; optické měření, krok 20 min, místní čas (ověřeno shodou s hodinovými srážkami); podmínky užití neuvedeny",
    "zdroj_srazky": "ČHMÚ otevřená data, recent 1h (SRA1H) Nemochovice 7,8 km a Staré Hutě 9,4 km, denní Koryčany; předběžná data",
    "obdobi": [ser[0][0].isoformat(timespec="minutes"), ser[-1][0].isoformat(timespec="minutes")],
    "pocet_bodu": len(ser), "vypadky": gaps,
    "zakladni_hladina_cm": {"medián": statistics.median([v for _, v in ser if v >= 30]), "rozsah_bezny": [43, 51]},
    "spa_cm": {"SPA1": 100, "SPA2": 120, "SPA3": 140},
    "max_leto_cm": max(v for _, v in ser if v < 90),
    "udalosti": vys, "dest_bez_odezvy": bez_odezvy, "artefakty": ARTEFAKTY,
    "pozn": "Hladina je u stavidla rybníka, takže reaguje i na manipulaci stavidlem; vzestupy do +24 cm = 1/4 cesty k SPA1. Čidlo neměří průtok - objem odtoku z něj nejde spočítat bez měrné křivky.",
}
with open(os.path.join(ROOT, "data", "kachnik_2026.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for u in vys:
    print(f"{u['start']} -> {u['vrchol']} {u['vrchol_cm']} cm (+{u['vzestup_cm']}), vzestup {u['doba_vzestupu_h']} h, návrat {u['doba_navratu_h']} h; "
          + "; ".join(f"{n}: {x['uhrn_12h_pred_az_vrchol_mm']} mm, max {x['max_1h_mm']} mm/h {x['max_1h_cas']}, zpoždění {x['zpozdeni_vrcholu_h']} h" for n, x in u['stanice'].items()))
print("bez odezvy:", bez_odezvy)

# ------------------------------------------------------------ obrázek
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw={"height_ratios": [1, 2]})
    for n, h in H.items():
        ts = sorted(h); axes[0].bar(ts, [h[t] for t in ts], width=1 / 24, label=n, alpha=.7)
    axes[0].set_ylabel("mm / h"); axes[0].legend(loc="upper right"); axes[0].set_title("Srážky (ČHMÚ, hodinové, místní čas) a hladina Stříbrníku u Kachníku (VOX, 20 min), léto 2026")
    T = [t for t, _ in ser]; V = [v for _, v in ser]
    axes[1].plot(T, V, lw=.8, color="#1f5f8b"); axes[1].set_ylabel("hladina u stavidla [cm]")
    axes[1].axhline(100, color="green", lw=1, ls="--"); axes[1].text(T[0], 101, "SPA 1 = 100 cm", color="green", fontsize=8)
    for u in vys:
        t = dt.datetime.strptime("2026 " + u["vrchol"], "%Y %d.%m. %H:%M"); axes[1].annotate(f"+{u['vzestup_cm']}", (t, u["vrchol_cm"]), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=8)
    axes[1].set_ylim(0, 110); axes[1].grid(alpha=.3); axes[0].grid(alpha=.3)
    fig.autofmt_xdate(); fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "docs", "img", "kachnik_nahled.png"), dpi=110)
    print("obrázek docs/img/kachnik_nahled.png")
    # detail čtyř epizod: 48 h kolem vrcholu
    fig, axes = plt.subplots(2, 2, figsize=(13, 7))
    for ax, idx in zip(axes.flat, [0, 3, 4, 6]):
        u = vys[idx]; p = dt.datetime.strptime("2026 " + u["vrchol"], "%Y %d.%m. %H:%M"); a, b = p - dt.timedelta(hours=30), p + dt.timedelta(hours=18)
        ax2 = ax.twinx()
        for n, h, c in zip(H, H.values(), ["#1f5f8b", "#e07b00"]):
            ts = [t for t in sorted(h) if a <= t <= b]; ax2.bar(ts, [h[t] for t in ts], width=1 / 24, color=c, alpha=.5, label=n)
        ax2.set_ylim(25, 0); ax2.set_ylabel("déšť mm/h (shora)")
        ts = [t for t, v in ser if a <= t <= b and v >= 30]; ax.plot(ts, [lvl[t] for t in ts], color="#1d1c19", lw=1.2, label="hladina")
        ax.set_ylim(40, 75); ax.set_ylabel("hladina cm"); ax.set_title(u["popis"] + f" (+{u['vzestup_cm']} cm)", fontsize=10); ax.grid(alpha=.3)
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m. %H:%M")); ax.tick_params(axis="x", labelsize=8, rotation=30)
        if idx == 0: ax2.legend(loc="lower right", fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "docs", "img", "kachnik_udalosti.png"), dpi=110)
    print("obrázek docs/img/kachnik_udalosti.png")
except ImportError:
    print("matplotlib chybí - bez obrázku")
