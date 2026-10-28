@echo off
title GOLGI MEMBRANE - Gateway to GAIA
color 0A
echo.
echo   ========================================
echo     GOLGI MEMBRANE — Gateway to GAIA
echo     lub-DUB
echo   ========================================
echo.
echo   Starting membrane on port 3141...
echo   Press Ctrl+C to close the membrane.
echo.
node "%~dp0golgi\server.js"
pause
