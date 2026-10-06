import pytest


@pytest.mark.skip(reason="implement missing_skills first")
def test_missing_skills_basic():
    from core.gap_analyzer import missing_skills
    assert missing_skills(["Python"], "J0001") == ["SQL"]
