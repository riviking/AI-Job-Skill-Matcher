from core.matcher import score_jobs


def test_tfidf_ranks_relevant_job_first():
    scores = score_jobs(["Python", "Machine Learning", "Statistics"], method="tfidf")
    assert scores.iloc[0].job_id == "J003"
    assert scores.score.between(0, 1).all()
