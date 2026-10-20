@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Katastralni parcely CUZK (10_parcely.py) -> data\parcely.geojson ===
echo Stahuje Atom feed a GML 4 k.u. z atom.cuzk.gov.cz / services.cuzk.gov.cz (CC BY 4.0). Bezi 1-5 minut.
python -m pip install --quiet numpy pyproj matplotlib rasterio
python 10_parcely.py
pause
