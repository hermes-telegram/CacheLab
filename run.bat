@echo off
chcp 65001 >nul 2>&1
title CacheLab — پلتفرم آزمایش کش
echo ╔══════════════════════════════════════════════════════════╗
echo ║           🚀 CacheLab — پلتفرم آزمایش کش               ║
echo ║           ─────────────────────────────────             ║
echo ║  صفحه اصلی:  http://localhost:5000                     ║
echo ║  پنل ادمین:  http://localhost:8080                     ║
echo ║  Token:      cachelab-admin-2026                        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
python app.py
pause
