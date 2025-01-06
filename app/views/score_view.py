from app.models import Score, Student, Chapter, Question, Application, Session
from app.extensions import db
from app.exceptions import APINotFoundError
from sqlalchemy.exc import NoResultFound

from .utils import get_less_equal_greater_filters, get_items_from_query

from typing import Optional
from flask import jsonify, request


def parse_json_get_scores(sessions):
    results = []
    for session in sessions:
        session_data = {
            "student_id": session.student_id,
            "chapter_id": session.chapter_id,
            "date": session.date,
            "number": session.number,
            "seconds": session.seconds,
            "finish_chapter": session.finish_chapter,
            "scores": []
        }

        for score in session.scores:
            score_data = {
                "question_id": score.question_id,
                "attempt": score.attempt,
                "answer": score.answer,
                "seconds": score.seconds,
                "is_correct": score.is_correct
            }
            
            session_data["scores"].append(score_data)
        
        results.append(session_data)
            

    return results

def filter_chapter(query, chapter_id):
    if chapter_id is None:
        return query
    
    if chapter_id.isdecimal():
        chapter_id = int(chapter_id)
        
        query = query.join(Session.chapter).filter(Chapter.number == chapter_id)
    else:
        query = query.filter(Session.chapter_id == chapter_id)
    
    return query

###### Not use
def filter_question(query, question_id):
    question_query = db.select(Question)

    query = query.join(Score.question)
    if question_id.isdecimal():
        question_id = int(question_id)
        
        query = query.filter(Question.number == question_id)
        question_query = question_query.filter(Question.number == question_id)

    else:
        query = query.filter(Question.id == question_id)
        question_query = question_query.filter(Question.id == question_id)

    question = db.session.scalars(question_query).all()
    if len(question) == 0:
        raise APINotFoundError("Capitulo con id o número {question_id} no existe")

    return query, question
############################################

def get_scores_view(app: Application, student_id: Optional[int]):
    query = db.select(Session).join(Session.student).where(Student.app_id == app.id)

    if student_id is not None:
        query = query.where(Session.student_id == student_id)

    chapter_id = request.args.get("chapter", None, type=str)
    query = filter_chapter(query, chapter_id) 

    items = get_items_from_query(query)

    return jsonify(parse_json_get_scores(items)), 200


def post_scores_view(chapter: Chapter, student: Student, data):
    student.session+=1
    
    last_session = db.session.scalar(
                    db.select(Session)
                    .where(Session.student_id == student.id)
                    .where(Session.chapter_id == chapter.id)
                    .order_by(Session.number.desc())
                    .limit(1)
                )
    session_number = last_session.number + 1 if last_session is not None else 1
    session = Session(
                number        = session_number, 
                seconds       = data['seconds'], 
                finish_chapter= data['finish_chapter'],
                date          = data['date'],
                student_id    = student.id,
                chapter_id    = chapter.id    
                )
    db.session.add(session)
    db.session.flush()
    
    
    for score in data["scores"]:
        new_score = Score(
            answer=score["answer"],
            seconds=score["seconds"],
            is_correct=score["is_correct"],
            attempt=score['attempt'],
            session_id=session.id,
            question_id=score["question_id"]
        )

        db.session.add(new_score)

    db.session.commit()

    return jsonify({"message": "Puntajes agregados correctamente"}), 201
