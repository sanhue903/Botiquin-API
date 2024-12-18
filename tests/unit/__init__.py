from app.models import Score
from app.extensions import db

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
