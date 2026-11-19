# Školní meteostanice na Raspberry Pi (ZŠ Koryčany) - návrh součástek

Stav: 19. 11. 2026, verze 1. Kód zatím ne. Ceny a dostupnost ✅ ověřeny online 19. 11. 2026 (rpishop.cz přes API obchodu, laskakit.cz z výsledků vyhledávání), pokud není uvedeno jinak.

Značky: ✅ ověřeno online v této relaci | 📄 doložený zdroj, originál nečten | 🤔 odhad | 💻 z paměti, neověřeno | ⏳ zdroj starší 12 měsíců.

## 1. Zadání a vstupy od uživatele (19. 11.)

- Rozpočet Doporučené varianty 5 000 - 10 000 Kč.
- U místa stanice **není 230 V**, je školní Wi-Fi. Napájení baterií / powerbankou.
- Škola má pájku a někoho, kdo s ní umí. Přesto vše navrženo bez pájení; výjimky označeny **[pájení]**.
- Na Pi poběží současně odesílač (hodinové průměry do sdílené tabulky) a webová stránka žáků.

## 2. Hlavní rozhodnutí

**Raspberry Pi Zero 2 WH** (559 Kč, rpishop, skladem ✅). Důvody:
- Spotřeba. Bez 230 V je energie hlavní omezení. Zero 2 W bere v klidu s Wi-Fi zhruba 0,6-0,8 W 💻, Pi 4 kolem 2,7 W a Pi 5 kolem 3 W 💻. Pi 4/5 by na baterii a malý solár nevydržely.
- Výkon stačí: 4 jádra, 512 MB RAM. Unese odesílač i jednoduchou webovou stránku žáků (Python/Flask). **Neunese** těžké nástroje typu Grafana + InfluxDB 💻. To je třeba říct žákům předem.
- Varianta "WH" má připájenou lištu GPIO, takže žáci nemusí pájet (Zero 2 W bez lišty je o 50 Kč levnější, ale vyžaduje **[pájení]** a teď je jen na objednávku).
- Pi Zero nemá analogové vstupy ani hodiny reálného času, proto převodník ADS1115 a modul DS3231.

**Bez pájení:** "Modul se šroubovými svorkami pro Raspberry Pi" (rpishop, 529 Kč ✅) vyvede všech 40 pinů na šroubovací svorky. Žáci zapojují šroubovákem. Čidla s teplotou, vlhkostí, tlakem a osvitem jsou na sběrnici I2C s konektory Qwiic / STEMMA QT / μŠup (zacvaknout kabel).

**Napájení bez 230 V - otevřeně:**
- Denní spotřeba: 0,7 W × 24 h = asi **17 Wh/den**, počítat s rezervou 20 Wh 🤔.
- Powerbanka 20 000 mAh (74 Wh jmenovitě) dá po ztrátách přeměny na 5 V asi 45-50 Wh, tedy **2-3 dny** 🤔.
- Solární panel 10 W v létě vyrobí asi 30-40 Wh/den, v prosinci jen 5-10 Wh/den 🤔. **Od listopadu do února solár 10 W nestačí.**
- Řešení v návrhu: solární modul s články 18650 + v zimě výměna nabité powerbanky 2× týdně do vstupu USB-C modulu (žákovská služba). Ve škole se powerbanka nabíjí ze zásuvky.
- Pokud by výměna powerbanek nefungovala, spolehlivější je **varianta B**: Pi Zero uvnitř školy na 230 V a venku úsporný Raspberry Pi Pico 2 W (209 Kč, rpishop ✅) s čidly, který posílá data přes Wi-Fi do Pi. Pico spotřebuje zlomek energie, malý solár ho uživí i v zimě 🤔. Cena: víc programování (dva programy místo jednoho).
- Pozor: **Li-ion články se nesmí nabíjet pod 0 °C** 💻. Solární modul Waveshare podle popisu v obchodě ochranu proti nabíjení v mrazu neuvádí. Baterii mít v krabici u zdi budovy, ne na stožáru; v mrazu počítat s výpadky.

**Wi-Fi:** Zero 2 W umí jen 2,4 GHz a má malou anténu na desce. Dosah od budovy přes zeď 🤔 10-30 m. Krabice musí být **plastová** (kov stíní). Před nákupem změřit signál mobilem v místě stanice (aplikace typu Wi-Fi analyzátor; lepší než -70 dBm). Když je slabý: opakovač Wi-Fi uvnitř u okna.

