import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Coach")

API_URL = "https://ai-interview-coach-2-294d.onrender.com"

# ==========================
# SIDEBAR
# ==========================

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Interview",
        "Interview History"
    ]
)

# ==========================
# STATE
# ==========================

if "questions" not in st.session_state:
    st.session_state.questions = []

if "question_ids" not in st.session_state:
    st.session_state.question_ids = []

if "history" not in st.session_state:
    st.session_state.history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None


# ==========================
# HISTORY API
# ==========================

def load_history():

    try:

        r = requests.get(
            f"{API_URL}/history"
        )

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return []

def load_dashboard():

    try:

        r = requests.get(
            f"{API_URL}/dashboard"
        )

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return None


# ==========================
# SUMMARY
# ==========================

def show_summary():

    st.markdown("## 📊 Final Summary")

    if not st.session_state.history:

        st.warning("No data available")

        return

    for i, item in enumerate(st.session_state.history):

        st.markdown(f"### Question {i+1}")

        st.write(item)

    st.success("Interview Completed 🚀")

# ==========================
# DASHBOARD
# ==========================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    data = load_dashboard()

    if data is None:

        st.error("Unable to load dashboard.")

    else:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Interviews",
                data["total_interviews"]
            )

        with col2:
            st.metric(
                "Total Questions",
                data["total_questions"]
            )

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "Total Answers",
                data["total_answers"]
            )

        with col4:
            st.metric(
                "Average Score",
                data["average_score"]
            )

        st.metric(
            "Best Score",
            data["best_score"]
        )

        st.markdown("---")

        st.subheader("🕒 Recent Interviews")

        for item in data["recent_interviews"]:

            st.markdown(
                f"""
**Session ID:** {item["session_id"]}

**Domain:** {item["domain"]}

**Mode:** {item["mode"]}

**Created:** {item["created_at"]}

---
"""
            )
# ==========================
# INTERVIEW PAGE
# ==========================

if menu == "Interview":

    domain = st.selectbox(
        "Domain",
        [
            "Data Science",
            "Machine Learning",
            "GenAI Engineer",
            "Backend Developer",
            "Frontend Developer",
            "DevOps",
            "AI Engineer",
            "Python Developer",
            "Java Developer",
            "C++ Developer",
            "JavaScript Developer",
            "Full Stack Developer",
            "Mobile App Developer",
            "Cloud Engineer",
            "Cybersecurity",
            "Blockchain Developer",
            "UI/UX Designer",
            "Data Engineer"
        ]
    )

    mode = st.selectbox(
        "Mode",
        [
            "Beginner",
            "Real Interview",
            "FAANG"
        ]
    )

    file = st.file_uploader(
        "Upload Resume (PDF)"
    )

    resume = ""

    if file:

        pdf = PdfReader(file)

        for p in pdf.pages:

            resume += p.extract_text() or ""

    jd = st.text_area(
        "Job Description"
    )

    if st.button("Start Interview"):

        st.session_state.questions = []
        st.session_state.question_ids = []
        st.session_state.history = []
        st.session_state.session_id = None

        try:

            r = requests.post(
                f"{API_URL}/question",
                json={
                    "resume": resume,
                    "jd": jd,
                    "domain": domain,
                    "mode": mode,
                    "history": [],
                    "session_id": None
                }
            )

            data = r.json()

            if "q" in data:

                st.session_state.questions.append(
                    data["q"]
                )

                st.session_state.question_ids.append(
                    data["question_id"]
                )

                st.session_state.session_id = data["session_id"]

            else:

                st.error(data)

        except Exception as e:

            st.error(e)
# ==========================
    # INTERVIEW FLOW
    # ==========================

    for i, q in enumerate(st.session_state.questions):

        st.markdown(f"### Question {i+1}")

        st.info(q)

        ans = st.text_area(
            "Your Answer",
            key=f"ans_{i}"
        )

        col1, col2, col3 = st.columns(3)

        # ---------- SUBMIT ----------
        with col1:

            if st.button(
                "Submit",
                key=f"submit_{i}"
            ):

                try:

                    r = requests.post(
                        f"{API_URL}/evaluate",
                        json={
                            "question_id": st.session_state.question_ids[i],
                            "q": q,
                            "a": ans,
                            "mode": mode
                        }
                    )

                    data = r.json()

                    if "result" in data:

                        output = f"""
Score: {data['score']}

Feedback:
{data['feedback']}

--------------------------------

{data['result']}
"""

                        if len(st.session_state.history) <= i:

                            st.session_state.history.append(
                                output
                            )

                        else:

                            st.session_state.history[i] = output

                    else:

                        st.error(data)

                except Exception as e:

                    st.error(e)

        # ---------- NEXT ----------
        with col2:

            if st.button(
                "Next Question",
                key=f"next_{i}"
            ):

                try:

                    r = requests.post(
                        f"{API_URL}/question",
                        json={
                            "resume": resume,
                            "jd": jd,
                            "domain": domain,
                            "mode": mode,
                            "history": st.session_state.questions,
                            "session_id": st.session_state.session_id
                        }
                    )

                    data = r.json()

                    if "q" in data:

                        st.session_state.questions.append(
                            data["q"]
                        )

                        st.session_state.question_ids.append(
                            data["question_id"]
                        )

                    else:

                        st.error(data)

                except Exception as e:

                    st.error(e)

        # ---------- END ----------
        with col3:

            if st.button(
                "End Interview",
                key=f"end_{i}"
            ):

                show_summary()

                st.stop()

        # ---------- RESULT ----------
        if i < len(st.session_state.history):

            st.success(
                st.session_state.history[i]
            )
# ==========================
# INTERVIEW HISTORY PAGE
# ==========================

elif menu == "Interview History":

    st.header("📜 Interview History")

    sessions = load_history()

    if not sessions:

        st.info("No interview history found.")

    else:

        st.subheader("Previous Interviews")

        for s in sessions:
            st.markdown(
        f"""
**Session ID:** {s['session_id']}

**Domain:** {s['domain']}

**Mode:** {s['mode']}

**Created At:** {s['created_at']}

---
"""
    )

       

        st.markdown("---")

        session_id = st.number_input(
            "Enter Session ID",
            min_value=1,
            step=1
        )

        if st.button("View Interview"):
            try:

                r = requests.get(
                    f"{API_URL}/history/{session_id}"
                )

                if r.status_code == 200:

                    interview = r.json()

                    st.success(
                        f"Interview Session #{interview['session_id']}"
                    )

                    st.write(
                        f"**Domain:** {interview['domain']}"
                    )

                    st.write(
                        f"**Mode:** {interview['mode']}"
                    )

                    st.write(
                        f"**Created At:** {interview['created_at']}"
                    )

                    st.markdown("---")

                    questions = interview["questions"]

                    if len(questions) == 0:

                        st.warning(
                            "No questions found."
                        )

                    else:

                        for item in questions:
                            st.markdown(
                                f"## Question {item['question_number']}"
                            )

                            st.info(
                                item["question"]
                            )

                            st.markdown("### Your Answer")

                            if item["answer"]:
                                st.write(
                                    item["answer"]
                                )
                            else:
                                st.warning(
                                    "Answer not available."
                                )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.metric(
                                    "Score",
                                    item["score"] if item["score"] else "N/A"
                                )

                            with col2:
                                st.write("")

                            st.markdown("### Feedback")

                            if item["feedback"]:
                                st.success(
                                    item["feedback"]
                                )
                            else:
                                st.warning(
                                    "Feedback not available."
                                )

                            st.markdown("---")

                else:

                    st.error("Interview not found.")

            except Exception as e:

                st.error(f"Error: {e}")