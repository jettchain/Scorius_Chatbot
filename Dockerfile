# ─────────────────────────────────────────
#  Dockerfile for Dialogflow-CX RAG Bot (with baked-in vector DB)
# ─────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# 安装 unzip + FAISS 所需依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件和向量库压缩包
COPY . .
COPY chroma_intent.zip /app/chroma_intent.zip

# 解压向量数据库到稳定路径（避免 /tmp 清空问题）
RUN mkdir -p /app/vdb/chroma_intent \
 && unzip -q /app/chroma_intent.zip -d /app/vdb/chroma_intent \
 && rm /app/chroma_intent.zip

# 设置环境变量（rag_model.py 要读取这个）
ENV VDB_DIR=/app/vdb/chroma_intent

# 启动 Functions Framework，监听 webhook
CMD ["functions-framework", "--target", "dialogflow_webhook", "--port", "8080"]
