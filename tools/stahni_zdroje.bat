@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Archivni kopie podkladu ke katalogu opatreni (stahni_zdroje.py) ===
echo Stahuje fotky a PDF do slozky ..\..\zdroje-archiv (vedle slozky repo, mimo git).
python stahni_zdroje.py
echo.
pause
