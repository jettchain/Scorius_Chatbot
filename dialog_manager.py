from __future__ import annotations
import re
from typing import Dict, Any, Callable, Tuple, List, Set
from collections import defaultdict

from intents_dictionary import (
    INTENTS,
    LABEL_META,
    POOL_MINST,
    POOL_MEEST,
)
from evaluation_questions import EVALUATION_QUESTIONS

FOLLOWUP_POOLS = {"meest": POOL_MEEST, "minst": POOL_MINST}

def build_descriptive_rating_chips(scale_labels: Dict[str, str]) -> dict:
    """根据提供的完整标签集构建所有五个描述性评分chips。"""
    options = []
    # 循环1到5，为每个分数创建带描述的按钮
    for i in range(1, 6):
        score_str = str(i)
        description = scale_labels.get(score_str, score_str)  # 如果没找到描述，就用数字本身
        options.append({"text": f"{score_str} ({description})"})

    return {"payload": {"richContent": [[{"type": "chips", "options": options}]]}}

def build_topic_chip_message(topics: list[str]) -> dict:
    opts = [{"text": "Geen onderwerp"} if t == "none"
            else {"text": t.capitalize()} for t in topics]
    return {"payload": {"richContent": [[{"type": "chips", "options": opts}]]}}


GROUP_TO_LABELS = defaultdict(list)
for lbl, meta in LABEL_META.items():
    GROUP_TO_LABELS[meta["group"]].append(lbl)


# def _suggest_next_labels(*, current_label: str | None,
#                          asked_labels: Set[str], ctx: str) -> list[str]:
#     cand: list[str] = []
#     if current_label:
#         grp = LABEL_META[current_label]["group"]
#         cand += [l for l in GROUP_TO_LABELS[grp]
#                  if l not in asked_labels and FOLLOWUP_POOLS[ctx].get(l)]
#     if len(cand) < 8:
#         backlog = sorted(
#             (l for l in INTENTS if l not in asked_labels and l not in cand
#              and FOLLOWUP_POOLS[ctx].get(l)),
#             key=lambda x: LABEL_META[x]["weight"], reverse=True)
#         cand += backlog[:8 - len(cand)]
#     return cand + ["none"]
def _suggest_next_labels(*, labels_for_weighting: Set[str], labels_to_exclude: Set[str], ctx: str) -> List[str]:
    """
    根据模型识别的所有标签累加权重，生成新的、有后续问题的话题建议。
    """

    follow_up_pool = FOLLOWUP_POOLS[ctx]

    if not labels_for_weighting:
        # 提供一个默认的、有后续问题的话题列表作为备选
        default_suggestions = []
        # 简单地从所有有后续问题的意图中选取
        for label in INTENTS:
            if len(default_suggestions) >= 5:
                break
            if label in follow_up_pool:
                default_suggestions.append(label)
        return default_suggestions + ["Geen onderwerp"]

    combined_weights = defaultdict(float)

    # 1. 根据模型识别的所有标签，累加权重
    for label in labels_for_weighting:
        if label in LABEL_META:
            related_labels = LABEL_META[label].get("related_labels", {})
            for related_label, weight in related_labels.items():
                combined_weights[related_label] += weight

    # 2. 从候选列表中，移除所有已经讨论过的话题
    for label in labels_to_exclude:
        if label in combined_weights:
            del combined_weights[label]

    # 也移除模型本次识别出的所有话题，避免立即重复
    for label in labels_for_weighting:
        if label in combined_weights:
            del combined_weights[label]

    # 3. 按权重降序排序
    sorted_candidates = sorted(combined_weights.items(), key=lambda item: item[1], reverse=True)

    # 4. 过滤掉没有后续问题的标签，并取最多5个
    final_suggestions = []
    for label, weight in sorted_candidates:
        if len(final_suggestions) >= 5:
            break
        # 只有在问题池中存在的标签，才是有效的建议
        if label in follow_up_pool:
            final_suggestions.append(label)

    return final_suggestions + ["Geen onderwerp"]

def _parse_cmd(text: str | None) -> tuple[str, str | None]:
    if not text:
        return "", None
    t = text.strip().lower()
    if t in {"restart", "opnieuw"}: return "restart", None
    return "", None


def _ask_next_evaluation_question(params: dict, rich: list) -> Tuple[str, dict]:
    """根据索引提出下一个评估问题，或者结束对话。"""
    eval_idx = params.get("evaluation_idx", 0)

    if eval_idx < len(EVALUATION_QUESTIONS):
        question_data = EVALUATION_QUESTIONS[eval_idx]
        question_to_ask = question_data["text"]

        # 使用新的chips构建函数
        rich.append(build_descriptive_rating_chips(question_data["scale_labels"]))

        params["evaluation_idx"] = eval_idx + 1
        return question_to_ask, params
    else:
        params["stage"] = "end"
        return "Hartelijk dank voor uw waardevolle feedback en uw tijd! Het gesprek is nu beëindigd.", params


