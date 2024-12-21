from app.models import Application, Chapter, Question, User, Role
from app.exceptions import SQLAlchemyError
from app.extensions import db
from flask_jwt_extended import create_access_token
from flask import jsonify

def register_mobile_app_view(data):
    """Register mobile app and create a user for the app:
    
        replace {APP_ID} with the actual id of the app
        email: {APP_ID}@app.cl
        password: PW{APP_ID}
    """
    new_app = Application(data['id'], data['name'])
    db.session.add(new_app)

    for chapter in data['chapters']:
        new_chapter = Chapter(id=chapter['id'],
                            app_id=new_app.id, 
                            number=chapter['number'], 
                            name=chapter['name']
                        )
        db.session.add(new_chapter)

        for question in chapter['questions']:
            new_question = Question(id=question['id'], 
                                    chapter_id=new_chapter.id,
                                    number=question['number'],
                                    text=question['text']
                                )
            db.session.add(new_question) 

    email = f'{new_app.id}@app.cl'
    password = f'PW{new_app.id}'
    app_user = User(email, password) 

    role = db.session.scalar(db.select(Role).where(Role.name == 'app'))
    
    if not role:
        raise SQLAlchemyError('No existe el role correspondiente')

    app_user.role_id = role.id
    
    db.session.add(app_user)
    db.session.commit()

    access_token = create_access_token(identity=app_user.id,
                                       expires_delta=False)

    return jsonify({'token': access_token}), 201

def get_app_view(app):
    json = {
        'id': app.id,
        'name': app.name,
        'chapter_count': len(app.chapters),
        'chapters': [{
            'id': chapter.id,
            'number': chapter.number,
            'name': chapter.name,
            'question_count': len(chapter.questions),
            'questions': [{
                'id': question.id,
                'number': question.number,
                'text': question.text
            } for question in chapter.questions]
            } for chapter in app.chapters]
    }

    return jsonify(json), 200