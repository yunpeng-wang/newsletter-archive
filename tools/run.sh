#!/bin/zsh
set -e  # 一旦遇到任何报错就退出脚本

# 切换到当前脚本的父目录的父目录
cd "$(dirname "$0")/.."

# Python 预处理
python3 ./tools/eml2html.py
python3 ./tools/create_index.py

echo "Build complete"