## 3. Tři varianty

Sloupec P/V = povinná / volitelná. "nedohledal jsem" = cenu jsem neověřil, v součtu je odhad 🤔 a přesný hledaný výraz.

### 3.1 Základ (nejlevnější funkční: srážky, teplota a vlhkost vzduchu, půda)

Napájení: 2 powerbanky na střídačku (jedna venku, druhá se nabíjí).

| součástka | co měří / k čemu | obchod | odkaz | cena s DPH | dostupnost 19. 11. | P/V |
|---|---|---|---|---|---|---|
| Raspberry Pi Zero 2 WH | počítač, Wi-Fi, odesílač + web žáků | rpishop | [odkaz](https://rpishop.cz/535843/raspberry-pi-zero-2-w-s-pripajenym-gpio-headerem/) | 559 Kč ✅ | skladem | P |
| microSD karta s vysokou výdrží 32 GB | systém a data | jiný obchod | nedohledal jsem; hledat "SanDisk High Endurance 32GB SDSQQNR-032G" (rpishop má jen běžné karty, 32GB teď nedostupná) | ~300 Kč 🤔 | - | P |
| Modul se šroubovými svorkami pro Raspberry Pi | zapojení bez pájení | rpishop | [odkaz](https://rpishop.cz/automatizacni-karty/3476-modul-se-sroubovymi-svorkami-pro-raspberry-pi.html) | 529 Kč ✅ | skladem | P |
| MS-WH-SP-RG srážkoměr | srážky, **0,2794 mm na překlop** ✅ (popis obchodu), jazýčkový kontakt, kabel 2,9 m s RJ11 | laskakit (rpishop srážkoměr nemá) | [odkaz](https://www.laskakit.cz/ms-wh-sp-rg-srazkomer/) | 498 Kč ✅ | skladem | P |
| Adafruit Sensirion SHT45 (PTFE, STEMMA QT) | teplota ±0,1 °C, vlhkost ±1 % (20-70 %) ✅ popis; PTFE membrána proti vodě a prachu | rpishop | [odkaz](https://rpishop.cz/715896/adafruit-sensirion-sht45-senzor-teploty-a-vlhjosti-s-ptfe/) | 389 Kč ✅ | skladem (2 ks) | P |
| JST-SH 4PIN kabel 500 mm (Qwiic, STEMMA QT) | propojení čidel I2C | rpishop | [odkaz](https://rpishop.cz/676099/jst-sh-4pin-kabel-500-mm-qwiic-stemma-qt-qw-st/) | 85 Kč ✅ × 2 = 170 Kč | skladem | P |
| μŠup / STEMMA QT / Qwiic kabel - dupont samec | první čidlo do šroubových svorek | laskakit (rpishop nemá) | [odkaz](https://www.laskakit.cz/--sup--stemma-qt--qwiic-jst-sh-4-pin-kabel-dupont-samec/) | 25,80 Kč ✅ | skladem | P |
| RTC DS3231 AT24C32 | hodiny při výpadku Wi-Fi | rpishop | [odkaz](https://rpishop.cz/rtc/6461-rtc-hodiny-realneho-casu-s-pametovym-modulem-pro-arduino-ds3231-at24c32-iic.html) | 115 Kč ✅ | skladem | P |
| Soldered kapacitní senzor vlhkosti půdy | vlhkost půdy, analogový výstup, kapacitní (bez koroze) | laskakit | [odkaz](https://www.laskakit.cz/soldered-kapacitni-senzor-vlhkosti-pudy/) | 148 Kč ✅ | skladem | P |
| 4kanálový I2C ADC převodník pro Raspberry Pi, ADS1115 | Pi nemá analogové vstupy (půda, později směrovka) | laskakit (rpishop ADS1115 nemá) | [odkaz](https://www.laskakit.cz/4-kanalovy-i2c-adc-prevodnik-pro-raspberry-pi--ads1115/) | 268 Kč ✅ | naskladní cca 25. 11. | P; možná **[pájení]** kolíkové lišty 🤔 |
| Vodotěsný teplotní senzor DS18B20, 3 m | teplota půdy (1-Wire) | rpishop | [odkaz](https://rpishop.cz/497710/produkt-23/) | 129 Kč ✅ | skladem | P |
| Rezistor 4,7 kΩ | pull-up pro DS18B20, do šroubových svorek | jiný obchod | nedohledal jsem; hledat "rezistor 4k7 0,25W" | ~5 Kč 🤔 | - | P |
| EMOS Powerbanka 20000 mAh, 10 W | napájení (2-3 dny) | rpishop | [odkaz](https://rpishop.cz/powerbanky/5240-emos-powerbanka-20000-mah-10-w.html) | 599 Kč ✅ | skladem (1 ks) | P |
| Gembird Powerbanka 10 000 mAh | druhá na výměnu (1-1,5 dne) | rpishop | [odkaz](https://rpishop.cz/powerbanky/5788-gembird-powerbanka-10-000-mah-cerna.html) | 379 Kč ✅ | skladem | P |
| Radiační kryt DIY | stínění teploměru | hobbymarket | nedohledal jsem; 6-8 bílých plastových podmisek pod květináč ø 20-25 cm + závitová tyč M6 | ~200 Kč 🤔 | - | P |
| Instalační krabice IP65 cca 200 × 150 × 100 mm, plast | elektronika venku | jiný obchod | nedohledal jsem (gme.cz načítá výsledky jen skriptem); hledat "krabice instalační IP65 ABS 200x150x100" | ~300 Kč 🤔 | - | P |
| Kabelové průchodky PG7 / PG9 (5-10 ks) | kabely do krabice bez zatékání | jiný obchod | nedohledal jsem; hledat "průchodka kabelová PG7 IP68" | ~100 Kč 🤔 | - | P |
| Stožár / držák | pozinkovaná trubka 2-3 m + objímky, nebo dřevěný kůl | hobbymarket | nedohledal jsem; hledat "trubka pozinkovaná 1 palec 3 m" | ~500 Kč 🤔 | - | P |
| Kabel USB-A - micro USB, vázací pásky, smršťovačky | drobný materiál | škola / jiný obchod | nedohledal jsem | ~150 Kč 🤔 | - | P |
| LaskaKit BME280 (μŠup) | tlak vzduchu (v krabici stačí) | laskakit | [odkaz](https://www.laskakit.cz/arduino-senzor-tlaku--teploty-a-vlhkosti-bme280/) | 228,20 Kč ✅ | skladem | V |

**Součet Základ:** ověřené povinné položky 3 808,80 Kč ✅ + odhady 🤔 ~1 555 Kč = **asi 5 400 Kč**. S tlakem (BME280) asi 5 600 Kč.

### 3.2 Doporučená (Základ + vítr, tlak, osvit, solár, koupený radiační kryt)

Změny proti Základu:

| součástka | co měří / k čemu | obchod | odkaz | cena s DPH | dostupnost 19. 11. | P/V |
|---|---|---|---|---|---|---|
| SparkFun Weather Meter Kit (SEN-15901): srážkoměr + anemometr + směrovka | srážky 0,2794 mm na překlop 💻, vítr (1 Hz = 2,4 km/h 💻), směr 16 poloh přes odpory 💻; vše bez napájení, jen spínače | cz.mouser.com (český web, sklad mimo ČR); rpishop ani laskakit sadu nemají | [hledání Mouser](https://cz.mouser.com/c/?q=SEN-15901) | ~1 670-1 700 Kč 📄 (z výpisu vyhledávače, stránku jsem nenačetl; ověřit, zda s DPH) | skladem 📄 | P, **nahrazuje** srážkoměr laskakit (-498 Kč) |
| LaskaKit BME280 (μŠup) | tlak | laskakit; rpishop má Adafruit BME280 za 529 Kč, ale starší verzi s lištou na **[pájení]** a bez Qwiic | [odkaz](https://www.laskakit.cz/arduino-senzor-tlaku--teploty-a-vlhkosti-bme280/) | 228,20 Kč ✅ | skladem | P |
| Adafruit VEML7700 Lux | osvit v luxech (náhrada záření, viz kap. 5) | rpishop | [odkaz](https://rpishop.cz/adafruit/4126-adafruit-veml7700-lux-i2c-svetelny-senzor.html) | 179 Kč ✅ | skladem | P |
| JST-SH 4PIN kabel 500 mm | další propojka I2C | rpishop | [odkaz](https://rpishop.cz/676099/jst-sh-4pin-kabel-500-mm-qwiic-stemma-qt-qw-st/) | 85 Kč ✅ | skladem | P |
| Kryt pro čidla meteostanice, 140 × 170 mm, plast (+ ocelová konzole) | radiační kryt, vnitřní prostor ø 62 × 120 mm | laskakit (rpishop nemá) | [odkaz](https://www.laskakit.cz/kryt-pro-cidla-meteostanice--140x170mm--plast/) | 1 228 Kč ✅ | skladem | P, **nahrazuje** DIY kryt (-200 Kč 🤔) |
| Waveshare Solar Power Manager modul (typ D) | MPPT nabíjení, panel 6-24 V, 3× 18650, výstup 5 V / 3 A, vstup USB-C pro powerbanku ✅ popis | rpishop | [odkaz](https://rpishop.cz/512386/waveshare-solar-power-manager-modul-typ-d/) | 379 Kč ✅ | skladem | P |
| Waveshare semi-flexibilní solární panel 18 V, 10 W (435 × 200 mm) | výroba energie | rpishop | [odkaz](https://rpishop.cz/540877/waveshare-semi-flexibilni-solarni-panel-z-polykrystalickeho-kremiku-18v-10w/) | 369 Kč ✅ | skladem | P |
| Nabíjecí baterie SONY VTC6 18650, 3000 mAh | 3 ks do solárního modulu (asi 1 den zálohy 🤔) | rpishop | [odkaz](https://rpishop.cz/18650/1462-sony-vtc6-baterie-18650-3000mah-30a.html) | 199 Kč ✅ × 3 = 597 Kč | skladem (počet neuveden) | P |
| Druhý kapacitní senzor půdy + druhý DS18B20 | druhá hloubka (10 a 30 cm) | laskakit / rpishop | viz Základ | 148 + 129 = 277 Kč ✅ | skladem | V |

Powerbanky ze Základu zůstávají pro zimu (vstup USB-C solárního modulu).

**Součet Doporučená:** ověřené povinné položky 8 046 Kč (Mouser 📄 1 670 Kč v tom) + odhady 🤔 ~1 355 Kč = **asi 9 400 Kč**. S volitelnou druhou hloubkou půdy asi 9 650 Kč.

### 3.3 Rozšířená (Doporučená + robustnější půda, kontrolní čidla, výdržnější karta)

| součástka | co měří / k čemu | obchod | odkaz | cena s DPH | dostupnost 19. 11. | P/V |
|---|---|---|---|---|---|---|
| Multifunkční půdní sonda ZTS-3000-TR-WS-N01 (RS485) | vlhkost a teplota půdy, průmyslové pouzdro | laskakit | [odkaz](https://www.laskakit.cz/multifunkcni-pudni-sonda-zts-3000-tr-ws-n01--teplota-a-vlhkost-rs485/) | 550,20 Kč ✅ | skladem | P; **napájecí napětí nedohledal jsem** (stránka mi byla zablokována), u podobných sond bývá 5-30 V 💻 |
| Waveshare převodník USB na RS485 | připojení sondy k Pi (+ redukce micro USB OTG) | rpishop | [odkaz](https://rpishop.cz/datove-redukce/4651-waveshare-prumyslovy-prevodnik-usb-na-rs485.html) | 239 Kč ✅ | na objednávku | P |
| Převodník USB na microUSB OTG Shim | USB do Pi Zero | rpishop | [odkaz](https://rpishop.cz/datove-redukce/4365-prevodnik-usb-na-microusb-otg-shim.html) | 69 Kč ✅ | skladem | P |
| Kingston 8GB microSDHC Industrial (pSLC) | výrazně odolnější karta | rpishop | [odkaz](https://rpishop.cz/prodej-ukoncen/5214-kingston-8gb-microsdhc-industrial-uhs-i-karta-adp.html) | 1 179 Kč ✅ | skladem, prodej končí | P, **nahrazuje** High Endurance |
| LaskaKit Outdoor Meteo THP SHT40 + BMP280 | druhé čidlo pro kontrolu prvního (žáci porovnávají) | laskakit | [odkaz](https://www.laskakit.cz/laskakit-outdoor-meteo-thp-senzor-sht40-bmp280/) | 366,20 Kč ✅ | skladem | V |
| MS-WH-SP-RG srážkoměr (druhý) | kontrola srážkoměru, náhradní díl | laskakit | [odkaz](https://www.laskakit.cz/ms-wh-sp-rg-srazkomer/) | 498 Kč ✅ | skladem | V |
| Druhý kapacitní senzor půdy + DS18B20 | druhá hloubka | viz výše | | 277 Kč ✅ | skladem | P |

**Součet Rozšířená:** Doporučená ~9 400 Kč + 550,20 + 239 + 69 + (1 179 - 300 🤔) + 277 = **asi 11 400 Kč**, s volitelnými kontrolními čidly asi **12 300 Kč**.

## 4. Hotová stanice pro srovnání

- Konkrétní cenu modelů Ecowitt WS2910, WS3900, GW1101 v Kč **jsem nedohledal** (zbozi.cz a heureka.cz z mého prostředí nejdou). Hledat: "Ecowitt WS2910" na zbozi.cz.
- Nalezeno: **Ecowitt WS90** (prodávaná i jako Shelly PbS Ecowitt WS90, 7 v 1: ultrazvukový vítr, piezo srážky, teplota, vlhkost, osvit, UV) za **4 949 - 6 272 Kč** 📄 (zbozi.cz, výpis vyhledávače). K připojení na Wi-Fi potřebuje bránu (GW1100 / GW2000), její cenu jsem nedohledal.

| | DIY na Pi | Ecowitt |
|---|---|---|
| cena | 5 400 - 12 300 Kč | asi 6 000-8 000 Kč s bránou 🤔 |
| srážky | člunkový, 0,28 mm, kalibrovatelný | WS90 má piezo snímač (bez pohyblivých dílů), u slabých dešťů méně přesný 💻 |
| učení | žáci staví, zapojují, programují, kalibrují | jen montáž a aplikace |
| data | vlastní, v jakémkoli formátu, i odesílač | přes cloud Ecowitt; místní rozhraní existuje 💻 |
| otevřenost | vše viditelné a opravitelné | uzavřený hardware, opravy výměnou dílu |
| spolehlivost | závisí na údržbě, první rok ladění | hotová, odladěná, vlastní solár a baterie |
| půda | ano | jen s dalšími čidly Ecowitt 💻 |

Shrnutí: Ecowitt dá dřív spolehlivá data a méně starostí, ale škola přijde o hlavní smysl projektu (žáci rozumí, z čeho číslo vzniklo) a o přímou kontrolu nad daty.

## 5. Co levná čidla neumí (záření pro FAO-56)

- Penman-Monteith potřebuje **globální záření v W/m²** (nebo MJ/m²/den). Měří se pyranometrem (cena v tisících Kč, konkrétní nabídku jsem nehledal).
- VEML7700 měří **osvětlení v luxech** (vážené citlivostí oka). Přepočet je jen hrubý: pro přímé slunce asi 1 W/m² ≈ 100-120 lx 💻; pod mraky se poměr mění. Chyba přepočtu 🤔 20 % a víc. Čidlo navíc musí být venku, vodorovně, pod průhledným krytem, který časem zmatní.
- Pro výpar v aplikaci proto **dál platí sluneční svit ČHMÚ** (Staré Město / Kroměříž / Holešov). Osvit ze školy poslouží žákům k pochopení (oblačnost, délka dne) a k porovnání.
- Vítr: aplikace počítá s větrem ve 2 m (přepočet z 10 m). Anemometr na školním dvoře ve 2-4 m mezi budovami ukáže **slabší a nárazovitější vítr** než stanice ČHMÚ. Pro FAO-56 použitelné jen orientačně.

## 6. Umístění (zjednodušené zásady WMO pro školní dvůr)

Zdroj zásad: WMO Guide to Instruments and Methods of Observation (WMO-No. 8) 💻 (originál v této relaci nečten).

- **Plocha:** nízká tráva (posekaná), ne asfalt, štěrk ani střecha. Nezalévat okolí čidel půdy.
- **Teplota a vlhkost:** v radiačním krytu ve výšce **1,25-2 m** nad trávou 💻. Ne u zdi, ne nad tmavou plochou.
- **Srážkoměr:** okraj nálevky vodorovně (vodováha na čidle), výška 0,5-1,5 m 💻. Překážky (budova, strom) ve vzdálenosti aspoň **2× jejich výšky**, lépe 4× 💻. Strom 8 m vysoký tedy aspoň 16 m daleko. Nic nad nálevkou.
- **Vítr:** co nejvýš a co nejdál od budov; ideál 10 m nad terénem je u školy nereálný. Prakticky: stožár 3-4 m na volné ploše. Do dat zapsat skutečnou výšku.
- **Osvit:** bez stínu po celý den, i v zimě (nízké slunce), vodorovně.
- **Půda:** čidla svisle do 10 cm (a 30 cm), na trávníku vedle stanice, bez stínu budovy. Zapsat typ půdy.
- **Krabice s elektronikou:** na stožáru pod radiačním krytem nebo u zdi (baterie a mráz, viz kap. 2). Kabel ke srážkoměru 2,9 m, I2C kabely krátké.
- **Bezpečnost:** v oploceném prostoru školy, mimo dosah na skok, ideálně v záběru kamery nebo z oken sborovny.

## 7. Schéma zapojení (pro učitele)

Všechno se šroubuje do svorkovnice na Pi. Čísla jsou fyzické piny lišty (1-40) a GPIO.

```
                 RASPBERRY PI ZERO 2 WH + svorkovnice
   pin 1  3,3 V  ----+----------------------+-----------------+
   pin 3  SDA (GPIO2) ---+                  |                 |
   pin 5  SCL (GPIO3) ---|-+                |                 |
   pin 9  GND   --------|-|-+              4,7 kΩ             |
                        | | |               |                 |
   SBĚRNICE I2C (4 dráty: 3,3 V, GND, SDA, SCL), čidla za sebou:
   [kabel Qwiic-dupont] -> SHT45 (0x44) -> BME280 (0x76/0x77) -> VEML7700 (0x10)
                        -> ADS1115 (0x48) -> DS3231 (0x68)
                             |  A0 = vlhkost půdy 10 cm
                             |  A1 = směrovka větru (s odporem 10 kΩ jako dělič)
                             |  A2 = vlhkost půdy 30 cm
                             |  A3 = napětí baterie (volitelně, dělič)
                                            |
   pin 7  GPIO4  -- 1-Wire: DS18B20 (žlutý data, červený 3,3 V, černý GND),
                    mezi GPIO4 a 3,3 V rezistor 4,7 kΩ (do svorek)
   pin 29 GPIO5  -- anemometr (2 dráty: GPIO5 a GND), každá otáčka = puls
   pin 31 GPIO6  -- srážkoměr (2 dráty: GPIO6 a GND), každý překlop = puls 0,2794 mm
   pin 39 GND    -- společná zem pro anemometr a srážkoměr

   NAPÁJENÍ: solární panel -> Solar Power Manager (3× 18650) -> USB 5 V -> micro USB "PWR" na Pi
             v zimě: nabitá powerbanka -> vstup USB-C Solar Power Manageru
```

Poznámky:
- Srážkoměr a anemometr jsou obyčejné spínače (jazýčkový kontakt). Pi je počítá jako přerušení na GPIO se zapnutým vnitřním pull-up odporem. Konektor RJ11 se odstřihne a dráty jdou do svorek. Který pár drátů je spínač, se zjistí multimetrem.
- I2C sběrnice: celková délka kabelů do ~1 m 💻. Proto krabice s Pi přímo pod radiačním krytem na stejném stožáru. Na delší vzdálenost potřeba převodník (nehledal jsem).
- Adresy I2C se nepřekrývají (uvedené výchozí podle popisů čidel ✅ u SHT45, ostatní 💻).
- Kapacitní čidlo půdy má elektroniku nahoře nechráněnou: horní část zalít / natřít (lak na elektroniku, smršťovačka), jinak do roka zkoroduje 💻.

## 8. Kapacitní vs odporové čidlo půdy

| | odporové (2 kovové hroty, např. HD-38 90,20 Kč, "Senzor vlhkosti půdy" 20,20 Kč na laskakit ✅) | kapacitní (Soldered 148 Kč ✅) | RS485 sonda (550,20 Kč ✅) |
|---|---|---|---|
| princip | proud mezi hroty | změna kapacity, kov není v kontaktu s půdou | kapacitní / FDR v pouzdře 💻 |
| koroze | **hroty zkorodují během týdnů až měsíců** (elektrolýza) 💻 | elektroda chráněná; slabé místo je nezalitá elektronika nahoře | pouzdro zalité, nejodolnější |
| přesnost | nízká, ovlivní ji i hnojivo (vodivost) | relativní (sucho - mokro), nutná kalibrace na místní půdu | lepší, výrobce udává % objemové vlhkosti 💻 |
| doporučení | **nekupovat** | Základ / Doporučená | Rozšířená |

Kalibrace kapacitního čidla (žáci): hodnota na vzduchu (0 %), ve sklenici vody (100 % "stupnice"), pak vzorek místní půdy vysušený a nasycený. Výsledek je "index vlhkosti", ne objemová vlhkost.

## 9. Rizika a nejistoty

- **Přesnost proti ČHMÚ:** amatérská čidla nejsou certifikovaná. Člunkový srážkoměr typicky podměřuje při silných přívalech (voda přetéká při překlápění) 💻 a při větru. Data z Koryčan budou přesto pro přívaly cennější než stanice 8-9 km daleko (viz `docs/MERENI.md`, bouřka 1. 8. 2026). Na webu označovat "školní měření, neověřeno".
- **Kalibrace srážkoměru (odměrný válec):**
  1. Změřit vnitřní rozměry vtokové plochy nálevky (pravítko, mm) a spočítat plochu A v cm².
  2. Do PET lahve s malým otvorem ve víčku nalít přesně V = 200 ml (odměrný válec). Lahev nechat **pomalu** kapat do nálevky (aspoň 10-15 min, simuluje déšť).
  3. Spočítat překlopy N. Odpovídající srážka v mm = V (cm³) / A (cm²) × 10. Konstanta = mm / N.
  4. Opakovat 3× a jednou rychleji (prudký déšť). Porovnat s 0,2794 mm. Rozdíl nad 5 % 🤔: zapsat novou konstantu do programu, nebo dorovnat seřizovacími šrouby člunku, pokud je čidlo má 💻.
  5. Kontrolně vedle stanice ruční srážkoměr (odměrná nádoba), žáci odečítají každé ráno v 7:00. Ruční srážkoměr jsem nehledal; hledat "srážkoměr ruční zahradní".
- **Zima:** člunkový srážkoměr sníh neměří (napadne, roztaje později, nebo zamrzne člunek). Data od prvního sněhu do tání označit jako nespolehlivá. Vyhřívání by spotřebovalo desítky W - na baterii nereálné.
- **Údržba (žákovská služba, 1× týdně):** vybrat listí a hmyz z nálevky (síťka proti listí), zkontrolovat vodováhu, otočit anemometr rukou, očistit kryt osvitu, vyměnit powerbanku (zima 2× týdně).
- **Co se rozbije nejdřív (zkušenost amatérů 💻):** napájení a SD karta (proto karta s vysokou výdrží a záloha obrazu systému), Wi-Fi výpadky, nezalitá elektronika půdního čidla, ložiska anemometru (1-3 roky), plast na UV (křehne po letech).
- **Baterie v mrazu:** Li-ion nenabíjet pod 0 °C; kapacita v mrazu klesá. Proto krabice u zdi a výměna powerbanek.
- **Vandalismus a zvířata:** stožár v oploceném prostoru, krabice na zámek nebo šrouby s neobvyklou hlavou. Ptáci sedají na srážkoměr (trn proti ptákům 💻).
- **Bezpečnost dat a osobních údajů:** do tabulky jen měřené hodnoty a čas, žádná jména žáků (pravidlo projektu).

## 10. Pro uživatele: co objednat a kde

- rpishop.cz: Pi Zero 2 WH, svorkovnice, SHT45, VEML7700, DS18B20, DS3231, kabely Qwiic, solární modul a panel, články 18650, powerbanky, (Rozšířená: RS485 převodník, OTG, Kingston Industrial).
- laskakit.cz (rpishop nemá nebo má jen variantu s pájením): srážkoměr, BME280 μŠup, kapacitní čidlo půdy, ADS1115, kabel μŠup-dupont, radiační kryt, (Rozšířená: půdní sonda RS485, outdoor THP).
- cz.mouser.com: SparkFun Weather Meter Kit (v českých obchodech, které jsem prošel, není; laskakit má samostatný anemometr WH-SP-WS01 za 228 Kč, ale nedostupný, a směrovku jsem tam nedohledal).
- Hobbymarket / gme.cz: krabice IP65, průchodky, trubka, rezistor (ceny nedohledal).

Ruční dohledání (přesné výrazy): "SanDisk High Endurance 32GB SDSQQNR-032G", "krabice instalační IP65 ABS 200x150x100", "průchodka kabelová PG7 IP68", "rezistor 4k7 0,25W", "Ecowitt WS2910", "Ecowitt GW1100", "WH-SP-WD směrovka" (laskakit), "srážkoměr ruční zahradní".
