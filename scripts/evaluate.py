"""Evaluation helpers. Owners: Yoosuf (matching) + Hijaz (skill F1) + Rivindu (test set).
    python -m scripts.evaluate
Test set format (data/processed/test_set.csv):
    cv_id, text, true_skills (semicolon list), relevant_jobs (semicolon job_ids)
"""
import pandas as pd
from core.skill_extractor import extract_skills
from core.matcher import score_jobs
from utils import config


def prf(pred: set, true: set) -> tuple[float, float, float]:
    tp = len(pred & true)
    p = tp / len(pred) if pred else 0.0
    r = tp / len(true) if true else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def precision_at_k(ranked: list[str], relevant: set, k: int = 5) -> float:
    return sum(j in relevant for j in ranked[:k]) / k


def run(method: str = "mpnet", use_gemini: bool = False):
    test = pd.read_csv(config.DATA_DIR / "test_set.csv")
    rows = []
    for t in test.itertuples():
        pred = set(extract_skills(t.text, use_gemini=use_gemini))
        true = set(str(t.true_skills).split(";"))
        p, r, f = prf(pred, true)
        ranked = score_jobs(sorted(pred), method=method).job_id.tolist()
        p5 = precision_at_k(ranked, set(str(t.relevant_jobs).split(";")))
        rows.append({"cv_id": t.cv_id, "precision": p, "recall": r, "f1": f, "p@5": p5})
    df = pd.DataFrame(rows)
    print(df.mean(numeric_only=True).round(3))
    return df


if __name__ == "__main__":
    for m in ["tfidf", "minilm", "mpnet"]:
        print(f"\n=== {m} ===")
        run(m)
