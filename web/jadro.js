/* jadro.js - vypocetni jadro aplikace Korycany voda (faze 3), v0.1, 19. 10. 2026
 *
 * Pracuje nad rastry z data/web/ (09_balicek_web.py): mrizka S-JTSK 5 m, pasma v PNG.
 * Bez knihoven. V prohlizeci: Jadro.nacti('data/web/') -> Promise. V node: Jadro.nactiZPoli(info, {pasmo: Uint8Array|Uint16Array}).
 *
 * Metody (zdroje viz docs/JADRO.md):
 *  - SCS-CN: Q = (P - Ia)^2 / (P - Ia + S), S = 25400/CN - 254 [mm], Ia = 0,2 S (Janecek a kol. 2012, kap. 2; USDA TR-55)
 *  - prevod CN na IPS I / III: standardni vztahy SCS (Hawkins; NEH-4): CN1 = 4,2 CN / (10 - 0,058 CN), CN3 = 23 CN / (10 + 0,13 CN)
 *  - povodi bodu: zpetne sledovani D8 (smer.png)
 *  - nadrz: zatopeni bunek pod zvolenou hladinou, souvisle s hrazi a jen uvnitr povodi bodu (zjednoduseni, bez tvaru hraze)
 * Vsechny vysledky jsou orientacni (model pro osvetu), viz docs/00-instrukce-projektu.md.
 */
(function (global) {
  'use strict';

  const J = { info: null, p: {}, verze: '0.1' };

  // ---------------------------------------------------------------- nacteni
  J.nactiZPoli = function (info, pasma) {
    J.info = info;
    J.p = pasma;
    const m = info.mrizka;
    J.ncol = m.ncol; J.nrow = m.nrow; J.krok = m.krok_m; J.x0 = m.x0; J.y1 = m.y1; J.plochaB = m.plocha_bunky_m2;
    return J;
  };

  // prohlizec: PNG -> typovana pole pres canvas
  J.nacti = async function (base) {
    const info = await (await fetch(base + 'rastr.json')).json();
    const pasma = {};
    await Promise.all(Object.entries(info.pasma).map(async ([nazev, p]) => {
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
    return J.nactiZPoli(info, pasma);
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
    let cnS = 0, cnN = 0, skS = 0, skN = 0, Qsum = 0, Qn = 0;
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
      if (P != null && cn) { Qsum += J.scsCN(P, J.cnProIPS(cn, ips || 2)); Qn++; }
    }
    st.plocha_ha = st.n_platnych * J.plochaB / 1e4;
    st.cn_vazene = cnN ? cnS / cnN : null;
    st.sklon_prumer_deg = skN ? skS / skN : null;
    st.sklon_prumer_pct = skN ? Math.tan(st.sklon_prumer_deg * Math.PI / 180) * 100 : null;
    st.tok_prochazi = st.akumulace_max * J.plochaB >= 0.25e6;   // udolnice >= 0,25 km2 (jako 02_rozvodnice.py)
    if (P != null && Qn) {
      const Q_mm = Qsum / Qn;
      st.odtok = { P_mm: P, ips: ips || 2, Q_mm, objem_m3: Q_mm / 1000 * Qn * J.plochaB, koef: Q_mm / P, pozn: 'SCS-CN po bunkach, Ia = 0,2 S' };
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
  J.povodiBunky = function (i0, maxBunek) {
    const max = maxBunek || 2e6;
    const maska = new Uint8Array(J.ncol * J.nrow);
    const fronta = new Int32Array(Math.min(max, J.ncol * J.nrow));
    let q0 = 0, q1 = 0;
    fronta[q1++] = i0; maska[i0] = 1;
    const smer = J.p.smer;
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
    const i0 = J.prichytKToku(b.i, polomerM == null ? 50 : polomerM);
    const pov = J.povodiBunky(i0);
    const st = J.statBunek(pov.bunky, P, ips);
    st.plocha_km2 = st.plocha_ha / 100;
    st.uzaver_lonlat = J.xyNaLonLat(...J.bunkaNaXY(i0));
    st.orez_okrajem = pov.orez || J.naOkraji(pov.maska);
    return { stat: st, maska: pov.maska, bunky: pov.bunky, uzaver: i0 };
  };
  // povodi sahajici k okraji rastru je neuplne
  J.naOkraji = function (maska) {
    for (let c = 0; c < J.ncol; c++) if (maska[c] || maska[(J.nrow - 1) * J.ncol + c]) return true;
    for (let r = 0; r < J.nrow; r++) if (maska[r * J.ncol] || maska[r * J.ncol + J.ncol - 1]) return true;
    return false;
  };

  // ---------------------------------------------------------------- nadrz / poldr
  // hraz v bode (lon,lat) prichycenem k toku, vyska hraze h m nad terenem; zatopi bunky v povodi bodu souvisle s hrazi pod hladinou
  J.nadrz = function (lon, lat, vyskaHrazeM, polomerM) {
    const b = J.lonLatNaBunku(lon, lat);
    if (!b) return null;
    const i0 = J.prichytKToku(b.i, polomerM == null ? 30 : polomerM);
    const pov = J.povodiBunky(i0);
    const z0 = J.vyska(i0), hl = z0 + vyskaHrazeM;
    const zat = new Uint8Array(J.ncol * J.nrow);
    const fronta = [i0]; zat[i0] = 1;
    let objem = 0, n = 0, hloubkaMax = 0;
    while (fronta.length) {
      const i = fronta.pop();
      const z = J.vyska(i);
      const d = hl - z; objem += d * J.plochaB; n++; if (d > hloubkaMax) hloubkaMax = d;
      const row = Math.floor(i / J.ncol), col = i - row * J.ncol;
      for (const [dc, dr] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const r = row + dr, c = col + dc;
        if (r < 0 || c < 0 || r >= J.nrow || c >= J.ncol) continue;
        const k = r * J.ncol + c;
        if (zat[k] || !pov.maska[k] || !J.platna(k)) continue;
        const zk = J.vyska(k);
        if (zk >= hl) continue;
        zat[k] = 1; fronta.push(k);
      }
    }
    const pStat = J.statBunek(pov.bunky);
    return { hraz: i0, hraz_lonlat: J.xyNaLonLat(...J.bunkaNaXY(i0)), kota_dna: z0, hladina: hl, vyska_hraze_m: vyskaHrazeM,
      objem_m3: objem, plocha_ha: n * J.plochaB / 1e4, hloubka_max_m: hloubkaMax, hloubka_prumer_m: n ? objem / (n * J.plochaB) : 0,
      povodi_km2: pStat.plocha_ha / 100, maska: zat, zatopene_vyuziti_ha: J.statBunek(J.maskaNaBunky(zat)).vyuziti_ha,
      pozn: 'zatopeni terenu pod hladinou, bez objemu hraze a bez ztrat; orientacni' };
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
