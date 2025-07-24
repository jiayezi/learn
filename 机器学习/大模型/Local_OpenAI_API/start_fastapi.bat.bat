@echo off
echo 正在激活 Python 虚拟环境...
call D:\code\PythonProjects\.venv_3.12\Scripts\activate.bat

echo 启动 FastAPI 模型服务...
cd /d "D:\code\PythonProjects\learn\机器学习\大模型\自建 OpenAI API 服务"
start cmd /k "uvicorn main:app --host 0.0.0.0 --port 8000"

echo FastAPI 服务已启动。
