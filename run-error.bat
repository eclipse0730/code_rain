@echo off
chcp 65001 > nul
cd /d "%~dp0"
title CodeRain Error

if not exist CodeRain_Error.exe (
    echo CodeRain_Error.exe를 찾을 수 없습니다.
    echo CodeRain_Error.exe와 run-error.bat를 같은 폴더에 두세요.
    pause
    exit /b 1
)

CodeRain_Error.exe --speed 0.003 --loop
