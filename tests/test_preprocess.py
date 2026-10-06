import pytest
from core.preprocess import clean_text


@pytest.mark.skip(reason="implement clean_text first")
def test_clean_text_removes_html_and_symbols():
    assert clean_text("Python!!  <b>SQL</b>") == "python sql"
