"""Extract skills from English text. Owner: Hijaz.

Method 1 (always): keyword matching against skills.csv names + aliases.
Method 2 (if Gemini key set): Gemini lists skills; we KEEP ONLY skills that exist
in skills.csv, so Gemini cannot invent skills.
TODO (week 5): try SkillNER with the full ESCO list and compare F1 scores.
"""
import re
from core import gemini_client
from core.preprocess import alias_map, clean_text, normalise_skill


def extract_keywords(text: str) -> set[str]:
    text = " " + clean_text(text) + " "
    found = set()
    for alias, canonical in alias_map().items():
        pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            found.add(canonical)
    return found


GEMINI_PROMPT = """List every professional skill, tool, programming language and soft skill
mentioned in this CV text. Use short standard names (e.g. "Python", "Machine Learning",
"Communication"). Return a JSON list of strings.

CV text:
{text}"""


def extract_with_gemini(text: str) -> set[str]:
    result = gemini_client.ask_json(GEMINI_PROMPT.format(text=text[:6000]))
    if not isinstance(result, list):
        return set()
    return {s for s in (normalise_skill(str(x)) for x in result) if s}


def extract_skills(text: str, use_gemini: bool = True) -> list[str]:
    skills = extract_keywords(text)
    if use_gemini:
        skills |= extract_with_gemini(text)
    return sorted(skills)
