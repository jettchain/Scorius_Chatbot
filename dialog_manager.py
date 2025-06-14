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

FOLLOWUP_POOLS = {"meest": POOL_MEEST, "minst": POOL_MINST}

# ── 主问题配置 ─────────────────────────────────────────────
# MAIN_QUESTIONS = [
#     {"text": "Waar ben je het meest tevreden over in je werk?", "ctx": "meest"},
#     {"text": "Waar ben je het minst tevreden over in je werk?", "ctx": "minst"},
# ]

# ── chips 构建 ────────────────────────────────────────────
# def build_topic_chip_message(topics: list[str]) -> dict:
#     opts = [{"text": "Geen onderwerp"} if t == "none"
#             else {"text": t.capitalize()} for t in topics]
#     return {"payload": {"richContent": [[{"type": "chips", "options": opts}]]}}
#
# GROUP_TO_LABELS = defaultdict(list)
# for lbl, meta in LABEL_META.items():
#     GROUP_TO_LABELS[meta["group"]].append(lbl)
#
# def _suggest_next_labels(*, current_label: str|None,
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
#         cand += backlog[:8-len(cand)]
#     return cand + ["none"]
#
# def _parse_cmd(text: str|None)->tuple[str,str|None]:
#     if not text:
#         return "", None
#     t=text.strip().lower()
#     if t in {"restart","opnieuw"}: return "restart",None
#     return "",None
#
# # ───────────────────────────────────────────────────────────
# def process_turn(
#     *, user_input: str|None, params: Dict[str,Any],
#     classify_fn: Callable[[str],str]
# )->Tuple[str,Dict[str,Any],list]:
#     if user_input is None: user_input=""
#
#     # 初次进入：补齐必需键
#     params.setdefault("stage", "main")
#     params.setdefault("main_idx", 0)
#     params.setdefault("asked_labels", [])
#
#     rich: list = []
#
#     # commands
#     cmd,_=_parse_cmd(user_input)
#     if cmd=="restart":
#         params.clear()
#         params.update(stage="main", main_idx=0)
#         return MAIN_QUESTIONS[0]["text"], params, rich
#
#     stage = params.get("stage","main")
#
#     # ── main ───────────────────────────────────────────────
#     if stage=="main":
#         idx = int(params.get("main_idx", 0))
#         ctx = MAIN_QUESTIONS[idx]["ctx"]
#
#         labels = classify_fn(user_input) or ""
#         queue = [l.strip() for l in labels.split(",") if l.strip()]
#
#         params.update(
#             stage="followup",
#             label_queue=queue,
#             current_label=None,
#             cursor=0,
#             asked_labels=[],
#             main_idx=idx,               # ← 写回，保证后续存在
#         )
#         return _next_followup(params, MAIN_QUESTIONS[idx], rich)
#
#     # ── follow-up ──────────────────────────────────────────
#     if stage=="followup":
#         idx=int(params.get("main_idx",0))
#         return _next_followup(params, MAIN_QUESTIONS[idx], rich)
#
#     # ── choose_label ──────────────────────────────────────
#     if stage == "choose_label":
#         lower = (user_input or "").strip().lower()
#         if lower == "none" or lower.startswith("geen"):
#             current_idx = int(params.get("main_idx", 0))
#             next_idx = current_idx + 1
#
#             # 如果第一个主问题 (main_idx=0) 刚刚结束
#             if current_idx == 0:
#                 params['go_next_round'] = True
#                 # 注意：这里我们立即返回，让 Dialogflow CX 处理页面跳转
#                 # 我们不在 webhook 内部直接返回下一个问题
#                 # Dialogflow CX 会根据 go_next_round=true 跳转到 Survey2 页面
#                 # Survey2 页面的 onLoad 会提出第二个主问题
#                 return "Ok, we gaan door naar de volgende vraag.", params, rich
#
#             if next_idx < len(MAIN_QUESTIONS):
#                 params.update(stage="main", main_idx=next_idx,
#                               label_queue=[], current_label=None, cursor=0)
#                 return MAIN_QUESTIONS[next_idx]["text"], params, rich
#
#             # 当所有问题都结束后，设置一个最终完成的标志
#             params['survey_complete'] = True
#             return "Bedankt voor het delen! We zijn klaar.", params, rich
#     # if stage=="choose_label":
#     #     lower=(user_input or "").strip().lower()
#     #     if lower=="none" or lower.startswith("geen"):
#     #         next_idx=int(params.get("main_idx",0))+1
#     #         if next_idx < len(MAIN_QUESTIONS):
#     #             params.update(stage="main", main_idx=next_idx,
#     #                           label_queue=[], current_label=None, cursor=0)
#     #             return MAIN_QUESTIONS[next_idx]["text"], params, rich
#     #         return "Bedankt voor het delen! We zijn klaar.", params, rich
#
#         params.update(current_label=lower, cursor=0, stage="followup")
#         idx=int(params.get("main_idx",0))
#         return _next_followup(params, MAIN_QUESTIONS[idx], rich)
#
#     return "Sorry, ik begrijp het niet.", params, rich
#
#
# # ---------- follow-up helper ---------------------------------
# def _next_followup(params: dict, cfg: dict, rich: list):
#     ctx = cfg["ctx"]                         # "minst" / "meest"
#     pool_dict = FOLLOWUP_POOLS[ctx]
#
#     # ---------- 1. 取 label -------------
#     label = params.get("current_label")
#     while not label:
#         queue: list[str] = params.get("label_queue", [])
#         if not queue:
#             # 智能推荐 chips
#             asked = set(params.get("asked_labels", []))
#             chips = _suggest_next_labels(
#                 current_label=None, asked_labels=asked, ctx=ctx
#             )
#             params.update(stage="choose_label")
#             rich.append(build_topic_chip_message(chips))
#             return (
#                 "Wil je nog over een ander onderwerp praten?",
#                 params,
#                 rich,
#             )
#         label = queue.pop(0)
#         params["current_label"] = label
#         params["cursor"] = 0       # reset
#
#     # ---------- 2. 取问题 -------------
#     pool = pool_dict.get(label, [])
#     idx = int(params.get("cursor", 0) or 0)
#
#     if idx >= len(pool):           # 该 label 没题 or 已问完
#         # 只在真的有 pool 时把它计入 asked_labels
#         if pool:
#             asked = set(params.get("asked_labels", []))
#             asked.add(label)
#             params["asked_labels"] = list(asked)
#
#         # 清掉 current_label，继续队列
#         params.update(current_label=None)
#         return _next_followup(params, cfg, rich)
#
#     # ---------- 3. 输出问题 ------------
#     params["cursor"] = idx + 1
#     return pool[idx], params, rich
def build_topic_chip_message(topics: list[str]) -> dict:
    opts = [{"text": "Geen onderwerp"} if t == "none"
            else {"text": t.capitalize()} for t in topics]
    return {"payload": {"richContent": [[{"type": "chips", "options": opts}]]}}


