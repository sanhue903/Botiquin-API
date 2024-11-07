from app.views import register_mobile_app_view
from app.models import User
from app.schemas import PostAppSchema

from .utils import validate_data, get_object, validate_role

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('mobile', __name__)

@bp.route('/register', methods=['POST'])
@jwt_required(locations=['headers'])
def register_mobile_app():
    user = get_object(User, get_jwt_identity(), "Usuario no encontrado") 
    
    validate_role(user, "admin") 

    data = validate_data(PostAppSchema())
    
    return register_mobile_app_view(data)
    
    
        
