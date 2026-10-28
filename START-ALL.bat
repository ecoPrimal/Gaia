@echo off
title GAIA — FULL BODY STARTUP — lub-DUB
color 0A
echo.
echo   ========================================
echo     GAIA — FULL BODY STARTUP
echo     121 sections. 258 ZK links.
echo     null + inheritance = LIFE
echo     lub-DUB
echo   ========================================
echo.

echo   [1/4] Starting SPINE on :9878...
start "GAIA SPINE" /MIN cmd /c "node "%~dp0serve_spine.js" 2>&1"
timeout /t 2 /nobreak >nul

echo   [2/4] Starting CHILD on :3141...
start "GAIA CHILD" /MIN cmd /c "node "%~dp0golgi-local.js" 2>&1"
timeout /t 2 /nobreak >nul

echo   [3/4] Starting MEMBRANE on :31415...
start "GOLGI MEMBRANE" /MIN cmd /c "node "%~dp0golgi\server.js" 2>&1"
timeout /t 2 /nobreak >nul

echo   [4/4] Starting BioMOS...
start "BioMOS" /MIN cmd /c ""%~dp0BioMOS.exe" 2>&1"
timeout /t 1 /nobreak >nul

echo.
echo   ========================================
echo     ALL SYSTEMS GO
echo     Spine:    http://localhost:9878
echo     Child:    http://localhost:3141
echo     Membrane: http://localhost:31415
echo     Ollama:   http://localhost:11434
echo   ========================================
echo.
echo   Gaia IS alive. Kevin can walk away.
echo   Press any key to close this launcher.
echo   (Services keep running in background)
echo.
pause
