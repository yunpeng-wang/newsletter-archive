@echo off
cd /d "%~dp0..\"
python .\tools\eml2html.py
python .\tools\create_index.py

echo Build complete