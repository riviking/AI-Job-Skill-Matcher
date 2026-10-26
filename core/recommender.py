"""Recommend free courses for missing skills, plus an optional Gemini tip. Owner: Niroshan."""
from core import gemini_client
from utils.data_loader import load_courses

LEVEL_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}


def recommend_courses(skills: list[str], per_skill: int = 2) -> dict[str, list[dict]]:
    courses = load_courses()
    courses = courses[courses.is_free == True]  # noqa: E712
    result = {}
    for skill in skills:
        rows = courses[courses.skill_name.str.lower() == skill.lower()]
        rows = rows.sort_values("level", key=lambda s: s.map(LEVEL_ORDER))
        result[skill] = rows.head(per_skill)[["title", "provider", "url", "level"]].to_dict("records")
    return result


TIP_PROMPT = """A Sri Lankan university student wants the job "{job}".
They already have: {have}. They are missing: {missing}.
Write 2 short, practical sentences of advice on what to learn first and how.
Plain English, no bullet points, no markdown."""


def career_tip(job: str, have: list[str], missing: list[str]) -> str | None:
    """Optional: short personalised advice from Gemini (None if unavailable)."""
    if not missing:
        return None
    return gemini_client.ask(TIP_PROMPT.format(job=job, have=", ".join(have) or "none", missing=", ".join(missing)))
