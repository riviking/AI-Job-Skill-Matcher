import pytest

from scripts.evaluate import mean_reciprocal_rank, ndcg_at_k, precision_at_k


def test_precision_at_k_uses_fixed_k_denominator():
    assert precision_at_k(["J1", "J2", "J3"], {"J1", "J3"}, k=5) == pytest.approx(0.4)


def test_ndcg_at_k_is_one_for_ideal_binary_ranking():
    assert ndcg_at_k(["J1", "J3", "J2"], {"J1", "J3"}, k=3) == pytest.approx(1.0)


def test_ndcg_at_k_rewards_relevant_jobs_near_the_top():
    ideal = ndcg_at_k(["J1", "J3", "J2"], {"J1", "J3"}, k=3)
    lower = ndcg_at_k(["J2", "J1", "J3"], {"J1", "J3"}, k=3)
    assert ideal > lower


def test_mrr_uses_the_first_relevant_result():
    assert mean_reciprocal_rank(["J1", "J2", "J3"], {"J2", "J3"}) == pytest.approx(0.5)
    assert mean_reciprocal_rank(["J1", "J2"], {"J3"}) == 0.0


def test_ranking_metrics_reject_non_positive_k():
    with pytest.raises(ValueError, match="k must be greater than zero"):
        precision_at_k(["J1"], {"J1"}, k=0)
    with pytest.raises(ValueError, match="k must be greater than zero"):
        ndcg_at_k(["J1"], {"J1"}, k=-1)
