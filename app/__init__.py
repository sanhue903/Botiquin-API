from flask import Flask
from config import Config, DevelopmentConfig

from app.extensions import db, ma, jwt, migrate
from .exceptions import error_bp 
from .controllers import auth_bp, mobile_app_bp, score_bp, student_bp

def create_app(config_class: Config = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    with app.app_context():
        # Initialize extensions
        db.init_app(app)
        ma.init_app(app)
        jwt.init_app(app)
        migrate.init_app(app, db)
        
        # Initialize database
        init_db()
        
        # Register blueprints
        app.register_blueprint(error_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(mobile_app_bp, url_prefix='/apps')
        app.register_blueprint(score_bp, url_prefix='/apps/<app_id>/students')
        app.register_blueprint(student_bp, url_prefix='/apps/<app_id>/students')
        
        return app

def init_db():
    from app.models import User, Role, Application, Chapter, Question, Student, Score  # noqa: F401
    
    db.create_all()

    