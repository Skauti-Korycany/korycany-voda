// test_jadro.js - testy jadra nad skutecnym balickem data/web (node: npm i pngjs; node web/test_jadro.js)
const fs = require('fs'), path = require('path'), { PNG } = require('pngjs');
const J = require('./jadro.js');
const base = path.join(__dirname, '..', 'data', 'web');
const info = JSON.parse(fs.readFileSync(path.join(base, 'rastr.json'), 'utf8'));
const pasma = {};
for (const [n, p] of Object.entries(info.pasma)) {
  const png = PNG.sync.read(fs.readFileSync(path.join(base, p.soubor)));
  const N = png.width * png.height;
  if (p.bity === 16) { const o = new Uint16Array(N); for (let i = 0; i < N; i++) o[i] = (png.data[i * 4] << 8) | png.data[i * 4 + 1]; pasma[n] = o; }
  else { const o = new Uint8Array(N); for (let i = 0; i < N; i++) o[i] = png.data[i * 4]; pasma[n] = o; }
}
J.nactiZPoli(info, pasma);
let chyb = 0;
function ok(nazev, podminka, detail) { console.log((podminka ? 'OK  ' : 'FAIL') + ' ' + nazev + (detail ? '  [' + detail + ']' : '')); if (!podminka) chyb++; }
const blizko = (a, b, tol) => Math.abs(a - b) <= tol * Math.abs(b);

// 1. souradnice proti pyproj
for (const kb of info.prevod.kontrolni_body) {
  const [X, Y] = J.lonLatNaXY(...kb.lonlat); const [lo, la] = J.xyNaLonLat(...kb.xy5514);
  ok('prevod lonlat->xy', Math.hypot(X - kb.xy5514[0], Y - kb.xy5514[1]) < 0.05, `${(Math.hypot(X - kb.xy5514[0], Y - kb.xy5514[1]) * 1000).toFixed(1)} mm`);
  ok('prevod xy->lonlat', Math.abs(lo - kb.lonlat[0]) < 1e-6 && Math.abs(la - kb.lonlat[1]) < 1e-6);
}

// 2. uzemi modelu z povodi.geojson vs cn_info.json
const pov = JSON.parse(fs.readFileSync(path.join(base, '..', 'povodi.geojson'), 'utf8'));
const cnInfo = JSON.parse(fs.readFileSync(path.join(base, '..', 'cn_info.json'), 'utf8'));
const uz = pov.features.find(f => f.properties.typ === 'uzemi_modelu');
const geom = uz.geometry.type === 'Polygon' ? [uz.geometry.coordinates] : uz.geometry.coordinates;
let bunky = [];
for (const poly of geom) bunky = bunky.concat(J.bunkyPolygonu(poly[0], poly.slice(1)));
const st = J.statBunek(bunky, 40, 2);
const ref = cnInfo.uzemi_modelu;
ok('uzemi modelu plocha', blizko(st.plocha_ha, ref.plocha_ha, 0.01), `${st.plocha_ha.toFixed(1)} vs ${ref.plocha_ha} ha`);
ok('uzemi modelu CN', Math.abs(st.cn_vazene - ref.cn_vazene) < 0.3, `${st.cn_vazene.toFixed(1)} vs ${ref.cn_vazene}`);
ok('uzemi modelu odtok P40', blizko(st.odtok.objem_m3, ref.odtok.P40mm.objem_m3, 0.03), `${Math.round(st.odtok.objem_m3)} vs ${ref.odtok.P40mm.objem_m3} m3, Q ${st.odtok.Q_mm.toFixed(2)} mm`);
const les = [4, 41, 42, 43].reduce((s, k) => s + (st.vyuziti_ha[k] || 0), 0);
ok('uzemi modelu les ~50 %', blizko(les / st.plocha_ha, 0.50, 0.03), `${(100 * les / st.plocha_ha).toFixed(1)} %`);
ok('uzemi modelu HSP odhad', Math.abs(100 * st.hsp_odhad_ha / st.plocha_ha - ref.podil_hsp_odhad_pct) < 1, `${(100 * st.hsp_odhad_ha / st.plocha_ha).toFixed(1)} vs ${ref.podil_hsp_odhad_pct} %`);
console.log('   sklon prumer', st.sklon_prumer_deg.toFixed(1), 'deg; vyska', st.vyska_min, '-', st.vyska_max, 'm; tok prochazi', st.tok_prochazi);

// 3. povodi bodu: hlasny profil Stribrnik -> ~4,2 km2 (povodi.geojson id 2)
const body = JSON.parse(fs.readFileSync(path.join(base, '..', 'rozvodnice_body.json'), 'utf8'));
const refS = pov.features.find(f => f.properties.typ === 'sidlo' && f.properties.id === 2).properties;
const s2 = body.sidla.find(s => s.id === 2);
const ll = J.xyNaLonLat(...s2.xy5514);
const t0 = Date.now();
const p2 = J.povodiBodu(ll[0], ll[1], s2.polomer_m, 40, 2);
ok('povodi Stribrnik plocha', blizko(p2.stat.plocha_km2, refS.plocha_celkem_km2, 0.02), `${p2.stat.plocha_km2.toFixed(2)} vs ${refS.plocha_celkem_km2} km2, ${Date.now() - t0} ms`);
const refCN2 = cnInfo.dilci_povodi['Koryčany (Stříbrník, ř. km 1,07)'];
ok('povodi Stribrnik CN', Math.abs(p2.stat.cn_vazene - refCN2.cn_vazene) < 0.5, `${p2.stat.cn_vazene.toFixed(1)} vs ${refCN2.cn_vazene}`);
ok('povodi Stribrnik neorezano', !p2.stat.orez_okrajem);

