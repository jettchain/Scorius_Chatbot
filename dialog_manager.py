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
    user_input = user_input or ""
    rich = []

    cmd, _ = _parse_cmd(user_input)
    if cmd == "restart":
        params.clear()
        return "Sessie is herstart.", params, rich

    # *** 最终修复：使用正确的键名来获取参数 ***
    current_round_ctx = params.get("session.params.round_context")
    processed_round_ctx = params.get("processed_round_ctx")

    if current_round_ctx and current_round_ctx != processed_round_ctx:
        labels = classify_fn(user_input) or ""
        params.update(
            stage="followup",
            label_queue=[l.strip() for l in labels.split(",") if l.strip()],
            current_label=None,
            cursor=0,
            asked_labels=[],
            processed_round_ctx=current_round_ctx
        )
        return _next_followup(params, rich)

    stage = params.get("stage")

    if stage == "followup":
        return _next_followup(params, rich)

    if stage == "choose_label":
        lower = user_input.strip().lower()

        if lower == "none" or lower.startswith("geen"):
            if current_round_ctx == 'meest':
                params['go_next_round'] = True
                return "Ok, we gaan door naar de volgende vraag.", params, rich
            else:
                params['survey_complete'] = True
                return "Bedankt voor het delen! We zijn klaar.", params, rich
        else:
            params.update(current_label=lower, cursor=0, stage="followup")
            return _next_followup(params, rich)

    return "Sorry, er is iets misgegaan. Probeer het opnieuw.", params, rich


# ---------- follow-up helper (此函数保持不变) -------------------
def _next_followup(params: dict, rich: list):
    # *** 最终修复：同样使用正确的键名来获取参数 ***
    ctx = params.get("session.params.round_context")
    if not ctx:
        return "Error: Context (meest/minst) not found in session.", params, rich

    pool_dict = FOLLOWUP_POOLS[ctx]

    label = params.get("current_label")
    while not label:
        queue: list[str] = params.get("label_queue", [])
        if not queue:
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