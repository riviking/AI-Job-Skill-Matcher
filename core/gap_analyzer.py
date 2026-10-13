"""Find which skills a student has and which are missing for a job. Owner: Niroshan."""
from utils.data_loader import job_skill_names


def compare(user_skills: list[str], job_id: str) -> dict[str, list[str]]:
    user = {s.lower() for s in user_skills}
    needed = job_skill_names(job_id)          # Required first, then Preferred
    return {
        "have": [s for s in needed if s.lower() in user],
        "missing": [s for s in needed if s.lower() not in user],
    }


def missing_skills(user_skills: list[str], job_id: str) -> list[str]:
    return compare(user_skills, job_id)["missing"]
