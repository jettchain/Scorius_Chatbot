# # main.py  ───── 使用 RAG 分类器版本 ─────────────────────────
# import logging, os, functions_framework
# from typing import Dict, Any
# from dialog_manager import process_turn
# from rag_model       import rag_predict      # ← 新增
#
#
# # ── 运行时环境变量（仅保留需要的） ──────────────────────────
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")   # 已由 Cloud Run env 注入
#
# # ── 分类函数：RAG → 逗号分隔 label 串 ─────────────────────
# def classify_label(text: str) -> str:
#     try:
#         return rag_predict(text.strip())
#     except Exception as exc:
#         logging.exception("RAG classifier error: %s", exc)
#         return "none"
#
# # ── 提取用户文本 ───────────────────────────────────────────
# def _extract_user_text(req: Dict[str, Any]) -> str:
#     return (
#         req.get("text")
#         or req.get("queryResult", {}).get("queryText")
#         or req.get("queryResult", {}).get("transcript")
#         or req.get("queryResult", {}).get("text")
#         or ""
#     )
#
# # ── 主 webhook 逻辑 ────────────────────────────────────────
# def handle_gemini(req_json: Dict[str, Any]) -> Dict[str, Any]:
#     sess   = req_json.get("sessionInfo") or {}
#     params = sess.get("parameters") or {}
#
#     reply, new_params, rich = process_turn(
#         user_input=_extract_user_text(req_json),
#         params=params,
#         classify_fn=classify_label,
#     )
#
#     return {
#         "fulfillment_response": {
#             "messages": [{"text": {"text": [reply]}}] + rich,
#             "merge_behavior": "APPEND",
#         },
#         "session_info": {"parameters": new_params},
#     }
#
# # ── Cloud Functions entry for Cloud Run ──────────────────
#
# @functions_framework.http
# def dialogflow_webhook(request):
#     try:
#         body = request.get_json(force=True, silent=True)
#         if body.get("fulfillmentInfo", {}).get("tag") != "gemini":
#             raise ValueError("Unsupported tag")
#         return handle_gemini(body)
#     except Exception:
#         logging.exception("Webhook crashed")
#         return {
#             "fulfillment_response": {
#                 "messages": [{"text": {"text": ["⚠️ Webhook error"]}}]
#             }
#         }, 200
# main.py  ───── 使用 RAG 分类器版本 (带Debug日志) ──────────────────

# import logging
# import os
# import functions_framework
# from typing import Dict, Any
# from dialog_manager import process_turn
# from rag_model import rag_predict
#
# # ── 运行时环境变量（仅保留需要的） ──────────────────────────
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # 已由 Cloud Run env 注入
#
#
# # ── 分类函数：RAG → 逗号分隔 label 串 ─────────────────────
# def classify_label(text: str) -> str:
#     print("--- DEBUG: Entered classify_label ---")
#     try:
#         result = rag_predict(text.strip())
#         print(f"--- DEBUG: rag_predict returned: {result} ---")
#         return result
#     except Exception as exc:
#         logging.exception("RAG classifier error: %s", exc)
#         print(f"--- DEBUG: RAG classifier exception: {exc} ---")
#         return "none"
#
#
# # ── 提取用户文本 ───────────────────────────────────────────
# def _extract_user_text(req: Dict[str, Any]) -> str:
#     return (
#             req.get("text")
#             or req.get("queryResult", {}).get("queryText")
#             or req.get("queryResult", {}).get("transcript")
#             or req.get("queryResult", {}).get("text")
#             or ""
#     )
#
#
# # ── 主 webhook 逻辑 ────────────────────────────────────────
# def handle_gemini(req_json: Dict[str, Any]) -> Dict[str, Any]:
#     print("--- DEBUG: Entered handle_gemini ---")
#     sess = req_json.get("sessionInfo") or {}
#     params = sess.get("parameters") or {}
#     user_text = _extract_user_text(req_json)
#     print(f"--- DEBUG: User text extracted: {user_text[:100]} ---")
#
#     print("--- DEBUG: Calling process_turn ---")
#     reply, new_params, rich = process_turn(
#         user_input=user_text,
#         params=params,
#         classify_fn=classify_label,
#     )
#     print("--- DEBUG: process_turn finished ---")
#
#     return {
#         "fulfillment_response": {
#             "messages": [{"text": {"text": [reply]}}] + rich,
#             "merge_behavior": "APPEND",
#         },
#         "session_info": {"parameters": new_params},
#     }
#
#
# # ── Cloud Functions entry for Cloud Run ──────────────────
#
# @functions_framework.http
# def dialogflow_webhook(request):
#     print("--- DEBUG: Webhook request received ---")
#     try:
#         body = request.get_json(force=True, silent=True)
#         if not body:
#             print("--- DEBUG: Request body is empty ---")
#             return "Error: No body", 400
#
#         print("--- DEBUG: Checking tag ---")
#         if body.get("fulfillmentInfo", {}).get("tag") != "gemini":
#             print("--- DEBUG: Unsupported tag ---")
#             raise ValueError("Unsupported tag")
#
#         print("--- DEBUG: Calling handle_gemini ---")
#         return handle_gemini(body)
#     except Exception:
#         logging.exception("Webhook crashed")
#         print("--- DEBUG: Webhook crashed ---")
#         return {
#             "fulfillment_response": {
#                 "messages": [{"text": {"text": ["⚠️ Webhook error"]}}]
#             }
#         }, 200
# main.py  ───── 使用 RAG 分类器版本 (带Debug日志) ──────────────────

