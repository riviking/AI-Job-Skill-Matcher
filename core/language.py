"""Language detection and Sinhala -> English translation. Owner: Mathu.

Steps: 1) replace known Sinhala skill words using our dictionary
       2) send the rest to Gemini for translation
       3) if Gemini is not available, return the dictionary result
"""
import re
from core import gemini_client
from utils.data_loader import load_sinhala_dict

SINHALA_CHARS = re.compile(r"[\u0D80-\u0DFF]")


def sinhala_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(bool(SINHALA_CHARS.match(c)) for c in letters) / len(letters)


def detect_language(text: str) -> str:
    """Return 'si' if the text is mostly/partly Sinhala script, else 'en'."""
    return "si" if sinhala_ratio(text) > 0.2 else "en"


def apply_dictionary(text: str) -> str:
    d = load_sinhala_dict()
    # longest terms first so "දත්ත විශ්ලේෂණය" is replaced before "දත්ත"
    for _, row in d.sort_values("sinhala_text", key=lambda s: s.str.len(), ascending=False).iterrows():
        text = text.replace(row.sinhala_text, f" {row.skill_name} ")
    return text


TRANSLATE_PROMPT = """You are translating a Sri Lankan university student's CV or skill list.
Translate the text below into clear English.
Keep technical terms, tools and programming languages exactly as they are.
Do not add any skills that are not in the text.

Text:
{text}"""


def translate_si_en(text: str) -> tuple[str, bool]:
    """Return (english_text, used_gemini)."""
    text = apply_dictionary(text)
    if sinhala_ratio(text) == 0:
        return text, False
    translated = gemini_client.ask(TRANSLATE_PROMPT.format(text=text))
    if translated:
        return translated, True
    return text, False
