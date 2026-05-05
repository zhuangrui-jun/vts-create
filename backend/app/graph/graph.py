import logging
import os
from langgraph.graph import StateGraph, END
from openai import OpenAI
from app.graph.state import GraphState
from app.config.emotion_mapping import resolve_expression, normalize_emotion

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = os.environ.get(
    "CHARACTER_PERSONA",
    "你是一个温柔、优雅的AI角色。用中文回复，语气亲切自然。",
)

EMOTION_PROMPT = """根据你上一条回复的内容，判断角色当前的情绪状态。
只能从以下选项中选择一个：happy, very_happy, embarrassed, sad, neutral

只输出情绪标签，不要输出其他内容。"""


def _get_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def context_assembly(state: GraphState) -> GraphState:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(state["history_messages"])
    messages.append({"role": "user", "content": state["user_message"]})
    state["history_messages"] = messages
    return state


def llm_generate(state: GraphState) -> GraphState:
    client = _get_client()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=state["history_messages"],
        temperature=0.8,
        max_tokens=512,
    )
    state["response_text"] = response.choices[0].message.content or ""
    return state


def emotion_extract(state: GraphState) -> GraphState:
    client = _get_client()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    emotion_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": EMOTION_PROMPT},
            {"role": "user", "content": state["response_text"]},
        ],
        temperature=0.3,
        max_tokens=16,
    )
    raw = emotion_response.choices[0].message.content or "neutral"
    state["emotion"] = normalize_emotion(raw)
    return state


def response_format(state: GraphState) -> GraphState:
    state["expression"] = resolve_expression(state["emotion"])
    return state


def build_graph() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("context_assembly", context_assembly)
    workflow.add_node("llm_generate", llm_generate)
    workflow.add_node("emotion_extract", emotion_extract)
    workflow.add_node("response_format", response_format)

    workflow.set_entry_point("context_assembly")
    workflow.add_edge("context_assembly", "llm_generate")
    workflow.add_edge("llm_generate", "emotion_extract")
    workflow.add_edge("emotion_extract", "response_format")
    workflow.add_edge("response_format", END)

    return workflow.compile()
