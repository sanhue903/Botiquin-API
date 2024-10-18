import uuid
from app.models import User
from app.extensions import db

def check_user_role(user_id: uuid.UUID, role: str) -> bool:
    return bool(
        db.session.scalar(
            db.select(User).where(User.role == role)
        )
    )

def check_id(type, id) -> bool:
    try:
        app = db.session.scalar(db.select(type).where(type.id == id))
    except Exception:
        return False
    
    if app is None:
        return False
    return True

def check_user(jwt_identity: dict) -> bool:
    try:
        user = db.session.scalar(db.select(User).where(User.id == jwt_identity['id']).where(User.email == jwt_identity['email']))
    except Exception:
        return False
    
    if user is None:
        return False
    return True