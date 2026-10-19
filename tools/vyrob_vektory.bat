@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - budovy a toky v území modelu
echo ============================================
echo.
if not exist "data\povodi.geojson" (echo CHYBI data\povodi.geojson - nejdřív spusť vyrob_rozvodnice.bat. & pause & exit /b 1)
if not exist "data\588601\588601.xml" (echo CHYBI data\588601\588601.xml - rozbal 588601.zip do složky data\588601. & pause & exit /b 1)
echo 1/2 Kontroluji knihovny...
python -m pip install --quiet numpy rasterio matplotlib pyproj
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/2 Ořezávám budovy a toky (pár sekund)...
python tools\03_vektory.py
if errorlevel 1 (echo CHYBA pri vypoctu - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO. Výstupy: repo\data\budovy.geojson, budovy_info.json, toky_cuzk.geojson, náhled data\vektory_nahled.png
pause
