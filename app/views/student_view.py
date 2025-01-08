from app.models import Student
from app.extensions import db
from app.schemas import StudentSchema

from .utils import get_less_equal_greater_filters, get_items_from_query

from typing import Optional
from flask import jsonify

def get_students_view(app_id: str, student_id: Optional[int]):
    query = db.select(Student).where(Student.app_id == app_id)

    if student_id is not None:
        query = query.where(Student.id == student_id)
    
    else:
        query = get_less_equal_greater_filters(query, Student,'age')
    
    items = get_items_from_query(query)
    
    serialize_items = StudentSchema(many=True).dump(items)
    
    return jsonify(serialize_items), 200
    

def post_student_view(app_id: str, student: Student):
    student.app_id = app_id
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify(StudentSchema().dump(student)), 201
    