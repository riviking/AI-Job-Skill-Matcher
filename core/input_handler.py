"""Read and validate uploaded CVs. Owner: Member 2."""
from utils import config


def validate_file(file) -> tuple[bool, str]:
    """Return (is_valid, error_message). Check type and size."""
    raise NotImplementedError


def read_pdf(file) -> str:
    """Extract text from a PDF using PyPDF2."""
    raise NotImplementedError


def read_docx(file) -> str:
    """Extract text from a DOCX using python-docx."""
    raise NotImplementedError
