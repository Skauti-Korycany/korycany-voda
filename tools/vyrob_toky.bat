@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ============================================
echo  Koryčany - vypálení toků ČÚZK do terénu (pro nádrže)
echo ============================================
echo.
if not exist "data\dmr\dmr5g_5m.tif" (
  echo CHYBI terén data\dmr\dmr5g_5m.tif - nejdřív spusť vyrob_teren.bat.
  pause
  exit /b 1
)
echo 1/3 Kontroluji knihovny...
python -m pip install --quiet numpy scipy rasterio matplotlib pyproj pillow
if errorlevel 1 (echo CHYBA pri instalaci - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 2/3 Vypaluji toky a počítám odtok (asi 1 minuta)...
python tools\14_toky_vypaleni.py
if errorlevel 1 (echo CHYBA pri vypoctu - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo 3/3 Balíček pro web...
python tools\09_balicek_web.py
if errorlevel 1 (echo CHYBA pri balicku - vyfot tohle okno a posli ho Claudovi. & pause & exit /b 1)
echo.
echo HOTOVO. Náhled: repo\docs\img\toky_vypaleni_nahled.png. Napiš Claudovi, že je hotovo.
pause
