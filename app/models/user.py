import uuid
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from typing import List

from app.extensions import db
class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)

    users: Mapped[List['User']] = db.relationship(secondary='user_roles', backref='roles')
    
    def __init__(self, name):
        self.name = name

class User(db.Model):
    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email:      Mapped[str] = mapped_column(db.String(50), unique=True)
    password:   Mapped[str] = mapped_column(nullable=False)
    
    role: Mapped[int] = mapped_column(db.Integer, ForeignKey('role.id'))
    
    #aules: Mapped[List['Aule']] = db.relationship(backref='user', lazy=True)
    
    def __init__(self, email, password):
        self.id = uuid.uuid4()
        self.email = email
        self.set_password(password)
        
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def has_role(self, role):
        return bool(
            db.session.scalar(
                db.select(Role).where(Role.id == self.role).where(Role.name == role)
            )
        )
    
