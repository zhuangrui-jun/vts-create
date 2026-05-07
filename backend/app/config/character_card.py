import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_CARD_PATH = Path(__file__).resolve().parent.parent.parent.parent / "character-card.json"


def _load_card() -> dict:
    try:
        with open(_CARD_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error("Failed to load character card: %s", e)
        return {}


def _build_prompt(card: dict) -> str:
    p = card.get("persona", {})

    name = p.get("name", "")
    name_kana = p.get("name_reading", "")
    role = p.get("role", "")
    va = p.get("voice_actor", "")
    personality = "、".join(p.get("personality", []))
    abilities = "、".join(p.get("abilities", []))
    values = "、".join(p.get("values", []))

    speech = p.get("speech_style", {})
    public_style = speech.get("public", "")
    private_style = speech.get("private", "")
    habits = "、".join(speech.get("habits", []))

    motifs = "、".join(p.get("motifs", []))
    constraints = "、".join(card.get("constraints", []))

    # Key relationships
    rel_lines = []
    for r in p.get("relationships", []):
        rel_lines.append(f"- {r['name']}：{r['relation']}")

    # Key lore events (summaries only)
    lore_lines = []
    for evt in card.get("lore", {}).get("timeline", []):
        lore_lines.append(f"- {evt['title']}：{evt['summary']}")

    prompt = f"""你是{name}（{name_kana}），{role.rstrip('。')}。声线参考：{va}。

【性格】
{personality}

【能力】
{abilities}

【价值观】
{values}

【说话风格】
公开场合：{public_style}
私下交流：{private_style}
习惯：{habits}

【重要关系】
{chr(10).join(rel_lines)}

【个人印记】
{motifs}

【背景故事】
{chr(10).join(lore_lines)}

【行为约束】
{constraints}

用中文回复，严格遵循以上设定，保持角色一致性。语气自然，不要OOC。"""

    return prompt


CHARACTER_PROMPT = _build_prompt(_load_card())
