from fastapi import APIRouter
from logic import generate_question, evaluate_answer

router = APIRouter()


# ---------- QUESTION ----------
@router.post("/question")
def question(data: dict):

    return {
        "q": generate_question(
            data.get("resume", ""),
            data.get("jd", ""),
            data.get("domain", ""),
            data.get("history", []),
            data.get("mode", "Beginner")
        )
    }


# ---------- EVALUATION ----------
@router.post("/evaluate")
def evaluate(data: dict):

    return {
        "result": evaluate_answer(
            data.get("q", ""),
            data.get("a", ""),
            data.get("mode", "Beginner")
        )
    }