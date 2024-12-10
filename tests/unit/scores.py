import pytest

from app.models import Score
from app.extensions import db
from app.exceptions import APINotFoundError
from app.views.score_view import filter_question, filter_chapter

class TestBase:
    def __init__(self):
        self.query = db.select(Score)    

    def run(self, test_scores, filter = ModuleNotFoundError):
        items = db.session.scalars(self.query).all()

        if filter is not None:
            scores = [score for score in test_scores if filter(score)]
        else:
            scores = test_scores
    
        assert len(items) == len(scores)

def test_base_class(app, mock_scores):
    test = TestBase()

    print(mock_scores[1])
    test.run(mock_scores[1])
        

def test_pass_filter_chapter(app, mock_scores):
    test = TestBase()
    chapter_id = mock_scores[0]["app"].chapters[0].id
    print(f"chapter_id: {chapter_id}")

    print(f"query before filter: {test.query}")
    question = filter_chapter(test.query, chapter_id)
    print(f"query query filter: {test.query}")

    assert chapter_id == question.id
    test.run(mock_scores[1], lambda score : score.question.chapter_id == chapter_id)

def test_fail_filter_question(app, mock_scores):
    test = TestBase()
    chapter_id = "NOCHAP"

    with pytest.raises(APINotFoundError) as e:
        filter_chapter(test.query, chapter_id)