// 4. SCS-CN zname hodnoty: CN 72, P 40 -> S 98.8, Ia 19.8, Q = 20.2^2/(20.2+98.8) = 3.43
ok('SCS-CN vzorec', Math.abs(J.scsCN(40, 72) - 3.43) < 0.02, J.scsCN(40, 72).toFixed(2));
ok('SCS-CN pod Ia = 0', J.scsCN(10, 72) === 0);
ok('CN IPS III > IPS II > IPS I', J.cnProIPS(72, 3) > 72 && J.cnProIPS(72, 1) < 72, `${J.cnProIPS(72, 1).toFixed(1)} / 72 / ${J.cnProIPS(72, 3).toFixed(1)}`);

// 4b. vazeni pres tvary - priklad Stasov z metodiky CVUT 2023 (kap. 2.6, tab. 7): CN2 81, CN3 90,7, P100 60,2 mm, 5,7 ha
ok('CN3 jako metodika 2023 (Stasov 81 -> 90,7)', Math.abs(J.cnProIPS(81, 3) - 90.7) < 0.05, J.cnProIPS(81, 3).toFixed(2));
const V2 = J.scsCN(60.2, 81) / 1000 * 57000, V3 = J.scsCN(60.2, J.cnProIPS(81, 3)) / 1000 * 57000;
ok('Stasov V_CN2 = 1232 m3', Math.abs(V2 - 1232) < 3, V2.toFixed(0));
ok('Stasov V_CN3 = 2127 m3 (metodika pocita s CN3 zaokrouhlenym na 90,7)', Math.abs(V3 - 2127) < 8, V3.toFixed(0));
// tab. 7: A, B jen CN2; C, D, E 75/25; F 50/50 -> qAPI volime tak, aby to tab. 6 dalo
const stasovPodil = { A: 21.4, B: 33.5, C: 15.4, D: 20.2, E: 9.1, F: 0.4 }, stasovQ = { A: 0.1, B: 0.1, C: 0.3, D: 0.3, E: 0.3, F: 0.5 };
const Vv = J.odtokVazeny({ P_mm: 60.2, Q_mm: J.scsCN(60.2, 81), objem_m3: V2, Q_mm_cn3: J.scsCN(60.2, 90.7), objem_m3_cn3: V3 }, stasovPodil, stasovQ);
ok('Stasov V_vysl = 1333,8 m3', Math.abs(Vv.objem_m3 - 1333.8) < 3, `${Vv.objem_m3.toFixed(1)} m3, vaha CN3 ${Vv.vaha_cn3.toFixed(3)}`);
// Korycany N10: podily a qAPI z data/navrhove_srazky.json
const NS = JSON.parse(fs.readFileSync(path.join(base, '..', 'navrhove_srazky.json'), 'utf8'));
const w3k = J.vahaCN3(NS.podil_tvaru_pct.N10, NS.qAPI);
ok('Korycany N10 vaha CN3 = 0,203 (D 0,20 a E 0,40 lezi na hranici intervalu, bereme nizsi vahu)', Math.abs(w3k - 0.203) < 0.002, w3k.toFixed(3));
const st10 = J.statBunek(bunky, NS.uhrny_6h_mm.N10, 2), v10 = J.odtokVazeny(st10.odtok, NS.podil_tvaru_pct.N10, NS.qAPI);
ok('uzemi modelu N10 vazeny odtok mezi CN2 a CN3', v10.objem_m3 > st10.odtok.objem_m3 && v10.objem_m3 < st10.odtok.objem_m3_cn3, `${Math.round(st10.odtok.objem_m3)} < ${Math.round(v10.objem_m3)} < ${Math.round(st10.odtok.objem_m3_cn3)} m3 (Q ${v10.Q_mm.toFixed(1)} mm, koef ${v10.koef.toFixed(2)})`);

// 5. nadrz: hraz 3 m na Stribrniku ~ 600 m nad profilem
const [X2, Y2] = s2.xy5514;
const n1 = J.nadrz(...J.xyNaLonLat(X2 + 100, Y2 - 500), 3, 60);
ok('nadrz objem > 0 a hloubka <= 3 m', n1 && n1.objem_m3 > 0 && n1.hloubka_max_m <= 3.0001, n1 && `${Math.round(n1.objem_m3)} m3, ${n1.plocha_ha.toFixed(2)} ha, povodi ${n1.povodi_km2.toFixed(2)} km2, dno ${n1.kota_dna} m`);
const n2 = J.nadrz(...J.xyNaLonLat(X2 + 100, Y2 - 500), 5, 60);
ok('nadrz 5 m > 3 m', n2.objem_m3 > n1.objem_m3, `${Math.round(n2.objem_m3)} m3`);

// 6. obrazek masky povodi
const bbox = J.obalMasky(p2.maska, 50);
const t1 = Date.now();
const im = J.obrazek(i => p2.maska[i] ? [30, 100, 200, 120] : null, bbox, 512);
let nenul = 0; for (let i = 3; i < im.data.length; i += 4) if (im.data[i]) nenul++;
ok('obrazek masky', nenul > 0.05 * im.width * im.height, `${im.width}x${im.height}, ${(100 * nenul / (im.width * im.height)).toFixed(0)} % pokryto, ${Date.now() - t1} ms`);

console.log(chyb ? `\n${chyb} CHYB` : '\nVSE OK');
process.exit(chyb ? 1 : 0);
