from app.models import Student
from app.extensions import db
from app.schemas import StudentSchema

from .utils import filter_query, get_items_from_query

from flask import jsonify

def get_students_view(app_id: str, student_id: int | None):
    query = db.select(Student)

    if student_id is not None:
        query = query.where(Student.id == student_id)
    
    else:
        query = filter_query(query, Student, 'age')
    
    items = get_items_from_query(query, page=1, limit=None)
    
    serialize_items = StudentSchema(many=True).dump(items)
    
    return jsonify({'students': serialize_items}), 200
    

def post_student_view(app_id: str):
    data = request.get_json()
    data['app_id'] = app_id
    
    db.session.add(validated_data)
    db.session.commit()
    
    return jsonify({'student': schema.dump(validated_data)}), 201
    