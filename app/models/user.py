import uuid
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey, event
from typing import List

from app.extensions import db
class Role(db.Model):
    """Role for give permissions to users"""
    id: Mapped[int]             = mapped_column(primary_key=True)
    name: Mapped[str]           = mapped_column(db.String(50), nullable=False, unique=True)

    users: Mapped[List['User']] = db.relationship(backref='role')
    
    
    def __init__(self, name):
        self.name = name

class User(db.Model):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str]    = mapped_column(db.String(50), unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    
    role_id: Mapped[int]  = mapped_column(db.Integer, ForeignKey('role.id'))
    
    
    def __init__(self, email: str, password: str):
        self.id    = uuid.uuid4()
        self.email = email
        
        self.set_password(password)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

@event.listens_for(Role.__table__, 'after_create')
def create_departments(*args, **kwargs):
    db.session.add(Role('default'))
    db.session.add(Role('admin'))
    db.session.add(Role('app'))
    db.session.commit()