from core.preprocess import clean_text, normalise_skill


def test_clean_text_removes_html_and_symbols():
    assert clean_text("Python!!  <b>SQL</b>") == "python sql"


def test_clean_text_keeps_cpp_and_csharp():
    assert "c++" in clean_text("I know C++ and C#.")


def test_normalise_alias():
    assert normalise_skill("MS Excel") == "Excel"
    assert normalise_skill("unknown skill") is None
