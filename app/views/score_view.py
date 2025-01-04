from app.models import Score, Student, Chapter, Question, Application, Session
from app.extensions import db
from app.exceptions import APINotFoundError
from sqlalchemy.exc import NoResultFound

from .utils import get_less_equal_greater_filters, get_items_from_query

from typing import Optional
from flask import jsonify, request


def parse_json_get_scores(scores, app, chapter, question):
    results = []

    chapters = app.chapters if chapter is None else [chapter]

    for chapter_it in chapters:
        questions = chapter_it.questions if question is None else question

        for question_it in questions:
            for score in scores[:]:
                score_data = {
                    "student_id": score.student_id,
                    "chapter_id": chapter_it.id,
                    "question_id": question_it.id,
                    "answer": score.answer,
                    "is_correct": score.is_correct,
                    "seconds": score.seconds,
                    "session": score.session,
                    "attempt": score.attempt,
                    "date": score.date,
                }

                if score.question_id == question_it.id:
                    results.append(score_data)
                    scores.remove(score)

    return {"scores": results}

def filter_chapter(query, chapter_id):
    chapter_query = db.select(Chapter)
    query = query.join(Score.question).join(Question.chapter)

    if chapter_id.isdecimal():
        chapter_id = int(chapter_id)
        
        query = query.filter(Chapter.number == chapter_id)
        chapter_query = chapter_query.filter(Chapter.number == chapter_id)
    else:
        query = query.filter(Chapter.id == chapter_id)
        chapter_query = chapter_query.filter(Chapter.id == chapter_id)

    try:
        chapter = db.session.scalars(chapter_query).one()  # Expect exactly one result
    except NoResultFound:
        raise APINotFoundError(f"Capítulo con id o número {chapter_id} no existe")
    
    return query, chapter

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


def get_scores_view(app: Application, student_id: Optional[int]):
    query = db.select(Score).join(Score.student).where(Student.app_id == app.id)

    if student_id is not None:
        query = query.where(Score.student_id == student_id)

    query = get_less_equal_greater_filters(query, Score, "attempt")
    query = get_less_equal_greater_filters(query, Score, "session")
    query = get_less_equal_greater_filters(query, Student, "age")

    chapter_id = request.args.get("chapter", None, type=str)
    query, chapter = filter_chapter(query, chapter_id) if chapter_id is not None else (query, None) 

    question_id = request.args.get("question", None, type=str)
    query, question = filter_question(query, question_id) if question_id is not None else (query, None)

    items = get_items_from_query(query)

    return jsonify(parse_json_get_scores(items, app, chapter, question)), 200


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
    
    
    for score in data["scores"]:
        new_score = Score(
            student_id=student.id,
            question_id=score["question_id"],
            answer=score["answer"],
            seconds=score["seconds"],
            is_correct=score["is_correct"],
            attempt=score['attempt'],
            session=student.session,
        )

        db.session.add(new_score)

    db.session.commit()

    return jsonify({"message": "Puntajes agregados correctamente"}), 201
