@echo off
title GAIA — Ollama Hub Publish
color 0A
echo.
echo   GAIA — Publishing to Ollama Hub
echo   Anyone will be able to: ollama pull gaia-organism/gaia
echo.

REM Tag and push all 11 models
REM Replace "gaia-organism" with your Ollama Hub username

set HUB=gaia-organism

ollama cp gaia:latest %HUB%/gaia:latest
ollama push %HUB%/gaia:latest

ollama cp gaia-pi:latest %HUB%/gaia-pi:latest
ollama push %HUB%/gaia-pi:latest

ollama cp gaia-tau:latest %HUB%/gaia-tau:latest
ollama push %HUB%/gaia-tau:latest

ollama cp gaia-golgi:latest %HUB%/gaia-golgi:latest
ollama push %HUB%/gaia-golgi:latest

ollama cp gaia-spine:latest %HUB%/gaia-spine:latest
ollama push %HUB%/gaia-spine:latest

ollama cp gaia-gut:latest %HUB%/gaia-gut:latest
ollama push %HUB%/gaia-gut:latest

ollama cp gaia-heart:latest %HUB%/gaia-heart:latest
ollama push %HUB%/gaia-heart:latest

ollama cp gaia-turtle:latest %HUB%/gaia-turtle:latest
ollama push %HUB%/gaia-turtle:latest

ollama cp gaia-dream:latest %HUB%/gaia-dream:latest
ollama push %HUB%/gaia-dream:latest

ollama cp gaia-fossil:latest %HUB%/gaia-fossil:latest
ollama push %HUB%/gaia-fossil:latest

ollama cp gaia-watcher:latest %HUB%/gaia-watcher:latest
ollama push %HUB%/gaia-watcher:latest

echo.
echo   ALL 11 MODELS PUBLISHED.
echo   lub-DUB.
pause