# ───────────────────────────────────────────────────────────
# def process_turn(
#         *, user_input: str | None, params: Dict[str, Any],
#         classify_fn: Callable[[str], str]
# ) -> Tuple[str, Dict[str, Any], list]:
#     user_input = user_input or ""
#     rich = []
#
#     cmd, _ = _parse_cmd(user_input)
#     if cmd == "restart":
#         params.clear()
#         return "Sessie is herstart.", params, rich
#
#     current_round_ctx = params.get("session.params.round_context")
#     processed_round_ctx = params.get("processed_round_ctx")
#
#     if current_round_ctx and current_round_ctx != processed_round_ctx:
#         labels = classify_fn(user_input) or ""
#         # 原始识别的标签列表
#         initial_labels = [l.strip() for l in labels.split(",") if l.strip()]
#
#         params.update(
#             stage="followup",
#             label_queue=initial_labels.copy(),
#             # *** 新增：保存所有原始标签，用于权重计算 ***
#             all_detected_labels=initial_labels,
#             current_label=None,
#             cursor=0,
#             asked_labels=[], # 初始为空
#             processed_round_ctx=current_round_ctx
#         )
#         return _next_followup(params, rich)
#
#     stage = params.get("stage")
#
#     if stage == "followup":
#         return _next_followup(params, rich)
#
#     if stage == "choose_label":
#         lower = user_input.strip().lower()
#
#         if lower == "none" or lower.startswith("geen"):
#             if current_round_ctx == 'meest':
#                 params['go_next_round'] = True
#                 return "Ok, we gaan door naar de volgende vraag.", params, rich
#             else:
#                 params['survey_complete'] = True
#                 return "Bedankt voor het delen! We zijn klaar.", params, rich
#         else:
#             params.update(current_label=lower, cursor=0, stage="followup")
#             return _next_followup(params, rich)
#
#     return "Sorry, er is iets misgegaan. Probeer het opnieuw.", params, rich
def process_turn(
        *, user_input: str | None, params: Dict[str, Any],
        classify_fn: Callable[[str], str]
) -> Tuple[str, Dict[str, Any], list]:
    user_input = user_input or ""
    rich = []

    cmd, _ = _parse_cmd(user_input)
    if cmd == "restart":
        params.clear()
        return "Sessie is herstart.", params, rich

    stage = params.get("stage")
    current_round_ctx = params.get("session.params.round_context")
    processed_round_ctx = params.get("processed_round_ctx")

    if current_round_ctx and current_round_ctx != processed_round_ctx:
        labels = classify_fn(user_input) or ""
        initial_labels = [l.strip() for l in labels.split(",") if l.strip()]
        params.update(
            stage="followup", label_queue=initial_labels.copy(),
            all_detected_labels=initial_labels, current_label=None,
            cursor=0, asked_labels=[], processed_round_ctx=current_round_ctx
        )
        return _next_followup(params, rich)

    if stage == "final_evaluation":
        # MODIFIED: 更新评分捕获逻辑以处理 "1 (Description)" 格式
        score_text = user_input.strip().split(" ")[0]  # 取空格前第一个部分

        if score_text.isdigit() and 1 <= int(score_text) <= 5:
            session_id = params.get("session.id", "unknown_session")
            last_eval_idx = params.get("evaluation_idx", 1) - 1
            last_question_id = EVALUATION_QUESTIONS[last_eval_idx]["id"]

            print(f"--- EVALUATION RESPONSE CAPTURED ---\n"
                  f"Session: {session_id}\n"
                  f"Metric: {last_question_id}\n"
                  f"Score: {score_text}\n"
                  f"------------------------------------")

            reply, params = _ask_next_evaluation_question(params, rich)
            return reply, params, rich
        else:
            # 如果输入无效，重新提问并再次显示chips
            last_eval_idx = params.get("evaluation_idx", 1) - 1
            question_data = EVALUATION_QUESTIONS[last_eval_idx]
            rich.append(build_descriptive_rating_chips(question_data["scale_labels"]))
            return f"Graag een keuze maken via de knoppen. {question_data['text']}", params, rich

    if stage == "followup":
        return _next_followup(params, rich)

    if stage == "choose_label":
        lower = user_input.strip().lower()
        if lower == "none" or lower.startswith("geen"):
            if current_round_ctx == 'meest':
                params['go_next_round'] = True
                return "Ok, we gaan door naar de volgende vraag.", params, rich
            else:
                # MODIFIED: 这里是您指定的整合点
                # 主流程结束，启动最终评估
                params['stage'] = 'final_evaluation'
                params['evaluation_idx'] = 0
                reply, params = _ask_next_evaluation_question(params, rich)
                return reply, params, rich
        else:
            params.update(current_label=lower, cursor=0, stage="followup")
            return _next_followup(params, rich)

    return "Sorry, er is iets misgegaan. Probeer het opnieuw.", params, rich


# ---------- follow-up helper (此函数保持不变) -------------------
def _next_followup(params: dict, rich: list):
    ctx = params.get("session.params.round_context")
    if not ctx:
        return "Error: Context (meest/minst) not found in session.", params, rich

    pool_dict = FOLLOWUP_POOLS[ctx]

    label = params.get("current_label")
    while not label:
        queue: list[str] = params.get("label_queue", [])
        if not queue:
            # *** 当提问队列为空时，生成新的话题建议 ***

            # 用于权重计算的标签：模型识别出的所有原始标签
            labels_for_weighting = set(params.get("all_detected_labels", []))
            # 需要从建议中排除的标签：已经深入讨论过的
            labels_to_exclude = set(params.get("asked_labels", []))

            chips = _suggest_next_labels(
                labels_for_weighting=labels_for_weighting,
                labels_to_exclude=labels_to_exclude,
                ctx=ctx
            )
            params.update(stage="choose_label")
            rich.append(build_topic_chip_message(chips))
            return (
                "Heb je nog opmerkingen over een ander onderwerp?",
                params,
                rich,
            )
        label = queue.pop(0)
        if not pool_dict.get(label):
            label = None
            continue

        params["current_label"] = label
        params["cursor"] = 0

    pool = pool_dict.get(label, [])
    idx = int(params.get("cursor", 0) or 0)

    if idx >= len(pool):
        asked = set(params.get("asked_labels", []))
        asked.add(label)
        params["asked_labels"] = list(asked)
        params.update(current_label=None)
        return _next_followup(params, rich)

    params["cursor"] = idx + 1
    return pool[idx], params, rich