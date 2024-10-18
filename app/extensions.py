from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

__all__ = [
    'db', 
    'ma', 
    'jwt', 
    'migrate'
]

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()