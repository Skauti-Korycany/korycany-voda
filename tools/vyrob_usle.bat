@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === USLE - ztrata pudy na orne pude (11_usle.py) ===
echo Potrebuje: data\dmr\*.tif (z vyrob_rozvodnice, vyrob_vyuziti, vyrob_cn) a data\vumop\R-2022-CZ0721.tif
python -m pip install --quiet rasterio numpy scipy pyproj matplotlib
python 11_usle.py
echo.
echo Vystupy: data\usle_info.json, data\dmr\usle_ls.tif, data\dmr\usle_A_C02.tif, docs\img\usle_nahled.png
pause
