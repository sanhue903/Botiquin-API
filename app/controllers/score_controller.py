from app.views import get_scores_view
from app.models import User, Application, Student

from .utils import get_object, validate_role, validate_data

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('score', __name__)

@bp.route('<student_id>/scores', methods=['GET'])
@jwt_required(locations=['headers'])
def get_scores(app_id: str, student_id: int | None):

    user = get_object(User, get_jwt_identity(), "Usuario no encontrado")

    validate_role(user, "default") 
    
    app = get_object(Application, app_id, "Aplicación no encontrada")

    if student_id is not None:
        get_object(Student, student_id, "Estudiante no encontrado")
    
    return get_scores_view(app.id, student_id)