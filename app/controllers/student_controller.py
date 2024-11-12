from app.models import User, Application
from app.views import get_students_view, post_student_view
from app.schemas import StudentSchema

from .utils import get_object, validate_role, validate_data

from flask import Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity

bp = Blueprint('student', __name__)

@bp.route('/<student_id>', methods=['GET'])
@jwt_required(locations=['headers'])
def get_students(app_id: str,student_id: int | None):
    user = get_object(User, get_jwt_identity(), "Usuario no encontrado")
    
    validate_role(user, "default")
    
    app = get_object(Application, app_id, "Aplicación no encontrada")
    
    return get_students_view(app.id, student_id)

@bp.route('', methods=['POST'])
@jwt_required(locations=['headers'])
def post_student(app_id: str):
    user = get_object(User, get_jwt_identity(), "Usuario no encontrado")

    validate_role(user, "app")

    app = get_object(Application, app_id, "Aplicación no encontrada")

    student = validate_data(StudentSchema(partial='app_id'))
    
    return post_student_view(app.id, student)