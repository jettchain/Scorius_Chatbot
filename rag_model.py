# """
# rag_model.py
# ────────────
# • 首次冷启动：从 GCS 下载 chroma_intent.zip → 解压到 /tmp/vdb → 初始化 Chroma + Gemini-Flash
# • 提供 rag_predict(text:str) → 逗号分隔的标签串（或 "none"）
# """
# from __future__ import annotations
# import io, os, zipfile, pathlib, logging
# from typing import List, Set
#
# from google.cloud import storage
# from vertexai.generative_models import GenerativeModel
# from langchain_chroma import Chroma
#
# # ---- 依赖于你项目里的 util / embedding ----------------------------
# from rag_embeddings import GeminiEmbeddings          # 你的 Embeddings 类
# from rag_utils      import build_prompt, extract_intents   # 你的辅助函数
# # --------------------------------------------------------------------
#
# # ─────────────────── 环境变量 ────────────────────
# VDB_ZIP_URI = os.getenv("VDB_ZIP_URI")          # gs://bucket/path/chroma_intent.zip
# VDB_DIR = pathlib.Path(os.getenv("VDB_DIR", "/app/vdb/chroma_intent"))
# EMBED_MODEL = "models/gemini-embedding-exp-03-07"
# LLM_NAME = "gemini-2.0-flash-lite-001"
#
# # ─────────────────── 下载并解压向量库 ────────────────────
# def _ensure_vdb():
#     if VDB_DIR.exists():
#         return
#     raise RuntimeError(f"Vector DB missing at {VDB_DIR}")
#
# _ensure_vdb()
#
# # ─────────────────── 初始化检索器 & LLM ────────────────────
# _embedding = GeminiEmbeddings(model=EMBED_MODEL, task_type="CLASSIFICATION")
#
#
# _vectordb = Chroma(
#     collection_name="intent_cls",
#     embedding_function=_embedding,
#     persist_directory=str(VDB_DIR),           # 只传这个路径
# )
#
# _retriever = _vectordb.as_retriever(search_kwargs={"k": 5})
#
# _model = GenerativeModel(
#     model_name=LLM_NAME,
#     generation_config={
#         "temperature": 0.1,
#         "top_k": 3,
#         "top_p": 0.5,
#         "max_output_tokens": 128,
#     },
# )
#
# # ─────────────────── 对外推断函数 ────────────────────
# def rag_predict(text: str) -> str:
#     """
#     对用户回答进行多标签主题识别。
#     返回逗号分隔的小写 label 串；若无命中则返回 "none".
#     """
#     try:
#         prompt, _ = build_prompt(text, retriever=_retriever, k=5)
#         resp = _model.generate_content(prompt).text
#         labels: Set[str] = extract_intents(resp)
#         return ", ".join(sorted(labels)) if labels else "none"
#     except Exception as exc:      # 兜底，别让会话崩溃
#         logging.exception("RAG prediction failed: %s", exc)
#         return "none"
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

# ---- 依赖于你项目里的 util / embedding ----------------------------
from rag_embeddings import GeminiEmbeddings
from rag_utils import build_prompt, extract_intents
# --------------------------------------------------------------------

# ─────────────────── 环境变量 ────────────────────
VDB_DIR = pathlib.Path(os.getenv("VDB_DIR"))
EMBED_MODEL = "models/gemini-embedding-exp-03-07"
LLM_NAME = "gemini-2.0-flash-lite-001"

# --- DEBUG: 全局变量，用于缓存模型 ---
_rag_pipeline = None

def _initialize_pipeline():
    """初始化并返回 RAG pipeline 的所有组件。"""
    global _rag_pipeline
    if _rag_pipeline:
        print("--- DEBUG: RAG pipeline already initialized, skipping. ---")
        return _rag_pipeline

    print("--- DEBUG: RAG pipeline cold start: Initializing... ---")

    print(f"--- DEBUG: Checking for VDB at {VDB_DIR} ---")
    if not VDB_DIR.exists():
        print(f"--- DEBUG: VDB missing at {VDB_DIR}! ---")
        raise RuntimeError(f"Vector DB missing at {VDB_DIR}")
    print("--- DEBUG: VDB found. ---")

    # 初始化组件
    print("--- DEBUG: Initializing GeminiEmbeddings... ---")
    embedding = GeminiEmbeddings(model=EMBED_MODEL, task_type="CLASSIFICATION")
    print("--- DEBUG: GeminiEmbeddings initialized. ---")

    print("--- DEBUG: Initializing Chroma DB... ---")
    vectordb = Chroma(
        collection_name="intent_cls",
        embedding_function=embedding,
        persist_directory=str(VDB_DIR),
    )
    print("--- DEBUG: Chroma DB initialized. ---")

    print("--- DEBUG: Creating retriever... ---")
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    print("--- DEBUG: Retriever created. ---")

    print("--- DEBUG: Initializing GenerativeModel... ---")
    model = GenerativeModel(
        model_name=LLM_NAME,
        generation_config={
            "temperature": 0.1,
            "top_k": 3,
            "top_p": 0.5,
            "max_output_tokens": 128,
        },
    )
    print("--- DEBUG: GenerativeModel initialized. ---")

    _rag_pipeline = {"retriever": retriever, "model": model}
    print("--- DEBUG: RAG pipeline initialized successfully. ---")
    return _rag_pipeline


# ─────────────────── 对外推断函数 ────────────────────
def rag_predict(text: str) -> str:
    """
    对用户回答进行多标签主题识别。
    返回逗号分隔的小写 label 串；若无命中则返回 "none".
    """
    print("--- DEBUG: Entered rag_predict ---")
    try:
        print("--- DEBUG: Calling _initialize_pipeline... ---")
        pipeline = _initialize_pipeline()
        retriever = pipeline["retriever"]
        model = pipeline["model"]
        print("--- DEBUG: Pipeline ready. ---")

        print("--- DEBUG: Calling build_prompt... ---")
        prompt, _ = build_prompt(text, retriever=retriever, k=5)
        print("--- DEBUG: build_prompt finished. ---")

        print("--- DEBUG: Calling model.generate_content... ---")
        resp = model.generate_content(prompt).text
        print("--- DEBUG: model.generate_content finished. ---")

        print("--- DEBUG: Calling extract_intents... ---")
        labels: Set[str] = extract_intents(resp)
        print("--- DEBUG: extract_intents finished. ---")

        return ", ".join(sorted(labels)) if labels else "none"
    except Exception as exc:  # 兜底，别让会话崩溃
        logging.exception("RAG prediction failed: %s", exc)
        print(f"--- DEBUG: RAG prediction exception: {exc}")
        return "none"

