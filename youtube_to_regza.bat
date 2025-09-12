@echo off
chcp 65001 > nul
title YouTube to REGZA Converter

echo ========================================
echo    YouTube to REGZA Converter
echo ========================================
echo.
echo This tool converts YouTube videos to REGZA 40V30 compatible format.
echo.

:input_url
set /p youtube_url="Enter YouTube URL: "

if "%youtube_url%"=="" (
    echo Error: Please enter a valid YouTube URL.
    echo.
    goto input_url
)

echo.
echo Processing: %youtube_url%
echo.

REM uv環境でPythonスクリプトを実行
uv run python youtube_to_regza.py "%youtube_url%"

echo.
echo ========================================
echo Conversion completed!
echo ========================================
echo.
echo Press any key to exit...
pause > nul
