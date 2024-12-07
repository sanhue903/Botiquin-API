from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

class Question(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    text: Mapped[str] = mapped_column()
    chapter_id: Mapped[str] = mapped_column(db.String(6), ForeignKey('chapter.id'))
    number: Mapped[int] 
    
    scores: Mapped[List['Score']] = db.relationship(backref='question', lazy=True)
    
    def __init__(self, id, chapter_id, number, text):
        self.id = id
        self.text = text
        self.chapter_id = chapter_id
        self.number = number
        
    def __repr__(self):
        return f'<Question {self.id}: {self.text}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'chapter_id': self.chapter_id
        }
    
class Chapter(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    name: Mapped[str] = mapped_column()
    number: Mapped[int] 

    app_id: Mapped[str] = mapped_column(db.String(6), ForeignKey('application.id'))
    
    questions: Mapped[List[Question]] = db.relationship(backref='chapter', lazy=True)
    
    def __init__(self, id, app_id, number, name):
        self.id = id
        self.app_id = app_id
        self.number = number
        self.name = name
        
    def __repr__(self):
        return f'<Chapter {self.id}: {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'app_id': self.app_id
        }
class Application(db.Model):
    id: Mapped[str] = mapped_column(db.String(6), primary_key=True)
    name: Mapped[str] = mapped_column()


    chapters: Mapped[List[Chapter]] = db.relationship(backref='application', lazy=True)
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
 
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def __repr__(self):
        return f'<App {self.id}: {self.name}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

