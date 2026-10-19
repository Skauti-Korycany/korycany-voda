@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - výroba mapy terénu z dílů DMR 5G
echo ============================================
echo.
echo 1/2 Instaluji potřebné knihovny (jen poprvé trvá pár minut)...
python -m pip install --quiet laspy lazrs numpy scipy rasterio matplotlib pyproj
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/2 Počítám terén z dílů ve složce ..\data ...
python tools\01_dmr_grid.py "..\data"
if errorlevel 1 (echo CHYBA pri vypoctu - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO. Výsledky jsou ve složce repo\data\dmr
echo Posli Claudovi soubory dmr5g_5m_hillshade.png a dmr5g_5m_info.json (nebo jen napis, ze jsou hotove).
pause
