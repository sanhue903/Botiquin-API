import pytest

from . import TestBase

from app.models import Score
from app.extensions import db
from app.exceptions import APINotFoundError
from app.views.score_view import filter_question, filter_chapter


def test_base_class(app, mock_scores):
    test = TestBase()

    print(mock_scores[1])
    test.run(mock_scores[1])
        

def test_pass_filter_chapter_by_id(app, mock_scores):
    test = TestBase()
    chapter_id = mock_scores[0]["app"].chapters[0].id

    test.query, chapter = filter_chapter(test.query, chapter_id)

    assert chapter_id == chapter.id
    test.run(mock_scores[1], lambda score : score.question.chapter_id == chapter_id)

def test_pass_filter_chapter_by_number(app, mock_scores):
    test = TestBase()
    chapter_id = mock_scores[0]["app"].chapters[0].number

    test.query, chapter = filter_chapter(test.query, str(chapter_id))

    assert chapter_id == chapter.number
    test.run(mock_scores[1], lambda score : score.question.chapter.number == chapter_id)

def test_fail_filter_chapter(app, mock_scores):
    test = TestBase()
    chapter_id = "NOCHAP"

    with pytest.raises(APINotFoundError) as e:
        filter_chapter(test.query, chapter_id)

def test_pass_filter_question_by_id(app, mock_scores):
    test = TestBase()
    question_id = mock_scores[0]["app"].chapters[0].questions[0].id

    test.query, question = filter_question(test.query, question_id)
    
    test.run(mock_scores[1], lambda score : score.question.id == question_id)

def test_pass_filter_question_by_number(app, mock_scores):
    test = TestBase()
    question_id = mock_scores[0]["app"].chapters[0].questions[0].number

    test.query, question = filter_question(test.query, str(question_id))
    
    test.run(mock_scores[1], lambda score : score.question.number == question_id)

def test_fail_filter_question(app, mock_scores):
    test = TestBase()
    question_id = "NOQUES"

    with pytest.raises(APINotFoundError) as e:
        filter_question(test.query, question_id)

