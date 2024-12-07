import pytest

from app.models import Score
from app.extensions import db
from app.views.score_view import filter_question, filter_chapter

class TestBase:
    def __init__(self):
        self.query = db.select(Score)    

    def run(self, test_scores, filter = ModuleNotFoundError):
        items = db.session.scalars(self.query)

        if filter is not None:
            scores = [score for score in test_scores if filter(score)]
        else:
            scores = test_scores
    
        assert len(items) == len(scores)

def test_base_class(test_client, mock_scores):
    test = TestBase()

    test.run(mock_scores[1])
        

def test_filter_question(test_client, mock_scores):
    test = TestBase()
    
    chapter_id = mock_scores[0]["app"].chapters[0].id
    
    filter_question(test.query, chapter_id)
    
    test.run(mock_scores[1], lambda score : score.question.chapter_id == chapter_id)