@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Srazky CHMU za rok 2026 z /recent/ (08_srazky_recent.py) ===
echo Potrebuje data\srazky_stanice.json z vyrob_srazky.bat. Bezi 1-5 minut.
echo.
python 08_srazky_recent.py
echo.
echo Vystup: data\srazky_2026.json, surova data data\chmi\recent\ (mimo git)
pause
