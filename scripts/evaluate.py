"""Evaluation helpers. Owners: Yoosuf (matching) + Mathu (skill F1) + Rivindu (test set).
    python -m scripts.evaluate
Test set format (data/processed/test_set.csv):
    cv_id, text, true_skills (semicolon list), relevant_jobs (semicolon job_ids)
"""
from math import log2

import pandas as pd
from core.skill_extractor import extract_skills
from core.matcher import score_jobs
from utils import config
from utils.data_loader import load_jobs


EVALUATION_K = 5


def prf(pred: set, true: set) -> tuple[float, float, float]:
    tp = len(pred & true)
    p = tp / len(pred) if pred else 0.0
    r = tp / len(true) if true else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def precision_at_k(ranked: list[str], relevant: set, k: int = 5) -> float:
    if k <= 0:
        raise ValueError("k must be greater than zero")
    return sum(j in relevant for j in ranked[:k]) / k


def ndcg_at_k(ranked: list[str], relevant: set, k: int = EVALUATION_K) -> float:
    """Compute binary-relevance NDCG for one ranked list."""
    if k <= 0:
        raise ValueError("k must be greater than zero")
    dcg = sum(1 / log2(rank + 1) for rank, job_id in enumerate(ranked[:k], start=1) if job_id in relevant)
    ideal_relevant = min(len(relevant), k)
    ideal_dcg = sum(1 / log2(rank + 1) for rank in range(1, ideal_relevant + 1))
    return dcg / ideal_dcg if ideal_dcg else 0.0


def mean_reciprocal_rank(ranked: list[str], relevant: set) -> float:
    """Return the reciprocal rank of the first relevant result (MRR per query)."""
    for rank, job_id in enumerate(ranked, start=1):
        if job_id in relevant:
            return 1 / rank
    return 0.0


def _split_values(value: object) -> set[str]:
    if pd.isna(value):
        return set()
    return {item.strip() for item in str(value).split(";") if item.strip()}


def run(method: str = "mpnet", use_gemini: bool = False):
    test_path = config.DATA_DIR / "test_set.csv"
    test = pd.read_csv(test_path)
    required_columns = {"cv_id", "text", "true_skills", "relevant_jobs"}
    missing_columns = required_columns - set(test.columns)
    if missing_columns:
        raise ValueError(f"{test_path} is missing columns: {sorted(missing_columns)}")

    known_job_ids = set(load_jobs().job_id.astype(str))
    invalid_relevance = {
        job_id
        for value in test.relevant_jobs
        for job_id in _split_values(value)
        if job_id not in known_job_ids
    }
    if invalid_relevance:
        raise ValueError(
            "Evaluation relevance labels refer to unknown job IDs: "
            f"{sorted(invalid_relevance)}. Update {test_path} to use IDs from jobs_clean.csv."
        )

    rows = []
    for t in test.itertuples():
        pred = set(extract_skills(t.text, use_gemini=use_gemini))
        true = _split_values(t.true_skills)
        p, r, f = prf(pred, true)
        ranked = score_jobs(sorted(pred), method=method).job_id.tolist()
        relevant = _split_values(t.relevant_jobs)
        rows.append({
            "cv_id": t.cv_id,
            "precision": p,
            "recall": r,
            "f1": f,
            f"p@{EVALUATION_K}": precision_at_k(ranked, relevant, EVALUATION_K),
            f"ndcg@{EVALUATION_K}": ndcg_at_k(ranked, relevant, EVALUATION_K),
            "mrr": mean_reciprocal_rank(ranked, relevant),
        })
    df = pd.DataFrame(rows)
    print(df.mean(numeric_only=True).round(3))
    return df


if __name__ == "__main__":
    for m in ["tfidf", "minilm", "mpnet"]:
        print(f"\n=== {m} ===")
        results = run(m)
        if results.empty:
            print("No evaluation examples found.")
