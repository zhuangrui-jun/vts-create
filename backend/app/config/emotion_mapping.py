import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_MAPPING = {
    "happy": "笑眯眯",
    "very_happy": "眯眯眼",
    "embarrassed": "泪珠",
    "sad": "眼泪",
    "neutral": "normal",
}

_VALID_EMOTIONS = frozenset(DEFAULT_MAPPING.keys())

_mapping = None


def load_mapping(path: str | None = None) -> dict[str, str]:
    global _mapping
    if _mapping is not None:
        return _mapping

    if path is None:
        path = os.environ.get("EMOTION_MAPPING_PATH", "./emotion_mapping.json")

    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        _mapping = {k.lower(): v for k, v in loaded.items()}
        logger.info("Loaded emotion mapping from %s: %s", path, _mapping)
    else:
        _mapping = dict(DEFAULT_MAPPING)
        logger.info("No mapping file at %s, using defaults", path)

    return _mapping


def normalize_emotion(label: str) -> str:
    key = label.strip().lower()
    if key in _VALID_EMOTIONS:
        return key
    logger.debug("Unknown emotion label '%s', falling back to neutral", label)
    return "neutral"


def resolve_expression(emotion: str) -> str:
    mapping = load_mapping()
    norm = normalize_emotion(emotion)
    return mapping.get(norm, mapping["neutral"])


def validate_expressions(model_expressions: set[str]) -> list[str]:
    mapping = load_mapping()
    warnings = []
    for emotion, expr in mapping.items():
        if expr not in model_expressions:
            msg = f"Expression '{expr}' (for emotion '{emotion}') not found in model's available expressions: {model_expressions}"
            logger.warning(msg)
            warnings.append(msg)
    return warnings
