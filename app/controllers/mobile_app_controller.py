from app.views import register_mobile_app_view, get_app_view
from app.models import User, Application
from app.schemas import PostAppSchema

from .utils import validate_data, get_object, validate_role

import uuid
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('mobile', __name__)

@bp.route('/register/', methods=['POST'])
@jwt_required(locations=['headers'])
def register_mobile_app():
    user_id = uuid.UUID(get_jwt_identity())
    user = get_object(User, user_id, "Usuario no encontrado")

    
    validate_role(user, "admin") 

    data = validate_data(PostAppSchema())
    
    return register_mobile_app_view(data)

@bp.route('/<app_id>/', methods=['GET'])
@jwt_required(locations=['headers'])
def get_app(app_id):
    user_id = uuid.UUID(get_jwt_identity())
    user = get_object(User, user_id, "Usuario no encontrado")
    validate_role(user, 'default')

    app = get_object(Application, app_id, "Aplicacion no encontrada")
    
    return get_app_view(app)

