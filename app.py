import streamlit as st
import requests
from PyPDF2 import PdfReader

st.title("🤖 AI Interview Coach")

API_URL = "https://ai-interview-coach-2-294d.onrender.com"

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
    "Data Science",
    "Machine Learning",
    "GenAI",
    "Backend Developer",
    "Frontend Developer",
    "DevOps"
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

    try:
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

    except Exception as e:
        st.error(f"Error: {e}")

# ---------- FLOW ----------
for i, q in enumerate(st.session_state.questions):

    st.markdown(f"### Q{i+1}: {q}")

    ans = st.text_area("Your Answer", key=f"ans_{i}")

    col1, col2, col3 = st.columns(3)

    # SUBMIT
    with col1:
        if st.button("Submit", key=f"sub_{i}"):

            try:
                r = requests.post(
                    f"{API_URL}/evaluate",
                    json={
                        "q": q,
                        "a": ans,
                        "mode": mode
                    }
                )

                data = r.json()

                if "result" in data:
                    st.session_state.history.append(data["result"])
                else:
                    st.error(f"API Error: {data}")

            except Exception as e:
                st.error(f"Error: {e}")

    # NEXT
    with col2:
        if st.button("Next", key=f"next_{i}"):

            try:
                r = requests.post(
                    f"{API_URL}/question",
                    json={
                        "resume": resume,
                        "jd": jd,
                        "domain": domain,
                        "mode": mode,
                        "history": st.session_state.questions
                    }
                )

                data = r.json()

                if "q" in data:
                    st.session_state.questions.append(data["q"])
                else:
                    st.error(f"API Error: {data}")

            except Exception as e:
                st.error(f"Error: {e}")

    # END
    with col3:
        if st.button("End", key=f"end_{i}"):

            show_summary()
            st.stop()

    # SHOW RESULT
    if i < len(st.session_state.history):
        st.success(st.session_state.history[i])