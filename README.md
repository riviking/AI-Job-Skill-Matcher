# 🎯 AI Job & Skill Matcher for University Students

A web application that reads a university student's CV or skills (in **English or Sinhala**), recommends the **top 5 matching jobs and internships**, shows the **missing skills** for each job, and suggests **free courses** to learn them.

**Course:** COSC 32142 / BECS 32253 – Artificial Intelligence (Mini Project)
**University:** University of Kelaniya, Faculty of Computing and Technology

---

## ✨ Features

- Upload a CV (PDF / DOCX) or type skills directly
- Sinhala input is translated to English automatically (Sinhala dictionary + Gemini API)
- Automatic skill extraction (keyword matching + Gemini), with editable skill chips
- Top 5 job / internship matches with a match percentage
- Missing skills for each job, with free course links and a short AI learning tip
- Downloadable PDF report and a feedback rating

## 🔁 How it works

```
CV / skills ──► Sinhala? ──► Translate (Gemini) ──► Extract skills ──► Match jobs ──► Top 5 jobs ──► Missing skills + free courses
                   └── No ───────────────────────────────┘
```

---

## 👥 Team

| # | Member | Role | Branch | GitHub |
|---|---|---|---|---|
| 1 | Rivindu (Leader) | Data, cleaning, test set, Streamlit UI, PDF report, deployment, user testing | `feature/data-cleaning`, `feature/streamlit-ui` | @username |
| 2 | Mathu | Gemini client, Sinhala translation, Sinhala dictionary | `feature/translation` | @username |
| 3 | Yoosuf | Matching model, embeddings, evaluation | `feature/matching` | @username |
| 5 | Hijaz | CV input handler, skill extraction | `feature/skill-extraction` | @username |
| 6 | Niroshan | Skill gap, course recommender, courses data, AI tip | `feature/gap-recommender` | @username |

> Numbers match the tags used in the project wireframes. Ravindu (#4) left the group; his tasks were taken over by Rivindu.

## 🗂️ Who owns what

| Area | Files | Owner |
|---|---|---|
| Data, cleaning, test set | `data/`, `core/preprocess.py`, `utils/`, `notebooks/01_data_cleaning.ipynb` | Rivindu |
| Gemini + Sinhala translation | `core/gemini_client.py`, `core/language.py`, `data/processed/sinhala_dictionary.csv` | Mathu |
| Matching + evaluation | `core/matcher.py`, `scripts/` | Yoosuf |
| UI, PDF report, deployment | `app.py`, `core/report.py`, `.streamlit/` | Rivindu |
| Input + skill extraction | `core/input_handler.py`, `core/skill_extractor.py` | Hijaz |
| Skill gap + courses + AI tip | `core/gap_analyzer.py`, `core/recommender.py`, `data/processed/courses.csv`, `data/processed/course_skills.csv` | Niroshan |

---

## 🧰 Tech stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| AI / ML | Google Gemini API (`gemini-2.5-flash`, `google-genai`), sentence-transformers (`all-mpnet-base-v2`), scikit-learn |
| Data | pandas, NumPy, PyPDF2, python-docx |
| Web app | Streamlit, fpdf2 |
| Deployment | Streamlit Community Cloud |

## 🚀 Quick start

```bash
git clone https://github.com/<leader-username>/ai-job-skill-matcher.git
cd ai-job-skill-matcher
python -m venv venv
# Windows: venv\Scripts\activate   |   Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## 🔑 Gemini API key (each member)

1. Go to https://aistudio.google.com and sign in with a Google account.
2. Click **Get API key → Create API key** (free tier, no card needed).
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste your key:
   ```toml
   GEMINI_API_KEY = "AIza..."
   ```
4. Never commit `secrets.toml` or share the key on WhatsApp. If it leaks, delete it in AI Studio and create a new one.

Gemini is used for Sinhala → English translation, extra skill extraction and the optional AI tip.
**Without a key the app still works** (dictionary translation + keyword skill extraction).

## 🛠️ Useful commands

```bash
pytest                              # run all unit tests
python -m scripts.build_embeddings  # rebuild job embeddings after jobs_clean.csv / job_skills.csv change
python -m scripts.evaluate          # compare TF-IDF / MiniLM / MPNet on the test set
```

## 📁 Project structure

```
ai-job-skill-matcher/
├── app.py                    Streamlit UI (3 screens)
├── requirements.txt
├── core/
│   ├── input_handler.py      read and validate PDF / DOCX CVs
│   ├── gemini_client.py      Gemini API wrapper
│   ├── language.py           Sinhala detection + translation
│   ├── preprocess.py         text cleaning, skill aliases
│   ├── skill_extractor.py    keyword + Gemini skill extraction
│   ├── matcher.py            sentence-transformer job matching
│   ├── gap_analyzer.py       have / missing skills
│   ├── recommender.py        free courses + AI tip
│   └── report.py             PDF report
├── utils/
│   ├── config.py             all settings (models, weights, paths)
│   └── data_loader.py        load CSV data
├── data/
│   ├── raw/                  raw data (NOT committed – keep in Google Drive)
│   └── processed/            cleaned CSVs + job embeddings
├── scripts/                  build_embeddings.py, evaluate.py
├── notebooks/                Colab notebooks
├── tests/                    pytest unit tests
└── docs/                     documents, diagrams, mockups
```

> The CSV files in `data/processed/` are **small samples** so the app runs from day 1. Rivindu replaces them with the real dataset.

## 🌐 Deployment

Deployed on Streamlit Community Cloud from the `main` branch. The Gemini key is stored in the app's **Settings → Secrets**, never in the repository.

## 🤝 How we work

- Never push directly to `main` or `dev`; work on your own `feature/*` branch.
- Open a Pull Request into `dev`; it must be approved by the next person in the review circle:
  **Rivindu → Hijaz → Mathu → Yoosuf → Niroshan → Rivindu**
- Run `pytest` before opening a PR.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow, commit message rules and how to fix merge conflicts.
