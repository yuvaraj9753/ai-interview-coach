from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    resume = Column(Text)
    jd = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("InterviewQuestion", back_populates="session")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"))
    question = Column(Text)
    question_number = Column(Integer)

    session = relationship("InterviewSession", back_populates="questions")
    answers = relationship("InterviewAnswer", back_populates="question")


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id"))
    answer = Column(Text)
    feedback = Column(Text)
    score = Column(String)

    question = relationship("InterviewQuestion", back_populates="answers")