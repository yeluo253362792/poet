#!/bin/bash
# 安装依赖
pip install -r requirements.txt

# 使用 Gunicorn 启动应用
gunicorn --bind 0.0.0.0:5000 wsgi:app
