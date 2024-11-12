from app.models import Score, Student
from app.extensions import db

from .utils import filter_query, get_items_from_query

def parse_json_get_scores():
    pass

def get_scores_view(app_id: str, student_id: int | None):
    query = db.select(Score).join(Score.student).where(Student.app_id == app_id)
    
    if student_id is not None:
        query = query.where(Score.student_id == student_id)
    
    query = filter_query(query, Score,  'attempt')
    query = filter_query(query, Score, 'session')
    query = filter_query(query, Student, 'age')
    
    
    
    