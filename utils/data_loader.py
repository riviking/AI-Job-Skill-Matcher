"""Load CSV data once. Owner: Rivindu.
In app.py these are wrapped with st.cache_data / st.cache_resource."""
from functools import lru_cache
import pandas as pd
from utils import config


@lru_cache(maxsize=None)
def load_jobs() -> pd.DataFrame:
    return pd.read_csv(config.JOBS_CSV)


@lru_cache(maxsize=None)
def load_skills() -> pd.DataFrame:
    return pd.read_csv(config.SKILLS_CSV)


@lru_cache(maxsize=None)
def load_job_skills() -> pd.DataFrame:
    return pd.read_csv(config.JOB_SKILLS_CSV)


@lru_cache(maxsize=None)
def load_courses() -> pd.DataFrame:
    courses = pd.read_csv(config.COURSES_CSV)
    links = pd.read_csv(config.COURSE_SKILLS_CSV)
    skills = load_skills()[["skill_id", "skill_name"]]
    return links.merge(courses, on="course_id").merge(skills, on="skill_id")


@lru_cache(maxsize=None)
def load_sinhala_dict() -> pd.DataFrame:
    d = pd.read_csv(config.SINHALA_DICT_CSV)
    return d.merge(load_skills()[["skill_id", "skill_name"]], on="skill_id", how="left")


def job_skill_names(job_id: str) -> list[str]:
    js = load_job_skills()
    sk = load_skills()
    rows = js[js.job_id == job_id].merge(sk, on="skill_id")
    rows = rows.sort_values("importance", key=lambda s: s.map({"Required": 0, "Preferred": 1}))
    return rows.skill_name.tolist()
