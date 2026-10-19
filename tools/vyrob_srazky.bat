@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Srazky CHMU pro okoli Korycan (07_srazky_chmi.py) ===
echo Stahuje se z opendata.chmi.cz, bezi 1-5 minut podle pripojeni.
echo.
python -m pip install --quiet matplotlib
python 07_srazky_chmi.py
echo.
echo Vystupy: data\srazky_chmi.json, data\srazky_stanice.json, docs\img\srazky_nahled.png
echo Surova data: data\chmi\ (mimo git)
pause
