@echo off
chcp 65001 >nul
rem Stahne aktualni verzi repozitare z GitHubu (vetev main) a prepise jim soubory v teto slozce repo.
rem Nic nemaze: soubory jen na PC (data\dmr, LAZ, VUMOP, surova data) zustanou. Slozka .git se nemeni.
setlocal
set "REPO=%~dp0.."
set "TMPD=%TEMP%\korycany-voda-aktualizace"
echo === Aktualizace z GitHubu do: %REPO% ===
echo.
if exist "%TMPD%" rmdir /s /q "%TMPD%"
mkdir "%TMPD%"
echo 1/3 Stahuji z GitHubu (asi 20 MB)...
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://codeload.github.com/Skauti-Korycany/korycany-voda/zip/refs/heads/main' -OutFile '%TMPD%\main.zip'"
if errorlevel 1 goto chyba
echo 2/3 Rozbaluji...
powershell -NoProfile -Command "Expand-Archive -Path '%TMPD%\main.zip' -DestinationPath '%TMPD%' -Force"
if errorlevel 1 goto chyba
echo 3/3 Kopiruji do slozky repo (nic se nemaze)...
robocopy "%TMPD%\korycany-voda-main" "%REPO%" /E /XD .git /NFL /NDL /NJH /NP
if errorlevel 8 goto chyba
rmdir /s /q "%TMPD%"
echo.
echo HOTOVO. Slozka repo odpovida GitHubu (vetev main).
pause
exit /b 0
:chyba
echo.
echo CHYBA - aktualizace se nepovedla. Posli Claudovi text z tohoto okna (nebo jeho fotku).
pause
exit /b 1