GROUP_TO_LABELS = defaultdict(list)
for lbl, meta in LABEL_META.items():
    GROUP_TO_LABELS[meta["group"]].append(lbl)


def _suggest_next_labels(*, current_label: str | None,
                         asked_labels: Set[str], ctx: str) -> list[str]:
    cand: list[str] = []
    if current_label:
        grp = LABEL_META[current_label]["group"]
        cand += [l for l in GROUP_TO_LABELS[grp]
                 if l not in asked_labels and FOLLOWUP_POOLS[ctx].get(l)]
    if len(cand) < 8:
        backlog = sorted(
            (l for l in INTENTS if l not in asked_labels and l not in cand
             and FOLLOWUP_POOLS[ctx].get(l)),
            key=lambda x: LABEL_META[x]["weight"], reverse=True)
        cand += backlog[:8 - len(cand)]
    return cand + ["none"]


def _parse_cmd(text: str | None) -> tuple[str, str | None]:
    if not text:
        return "", None
    t = text.strip().lower()
    if t in {"restart", "opnieuw"}: return "restart", None
    return "", None


# ───────────────────────────────────────────────────────────
def process_turn(
        *, user_input: str | None, params: Dict[str, Any],
        classify_fn: Callable[[str], str]
) -> Tuple[str, Dict[str, Any], list]:
    if user_input is None: user_input = ""

    # 检查是否是首次进入，或者是否需要重置
    cmd, _ = _parse_cmd(user_input)
    if cmd == "restart" or 'stage' not in params:
        params.clear()
        params['stage'] = 'initial'  # 设置一个初始状态，等待DF传入上下文
        # 初始返回可以为空，因为DF页面会先提问
        return "Webhook ready.", params, []

    rich: list = []
    stage = params.get("stage", "initial")

    # 新逻辑: Webhook不再主动提问，而是处理对问题的回答
    # 我们期望Dialogflow在调用webhook时，已经设置了'round_context' ('meest' 或 'minst')
    if params.get('round_context') and stage != 'followup_done':

        # 当收到新的 round_context 时，我们认为是新一轮的开始
        if stage != 'followup':
            labels = classify_fn(user_input) or ""
            queue = [l.strip() for l in labels.split(",") if l.strip()]
            params.update(
                stage="followup",
                label_queue=queue,
                current_label=None,
                cursor=0,
                asked_labels=[],
            )

        # 进入或继续追问
        return _next_followup(params, rich)

    # 当用户选择了一个新的追问主题时
    if stage == "choose_label":
        lower = (user_input or "").strip().lower()

        # 如果用户选择"不再讨论"
        if lower == "none" or lower.startswith("geen"):
            ctx = params.get("round_context")
            params['stage'] = 'followup_done'  # 标记本轮追问结束

            # 如果是第一轮(meest)结束，设置参数以跳转页面
            if ctx == 'meest':
                params['go_next_round'] = True
                return "Ok, we gaan door naar de volgende vraag.", params, rich

            # 如果是第二轮(minst)结束，设置参数以结束流程
            if ctx == 'minst':
                params['survey_complete'] = True
                return "Bedankt voor het delen! We zijn klaar.", params, rich

        # 如果用户选择了新主题，则继续追问
        params.update(current_label=lower, cursor=0, stage="followup")
        return _next_followup(params, rich)

    return "Sorry, ik begrijp het niet. Kunt u dat herhalen?", params, rich


