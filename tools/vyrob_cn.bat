@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - půdy (HSP z BPEJ) a odtok (CN)
echo ============================================
echo.
if not exist "data\dmr\vyuziti_kod.tif" (echo CHYBI data\dmr\vyuziti_kod.tif - nejdřív spusť vyrob_vyuziti.bat. & pause & exit /b 1)
echo 1/3 Kontroluji knihovny...
python -m pip install --quiet numpy scipy rasterio matplotlib pyproj
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/3 Stahuji BPEJ ze Státního pozemkového úřadu a odvozuji hydrologické skupiny půd...
python tools\05_hsp.py
if errorlevel 1 (echo CHYBA - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 3/3 Počítám CN a odtok z návrhového deště...
python tools\06_cn.py
if errorlevel 1 (echo CHYBA - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO. Výstupy: repo\data\hsp_info.json, cn_info.json, bpej.geojson, náhledy data\hsp_nahled.png a cn_nahled.png
echo Napiš Claudovi "hotovo".
pause
