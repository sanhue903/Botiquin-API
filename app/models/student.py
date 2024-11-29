from sqlalchemy import ForeignKey
from sqlalchemy.sql import functions
from sqlalchemy.orm import Mapped, mapped_column

from typing import List
import datetime

from app.extensions import db

class Score(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str] = mapped_column(default='')
    seconds: Mapped[float] = mapped_column(default=0.0)
    is_correct: Mapped[bool] = mapped_column(default=False)
    date: Mapped[datetime.datetime] = mapped_column(db.DateTime(timezone=True), server_default=functions.now())
    attempt: Mapped[int] = mapped_column(default=1)
    session: Mapped[int] = mapped_column(default=0)

    student_id: Mapped[int] = mapped_column(ForeignKey('student.id'))
    question_id: Mapped[str] = mapped_column(ForeignKey('question.id'))
    
    def __init__(self, student_id: int, question_id: str, answer: str, seconds: float, is_correct: bool, date: datetime.datetime=datetime.datetime.now(), attempt: int=1, session: int=0):
        self.student_id  = student_id
        self.question_id = question_id
        self.seconds     = seconds
        self.is_correct  = is_correct
        self.answer      = answer
        self.date        = date
        self.attempt     = attempt
        self.session     = session

    def __repr__(self):
        return f'<Score {self.id}: {self.question_id} - {self.is_correct} - {self.seconds}>'

class Student(db.Model):
    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50))
    age:  Mapped[int]
    session: Mapped[int] = mapped_column(default=0)
    last_chapter: Mapped[int] = mapped_column(default=0)    

    app_id: Mapped[str] = mapped_column(ForeignKey('application.id'), nullable=False)

    scores: Mapped[List['Score']] = db.relationship(backref='student', lazy=True)    
    
    def __init__(self, name, age, app_id=None):
        self.name = name    
        self.age = age
        self.app_id = app_id
        
    def __repr__(self):
        return f'<Student {self.id}: {self.name}>'
        