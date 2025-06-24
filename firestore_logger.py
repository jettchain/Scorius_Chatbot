# firestore_logger.py
import os
from google.cloud import firestore
from typing import Dict, Any

# 初始化 Firestore 客户端。
# 在 Cloud Run 环境中，客户端会自动检测项目 ID 和凭据。
db = firestore.Client()

SESSION_COLLECTION = "chatbot_sessions"

def log_session_data(session_id: str, data: Dict[str, Any]):
    """
    在一个特定会话的 Firestore 文档中存储或合并数据。
    """
    if not session_id:
        print("--- ERROR: 未提供用于 Firestore 日志记录的 session_id。 ---")
        return

    try:
        # 使用 session_id 作为文档 ID。
        # .set(data, merge=True) 确保我们可以在不覆盖整个文档的情况下添加数据。
        doc_ref = db.collection(SESSION_COLLECTION).document(session_id)
        doc_ref.set(data, merge=True)
        print(f"--- DEBUG: 数据已成功记录到 Firestore，会话为 {session_id} ---")
    except Exception as e:
        print(f"--- ERROR: 无法写入 Firestore: {e} ---")

def prepare_evaluation_data(session_params: Dict[str, Any], score: str, question_id: str):
    """
    准备在评估问题后需要存储的数据。
    """
    evaluation_log = {
        "evaluations": firestore.ArrayUnion([{
            "question_id": question_id,
            "score": int(score),
            "timestamp": firestore.SERVER_TIMESTAMP
        }])
    }
    return evaluation_log

def prepare_conversation_turn(user_input: str, bot_reply: str, labels: str, stage: str, timestamp: Any):
    """
    准备要记录的单个对话回合。
    """
    return {
        "conversation_history": firestore.ArrayUnion([{
            "user_input": user_input,
            "bot_reply": bot_reply,
            "detected_labels": labels,
            "stage": stage,
            "timestamp": timestamp
        }])
    }