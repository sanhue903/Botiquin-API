from app.models import Score, Student, Chapter, Question, Application
from app.extensions import db
from app.exceptions import APINotFoundError
 
from .utils import filter_query, get_items_from_query

from typing import Optional
from flask import jsonify, request
 


def parse_json_get_scores(scores, app, chapter, question):
    results = [] 
    
    chapters = app.chapters if chapter is None else [chapter]

    for chapter_it in chapters:
        questions = chapter_it.questions if question is None else [question]
        
        for question_it in questions:
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

def filter_chapter(query, chapter_id):
    chapter = None

    if chapter_id is not None:
        query = query.join(Question)
        chapter_query= db.select(Chapter)
        
        if chapter_id.isdecimal():
            query = query.join(Chapter).where(Chapter.number == chapter_id)
            chapter_query = chapter_query.where(Chapter.number == chapter_id)
        
        else:
            query = query.where(Question.chapter_id == chapter_id)
            chapter_query = chapter_query.where(Chapter.id == chapter_id)
        
        if chapter := db.session.scalar(chapter_query) is None:
            raise APINotFoundError(f"Capitulo con id o número {chapter_id} no existe")

    return chapter

def filter_question(query, question_id):
    question = None

    if question_id is not None:
        question_query = db.select(Question)
        
        if question_id.isdecimal():
            query = query.join(Question)
        
            query = query.where(Question.number == question_id)
            question_query = question_query.where(Question.number)
        
        else:
            query = query.where(Score.question_id == question_id)
            question_query = question_query.where(Question.id == question_id)
        
        if question := db.session.scalars(question_query) is None:
            raise APINotFoundError("Capitulo con id o número {question_id} no existe")

    return question

def get_scores_view(app: Application, student_id: Optional[int]):
    query = db.select(Score).join(Score.student).where(Student.app_id == app.id)
    
    if student_id is not None:
        query = query.where(Score.student_id == student_id)
    
    query = filter_query(query, Score, 'attempt', 'attempt')
    query = filter_query(query, Score, 'session', 'session')
    query = filter_query(query, Student, 'age', 'age')
   
    chapter_id = request.args.get('chapter', None, type=str)
    chapter = filter_chapter(query, chapter_id)
    
    question_id = request.args.get('question', None, type=str)
    question = filter_question(query, question_id)
    
    items = get_items_from_query(query)
    
    return jsonify(parse_json_get_scores(items, app, chapter, question)), 200

def post_scores_view(app: Application, chapter: Chapter, student: Student, data):
    if chapter.number > student.last_chapter:
        student.last_chapter = chapter.number
    student.session+= 1
    
    for score in data['chapter']['scores']:
        if score['question_id'] not in [q.id for q in chapter.questions]:
            raise APINotFoundError(f"Pregunta con id {score['question_id']} no encontrado")

        last_attempt = db.session.scalar(db.select(Score)
                                        .where(Score.student_id == student.id)
                                        .where(Score.question_id == score['question_id'])
                                        .order_by(Score.attempt.desc())
                                        .limit(1)
                                    )
        
        new_score = Score(
                        student_id=student.id, 
                        question_id=score['question_id'], 
                        answer=score['answer'], 
                        seconds=score['seconds'], 
                        is_correct=score['is_correct'],
                        date=score['date'],
                        attempt=last_attempt.attempt + 1 if last_attempt is not None else 1, 
                        session=student.session
                    )
        
        db.session.add(new_score)
    
    db.session.commit()
    
    return jsonify({'message': 'Puntajes agregados correctamente'}), 201