from core.gap_analyzer import compare


def test_gap():
    result = compare(["Python", "Statistics"], "J003")
    assert "Machine Learning" in result["missing"]
    assert "Python" in result["have"]
