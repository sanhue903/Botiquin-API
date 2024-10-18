from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Application
from app.controllers.utils import check_id, check_user
from app.views import student_get_view, student_post_view

bp = Blueprint('students', __name__)

@bp.route('/<student_id>',methods=['GET'])
@jwt_required(locations=['headers'])
def get_students(app_id: str, student_id: int | None):
    if not check_id(Application, app_id):
        return jsonify({'message': 'App not found'}), 404
    
    if not check_user(get_jwt_identity()):
        return jsonify({'message': 'User not found'}), 404

    return student_get_view(app_id, student_id)

@bp.route('',methods=['POST'])
@jwt_required(locations=['headers'])
def post_students(app_id: str):
    if not check_id(Application, app_id):
        return jsonify({'message': 'App not found'}), 404
    
    if get_jwt_identity() != app_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    return student_post_view(app_id)