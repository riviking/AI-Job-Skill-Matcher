"""Text cleaning and skill name normalisation. Owner: Member 1."""


def clean_text(text: str) -> str:
    """Lowercase, remove HTML, URLs, emails, phone numbers, symbols, extra spaces."""
    raise NotImplementedError


def normalise_skill(skill: str) -> str:
    """Map aliases to canonical skill names (e.g. "ms excel" -> "Excel")."""
    raise NotImplementedError
