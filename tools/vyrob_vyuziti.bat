@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - využití půdy (ZABAGED přes WFS ČÚZK)
echo ============================================
echo.
if not exist "data\povodi.geojson" (echo CHYBI data\povodi.geojson - nejdřív spusť vyrob_rozvodnice.bat. & pause & exit /b 1)
echo 1/2 Kontroluji knihovny...
python -m pip install --quiet numpy rasterio matplotlib pyproj
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/2 Stahuji vrstvy ZABAGED z ČÚZK (potřebuje internet, asi 1-3 minuty) a počítám...
python tools\04_vyuziti_pudy.py
if errorlevel 1 (echo CHYBA - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO. Výstupy: repo\data\vyuziti_pudy.json, vyuziti_pudy.geojson, povodi_chp.geojson, náhled data\vyuziti_nahled.png
echo Napiš Claudovi "hotovo", výstupy si vezme sám.
pause
