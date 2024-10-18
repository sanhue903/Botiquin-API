from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Application, Student
from app.controllers.utils import check_id, check_user
from app.views import get_score_view

bp = Blueprint('score', __name__)

@bp.route('/<student_id>/scores',methods=['GET'])
@jwt_required(locations=['headers'])
def get_scores(app_id: str, student_id: int):
    if not check_user(get_jwt_identity()):
        return jsonify({'message': 'User not found'}), 404

    if not check_id(Application, app_id):
        return jsonify({'message': 'App not found'}), 404
    
    if not check_id(Student, student_id):
        return jsonify({'message': 'Student not found'}), 404
    
    return get_score_view(app_id, student_id)

