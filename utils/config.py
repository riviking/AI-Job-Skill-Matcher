"""Central settings. Change values here, not inside modules."""
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

MATCH_MODEL = "sentence-transformers/all-mpnet-base-v2"
FALLBACK_MATCH_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TRANSLATION_MODEL = "facebook/nllb-200-distilled-600M"

SEMANTIC_WEIGHT = 0.7   # tuned on validation set (see Model Evaluation Plan)
OVERLAP_WEIGHT = 0.3
TOP_K = 5
MAX_FILE_MB = 5
ALLOWED_TYPES = ("pdf", "docx")
