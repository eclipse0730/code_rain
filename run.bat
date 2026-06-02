@echo off
chcp 65001 > nul
cd /d "%~dp0"
title CodeRain

if not exist CodeRain.exe (
    echo CodeRain.exe를 찾을 수 없습니다.
    echo CodeRain.exe와 run.bat를 같은 폴더에 두세요.
    pause
    exit /b 1
)

CodeRain.exe --theme ai --speed 0.0015 --loop --noise
