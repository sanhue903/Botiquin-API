from flask import Flask
from flask_cors import CORS
from config import Config, DevelopmentConfig

from app.extensions import db, ma, jwt, migrate

def create_app(config_class: Config= DevelopmentConfig):
    app = Flask(__name__)
    config = config_class()
    print(config.__class__.__name__)
    app.config.from_object(config)
    CORS(app)

    # Initialize Flask extensions here

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        create_database()

    # Register blueprints here
    ### Swagger ###
    if type(config) is DevelopmentConfig:
        print("SWAGGER_URL: ", config_class.SWAGGER_URL)
        app.register_blueprint(config_class.SWAGGER_BLUEPRINT, url_prefix=config_class.SWAGGER_URL)
        print("tamos")

    return app

def create_database():
    from app.models import User, Student, Role, Score, Application, Chapter, Question
        
    db.create_all() 