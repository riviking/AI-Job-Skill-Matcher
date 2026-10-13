"""Precompute job embeddings once (run in Colab or locally). Owner: Yoosuf.
    python -m scripts.build_embeddings
Run again every time jobs_clean.csv or job_skills.csv changes."""
import numpy as np
from utils import config
from core.matcher import all_job_texts, load_sentence_model

if __name__ == "__main__":
    model = load_sentence_model(config.MATCH_MODEL)
    emb = model.encode(list(all_job_texts()), normalize_embeddings=True, show_progress_bar=True)
    np.save(config.JOB_EMBEDDINGS, emb)
    print(f"Saved {emb.shape} to {config.JOB_EMBEDDINGS}")
