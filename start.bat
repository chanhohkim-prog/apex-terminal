@echo off
title Apex Terminal - AI Bloomberg Launcher
echo ========================================================
echo    APEX TERMINAL - Next-Gen AI Bloomberg Launcher
echo ========================================================
echo.

echo [1/2] Starting Python FastAPI Backend on port 8000...
start "Apex Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\python run.py"

timeout /t 2 >nul

echo [2/2] Starting Next.js Terminal Frontend on port 3000...
start "Apex Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 3 >nul

echo.
echo Launching Bloomberg Terminal UI in browser...
start http://localhost:3000

echo.
echo ========================================================
echo Terminal services are now active!
echo Frontend: http://localhost:3000
echo Backend:  http://127.0.0.1:8000/docs
echo ========================================================
pause
