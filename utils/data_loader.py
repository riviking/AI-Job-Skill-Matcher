"""Load data and models once (cached). Owner: Member 1."""
import pandas as pd
import numpy as np
from utils import config


def load_jobs() -> pd.DataFrame:
    # TODO: wrap with @st.cache_data in app.py
    return pd.read_csv(config.JOBS_CSV)


def load_job_embeddings() -> np.ndarray:
    return np.load(config.JOB_EMBEDDINGS)


def load_match_model():
    # TODO: wrap with @st.cache_resource in app.py
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(config.MATCH_MODEL)
