#!/usr/bin/env bash
# Run ONCE by the leader after the first push to main. Creates dev + feature branches on GitHub.
set -e
git checkout main
git pull origin main
git checkout -b dev
git push -u origin dev
for b in feature/data-cleaning feature/translation feature/skill-extraction \
         feature/matching feature/gap-recommender feature/streamlit-ui; do
  git checkout dev
  git checkout -b "$b"
  git push -u origin "$b"
done
git checkout dev
echo "Done. Branches created:"
git branch -a
