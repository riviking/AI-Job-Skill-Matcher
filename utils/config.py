"""Central settings. Change values here, not inside modules. Owner: Rivindu."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "processed"

JOBS_CSV = DATA_DIR / "jobs_clean.csv"
SKILLS_CSV = DATA_DIR / "skills.csv"
JOB_SKILLS_CSV = DATA_DIR / "job_skills.csv"
COURSES_CSV = DATA_DIR / "courses.csv"
COURSE_SKILLS_CSV = DATA_DIR / "course_skills.csv"
SINHALA_DICT_CSV = DATA_DIR / "sinhala_dictionary.csv"
JOB_EMBEDDINGS = DATA_DIR / "job_embeddings.npy"
FEEDBACK_CSV = DATA_DIR / "feedback.csv"

# Models
MATCH_MODEL = "sentence-transformers/all-mpnet-base-v2"
FALLBACK_MATCH_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.5-flash"     # free tier model (check ai.google.dev if it changes)

# Matching
SEMANTIC_WEIGHT = 0.7                 # tuned on validation set (see Model Evaluation Plan)
OVERLAP_WEIGHT = 0.3
TOP_K = 5

# Input
MAX_FILE_MB = 5
ALLOWED_TYPES = ("pdf", "docx")


def get_gemini_key() -> str | None:
    """Read the key from env var or Streamlit secrets. Returns None if not set."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None
