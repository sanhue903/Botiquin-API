from app.views import sign_up_view, log_in_view
from app.models import User
from app.schemas import SignUpSchema, LogInSchema
from app.extensions import db
from app.exceptions import APIConflictError, APINotFoundError, APIUnauthorizedError

from .utils import validate_data

from flask import Blueprint
bp = Blueprint('auth', __name__)

@bp.route('/signup/', methods=['POST'])
def sign_up_user():
    data = validate_data(SignUpSchema())
    
    if db.session.scalar(db.select(User).where(User.email == data['email'])):
        raise APIConflictError('Ya existe un usuario con ese email')
    
    if data['password'] != data['confirm_password']:
        raise APIConflictError('Las contraseñas no coinciden')
    
    return sign_up_view(data['email'], data['password'])

@bp.route('/login/', methods=['POST'])
def log_in():
    data = validate_data(LogInSchema())
    
    user = db.session.scalar(db.select(User).where(User.email == data['email']))

    if not user:
        raise APINotFoundError("User not found")
    
    if not user.check_password(data['password']):
        raise APIUnauthorizedError("Wrong password")

    
    
    return log_in_view(user)