# ---------- follow-up helper (辅助函数修改) -------------------
def _next_followup(params: dict, rich: list):
    # 从 params 直接获取上下文
    ctx = params.get("round_context")
    if not ctx:
        return "Error: Context (meest/minst) not found in session.", params, rich

    pool_dict = FOLLOWUP_POOLS[ctx]

    # ---------- 1. 取 label -------------
    label = params.get("current_label")
    while not label:
        queue: list[str] = params.get("label_queue", [])
        if not queue:
            # 智能推荐 chips
            asked = set(params.get("asked_labels", []))
            chips = _suggest_next_labels(
                current_label=None, asked_labels=asked, ctx=ctx
            )
            params.update(stage="choose_label")
            rich.append(build_topic_chip_message(chips))
            return (
                "Wil je nog over een ander onderwerp praten?",
                params,
                rich,
            )
        label = queue.pop(0)
        # 检查这个label在当前上下文(meest/minst)中是否有追问
        if not pool_dict.get(label):
            label = None  # 如果没有，则跳过，继续循环
            continue

        params["current_label"] = label
        params["cursor"] = 0  # reset

    # ---------- 2. 取问题 -------------
    pool = pool_dict.get(label, [])
    idx = int(params.get("cursor", 0) or 0)

    if idx >= len(pool):  # 该 label 没题 or 已问完
        asked = set(params.get("asked_labels", []))
        asked.add(label)
        params["asked_labels"] = list(asked)

        params.update(current_label=None)
        return _next_followup(params, rich)  # 递归调用自己，处理下一个label

    # ---------- 3. 输出问题 ------------
    params["cursor"] = idx + 1
    return pool[idx], params, rich