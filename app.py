import streamlit as st
import requests
from PyPDF2 import PdfReader
import os

st.title("🤖 AI Interview Coach")

API_URL ="https://ai-interview-coach-2-294d.onrender.com"


# ---------- STATE ----------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "history" not in st.session_state:
    st.session_state.history = []


# ---------- SUMMARY ----------
def show_summary():
    st.markdown("## 📊 Final Summary")

    if not st.session_state.history:
        st.warning("No data available")
        return

    for i, item in enumerate(st.session_state.history):
        st.markdown(f"### Q{i+1}")
        st.write(item)

    st.success("Interview Completed 🚀")


# ---------- INPUT ----------
domain = st.selectbox("Domain", [
    "Data Science", "Machine Learning", "GenAI",
    "Backend Developer", "Frontend Developer", "DevOps"
])

mode = st.selectbox("Mode", ["Beginner", "Real Interview", "FAANG"])

file = st.file_uploader("Upload Resume (PDF)")
resume = ""

if file:
    pdf = PdfReader(file)
    for p in pdf.pages:
        resume += p.extract_text() or ""

jd = st.text_area("Job Description")


# ---------- START ----------
if st.button("Start Interview"):

    st.session_state.questions = []
    st.session_state.history = []

    r = requests.post(
        f"{API_URL}/question",
        json={
            "resume": resume,
            "jd": jd,
            "domain": domain,
            "mode": mode,
            "history": []
        }
    )



    data = r.json()

    if "q" in data:
        st.session_state.questions.append(data["q"])
    else:
        st.error(f"API Error: {data}")

    