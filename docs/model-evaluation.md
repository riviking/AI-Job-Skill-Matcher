# Matching Model Evaluation

Run the evaluation from the repository root:

```bash
python -m scripts.evaluate
```

The script compares the TF-IDF baseline, `all-MiniLM-L6-v2`, and
`all-mpnet-base-v2`. Skill extraction uses its local, deterministic path by
default; Gemini is not used to score or rank jobs.

For each test profile, it reports skill extraction precision, recall, and F1,
plus binary-relevance Precision@5, NDCG@5, and reciprocal rank. The summary
printed for each model is the mean across profiles.

## Current smoke-set results

The checked-in test set contains three synthetic smoke profiles covering an AI
internship, an accounting role, and a junior software role. They were created
from example job records to check that the evaluation pipeline runs; their
relevance labels have not been independently reviewed. This is not a real
student benchmark and cannot support model quality claims. Replace or
supplement it with realistic student profiles and human-reviewed relevant job
IDs before drawing conclusions about model quality.

| Model | Precision@5 | NDCG@5 | MRR | Run status |
|---|---:|---:|---:|---|
| TF-IDF | 0.133 | 0.500 | 0.460 | Completed locally |
| MiniLM | 0.133 | 0.667 | 0.689 | Completed with cached weights |
| MPNet | 0.133 | 0.544 | 0.548 | Completed with cached weights |

These are macro averages from the three synthetic smoke profiles. The
transformer weights were already cached locally, so the comparison completed
in offline mode without Hugging Face authentication. The scores confirm that
the pipeline runs; the profiles and labels are too small and synthetic to
support a reliable quality claim. Use realistic profiles and human-reviewed
relevance labels for the final project evaluation.

The `relevant_jobs` values in `data/processed/test_set.csv` must exactly match
IDs in `data/processed/jobs_clean.csv`. The evaluator checks this before
running a model so stale or mistyped labels cannot silently produce zero
ranking scores.
