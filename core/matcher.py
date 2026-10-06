"""Embed user skills and score jobs (hybrid score). Owner: Member 3."""
import pandas as pd


def embed(skills: list[str]):
    """Encode the joined skill list with the sentence model."""
    raise NotImplementedError


def score_jobs(skills: list[str]) -> pd.DataFrame:
    """Score = SEMANTIC_WEIGHT * cosine + OVERLAP_WEIGHT * overlap. Columns: job_id, title, score."""
    raise NotImplementedError


def top_k(scores: pd.DataFrame, k: int = 5, filters: dict | None = None) -> pd.DataFrame:
    raise NotImplementedError
