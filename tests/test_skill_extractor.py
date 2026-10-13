from core.skill_extractor import extract_skills


def test_keyword_extraction():
    skills = extract_skills("Experience in ML, MS Excel and team work", use_gemini=False)
    assert {"Machine Learning", "Excel", "Teamwork"} <= set(skills)
