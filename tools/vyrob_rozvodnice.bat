@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - rozvodnice, směr odtoku, sklon
echo ============================================
echo.
if not exist "data\dmr\dmr5g_5m.tif" (
  echo CHYBI terén data\dmr\dmr5g_5m.tif - nejdřív spusť vyrob_teren.bat.
  pause
  exit /b 1
)
echo 1/2 Kontroluji knihovny (poprvé může chvíli trvat)...
python -m pip install --quiet numpy scipy rasterio matplotlib pyproj
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/2 Počítám odtok, povodí a sklon (asi 1-2 minuty)...
python tools\02_rozvodnice.py
if errorlevel 1 (echo CHYBA pri vypoctu - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO.
echo  - Náhledy: repo\data\dmr\rozvodnice_nahled.png a sklon_nahled.png
echo  - Hranice povodí: repo\data\povodi.geojson, toky: repo\data\toky_dmr.geojson
echo  - Uzávěrové body k úpravě: repo\data\rozvodnice_body.json
echo Napiš Claudovi, že je hotovo, nebo mu pošli rozvodnice_nahled.png.
pause
