
# main.py  ───── 使用 RAG 分类器版本 ─────────────────────────
import tracing_bootstrap
import logging, os, functions_framework
from typing import Dict, Any
from dialog_manager import process_turn
from rag_model       import rag_predict      # ← 新增
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

# ── 运行时环境变量（仅保留需要的） ──────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")   # 已由 Cloud Run env 注入

# ── 分类函数：RAG → 逗号分隔 label 串 ─────────────────────
def classify_label(text: str) -> str:
    try:
        return rag_predict(text.strip())
    except Exception as exc:
        logging.exception("RAG classifier error: %s", exc)
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
    sess   = req_json.get("sessionInfo") or {}
    params = sess.get("parameters") or {}

    reply, new_params, rich = process_turn(
        user_input=_extract_user_text(req_json),
        params=params,
        classify_fn=classify_label,
    )

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
    # ① 整条 Webhook 建一个顶级 span
    with tracer.start_as_current_span("dialogflow_webhook"):

        try:
            body = request.get_json(force=True, silent=True)

            # ② 把判 tag 写在 span 里，出错更好追踪
            if body.get("fulfillmentInfo", {}).get("tag") != "gemini":
                raise ValueError("Unsupported tag")

            # ③ 正常业务
            return handle_gemini(body)

        except Exception:
            # Trace 会自动把异常标红；同时保留旧的日志
            logging.exception("Webhook crashed")
            return {
                "fulfillment_response": {
                    "messages": [{"text": {"text": [" Webhook error"]}}]
                }
            }, 200
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