import logging
import os
import functions_framework
from typing import Dict, Any
from dialog_manager import process_turn
from rag_model import rag_predict
import json  # 导入json库以便更好地打印

# ── 运行时环境变量（仅保留需要的） ──────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # 已由 Cloud Run env 注入


# ── 分类函数：RAG → 逗号分隔 label 串 ─────────────────────
def classify_label(text: str) -> str:
    print("--- DEBUG: Entered classify_label ---")
    try:
        result = rag_predict(text.strip())
        print(f"--- DEBUG: rag_predict returned: {result} ---")
        return result
    except Exception as exc:
        logging.exception("RAG classifier error: %s", exc)
        print(f"--- DEBUG: RAG classifier exception: {exc} ---")
        return "none"


# ── 提取用户文本 ───────────────────────────────────────────
def _extract_user_text(req: Dict[str, Any]) -> str:
    return (
            req.get("text")
            or req.get("queryResult", {}).get("queryText")
            or req.get("queryResult", {}).get("transcript")
            or req.get("queryResult", {}).get("text")
            or ""
    )


# ── 主 webhook 逻辑 ────────────────────────────────────────
def handle_gemini(req_json: Dict[str, Any]) -> Dict[str, Any]:
    print("--- DEBUG: Entered handle_gemini ---")
    sess = req_json.get("sessionInfo") or {}
    params = sess.get("parameters") or {}
    user_text = _extract_user_text(req_json)
    print(f"--- DEBUG: User text extracted: {user_text[:100]} ---")

    print("--- DEBUG: Calling process_turn ---")
    reply, new_params, rich = process_turn(
        user_input=user_text,
        params=params,
        classify_fn=classify_label,
    )
    print("--- DEBUG: process_turn finished ---")

    return {
        "fulfillment_response": {
            "messages": [{"text": {"text": [reply]}}] + rich,
            "merge_behavior": "APPEND",
        },
        "session_info": {"parameters": new_params},
    }


# ── Cloud Functions entry for Cloud Run ──────────────────

@functions_framework.http
def dialogflow_webhook(request):
    print("--- DEBUG: Webhook request received ---")
    try:
        body = request.get_json(force=True, silent=True)

        # *** 新增的调试日志 ***
        # ------------------------------------------------------------------
        print(f"--- FULL WEBHOOK BODY RECEIVED: {json.dumps(body, indent=2)} ---")
        # ------------------------------------------------------------------

        if not body:
            print("--- DEBUG: Request body is empty ---")
            return "Error: No body", 400

        print("--- DEBUG: Checking tag ---")
        if body.get("fulfillmentInfo", {}).get("tag") != "gemini":
            print("--- DEBUG: Unsupported tag ---")
            raise ValueError("Unsupported tag")

        print("--- DEBUG: Calling handle_gemini ---")
        return handle_gemini(body)
    except Exception:
        logging.exception("Webhook crashed")
        print("--- DEBUG: Webhook crashed ---")
        return {
            "fulfillment_response": {
                "messages": [{"text": {"text": ["⚠️ Webhook error"]}}]
            }
        }, 200