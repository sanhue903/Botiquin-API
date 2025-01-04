from sqlalchemy import ForeignKey
from sqlalchemy.sql import functions
from sqlalchemy.orm import Mapped, mapped_column

from typing import List
import datetime

from app.extensions import db

class Score(db.Model):
    id: Mapped[int]          = mapped_column(primary_key=True)
    answer: Mapped[str]      = mapped_column(nullable=False)
    seconds: Mapped[float]   = mapped_column(nullable=False)
    is_correct: Mapped[bool] = mapped_column(nullable=False)
    attempt: Mapped[int]     = mapped_column(nullable=False)

    session_id: Mapped[int]  = mapped_column(ForeignKey('session.id'), nullable=False)
    question_id: Mapped[str] = mapped_column(ForeignKey('question.id'), nullable=False)
    
    def __init__(self, answer: str, seconds: float, is_correct: bool, attempt: int, session_id: int, question_id: str):
        self.answer     = answer
        self.seconds    = seconds
        self.is_correct = is_correct
        self.attempt    = attempt

        self.session_id  = session_id
        self.question_id = question_id

class Session(db.Model):
    id: Mapped[int]                 = mapped_column(primary_key=True)
    number: Mapped[int]             = mapped_column(nullable=False)
    seconds: Mapped[float]          = mapped_column(nullable=False)
    finish_chapter: Mapped[bool]    = mapped_column(nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(db.DateTime(timezone=True), nullable=False)
    
    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    chapter_id: Mapped[str] = mapped_column(ForeignKey('chapter.id'))

    scores: Mapped[List['Score']] = db.relationship(backref='session', lazy=True)    
    

    def __init__(self, number: int, seconds: float, finish_chapter: bool, date: datetime.datetime, 
                 student_id: int, chapter_id: str):
        self.number         = number
        self.seconds        = seconds
        self.finish_chapter = finish_chapter
        self.date           = date
        
        self.student_id = student_id
        self.chapter_id = chapter_id
        
class Student(db.Model):
    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))
    age:  Mapped[int] = mapped_column(nullable=False)
    session: Mapped[int]      = mapped_column(default=0)

    app_id: Mapped[str] = mapped_column(ForeignKey('application.id'), nullable=False)

    sessions: Mapped[List['Session']] = db.relationship(backref='student', lazy=True)

    
    def __init__(self, name: str, age: int, app_id: str):
        self.name = name    
        self.age  = age

        self.app_id = app_id