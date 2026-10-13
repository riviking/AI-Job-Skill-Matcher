"""Text cleaning and skill name normalisation. Owner: Rivindu."""
import re
from functools import lru_cache
from utils.data_loader import load_skills


def clean_text(text: str) -> str:
    """Lowercase, remove HTML, URLs, emails, phone numbers, symbols and extra spaces.
    Keeps characters used in skill names: + # . (C++, C#, Node.js)."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d\s\-]{7,}\d", " ", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s\u0D80-\u0DFF]", " ", text)
    text = re.sub(r"(?<!\w)\.|\.(?!\w)", " ", text)   # dots not inside words
    return re.sub(r"\s+", " ", text).strip()


@lru_cache(maxsize=None)
def alias_map() -> dict[str, str]:
    """{'ms excel': 'Excel', 'excel': 'Excel', 'ml': 'Machine Learning', ...}"""
    mapping = {}
    for _, row in load_skills().iterrows():
        mapping[row.skill_name.lower()] = row.skill_name
        if isinstance(row.aliases, str):
            for a in row.aliases.split(";"):
                if a.strip():
                    mapping[a.strip().lower()] = row.skill_name
    return mapping


def normalise_skill(skill: str) -> str | None:
    """Map any alias to its canonical name. Returns None if unknown."""
    return alias_map().get(skill.strip().lower())
