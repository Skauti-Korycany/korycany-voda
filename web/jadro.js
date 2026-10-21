/* jadro.js - vypocetni jadro aplikace Korycany voda (faze 3), v0.3, 21. 10. 2026
 *
 * Pracuje nad rastry z data/web/ (09_balicek_web.py): mrizka S-JTSK 5 m, pasma v PNG.
 * Bez knihoven. V prohlizeci: Jadro.nacti('data/web/') -> Promise. V node: Jadro.nactiZPoli(info, {pasmo: Uint8Array|Uint16Array}).
 *
 * Metody (zdroje viz docs/JADRO.md):
 *  - SCS-CN: Q = (P - Ia)^2 / (P - Ia + S), S = 25400/CN - 254 [mm], Ia = 0,2 S (Janecek a kol. 2012, kap. 2; USDA TR-55)
 *  - prevod CN na IPS I / III: standardni vztahy SCS (Hawkins; NEH-4): CN1 = 4,2 CN / (10 - 0,058 CN), CN3 = 23 CN / (10 + 0,13 CN)
 *    (metodika CVUT 2023 pouziva tytez hodnoty: Stasov CN2 81 -> CN3 90,7)
 *  - odtok vazeny pres tvary deste A-F a stav nasyceni CN2/CN3 (Kavka a kol. 2023, kap. 2.5, tab. 6; data/navrhove_srazky.json):
 *    V = sum_i p_i * (w2_i * V_CN2 + w3_i * V_CN3), vahy w podle qAPI tvaru i (<=0,2: 1/0; <=0,4: 0,75/0,25; <=0,6: 0,5/0,5; <=0,8: 0,25/0,75; >0,8: 0/1)
 *  - povodi bodu: zpetne sledovani D8 (smer.png)
 *  - nadrz (v0.3): hraz na vektorovem toku CUZK (HY-NET, vypaleny do DMR skriptem 14), osa hraze kolmo na tok az k terenu nad korunou;
 *    tok s povodim >= 0,25 km2: zatopeni bunek pod hladinou souvisle s hrazi (DMR 5 m); mensi tok: jen tun/poldr v udolnici,
 *    objem z pricneho profilu v ose hraze a podelneho sklonu dna jako rozsah (V = A*L/3 az A*L/2, L = h / sklon)
 * Vsechny vysledky jsou orientacni (model pro osvetu), viz docs/00-instrukce-projektu.md.
 */
