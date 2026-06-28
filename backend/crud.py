from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewAnswer
)


def create_interview_session(
    db: Session,
    resume: str,
    jd: str,
    domain: str,
    mode: str
):
    session = InterviewSession(
        resume=resume,
        jd=jd,
        domain=domain,
        mode=mode
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_interview_session(
    db: Session,
    session_id: int
):
    return (
        db.query(InterviewSession)
        .filter(InterviewSession.id == session_id)
        .first()
    )


def create_interview_question(
    db: Session,
    session_id: int,
    question: str,
    question_number: int
):

    obj = InterviewQuestion(
        session_id=session_id,
        question=question,
        question_number=question_number
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def create_interview_answer(
    db: Session,
    question_id: int,
    answer: str,
    feedback: str,
    score: str
):

    obj = InterviewAnswer(
        question_id=question_id,
        answer=answer,
        feedback=feedback,
        score=score
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

def get_all_sessions(db: Session):

    sessions = (
        db.query(InterviewSession)
        .order_by(InterviewSession.created_at.desc())
        .all()
    )

    result = []

    for s in sessions:

        result.append({
            "session_id": s.id,
            "domain": s.domain,
            "mode": s.mode,
            "created_at": str(s.created_at),
            "total_questions": len(s.questions)
        })

    return result


def get_session_details(
    db: Session,
    session_id: int
):

    session = (
        db.query(InterviewSession)
        .filter(InterviewSession.id == session_id)
        .first()
    )

    if session is None:
        return None

    questions = []

    for q in session.questions:

        answer = None

        if len(q.answers) > 0:
            answer = q.answers[0]

        questions.append({

            "question_number": q.question_number,

            "question": q.question,

            "answer": answer.answer if answer else "",

            "score": answer.score if answer else "",

            "feedback": answer.feedback if answer else ""

        })

    return {
        "session_id": session.id,
        "domain": session.domain,
        "mode": session.mode,
        "created_at": str(session.created_at),
        "questions": questions
    }

def get_dashboard_stats(db: Session):

    total_interviews = db.query(InterviewSession).count()

    total_questions = db.query(InterviewQuestion).count()

    total_answers = db.query(InterviewAnswer).count()

    scores = db.query(InterviewAnswer.score).all()

    score_list = []

    for s in scores:

        if s[0]:

            try:

                value = float(
                    str(s[0]).split("/")[0]
                )

                score_list.append(value)

            except:
                pass

    average_score = (
        round(sum(score_list) / len(score_list), 2)
        if score_list else 0
    )

    best_score = (
        max(score_list)
        if score_list else 0
    )

    recent_sessions = (
        db.query(InterviewSession)
        .order_by(
            InterviewSession.created_at.desc()
        )
        .limit(5)
        .all()
    )

    recent = []

    for s in recent_sessions:

        recent.append({

            "session_id": s.id,

            "domain": s.domain,

            "mode": s.mode,

            "created_at": str(s.created_at)

        })

    return {

        "total_interviews": total_interviews,

        "total_questions": total_questions,

        "total_answers": total_answers,

        "average_score": average_score,

        "best_score": best_score,

        "recent_interviews": recent

    }