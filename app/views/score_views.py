from flask import jsonify, request
from app.extensions import db, ma
from app.models import Score
from marshmallow import ValidationError
from app.views.utils import filter_query, get_items_from_query

def parse_json(scores, app, chapter, question):
    results = []
    for chapter_it in app.chapters if len(chapter) == 0 else chapter:     
        for question_it in chapter_it.questions if len(question) == 0 else question:    
            for score in scores[:]:
                score_data = {
                    'student_id': score.student_id,
                    'chapter_id': chapter_it.id,
                    'question_id': question_it.id,
                    'answer': score.answer,
                    'is_correct': score.is_correct,
                    'seconds': score.seconds,
                    'session': score.session,
                    'attempt': score.attempt,
                    'date': score.date
                }
                if score.question_id == question_it.id:
                    results.append(score_data)
                    scores.remove(score)
                            
        
    return {'scores': results}

def get_score_view(app_id, student_id):
    query = db.select(Score).where(Score.app_id == app_id)
    
    query = filter_query(query, Score, 'attempt')
    query = filter_query(query, Score, 'session')
    query = filter_query(query, Score, 'age')
    
    question_id = request.args.get('question', None, type=str)
    chapter_id = request.args.get('chapter', None, type=str)
   
    if chapter_id is None and question_id is not None:
        return jsonify({'message': 'Chapter is required to filter with Question'}), 400
    
    if chapter_id is not None:
    
     
    
    items = get_items_from_query(query, page=1, limit=None)
    
    serialize_items = parse_json(items, app_id, [], [])
    
    return jsonify(serialize_items), 200
    
def post_score_view():
    pass    