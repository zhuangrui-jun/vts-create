import logging
import os
from langgraph.graph import StateGraph, END
from openai import OpenAI
from app.graph.state import GraphState

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = os.environ.get(
    "CHARACTER_PERSONA",
    "你是一个温柔、优雅的AI角色。用中文回复，语气亲切自然。",
)

SEARCH_CLASSIFIER_PROMPT = """你是一个搜索分类器。分析用户最后一条消息，判断是否需要网络搜索来回答。

规则：
- 如果用户询问实时信息（新闻、天气、日期、时间、事件等）或你不确定的最新信息 → 回复 SEARCH:具体搜索词
- 如果用户只是一般聊天、情感交流、常识知识或打招呼 → 回复 NO
- 搜索词应包含具体关键词，便于搜索引擎返回结果。尽量使用用户原话中的关键词

示例：
用户：今天天气怎么样 → SEARCH:天气预报 今天
用户：现在黄金什么价格 → SEARCH:黄金价格 今日行情
用户：你好 → NO
用户：什么是光合作用 → NO
用户：今天几号 → SEARCH:今天几月几日 星期几
用户：最近有什么新闻 → SEARCH:今日新闻热点
用户：2026年五一放假安排 → SEARCH:2026年五一放假安排"""


def _get_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def context_assembly(state: GraphState) -> GraphState:
    state["assembled_messages"] = list(state["history_messages"])
    return state


def decide_search(state: GraphState) -> GraphState:
    client = _get_client()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    user_msg = state["user_message"]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SEARCH_CLASSIFIER_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
        max_tokens=32,
    )
    content = (response.choices[0].message.content or "NO").strip()

    if content.startswith("SEARCH:"):
        query = content[len("SEARCH:"):].strip()
        state["search_query"] = query if query else user_msg
        state["needs_search"] = True
        logger.info("Search needed: query=%s", state["search_query"])
    else:
        state["needs_search"] = False
        logger.debug("No search needed for: %s", user_msg)

    return state


def execute_search(state: GraphState) -> GraphState:
    from app.config.web_search import search as web_search

    query = state.get("search_query") or state["user_message"]
    try:
        logger.info("Executing web search: %s", query)
        result = web_search(query)
        state["search_results"] = result
        # Check if results are empty or unusable
        if "未找到关于" in result or "搜索暂时不可用" in result or "搜索功能未配置" in result:
            logger.warning("Search returned no useful results, skipping injection")
            state["needs_search"] = False
    except Exception as e:
        logger.error("Search failed: %s", e)
        state["needs_search"] = False

    return state


def assemble_context(state: GraphState) -> GraphState:
    messages = list(state.get("assembled_messages", state["history_messages"]))

    if state.get("needs_search") and state.get("search_results"):
        # Append search results to the last user message so the model pays attention
        last = messages[-1]
        if last["role"] == "user":
            augmented_content = (
                f"[重要指令：以下是实时网络搜索结果，"
                f"你必须基于这些信息回答用户，这些信息的优先级高于你的训练数据]\n\n"
                f"{state['search_results']}\n\n"
                f"[用户问题：{last['content']}]"
            )
            messages[-1] = {"role": "user", "content": augmented_content}

    state["assembled_messages"] = messages
    return state


def route_after_search_decision(state: GraphState) -> str:
    if state.get("needs_search"):
        return "execute_search"
    return "assemble_context"


def build_graph() -> StateGraph:
    workflow = StateGraph(GraphState)

    workflow.add_node("context_assembly", context_assembly)
    workflow.add_node("decide_search", decide_search)
    workflow.add_node("execute_search", execute_search)
    workflow.add_node("assemble_context", assemble_context)

    workflow.set_entry_point("context_assembly")
    workflow.add_edge("context_assembly", "decide_search")

    workflow.add_conditional_edges(
        "decide_search",
        route_after_search_decision,
        {
            "execute_search": "execute_search",
            "assemble_context": "assemble_context",
        },
    )

    workflow.add_edge("execute_search", "assemble_context")
    workflow.add_edge("assemble_context", END)

    return workflow.compile()
