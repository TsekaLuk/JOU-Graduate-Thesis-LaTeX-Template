@echo off
setlocal

echo ==> Downloading fallback fonts...
python scripts\download_fonts.py
if errorlevel 1 goto :error

echo ==> Building thesis with latexmk...
latexmk main.tex
if errorlevel 1 goto :error

echo ==> Done: main.pdf
exit /b 0

:error
echo Build failed.
exit /b 1
