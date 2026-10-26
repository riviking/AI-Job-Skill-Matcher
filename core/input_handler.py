"""Read and validate uploaded CVs. Owner: Hijaz."""
import io
from utils import config


def validate_file(file) -> tuple[bool, str]:
    """Return (is_valid, error_message). `file` is a Streamlit UploadedFile."""
    if file is None:
        return False, "Please upload a file."
    ext = file.name.rsplit(".", 1)[-1].lower()
    if ext not in config.ALLOWED_TYPES:
        return False, "Only PDF or DOCX files are allowed."
    if file.size > config.MAX_FILE_MB * 1024 * 1024:
        return False, f"File too large. Maximum size is {config.MAX_FILE_MB} MB."
    return True, ""


def read_pdf(data: bytes) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(data))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def read_docx(data: bytes) -> str:
    import docx
    document = docx.Document(io.BytesIO(data))
    return "\n".join(p.text for p in document.paragraphs)


def read_file(file) -> str:
    """Read an uploaded file and return its text ('' if no text found, e.g. scanned PDF)."""
    data = file.getvalue()
    if file.name.lower().endswith(".pdf"):
        return read_pdf(data)
    return read_docx(data)
