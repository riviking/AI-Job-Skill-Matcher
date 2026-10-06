# Team workflow rules

## Branches
```
main      <- stable, demo-ready code only (protected)
dev       <- integration branch, everyone merges here
feature/* <- one branch per task, created from dev
fix/*     <- bug fixes, created from dev
```

| Branch | Owner |
|---|---|
| feature/data-cleaning | Member 1 |
| feature/translation | Member 2 |
| feature/skill-extraction | Member 2 |
| feature/matching | Member 3 |
| feature/gap-recommender | Member 3 |
| feature/streamlit-ui | Member 4 |

## Daily steps
```bash
git checkout dev
git pull origin dev                 # always get latest first
git checkout -b feature/my-task     # or: git checkout feature/my-task && git merge dev
# ... work ...
git add .
git commit -m "Add Sinhala language detection"
git push origin feature/my-task
```
Then open a Pull Request on GitHub: **base = dev**, **compare = your branch**.

## Rules
1. Never push directly to `main` (or `dev`).
2. One task = one branch = one Pull Request.
3. Every PR needs 1 approval from another member.
4. Write `Closes #<issue number>` in the PR description.
5. Run `pytest` before opening a PR.
6. Commit messages: start with a verb, say what changed ("Fix empty PDF error in input handler").
7. Never commit datasets over 50 MB, volunteer CVs, or passwords/API keys.
8. `dev` -> `main` merge is done by the leader once a week after testing.

## Fixing merge conflicts
```bash
git checkout feature/my-task
git pull origin dev        # conflicts appear here
# edit files, keep the right code, remove <<<<<<< ======= >>>>>>> markers
git add .
git commit -m "Resolve merge conflict with dev"
git push
```
Stuck? Ask in the group before force-pushing anything.
