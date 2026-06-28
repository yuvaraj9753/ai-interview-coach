from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.crud import (
    create_interview_session,
    create_interview_question,
    create_interview_answer,
    get_interview_session,
    get_all_sessions,
    get_session_details,
    get_dashboard_stats
)

from backend.services.logic import (
    generate_question,
    evaluate_answer
)

from backend.schemas import (
    QuestionRequest,
    QuestionResponse,
    EvaluationRequest,
    EvaluationResponse
)

router = APIRouter()


# ==========================
# Generate Question
# ==========================
@router.post("/question", response_model=QuestionResponse)
def question(
    data: QuestionRequest,
    db: Session = Depends(get_db)
):

    # First Question -> Create Session
    if data.session_id is None:

        session = create_interview_session(
            db=db,
            resume=data.resume,
            jd=data.jd,
            domain=data.domain,
            mode=data.mode
        )

    else:

        session = get_interview_session(
            db=db,
            session_id=data.session_id
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Interview Session Not Found"
            )

    q = generate_question(
        data.resume,
        data.jd,
        data.domain,
        data.history,
        data.mode
    )

    question = create_interview_question(
        db=db,
        session_id=session.id,
        question=q,
        question_number=len(data.history) + 1
    )

    return {
        "q": q,
        "session_id": session.id,
        "question_id": question.id
    }


# ==========================
# Evaluate Answer
# ==========================
@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(
    data: EvaluationRequest,
    db: Session = Depends(get_db)
):

    result = evaluate_answer(
        data.q,
        data.a,
        data.mode
    )

    create_interview_answer(
        db=db,
        question_id=data.question_id,
        answer=data.a,
        feedback=result["feedback"],
        score=result["score"]
    )

    return {
        "result": result["result"],
        "feedback": result["feedback"],
        "score": result["score"]
    }


# ==========================
# Interview History
# ==========================
@router.get("/history")
def interview_history(
    db: Session = Depends(get_db)
):

    return get_all_sessions(db)


# ==========================
# Interview Details
# ==========================
@router.get("/history/{session_id}")
def interview_details(
    session_id: int,
    db: Session = Depends(get_db)
):

    interview = get_session_details(
        db=db,
        session_id=session_id
    )

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview Not Found"
        )

    return interview

# ==========================
# Dashboard
# ==========================

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):

    return get_dashboard_stats(db)