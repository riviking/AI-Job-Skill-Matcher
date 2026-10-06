"""Language detection and Sinhala-to-English translation. Owner: Member 2."""


def detect_language(text: str) -> str:
    """Return "si" or "en" using langdetect."""
    raise NotImplementedError


def translate_si_en(text: str) -> str:
    """Apply Sinhala skill dictionary, then translate with NLLB (sin_Sinh -> eng_Latn)."""
    raise NotImplementedError
