def tokenize(text: str) -> list[str]:
    """Extract all 2-4 char substrings from text, longer first."""
    tokens = []
    for size in (4, 3, 2):
        for i in range(len(text) - size + 1):
            tokens.append(text[i:i + size])
    return tokens
