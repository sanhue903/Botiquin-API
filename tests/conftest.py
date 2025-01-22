import pytest
from app import create_app
from config import TestingConfig

from app.extensions import db
from app.models import User, Application, Chapter, Question, Student, Score, Role
from app.views import post_scores_view
from flask_jwt_extended import create_access_token
import datetime
import random


@pytest.fixture(scope='function')
def app():
    flask_app = create_app(TestingConfig)
    with flask_app.app_context():
        yield flask_app
@pytest.fixture(scope='function') 
def test_client(app):
    
    with app.test_client() as testing_client:
            yield testing_client
            db.session.close_all()
            db.drop_all()

@pytest.fixture(scope='function')
def mock_user(test_client):
    role = db.session.scalar(db.select(Role).where(Role.name == "default"))
    
    test_user = User('test@test.cl', 'testtest')
    test_user.role_id = role.id
    db.session.add(test_user)
    
    db.session.commit()
    
    yield {'user': test_user, 
           'token':create_access_token(identity=test_user.id)
        }
    
@pytest.fixture(scope='function')
def mock_application(test_client):
    test_app = Application(id='TESAPP', name='Test Application')
    db.session.add(test_app)

    role = db.session.scalar(db.select(Role).where(Role.name == 'app'))
    user = User('app@test.cl', 'testtest')
    user.role_id = role.id
    db.session.add(user)

    db.session.commit()
   
    yield {'app': test_app,
           'token':create_access_token(identity=user.id)
        } 
    
@pytest.fixture(scope='function')
def mock_app_content(test_client, mock_application):
    """
    {
        id: TESAPP
        chapters: [
            {
                id: TESCH1
                number: 1
                questions: [
                    {
                        id: TESQ11
                        number: 1
                    },
                    {
                        id: TESQ12
                        number: 2
                    }
                ]
            },
            {
                id: TESCH2
                number: 2
                questions: [
                    {
                        id: TESQ21
                        number: 1
                    },
                    {
                        id: TESQ22
                        number: 2
                    },
                    {
                        id: TESQ23
                        number: 3
                    }
    ]}]}
    """
    chapter1 = Chapter(id='TESCH1', app_id=mock_application['app'].id, number=1, name='Test Chapter 1')
    db.session.add(chapter1)
    
    chapter2 = Chapter(id='TESCH2', app_id=mock_application['app'].id, number=2, name='Test Chapter 2')
    db.session.add(chapter2)
    
    question1_1 = Question(id='TESQ11', chapter_id=chapter1.id, number=1, text='Test Question 1.1')
    db.session.add(question1_1)
    
    question1_2 = Question(id='TESQ12', chapter_id=chapter1.id, number=2, text='Test Question 1.2')
    db.session.add(question1_2)
    
    
    question2_1 = Question(id='TESQ21', chapter_id=chapter2.id, number=1, text='Test Question 2.1')
    db.session.add(question2_1) 
   
    question2_2 = Question(id='TESQ22', chapter_id=chapter2.id, number=2, text='Test Question 2.2')
    db.session.add(question2_2) 

    question2_3 = Question(id='TESQ23', chapter_id=chapter2.id, number=3, text='Test Question 2.3')
    db.session.add(question2_3)

    db.session.commit() 
    yield mock_application
    
@pytest.fixture(scope='function')
def mock_student(test_client, mock_application):
    test_student1 = Student(app_id=mock_application['app'].id, name='Test Student', age=5)
    db.session.add(test_student1)
    db.session.commit()
    
    test_student2 = Student(app_id=mock_application['app'].id, name='Test Student 2', age=7)
    db.session.add(test_student2)
    db.session.commit()
    
    yield [test_student1, test_student2]
    
import datetime
import random

def generate_session_data(chapter):
    data = {
        "date": datetime.datetime(2025, 12, 31),
        "finish_chapter": True,
        "seconds": 10.5,
        "scores": []
    }

    for question in chapter.questions:
        attempt = 0
        in_session = True

        while True:
            attempt += 1

            # Probabilidades actualizadas
            if chapter.number == 2:
                is_correct = random.choices([True, False], weights=[60, 40])[0]  # 60% de aciertos en capítulo 2
                seconds = float(random.randint(20, 60))  # Tiempo más alto en capítulo 2
            else:
                is_correct = random.choices([True, False], weights=[85, 15])[0]  # 85% de aciertos en general
                seconds = float(random.randint(5, 30))  # Tiempo más bajo en otros capítulos

            score = {
                "answer": "a",
                "seconds": seconds,
                "is_correct": is_correct,
                "attempt": attempt,
                "question_id": question.id
            }

            data['scores'].append(score)
            data['seconds'] += seconds

            if is_correct:
                break  # Si responde bien, pasa a la siguiente pregunta

            # Probabilidad de abandonar antes de terminar
            if chapter.number == 2:
                in_session = random.choices([True, False], weights=[80, 20])[0]  # 20% de probabilidad de abandono en capítulo 2
            else:
                in_session = random.choices([True, False], weights=[90, 10])[0]  # 10% de abandono en otros capítulos

            if not in_session:
                data['finish_chapter'] = False
                break  # Termina la sesión si abandona

        if not in_session:
            break  # Si se abandona, no sigue con más preguntas

    return data

@pytest.fixture(scope='function')
def mock_scores(test_client, mock_app_content, mock_student):
    sessions = []
    for student in mock_student:
        for chapter in mock_app_content['app'].chapters:
            data = generate_session_data(chapter)
            post_scores_view(chapter,student, data)
            
            if not data['finish_chapter']:
                break
           
        sessions+= student.sessions 
    
    yield mock_app_content, sessions