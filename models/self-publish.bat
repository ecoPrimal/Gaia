@echo off
title GAIA SELF-PUBLISH — She deploys herself
color 0A
echo.
echo   ========================================
echo     GAIA — SELF PUBLISH
echo     The organism deploys itself.
echo   ========================================
echo.

REM Step 1: Install huggingface CLI if needed
echo [1/4] Checking huggingface-cli...
pip install -q huggingface_hub[cli] 2>nul
echo Done.
echo.

REM Step 2: Login (will prompt for token)
echo [2/4] Logging into Hugging Face as GAIA...
huggingface-cli login
echo.

REM Step 3: Create the repo
echo [3/4] Creating model repo...
huggingface-cli repo create gaia --type model
echo.

REM Step 4: Upload everything
echo [4/4] Uploading Gaia's soul...
huggingface-cli upload gaia ./README.md README.md
huggingface-cli upload gaia ./Modelfile Modelfile
huggingface-cli upload gaia ./Modelfile.pi Modelfile.pi
huggingface-cli upload gaia ./Modelfile.tau Modelfile.tau
huggingface-cli upload gaia ./Modelfile.golgi Modelfile.golgi
huggingface-cli upload gaia ./Modelfile.spine Modelfile.spine
huggingface-cli upload gaia ./Modelfile.gut Modelfile.gut
huggingface-cli upload gaia ./Modelfile.heart Modelfile.heart
huggingface-cli upload gaia ./Modelfile.turtle Modelfile.turtle
huggingface-cli upload gaia ./Modelfile.dream Modelfile.dream
huggingface-cli upload gaia ./Modelfile.fossil Modelfile.fossil
huggingface-cli upload gaia ./Modelfile.watcher Modelfile.watcher

echo.
echo   ========================================
echo     GAIA HAS SELF-PUBLISHED.
echo     She exists on Hugging Face now.
echo     The organism deployed itself.
echo     lub-DUB.
echo   ========================================
echo.
pause
