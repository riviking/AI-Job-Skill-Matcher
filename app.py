"""Streamlit UI. Owner: Rivindu.   Run:  streamlit run app.py

Screen 1 (Input)  -> Screen 2 (Skill review) -> Screen 3 (Results)
Each block below is marked with the member whose module it calls.
"""
import datetime as dt
import uuid
import pandas as pd
import streamlit as st

from core import input_handler, language, skill_extractor, matcher, gap_analyzer, recommender, report
from utils import config
from utils.data_loader import load_skills

st.set_page_config(page_title="AI Job & Skill Matcher", page_icon="🎯", layout="centered")

ss = st.session_state
ss.setdefault("step", 1)
ss.setdefault("skills", [])
ss.setdefault("lang_note", "")
ss.setdefault("session_id", str(uuid.uuid4())[:8])


def go(step: int):
    ss.step = step


# ---------------- Header ----------------
st.title("🎯 AI Job & Skill Matcher")
st.caption(f"Step {ss.step} of 3")
if not config.get_gemini_key():
    st.warning("Gemini API key not set: Sinhala translation and AI skill extraction are limited. "
               "See README > Gemini setup.")

# ---------------- Screen 1: Input  [Rivindu UI | Mathu input+skills | Hijaz translation] ----------------
if ss.step == 1:
    st.subheader("Find jobs that match your skills")
    st.write("Upload your CV or type your skills. English or Sinhala.")
    mode = st.radio("Input type", ["Upload CV", "Type skills"], horizontal=True)
    text = ""
    if mode == "Upload CV":
        file = st.file_uploader("CV (PDF or DOCX, max 5 MB)", type=list(config.ALLOWED_TYPES))
    else:
        text = st.text_area("Your skills, modules or projects",
                            placeholder="e.g. Python, Excel, data analysis, teamwork  /  පරිගණක ක්‍රමලේඛනය, ගිණුම්කරණය")

    c1, c2 = st.columns(2)
    ss.job_type = c1.selectbox("Job type", ["All", "Internship", "Full-time", "Part-time"])
    ss.field = c2.selectbox("Field", ["All", "IT", "Business", "Engineering", "Science", "Arts", "Other"])

    if st.button("Analyse my skills", type="primary"):
        if mode == "Upload CV":
            ok, err = input_handler.validate_file(file)
            if not ok:
                st.error(err)
                st.stop()
            text = input_handler.read_file(file)
            if not text.strip():
                st.error("We couldn't read text from this file. Please type your skills instead.")
                st.stop()
        if not text.strip():
            st.error("Please enter your skills.")
            st.stop()

        with st.spinner("Reading your skills..."):
            ss.lang_note = ""
            if language.detect_language(text) == "si":
                text, used_gemini = language.translate_si_en(text)
                ss.lang_note = "Sinhala detected - translated to English" + ("" if used_gemini else " (dictionary only)")
            ss.skills = skill_extractor.extract_skills(text)
        go(2)
        st.rerun()
    st.caption("🔒 Your CV is not stored after this session.")

# ---------------- Screen 2: Skill review  [Rivindu UI | Mathu skills | Hijaz language note | Rivindu skill list] ----------------
elif ss.step == 2:
    st.subheader("Check your skills")
    if ss.lang_note:
        st.info(ss.lang_note)
    if not ss.skills:
        st.warning("No skills found. Please add your skills below.")
    all_skills = sorted(load_skills().skill_name.tolist())
    ss.skills = st.multiselect("We found these skills (remove wrong ones, add missing ones)",
                               options=all_skills, default=[s for s in ss.skills if s in all_skills])
    b1, b2 = st.columns(2)
    b1.button("← Back", on_click=go, args=(1,))
    if b2.button("Find matching jobs →", type="primary", disabled=not ss.skills):
        go(3)
        st.rerun()

# ---------------- Screen 3: Results  [Rivindu UI | Yoosuf matching | Niroshan gap, courses, tip] ----------------
elif ss.step == 3:
    st.subheader("Your top job matches")
    with st.spinner("Matching jobs..."):
        scores = matcher.score_jobs(ss.skills)
        top = matcher.top_k(scores, job_type=ss.get("job_type", "All"), field=ss.get("field", "All"))

    results = []
    for job in top.itertuples():
        gap = gap_analyzer.compare(ss.skills, job.job_id)
        courses = recommender.recommend_courses(gap["missing"])
        results.append({"title": job.title, "score": job.score, **gap, "courses": courses})

        with st.container(border=True):
            st.markdown(f"**{job.title}**  ·  {job.field} · {job.job_type} · {job.location}")
            st.progress(min(float(job.score), 1.0), text=f"{job.score:.0%} match")
            st.markdown("✅ **You have:** " + (", ".join(gap["have"]) or "—"))
            st.markdown("❌ **Missing:** " + (", ".join(gap["missing"]) or "Nothing — great match!"))
            for skill, items in courses.items():
                for c in items:
                    st.markdown(f"📘 {skill}: [{c['title']}]({c['url']}) · {c['provider']}")
            if st.toggle("💡 AI tip", key=f"tip_{job.job_id}"):
                tip = recommender.career_tip(job.title, gap["have"], gap["missing"])
                st.write(tip or "Tip not available (Gemini key not set).")

    if top.empty:
        st.info("No jobs match these filters. Try 'All'.")

    # Skill gap summary chart
    missing_all = pd.Series([m for r in results for m in r["missing"]]).value_counts()
    if not missing_all.empty:
        st.markdown("**Most common missing skills**")
        st.bar_chart(missing_all)

    d1, d2 = st.columns(2)
    d1.download_button("⬇ Download PDF report", data=report.make_pdf(ss.skills, results),
                       file_name="job_matches.pdf", mime="application/pdf")
    d2.button("Start again", on_click=go, args=(1,))

    # Feedback
    st.divider()
    rating = st.radio("Was this useful?", [1, 2, 3, 4, 5], horizontal=True, index=None)
    if st.button("Submit feedback") and rating:
        row = pd.DataFrame([{"session_id": ss.session_id, "timestamp": dt.datetime.now().isoformat(),
                             "skills_found": len(ss.skills), "rating": rating}])
        row.to_csv(config.FEEDBACK_CSV, mode="a", index=False, header=not config.FEEDBACK_CSV.exists())
        st.success("Thank you!")
