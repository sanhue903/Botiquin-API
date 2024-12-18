import pytest

from . import TestBase

from app.models import Student, Score
from app.views.utils import filter_query

def test_equal_filter_query(app, mock_scores):
    test = TestBase()
    test.query = test.query.join(Score.student)
    test.query = filter_query(test.query, Student, "age", 5)  

    test.run(mock_scores[1], lambda score : score.student.age == 5)

def test_less_filter_query(app, mock_scores):
    test = TestBase()
    test.query = test.query.join(Score.student)
    test.query = filter_query(test.query, Student, "age", 6, 'lte')  

    test.run(mock_scores[1], lambda score : score.student.age <= 6)

def test_greater_filter_query(app, mock_scores):
    test = TestBase()
    test.query = test.query.join(Score.student)
    test.query = filter_query(test.query, Student, "age", 6, 'gte')  

    test.run(mock_scores[1], lambda score : score.student.age >= 6)
