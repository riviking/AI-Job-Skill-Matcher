from core.language import detect_language, apply_dictionary


def test_detect_sinhala():
    assert detect_language("මට ගිණුම්කරණය පුළුවන්") == "si"
    assert detect_language("I know Python") == "en"


def test_dictionary_translation():
    assert "Accounting" in apply_dictionary("ගිණුම්කරණය")