(function (global) {
  'use strict';

  const J = { info: null, p: {}, verze: '0.3' };

  // ---------------------------------------------------------------- nacteni
  J.nactiZPoli = function (info, pasma, toky) {
    J.info = info;
    J.p = pasma;
    J.toky = toky || null;   // data/web/toky.json (14_toky_vypaleni.py); bez nich nadrz nefunguje
    const m = info.mrizka;
    J.ncol = m.ncol; J.nrow = m.nrow; J.krok = m.krok_m; J.x0 = m.x0; J.y1 = m.y1; J.plochaB = m.plocha_bunky_m2;
    return J;
  };

  // prohlizec: PNG -> typovana pole pres canvas
  // opts.bez = pole pasem, ktera se nenactou (napr. ['smer_v'] kdyz se nepocitaji nadrze); opts.toky = false -> bez toky.json
  J.nacti = async function (base, opts) {
    opts = opts || {};
    const info = await (await fetch(base + 'rastr.json')).json();
    const pasma = {};
    await Promise.all(Object.entries(info.pasma).filter(([nazev]) => !(opts.bez || []).includes(nazev)).map(async ([nazev, p]) => {
      const img = new Image();
      img.src = base + p.soubor;
      await img.decode();
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(img, 0, 0);
      const d = ctx.getImageData(0, 0, img.width, img.height).data;
      const n = img.width * img.height;
      if (p.bity === 16) {
        const out = new Uint16Array(n);
        for (let i = 0; i < n; i++) out[i] = (d[i * 4] << 8) | d[i * 4 + 1];
        pasma[nazev] = out;
      } else {
        const out = new Uint8Array(n);
        for (let i = 0; i < n; i++) out[i] = d[i * 4];
        pasma[nazev] = out;
      }
    }));
    let toky = null;
    if (opts.toky !== false) try { const r = await fetch(base + 'toky.json'); if (r.ok) toky = await r.json(); } catch (e) { toky = null; }
    return J.nactiZPoli(info, pasma, toky);
  };

  // ---------------------------------------------------------------- souradnice
  J.lonLatNaXY = function (lon, lat) {
    const c = J.info.prevod.lonlat_na_xy;
    const u = (lon - c.lon0) * 100, v = (lat - c.lat0) * 100;
    const t = [1, u, v, u * u, u * v, v * v];
    let X = 0, Y = 0;
    for (let i = 0; i < 6; i++) { X += c.cx[i] * t[i]; Y += c.cy[i] * t[i]; }
    return [X, Y];
  };
  J.xyNaLonLat = function (X, Y) {
    const c = J.info.prevod.xy_na_lonlat;
    const u = (X - c.xc) / 1000, v = (Y - c.yc) / 1000;
    const t = [1, u, v, u * u, u * v, v * v];
    let lon = 0, lat = 0;
    for (let i = 0; i < 6; i++) { lon += c.clon[i] * t[i]; lat += c.clat[i] * t[i]; }
    return [lon, lat];
  };
  J.xyNaBunku = function (X, Y) {
    const col = Math.floor((X - J.x0) / J.krok), row = Math.floor((J.y1 - Y) / J.krok);
    if (col < 0 || row < 0 || col >= J.ncol || row >= J.nrow) return null;
    return { col, row, i: row * J.ncol + col };
  };
  J.bunkaNaXY = function (i) {
    const row = Math.floor(i / J.ncol), col = i - row * J.ncol;
    return [J.x0 + (col + 0.5) * J.krok, J.y1 - (row + 0.5) * J.krok];
  };
  J.lonLatNaBunku = function (lon, lat) { const [X, Y] = J.lonLatNaXY(lon, lat); return J.xyNaBunku(X, Y); };

  // ---------------------------------------------------------------- dekodovani pasem
  J.vyska = i => J.p.vyska[i] === 0 ? null : 200 + J.p.vyska[i] / 10;
  J.sklonDeg = i => J.p.sklon[i] === 255 ? null : J.p.sklon[i] / 4;
  J.akumulace = i => J.p.akumulace[i] === 0 ? null : Math.pow(10, (J.p.akumulace[i] - 1) / 40);
  J.cn = i => J.p.cn[i] || null;
  J.hsp = i => J.p.hsp[i] || null;          // 1..4 = A..D
  J.vyuziti = i => J.p.vyuziti[i] || null;
  J.platna = i => J.p.vyska[i] !== 0;

  // ---------------------------------------------------------------- SCS-CN
  J.cnProIPS = function (cn, ips) {
    if (ips === 1) return 4.2 * cn / (10 - 0.058 * cn);
    if (ips === 3) return 23 * cn / (10 + 0.13 * cn);
    return cn;
  };
  // P v mm, CN bezrozm.; vraci Q v mm (0 pri P <= Ia)
  J.scsCN = function (P, cn, ia) {
    if (!cn || cn <= 0) return 0;
    const S = 25400 / cn - 254;
    const Ia = (ia == null ? 0.2 : ia) * S;
    if (P <= Ia) return 0;
    return (P - Ia) * (P - Ia) / (P - Ia + S);
  };

  // vahy stavu nasyceni podle qAPI (Kavka a kol. 2023, tab. 6); hranice intervalu bereme jako "do vcetne"
  J.vahyCN = function (qapi) {
    const w3 = qapi <= 0.2 ? 0 : qapi <= 0.4 ? 0.25 : qapi <= 0.6 ? 0.5 : qapi <= 0.8 ? 0.75 : 1;
    return { cn2: 1 - w3, cn3: w3 };
  };
  // celkova vaha CN3 pro lokalitu: podil_pct = {A: %, ...} (zastoupeni tvaru), qapi = {A: 0..1, ...}
  J.vahaCN3 = function (podilPct, qapi) {
    let w = 0, ps = 0;
    for (const t of Object.keys(podilPct)) { const p = podilPct[t] / 100; ps += p; w += p * J.vahyCN(qapi[t]).cn3; }
    return ps > 0 ? w / ps : 0;
  };
  // odtok z objektu st.odtok (ma Q_mm = CN2 a Q_mm_cn3) vazeny pres tvary: vraci {Q_mm, objem_m3, rozsah_m3, vaha_cn3}
  J.odtokVazeny = function (odtok, podilPct, qapi) {
    if (!odtok || odtok.Q_mm_cn3 == null) return null;
    const w3 = J.vahaCN3(podilPct, qapi);
    const Q = odtok.Q_mm * (1 - w3) + odtok.Q_mm_cn3 * w3;
    const V = odtok.objem_m3 * (1 - w3) + odtok.objem_m3_cn3 * w3;
    return { Q_mm: Q, objem_m3: V, koef: Q / odtok.P_mm, rozsah_m3: [odtok.objem_m3, odtok.objem_m3_cn3], vaha_cn3: w3,
      pozn: 'SCS-CN po bunkach, vazeno pres tvary deste A-F a stav nasyceni CN2/CN3 podle qAPI (Kavka a kol. 2023, tab. 6)' };
  };

  // ---------------------------------------------------------------- rasterizace polygonu
  // ring = [[lon,lat],...] (prvni = posledni nepovinne); vraci pole indexu bunek, jejichz stred lezi uvnitr (even-odd)
  J.bunkyPolygonu = function (ring, diry) {
    const xy = ring.map(([lo, la]) => J.lonLatNaXY(lo, la));
    const prst = [xy].concat((diry || []).map(r => r.map(([lo, la]) => J.lonLatNaXY(lo, la))));
    let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
    for (const [X, Y] of xy) { if (X < xmin) xmin = X; if (X > xmax) xmax = X; if (Y < ymin) ymin = Y; if (Y > ymax) ymax = Y; }
    const c0 = Math.max(0, Math.floor((xmin - J.x0) / J.krok)), c1 = Math.min(J.ncol - 1, Math.floor((xmax - J.x0) / J.krok));
    const r0 = Math.max(0, Math.floor((J.y1 - ymax) / J.krok)), r1 = Math.min(J.nrow - 1, Math.floor((J.y1 - ymin) / J.krok));
    const out = [];
    for (let row = r0; row <= r1; row++) {
      const Y = J.y1 - (row + 0.5) * J.krok;
      // pruseciky vsech prstencu s vodorovnou primkou Y
      const xs = [];
      for (const p of prst) {
        const n = p.length;
        for (let k = 0; k < n; k++) {
          const [xa, ya] = p[k], [xb, yb] = p[(k + 1) % n];
          if ((ya > Y) !== (yb > Y)) xs.push(xa + (Y - ya) * (xb - xa) / (yb - ya));
        }
      }
      if (!xs.length) continue;
      xs.sort((a, b) => a - b);
      for (let k = 0; k + 1 < xs.length; k += 2) {
        const ca = Math.max(c0, Math.ceil((xs[k] - J.x0) / J.krok - 0.5)), cb = Math.min(c1, Math.floor((xs[k + 1] - J.x0) / J.krok - 0.5));
        for (let col = ca; col <= cb; col++) out.push(row * J.ncol + col);
      }
    }
    return out;
  };

  // ---------------------------------------------------------------- statistika mnoziny bunek
  // bunky = pole indexu; P = navrhovy dest mm (nepovinne); ips = 1|2|3
  J.statBunek = function (bunky, P, ips) {
    const st = { n: 0, n_platnych: 0, plocha_ha: 0, cn_vazene: null, sklon_prumer_deg: null, sklon_prumer_pct: null,
      vyska_min: null, vyska_max: null, vyuziti_ha: {}, hsp_ha: { A: 0, B: 0, C: 0, D: 0 }, hsp_odhad_ha: 0,
      akumulace_max: 0, bunka_akumulace_max: null, tok_prochazi: false, odtok: null };
    let cnS = 0, cnN = 0, skS = 0, skN = 0, Qsum = 0, Qn = 0, Q3sum = 0;
    const hspK = ['A', 'B', 'C', 'D'];
    for (const i of bunky) {
      st.n++;
      if (!J.platna(i)) continue;
      st.n_platnych++;
      const cn = J.cn(i); if (cn) { cnS += cn; cnN++; }
      const sk = J.sklonDeg(i); if (sk != null) { skS += sk; skN++; }
      const z = J.vyska(i); if (st.vyska_min == null || z < st.vyska_min) st.vyska_min = z; if (st.vyska_max == null || z > st.vyska_max) st.vyska_max = z;
      const v = J.vyuziti(i); if (v) st.vyuziti_ha[v] = (st.vyuziti_ha[v] || 0) + J.plochaB / 1e4;
      const h = J.hsp(i); if (h) { st.hsp_ha[hspK[h - 1]] += J.plochaB / 1e4; if (J.p.hsp_zdroj[i] === 2) st.hsp_odhad_ha += J.plochaB / 1e4; }
      const a = J.akumulace(i); if (a != null && a > st.akumulace_max) { st.akumulace_max = a; st.bunka_akumulace_max = i; }
      if (P != null && cn) { Qsum += J.scsCN(P, J.cnProIPS(cn, ips || 2)); Q3sum += J.scsCN(P, J.cnProIPS(cn, 3)); Qn++; }
    }
    st.plocha_ha = st.n_platnych * J.plochaB / 1e4;
    st.cn_vazene = cnN ? cnS / cnN : null;
    st.sklon_prumer_deg = skN ? skS / skN : null;
    st.sklon_prumer_pct = skN ? Math.tan(st.sklon_prumer_deg * Math.PI / 180) * 100 : null;
    st.tok_prochazi = st.akumulace_max * J.plochaB >= 0.25e6;   // udolnice >= 0,25 km2 (jako 02_rozvodnice.py)
    if (P != null && Qn) {
      const Q_mm = Qsum / Qn;
      const Q3 = Q3sum / Qn;
      st.odtok = { P_mm: P, ips: ips || 2, Q_mm, objem_m3: Q_mm / 1000 * Qn * J.plochaB, koef: Q_mm / P,
        Q_mm_cn3: Q3, objem_m3_cn3: Q3 / 1000 * Qn * J.plochaB, pozn: 'SCS-CN po bunkach, Ia = 0,2 S; Q_mm = stav podle ips, Q_mm_cn3 = nasycene (CN3)' };
    }
    return st;
  };
  J.statPolygon = (ring, P, ips, diry) => J.statBunek(J.bunkyPolygonu(ring, diry), P, ips);

  // ---------------------------------------------------------------- povodi bodu (zpetne D8)
  const D8 = { 1: [1, 0], 2: [1, 1], 4: [0, 1], 8: [-1, 1], 16: [-1, 0], 32: [-1, -1], 64: [0, -1], 128: [1, -1] };   // kod -> [dcol, drow]
  const SOUSEDE = Object.entries(D8).map(([k, [dc, dr]]) => ({ dc, dr, kodDoMne: ({ 1: 16, 2: 32, 4: 64, 8: 128, 16: 1, 32: 2, 64: 4, 128: 8 })[k] }));

  // prichyceni k toku: bunka s nejvetsi akumulaci v okruhu polomer_m
  J.prichytKToku = function (i, polomerM) {
    const r = Math.max(0, Math.round((polomerM || 0) / J.krok));
    const row0 = Math.floor(i / J.ncol), col0 = i - row0 * J.ncol;
    let best = i, bestA = -1;
    for (let dr = -r; dr <= r; dr++) for (let dc = -r; dc <= r; dc++) {
      if (dr * dr + dc * dc > r * r) continue;
      const row = row0 + dr, col = col0 + dc;
      if (row < 0 || col < 0 || row >= J.nrow || col >= J.ncol) continue;
      const k = row * J.ncol + col, a = J.p.akumulace[k];
      if (a > bestA) { bestA = a; best = k; }
    }
    return best;
  };

  // vraci {bunky: Int32Array indexu, maska: Uint8Array (cela mrizka, 1 = uvnitr), uzaver: i, orez: bool}
  // i0 = index bunky nebo pole indexu (povodi vice bunek najednou, napr. cela hraz)
  // smer = pasmo D8 (vychozi J.p.smer z terenu; nadrz pouziva J.p.smer_v po vypaleni toku, kdyz je nactene)
  J.povodiBunky = function (i0, maxBunek, smerPasmo) {
    const max = maxBunek || 2e6;
    const maska = new Uint8Array(J.ncol * J.nrow);
    const fronta = new Int32Array(Math.min(max, J.ncol * J.nrow));
    let q0 = 0, q1 = 0;
    for (const i of (Array.isArray(i0) ? i0 : [i0])) if (!maska[i]) { fronta[q1++] = i; maska[i] = 1; }
    const smer = smerPasmo || J.p.smer;
    while (q0 < q1) {
      const i = fronta[q0++];
      const row = Math.floor(i / J.ncol), col = i - row * J.ncol;
      for (const s of SOUSEDE) {
        const r = row + s.dr, c = col + s.dc;
        if (r < 0 || c < 0 || r >= J.nrow || c >= J.ncol) continue;
        const k = r * J.ncol + c;
        if (maska[k] || smer[k] !== s.kodDoMne) continue;
        maska[k] = 1;
        if (q1 >= fronta.length) return { bunky: fronta.subarray(0, q1), maska, uzaver: i0, orez: true };
        fronta[q1++] = k;
      }
    }
    return { bunky: fronta.subarray(0, q1), maska, uzaver: i0, orez: false };
  };
  J.povodiBodu = function (lon, lat, polomerM, P, ips) {
    const b = J.lonLatNaBunku(lon, lat);
    if (!b) return null;
    const i0 = J.prichytKToku(b.i, polomerM == null ? 50 : polomerM);   // polomerM = 0 -> bez prichyceni
    const pov = J.povodiBunky(i0);
    const st = J.statBunek(pov.bunky, P, ips);
    st.plocha_km2 = st.plocha_ha / 100;
    st.uzaver_lonlat = J.xyNaLonLat(...J.bunkaNaXY(i0));
    st.posun_m = Math.hypot(...J.bunkaNaXY(i0).map((v, k) => v - J.bunkaNaXY(b.i)[k]));
    st.pod_rozlisenim = st.n_platnych < 8;
    st.orez_okrajem = pov.orez || J.naOkraji(pov.maska);
    return { stat: st, maska: pov.maska, bunky: pov.bunky, uzaver: i0 };
  };
  // povodi sahajici k okraji rastru je neuplne
  J.naOkraji = function (maska) {
    for (let c = 0; c < J.ncol; c++) if (maska[c] || maska[(J.nrow - 1) * J.ncol + c]) return true;
    for (let r = 0; r < J.nrow; r++) if (maska[r * J.ncol] || maska[r * J.ncol + J.ncol - 1]) return true;
    return false;
  };

  // ---------------------------------------------------------------- nadrz / poldr (v0.3, 21. 10. 2026)
  // Hraz se stavi jen na vodnim toku z mapy CUZK (data/web/toky.json, body po 5 m od pramene po proudu).
  // Osa hraze je kolmo na tok a konci tam, kde teren dosahne koruny (dno + vyska hraze), nejvys maxDelkaHrazeM.
  // Tok s povodim >= MALY_TOK_KM2: zatopeni bunek DMR pod hladinou, souvisle s hrazi, uvnitr povodi hraze.
  // Mensi tok: DMR 5 m jeho udoli nerozlisi -> jen "tun / poldr v udolnici": objem z pricneho profilu v ose hraze
  // a podelneho sklonu dna jako rozsah V = A*L/3 (udoli tvaru V) az A*L/2 (udoli s plochym dnem), L = h / sklon.
  J.MALY_TOK_KM2 = 0.25;
  J.MIN_BUNEK_ZATOPY = 20;   // mensi zatopa v DMR = sum; prejde se na odhad z profilu

  // vyska v bode S-JTSK, bilinearne mezi stredy bunek (null mimo data)
  J.zBod = function (X, Y) {
    const fc = (X - J.x0) / J.krok - 0.5, fr = (J.y1 - Y) / J.krok - 0.5;
    const c = Math.floor(fc), r = Math.floor(fr), tc = fc - c, tr = fr - r;
    if (c < 0 || r < 0 || c + 1 >= J.ncol || r + 1 >= J.nrow) return null;
    const i = r * J.ncol + c, z00 = J.vyska(i), z01 = J.vyska(i + 1), z10 = J.vyska(i + J.ncol), z11 = J.vyska(i + J.ncol + 1);
    if (z00 == null || z01 == null || z10 == null || z11 == null) { const b = J.xyNaBunku(X, Y); return b ? J.vyska(b.i) : null; }
    return (z00 * (1 - tc) + z01 * tc) * (1 - tr) + (z10 * (1 - tc) + z11 * tc) * tr;
  };

  // nejblizsi bod na vektorovem toku: {linie, k (usek), u (0..1), X, Y, d (vzdalenost od kliku), s (m od zacatku linie)}
  J.prichytKVektoru = function (X, Y, maxM) {
    if (!J.toky) return null;
    let best = null;
    for (const l of J.toky.linie) {
      const xs = l.x, ys = l.y;
      for (let k = 0; k + 1 < xs.length; k++) {
        const ax = xs[k], ay = ys[k], bx = xs[k + 1], by = ys[k + 1];
        const dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy;
        let u = L2 > 0 ? ((X - ax) * dx + (Y - ay) * dy) / L2 : 0;
        u = Math.max(0, Math.min(1, u));
        const px = ax + u * dx, py = ay + u * dy, d = Math.hypot(X - px, Y - py);
        if (!best || d < best.d) best = { linie: l, k, u, X: px, Y: py, d };
      }
    }
    if (!best || (maxM != null && best.d > maxM)) return best ? { daleko: true, d: best.d } : null;
    const l = best.linie;
    if (!l._s) { l._s = [0]; for (let k = 1; k < l.x.length; k++) l._s.push(l._s[k - 1] + Math.hypot(l.x[k] - l.x[k - 1], l.y[k] - l.y[k - 1])); }
    best.s = l._s[best.k] + best.u * (l._s[best.k + 1] - l._s[best.k]);
    return best;
  };

  // body dna proti proudu od mista (linie, s) po krocich ~5 m az do vzdalenosti maxM; pri zacatku linie pokracuje
  // do pritoku s nejvetsim povodim. Vraci [{d, X, Y, z}] (d = m proti proudu od mista)
  J.dnoProtiProudu = function (l, s, maxM) {
    const out = [];
    let lin = l, d0 = 0, sLoc = s;
    while (lin && d0 < maxM) {
      if (!lin._s) { lin._s = [0]; for (let k = 1; k < lin.x.length; k++) lin._s.push(lin._s[k - 1] + Math.hypot(lin.x[k] - lin.x[k - 1], lin.y[k] - lin.y[k - 1])); }
      for (let k = lin.x.length - 1; k >= 0; k--) {
        if (lin._s[k] > sLoc) continue;
        const d = d0 + (sLoc - lin._s[k]);
        if (d > maxM) break;
        if (lin.z_dno[k] != null) out.push({ d, X: lin.x[k], Y: lin.y[k], z: lin.z_dno[k] });
      }
      d0 += sLoc;
      const pr = (lin.pritoky || []).map(i => J.toky.linie[i]);
      if (!pr.length) break;
      lin = pr.reduce((a, b) => (b.A_km2[b.A_km2.length - 1] > a.A_km2[a.A_km2.length - 1] ? b : a));
      if (!lin._s) { lin._s = [0]; for (let k = 1; k < lin.x.length; k++) lin._s.push(lin._s[k - 1] + Math.hypot(lin.x[k] - lin.x[k - 1], lin.y[k] - lin.y[k - 1])); }
      sLoc = lin._s[lin._s.length - 1];
    }
    return out;
  };

  // bunky usecky (vzorkovani po 1 m)
  J.bunkyUsecky = function (Xa, Ya, Xb, Yb) {
    const n = Math.max(1, Math.ceil(Math.hypot(Xb - Xa, Yb - Ya)));
    const set = new Set();
    for (let k = 0; k <= n; k++) { const b = J.xyNaBunku(Xa + (Xb - Xa) * k / n, Ya + (Yb - Ya) * k / n); if (b) set.add(b.i); }
    return [...set];
  };

  // opts: {polomerM: max. vzdalenost kliku od toku (60), maxDelkaHrazeM (300), maxBunek zatopy (400 000)}
  J.nadrz = function (lon, lat, vyskaHrazeM, opts) {
    if (typeof opts === 'number') opts = { polomerM: opts };
    opts = opts || {};
    const maxDelka = opts.maxDelkaHrazeM || 300, maxBunek = opts.maxBunek || 400000;
    const h = vyskaHrazeM;
    if (!J.toky) return { chyba: 'chybi data toku (data/web/toky.json)' };
    const [Xk, Yk] = J.lonLatNaXY(lon, lat);
    const pt = J.prichytKVektoru(Xk, Yk, opts.polomerM == null ? 60 : opts.polomerM);
    if (!pt) return null;
    if (pt.daleko) return { chyba: 'daleko_od_toku', vzdalenost_m: pt.d };
    const l = pt.linie, k = pt.k, varovani = [];

    // plocha povodi a dno v miste hraze (dno = nejnizsi z bodu linie do 10 m)
    const A_km2 = l.A_km2[k] + pt.u * (l.A_km2[k + 1] - l.A_km2[k]);
    let zDno = Infinity;
    for (let j = Math.max(0, k - 2); j <= Math.min(l.x.length - 1, k + 3); j++) if (l.z_dno[j] != null && Math.abs(l._s[j] - pt.s) <= 10) zDno = Math.min(zDno, l.z_dno[j]);
    if (!isFinite(zDno)) zDno = J.zBod(pt.X, pt.Y);
    const hl = zDno + h;

    // smer toku: prumer pres +-15 m linie (po proudu); normala doleva
    const ja = Math.max(0, k - 2), jb = Math.min(l.x.length - 1, k + 3);
    let tx = l.x[jb] - l.x[ja], ty = l.y[jb] - l.y[ja];
    const tn = Math.hypot(tx, ty) || 1; tx /= tn; ty /= tn;
    const nx = -ty, ny = tx;

    // osa hraze: od toku na obe strany po 2,5 m, dokud teren nedosahne koruny
    const krok = 2.5, profil = [{ d: 0, z: zDno }];
    const konce = [];
    let uzavira = true;
    for (const sg of [-1, 1]) {
      let dEnd = null;
      for (let d = krok; d <= maxDelka / 2; d += krok) {
        const z = J.zBod(pt.X + sg * nx * d, pt.Y + sg * ny * d);
        if (z == null) break;
        profil.push({ d: sg * d, z });
        if (z >= hl) { dEnd = d; break; }
      }
      if (dEnd == null) { uzavira = false; dEnd = Math.abs(profil.filter(p => Math.sign(p.d) === sg).reduce((m, p) => Math.max(m, Math.abs(p.d)), krok)); }
      konce.push([pt.X + sg * nx * dEnd, pt.Y + sg * ny * dEnd]);
    }
    profil.sort((a, b) => a.d - b.d);
    if (!uzavira) varovani.push(`hráz by musela být delší než ${maxDelka} m, terén nedosáhne koruny - výsledek je jen dolní odhad`);
    const delkaHraze = Math.hypot(konce[1][0] - konce[0][0], konce[1][1] - konce[0][1]);
    // pricny profil: zatopena plocha prurezu a sirka hladiny v ose hraze
    let Ac = 0, W = 0;
    for (const p of profil) { const dz = hl - Math.max(p.z, zDno); if (dz > 0) { Ac += dz * krok; W += krok; } }

    // podelny sklon dna proti proudu (regrese pres prvnich 100 m, min. 20 m)
    const dno = J.dnoProtiProudu(l, pt.s, 600);
    const usek = dno.filter(p => p.d <= 100);
    let sklon = null;
    if (usek.length >= 5 && usek[usek.length - 1].d >= 20) {
      let sx = 0, sy = 0, sxx = 0, sxy = 0; const n = usek.length;
      for (const p of usek) { sx += p.d; sy += p.z; sxx += p.d * p.d; sxy += p.d * p.z; }
      sklon = (n * sxy - sx * sy) / (n * sxx - sx * sx);
    }
    const SKLON_MIN = 0.005;
    if (sklon == null || sklon < SKLON_MIN) { varovani.push(`dno skoro bez spádu (${sklon == null ? '?' : (100 * sklon).toFixed(1)} %), délka vzdutí počítána se ${100 * SKLON_MIN} %`); sklon = Math.max(sklon || 0, SKLON_MIN); }
    let Lvzduti = h / sklon;
    const Ldostupne = dno.length ? dno[dno.length - 1].d : 0;
    if (Lvzduti > Ldostupne + 5) { varovani.push(`vzdutí ${Math.round(Lvzduti)} m sahá za konec toku v datech (${Math.round(Ldostupne)} m), zkráceno`); Lvzduti = Math.max(Ldostupne, krok); }
    const profilOdhad = { prurez_m2: Ac, sirka_m: W, sklon_dna: sklon, delka_vzduti_m: Lvzduti,
      objem_m3: [Ac * Lvzduti / 3, Ac * Lvzduti / 2], plocha_m2: [W * Lvzduti / 2, W * Lvzduti] };

    // bunky hraze: osa + rada bunek po proudu (hraz 2 bunky siroka, aby zatopa neprosakovala diagonalne)
    const hrazSet = new Set(J.bunkyUsecky(konce[0][0], konce[0][1], konce[1][0], konce[1][1]));
    for (const i of J.bunkyUsecky(konce[0][0] + tx * J.krok, konce[0][1] + ty * J.krok, konce[1][0] + tx * J.krok, konce[1][1] + ty * J.krok)) hrazSet.add(i);
    const hrazBunky = [...hrazSet];
    const pov = J.povodiBunky(hrazBunky, null, J.p.smer_v);   // povodi hraze z D8 po vypaleni toku (sedi s vektorem i v intravilanu)

    const lonlat = (X, Y) => J.xyNaLonLat(X, Y);
    const vysl = {
      verze: '0.3', tok_id: l.id, povodi_km2: A_km2, povodi_bunky: pov.bunky,
      bod_lonlat: lonlat(pt.X, pt.Y), posun_m: pt.d, hraz_lonlat: konce.map(([X, Y]) => lonlat(X, Y)),
      delka_hraze_m: delkaHraze, hraz_uzavira: uzavira, kota_dna: zDno, hladina: hl, vyska_hraze_m: h,
      profil, profil_odhad: profilOdhad, varovani,
    };

    // ---------------- tun / poldr v udolnici (maly tok, nebo zatopa v DMR pod rozlisenim)
    const tunProfil = duvod => {
      // ---------------- tun / poldr v udolnici: objem z profilu, obrys = klin podel toku proti proudu
      const L = Lvzduti, levy = [], pravy = [];
      const body = [{ d: 0, X: pt.X, Y: pt.Y }].concat(dno.filter(p => p.d > 0 && p.d < L));
      body.push({ d: L, ...(() => { const p = dno.find(q => q.d >= L) || dno[dno.length - 1] || { X: pt.X, Y: pt.Y }; return { X: p.X, Y: p.Y }; })() });
      for (let j = 0; j < body.length; j++) {
        const a = body[Math.max(0, j - 1)], b = body[Math.min(body.length - 1, j + 1)];
        let ux = a.X - b.X, uy = a.Y - b.Y; const un = Math.hypot(ux, uy) || 1; ux /= un; uy /= un;   // po proudu
        const w = (W / 2) * Math.max(0, 1 - body[j].d / L);
        levy.push(lonlat(body[j].X - uy * w, body[j].Y + ux * w));
        pravy.push(lonlat(body[j].X + uy * w, body[j].Y - ux * w));
      }
      return Object.assign(vysl, {
        typ: 'tun_udolnice', orientacni: true,
        objem_m3: (profilOdhad.objem_m3[0] + profilOdhad.objem_m3[1]) / 2, objem_rozsah_m3: profilOdhad.objem_m3,
        plocha_ha: (profilOdhad.plocha_m2[0] + profilOdhad.plocha_m2[1]) / 2 / 1e4, plocha_rozsah_m2: profilOdhad.plocha_m2,
        hloubka_max_m: h, obrys_lonlat: levy.concat(pravy.reverse()), maska: null,
        pozn: `${duvod}: objem jen z příčného profilu v ose hráze a sklonu dna, rozsah V-údolí až ploché dno; orientační`,
      });
    };
    if (A_km2 < J.MALY_TOK_KM2) return tunProfil(`tok s povodím pod ${J.MALY_TOK_KM2} km² - DMR 5G (5 m) jeho údolí nerozliší`);

    // ---------------- nadrz: zatopeni bunek DMR pod hladinou, souvisle s hrazi, uvnitr povodi hraze
    const zat = new Uint8Array(J.ncol * J.nrow);
    for (const i of hrazBunky) zat[i] = 2;   // 2 = teleso hraze
    // seminko: prvni bod proti proudu nejmene 7,5 m od osy, ktery neni hraz a lezi pod hladinou
    let seed = null;
    for (const p of dno) {
      if (p.d < 7.5) continue;
      const b = J.xyNaBunku(p.X, p.Y);
      if (b && !zat[b.i] && pov.maska[b.i] && J.platna(b.i) && J.vyska(b.i) < hl) { seed = b.i; break; }
      if (p.d > 40) break;
    }
    if (seed == null) {
      varovani.push('za hrází není terén pod hladinou (příliš nízká hráz nebo strmé dno)');
      return Object.assign(vysl, { typ: 'nadrz', objem_m3: 0, plocha_ha: 0, hloubka_max_m: 0, hloubka_prumer_m: 0, n_bunek: 0, pod_rozlisenim: true, maska: zat.fill(0), zatopene_vyuziti_ha: {} });
    }
    // vzdalenost bunky od osy hraze (pro test prelivu mimo povodi)
    const [ax, ay] = konce[0], [bx, by] = konce[1], abx = bx - ax, aby = by - ay, ab2 = abx * abx + aby * aby || 1;
    const odOsy = i => { const [X, Y] = J.bunkaNaXY(i); const u = Math.max(0, Math.min(1, ((X - ax) * abx + (Y - ay) * aby) / ab2)); return Math.hypot(X - ax - u * abx, Y - ay - u * aby); };
    const fronta = [seed]; zat[seed] = 1;
    let objem = 0, n = 0, hloubkaMax = 0, preliv = false, orez = false;
    while (fronta.length) {
      const i = fronta.pop();
      const d = hl - J.vyska(i);
      objem += d * J.plochaB; n++; if (d > hloubkaMax) hloubkaMax = d;
      if (n >= maxBunek) { orez = true; break; }
      const row = Math.floor(i / J.ncol), col = i - row * J.ncol;
      for (const [dc, dr] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const r = row + dr, c = col + dc;
        if (r < 0 || c < 0 || r >= J.nrow || c >= J.ncol) continue;
        const kk = r * J.ncol + c;
        if (zat[kk] || !J.platna(kk)) continue;
        if (J.vyska(kk) >= hl) continue;
        if (!pov.maska[kk]) { if (!preliv && odOsy(kk) > 15) preliv = true; continue; }
        zat[kk] = 1; fronta.push(kk);
      }
    }
    for (const i of hrazBunky) if (zat[i] === 2) zat[i] = 0;
    if (preliv) varovani.push('hladina je výš než sedlo na rozvodnici - voda by přetékala do vedlejšího údolí, zátopa je oříznutá rozvodnicí');
    if (orez) varovani.push(`zátopa přes ${maxBunek} buněk - výpočet zastaven, výsledek je dolní odhad`);
    if (!uzavira) varovani.push('zátopa je omezená jen rozvodnicí, ne hrází');
    if (n < J.MIN_BUNEK_ZATOPY) {
      for (const i of J.maskaNaBunky(zat)) zat[i] = 0;
      varovani.push(`zátopa v DMR jen ${n} buněk po 25 m² - údolí je pro 5 m rastr moc úzké, použit odhad z příčného profilu`);
      return tunProfil('údolí užší, než rozliší DMR 5G (5 m)');
    }
    return Object.assign(vysl, {
      typ: 'nadrz', orientacni: true, n_bunek: n, pod_rozlisenim: n < 8,
      objem_m3: objem, plocha_ha: n * J.plochaB / 1e4, hloubka_max_m: hloubkaMax, hloubka_prumer_m: n ? objem / (n * J.plochaB) : 0,
      maska: zat, zatopene_vyuziti_ha: J.statBunek(J.maskaNaBunky(zat)).vyuziti_ha, preliv_mimo_povodi: preliv,
      pozn: 'zatopení terénu DMR 5G (5 m buňky) pod hladinou za hrází kolmou na tok ČÚZK, souvisle s hrází, uvnitř povodí hráze; bez ztrát, koryto užší než buňka v objemu chybí; orientační',
    });
  };
  J.maskaNaBunky = function (maska) { const o = []; for (let i = 0; i < maska.length; i++) if (maska[i]) o.push(i); return o; };

  // ---------------------------------------------------------------- vykresleni do mapy (Web Mercator)
  // vraci {imageData, bounds:[[latS,lonW],[latN,lonE]]} pro L.imageOverlay; barva(i) -> [r,g,b,a] nebo null
  J.obrazek = function (barva, bboxLonLat, sirkaPx) {
    const [lonW, latS, lonE, latN] = bboxLonLat;
    const merc = la => Math.log(Math.tan(Math.PI / 4 + la * Math.PI / 360));
    const mS = merc(latS), mN = merc(latN);
    const w = sirkaPx || 1024, h = Math.round(w * (mN - mS) / ((lonE - lonW) * Math.PI / 180));
    const data = new Uint8ClampedArray(w * h * 4);
    for (let py = 0; py < h; py++) {
      const m = mN - (py + 0.5) / h * (mN - mS);
      const lat = (2 * Math.atan(Math.exp(m)) - Math.PI / 2) * 180 / Math.PI;
      for (let px = 0; px < w; px++) {
        const lon = lonW + (px + 0.5) / w * (lonE - lonW);
        const b = J.lonLatNaBunku(lon, lat);
        if (!b) continue;
        const c = barva(b.i);
        if (!c) continue;
        const o = (py * w + px) * 4;
        data[o] = c[0]; data[o + 1] = c[1]; data[o + 2] = c[2]; data[o + 3] = c[3] == null ? 255 : c[3];
      }
    }
    return { width: w, height: h, data, bounds: [[latS, lonW], [latN, lonE]] };
  };
  // obal masky v lon/lat (pro bbox obrazku)
  J.obalMasky = function (maska, okrajM) {
    let r0 = J.nrow, r1 = -1, c0 = J.ncol, c1 = -1;
    for (let i = 0; i < maska.length; i++) if (maska[i]) { const r = Math.floor(i / J.ncol), c = i - r * J.ncol; if (r < r0) r0 = r; if (r > r1) r1 = r; if (c < c0) c0 = c; if (c > c1) c1 = c; }
    if (r1 < 0) return null;
    const o = okrajM || 0;
    const a = J.xyNaLonLat(J.x0 + c0 * J.krok - o, J.y1 - (r1 + 1) * J.krok - o), b = J.xyNaLonLat(J.x0 + (c1 + 1) * J.krok + o, J.y1 - r0 * J.krok + o);
    return [Math.min(a[0], b[0]), Math.min(a[1], b[1]), Math.max(a[0], b[0]), Math.max(a[1], b[1])];
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = J;
  global.Jadro = J;
})(typeof window !== 'undefined' ? window : globalThis);
