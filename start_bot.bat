@echo off
title AI Daily Telegram Bot
cd /d "%~dp0"

echo ============================================
echo   AI Daily Telegram Bot - Auto Runner
echo ============================================
echo.

:start
echo [%date% %time%] Starting bot...
python run_bot.py

echo.
echo [%date% %time%] Bot stopped. Restarting in 10 seconds...
echo Press Ctrl+C to stop.
timeout /t 10 /nobreak >nul
goto start
