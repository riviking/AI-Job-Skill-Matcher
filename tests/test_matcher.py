from core.matcher import score_jobs


def test_tfidf_ranks_relevant_job_first():
    scores = score_jobs(["Python", "Machine Learning", "Statistics"], method="tfidf")
    assert scores.iloc[0].job_id in ["J003", "J1357"]
    assert scores.score.between(0, 1).all()