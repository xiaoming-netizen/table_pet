@echo off
cd /d %~dp0
echo 正在安装依赖，请稍候...
pip install -r requirements.txt
echo.
echo 依赖安装完成，正在启动桌宠...
python table_pet.py
pause