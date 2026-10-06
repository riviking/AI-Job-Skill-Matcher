"""Streamlit UI. Owner: Member 4. Run: streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="AI Job & Skill Matcher", page_icon="🎯", layout="centered")

st.title("AI Job & Skill Matcher")
st.caption("Upload your CV or type your skills. English or Sinhala.")

mode = st.radio("Input type", ["Upload CV", "Type skills"], horizontal=True)
if mode == "Upload CV":
    st.file_uploader("CV (PDF or DOCX, max 5 MB)", type=["pdf", "docx"])
else:
    st.text_area("Your skills or modules")

col1, col2 = st.columns(2)
col1.selectbox("Job type", ["All", "Internship", "Full-time", "Part-time"])
col2.selectbox("Field", ["All", "IT", "Business", "Engineering", "Science", "Arts", "Other"])

if st.button("Analyse my skills", type="primary"):
    st.info("Pipeline not connected yet - see core/ modules.")

st.caption("Your CV is not stored after this session.")
