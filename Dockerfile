# ─────────────────────────────────────────
#  Dockerfile  for Dialogflow-CX RAG Bot
# ─────────────────────────────────────────
# 1) 基础镜像：精简版 Python 3.10
FROM python:3.10-slim

# 2) 工作目录
WORKDIR /app

# 3) 系统依赖（如需 faiss、curl/unzip 可在此添加）
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip && \
    rm -rf /var/lib/apt/lists/*

# 4) 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) 复制源代码
COPY . .

# 6) 运行时环境变量（可在 gcloud run deploy 时覆盖）
#    VDB_ZIP_URI 必须在部署命令里 --set-env-vars 指定
ENV VDB_DIR=/tmp/vdb/chroma_intent

# 7) 启动命令：使用 Functions Framework 暴露 webhook
#    --target 对应 main.py 中 @functions_framework.http 修饰的函数名
CMD ["functions-framework", "--target", "dialogflow_webhook", "--port", "8080"]

RUN ls -la /app