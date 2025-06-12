# ─────────────────────────────────────────
#  Dockerfile  for Dialogflow-CX RAG Bot
# ─────────────────────────────────────────
# 1) 基础镜像：精简版 Python 3.10
FROM python:3.10-slim

# 2) 工作目录
WORKDIR /app

# 3) 系统依赖（faiss 需要 libgomp1）
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 4) 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) 复制源代码
COPY . .
COPY chroma_intent/ /tmp/vdb/chroma_intent

# 6) 运行时环境变量（可在 gcloud run deploy 时覆盖）
ENV VDB_DIR=/tmp/vdb/chroma_intent

# 7) 启动命令：使用 Functions Framework 暴露 webhook
CMD ["functions-framework", "--target", "dialogflow_webhook", "--port", "8080"]
