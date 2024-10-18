from flask import jsonify, request
from app.extensions import db, ma
from app.models import Student
from marshmallow import ValidationError
from app.views.utils import filter_query, get_items_from_query

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student 
        load_instance = True
        include_fk = True

def student_get_view(app_id: str, id: int | None):
    query = db.select(Student).where(Student.app_id == app_id)
    query = filter_query(query, Student, 'age')
    
    items = get_items_from_query(query, page=1, limit=None)
    
    serialize_items = StudentSchema(many=True).dump(items)
    
    return jsonify({'students': serialize_items}), 200
    

def student_post_view(app_id: str):
    data = request.get_json()
    data['app_id'] = app_id
    
    schema = StudentSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        print(e.messages)
        return jsonify({'message': 'Invalid data'}), 422
    
    db.session.add(validated_data)
    db.session.commit()
    
    return jsonify({'student': schema.dump(validated_data)}), 201
    