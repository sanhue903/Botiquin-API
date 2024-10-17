import uuid
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from typing import List

from app.extensions import db
class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, name):
        self.name = name

class User(db.Model):
    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email:      Mapped[str] = mapped_column(db.String(50), unique=True)
    password:   Mapped[str] = mapped_column(nullable=False)
    
    role: Mapped[List[Role]] = db.relationship(secondary='user_roles', backref='users')
    
    #aules: Mapped[List['Aule']] = db.relationship(backref='user', lazy=True)
    
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.set_password(password)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    


class UserRole(db.Model):
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), primary_key=True)
    
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id