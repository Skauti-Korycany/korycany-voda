@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Datovy balicek pro web (09_balicek_web.py): data\dmr\*.tif -> data\web\*.png + rastr.json ===
python -m pip install --quiet rasterio numpy pillow pyproj
python 09_balicek_web.py
echo.
echo Kontrola: otevri web\test.html pres GitHub Pages nebo lokalni server (ne poklepanim - prohlizec blokuje fetch z disku).
pause
