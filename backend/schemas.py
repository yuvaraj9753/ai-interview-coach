from pydantic import BaseModel
from typing import List, Optional


class QuestionRequest(BaseModel):
    resume: str
    jd: str
    domain: str
    mode: str
    history: List[str] = []
    session_id: Optional[int] = None


class QuestionResponse(BaseModel):
    q: str
    session_id: int
    question_id: int


class EvaluationRequest(BaseModel):
    question_id: int
    q: str
    a: str
    mode: str


class EvaluationResponse(BaseModel):
    result: str
    score: str
    feedback: str


# ==========================
# Interview History
# ==========================

class HistoryItem(BaseModel):
    session_id: int
    domain: str
    mode: str
    created_at: str
    total_questions: int


class HistoryQuestion(BaseModel):
    question_number: int
    question: str
    answer: Optional[str] = None
    score: Optional[str] = None
    feedback: Optional[str] = None