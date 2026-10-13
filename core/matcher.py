"""Score jobs against the user's skills. Owner: Yoosuf.

Score = SEMANTIC_WEIGHT * cosine_similarity + OVERLAP_WEIGHT * skill_overlap
method="mpnet"  -> sentence-transformers (main model)
method="minilm" -> smaller sentence-transformers model
method="tfidf"  -> baseline, also used automatically if models can't load
"""
from functools import lru_cache
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import config
from utils.data_loader import load_jobs, job_skill_names


def job_text(job_id: str, title: str) -> str:
    return f"{title}. Skills: {', '.join(job_skill_names(job_id))}"


@lru_cache(maxsize=None)
def all_job_texts() -> tuple[str, ...]:
    jobs = load_jobs()
    return tuple(job_text(r.job_id, r.title) for r in jobs.itertuples())


@lru_cache(maxsize=None)
def load_sentence_model(name: str):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name)


@lru_cache(maxsize=None)
def job_embeddings(model_name: str) -> np.ndarray:
    """Use precomputed file if it exists (scripts/build_embeddings.py), else compute."""
    if model_name == config.MATCH_MODEL and config.JOB_EMBEDDINGS.exists():
        return np.load(config.JOB_EMBEDDINGS)
    return load_sentence_model(model_name).encode(list(all_job_texts()), normalize_embeddings=True)


def semantic_scores(skills: list[str], method: str) -> np.ndarray:
    query = "Skills: " + ", ".join(skills)
    if method in ("mpnet", "minilm"):
        name = config.MATCH_MODEL if method == "mpnet" else config.FALLBACK_MATCH_MODEL
        try:
            q = load_sentence_model(name).encode([query], normalize_embeddings=True)
            return (job_embeddings(name) @ q.T).ravel()
        except Exception as e:
            print(f"[matcher] {method} unavailable ({e}); falling back to TF-IDF")
    vec = TfidfVectorizer().fit(list(all_job_texts()) + [query])
    return cosine_similarity(vec.transform([query]), vec.transform(all_job_texts())).ravel()


def overlap_scores(skills: list[str]) -> np.ndarray:
    user = {s.lower() for s in skills}
    out = []
    for job_id in load_jobs().job_id:
        needed = {s.lower() for s in job_skill_names(job_id)}
        out.append(len(user & needed) / len(needed) if needed else 0.0)
    return np.array(out)


def score_jobs(skills: list[str], method: str = "mpnet") -> pd.DataFrame:
    jobs = load_jobs().copy()
    sem = np.clip(semantic_scores(skills, method), 0, 1)
    jobs["score"] = config.SEMANTIC_WEIGHT * sem + config.OVERLAP_WEIGHT * overlap_scores(skills)
    return jobs.sort_values("score", ascending=False)


def top_k(scores: pd.DataFrame, k: int = config.TOP_K, job_type: str = "All", field: str = "All") -> pd.DataFrame:
    if job_type != "All":
        scores = scores[scores.job_type == job_type]
    if field != "All":
        scores = scores[scores.field == field]
    return scores.head(k)
