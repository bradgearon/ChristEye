@echo off
setlocal
python -m pip install -r requirements.txt
if errorlevel 1 goto error
python -m christeye demo --out outputs\demo
if errorlevel 1 goto error
echo Done. Open outputs\demo\senescence_scenario_comparison.png
pause
exit /b 0
:error
echo Python or packages are missing. See README.md
pause
exit /b 1
