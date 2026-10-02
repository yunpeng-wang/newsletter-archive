@echo off
cd /d "%~dp0..\"
python .\tools\eml2html.py
python .\tools\json2js.py

echo Build complete