from app.views import get_scores_view, post_scores_view
from app.models import User, Application, Student, Chapter, Question
from app.schemas import PostSessionSchema
from app.exceptions import APINotFoundError

from .utils import get_object, validate_role, validate_data

from typing import Optional
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

import uuid

bp = Blueprint('score', __name__)

@bp.route('/scores/', methods=['GET'])
@bp.route('/<student_id>/scores/', methods=['GET'])
@jwt_required()
def get_scores(app_id: str, student_id: Optional[int] = None):
    user_id = uuid.UUID(get_jwt_identity())
    user = get_object(User, user_id, "Usuario no encontrado")

    validate_role(user, "default") 
    
    app = get_object(Application, app_id, "Aplicación no encontrada")

    if student_id is not None:
        get_object(Student, student_id, "Estudiante no encontrado")

    return get_scores_view(app, student_id)

@bp.route('/<student_id>/scores/', methods=['POST'])
@jwt_required(locations=['headers'])
def post_scores(app_id:str, student_id: int):
    user_id = uuid.UUID(get_jwt_identity())
    user = get_object(User, user_id, "Usuario no encontrado")

    validate_role(user, "app") 
    
    app = get_object(Application, app_id, "Aplicación no encontrada")

    if student_id is not None:
        student = get_object(Student, student_id, "Estudiante no encontrado")

    data = validate_data(PostSessionSchema())
    
    chapter = get_object(Chapter, data['chapter_id'], "Capitulo no encontrado")
    if chapter.id not in [c.id for c in app.chapters]:
        raise APINotFoundError(f'Capitulo con id {chapter.id} no pertenece a la aplicación {app.id}')

    for scores in data['scores']:
        question = get_object(Question, scores['question_id'], "Pregunta no encontrada")
        
        if question.id not in [q.id for q in chapter.questions]:
            raise APINotFoundError(f'Pregunta con id {question.id} no pertenece al capitulo {chapter.id}')
       
    return post_scores_view(chapter, student, data)