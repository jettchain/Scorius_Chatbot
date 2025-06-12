"""
rag_model.py
────────────
• 首次冷启动：从 GCS 下载 chroma_intent.zip → 解压到 /tmp/vdb → 初始化 Chroma + Gemini-Flash
• 提供 rag_predict(text:str) → 逗号分隔的标签串（或 "none"）
"""

from __future__ import annotations

import io, os, zipfile, pathlib, logging
from typing import List, Set

from google.cloud import storage
from vertexai.generative_models import GenerativeModel
from langchain_chroma import Chroma
from chromadb.config import Settings

# ---- 依赖于你项目里的 util / embedding ----------------------------
from rag_embeddings import GeminiEmbeddings          # 你的 Embeddings 类
from rag_utils      import build_prompt, extract_intents   # 你的辅助函数
# --------------------------------------------------------------------

# ─────────────────── 环境变量 ────────────────────
VDB_ZIP_URI = os.getenv("VDB_ZIP_URI")          # gs://bucket/path/chroma_intent.zip
VDB_DIR      = pathlib.Path("/tmp/vdb/chroma_intent")
EMBED_MODEL  = "models/gemini-embedding-exp-03-07"
LLM_NAME     = "gemini-2.0-flash-lite-001"

# ─────────────────── 下载并解压向量库 ────────────────────
def _ensure_vdb():
    if VDB_DIR.exists():
        return
    if not VDB_ZIP_URI:
        raise RuntimeError("VDB_ZIP_URI env var not set")

    logging.info("⏬ Downloading vector DB: %s", VDB_ZIP_URI)

    bucket, *blob_path = VDB_ZIP_URI.replace("gs://", "").split("/", 1)
    data = storage.Client().bucket(bucket).blob(blob_path[0]).download_as_bytes()

    VDB_DIR.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(VDB_DIR.parent)

    logging.info("✅ Vector DB ready at %s", VDB_DIR)

_ensure_vdb()

# ─────────────────── 初始化检索器 & LLM ────────────────────
_embedding = GeminiEmbeddings(model=EMBED_MODEL, task_type="CLASSIFICATION")

chroma_cfg = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=str(VDB_DIR),  # 数据目录
    anonymized_telemetry=False,      # 可选：关掉遥测
)

_vectordb = Chroma(
    collection_name="intent_cls",
    embedding_function=_embedding,
    client_settings=chroma_cfg,      # ← 这里不再传 dict
)

_retriever = _vectordb.as_retriever(search_kwargs={"k": 5})

_model = GenerativeModel(
    model_name=LLM_NAME,
    generation_config={
        "temperature": 0.1,
        "top_k": 3,
        "top_p": 0.5,
        "max_output_tokens": 1024,
    },
)

# ─────────────────── 对外推断函数 ────────────────────
def rag_predict(text: str) -> str:
    """
    对用户回答进行多标签主题识别。
    返回逗号分隔的小写 label 串；若无命中则返回 "none".
    """
    try:
        prompt, _ = build_prompt(text, retriever=_retriever, k=5)
        resp = _model.generate_content(prompt).text
        labels: Set[str] = extract_intents(resp)
        return ", ".join(sorted(labels)) if labels else "none"
    except Exception as exc:      # 兜底，别让会话崩溃
        logging.exception("RAG prediction failed: %s", exc)
        return "none"
