import uuid
from marshmallow import Schema, ValidationError
from app.exceptions import APIValidationError, APINotFoundError, APIAuthError

from typing import Union
from flask import request
from app.extensions import db
from app.models import User
def validate_data(schema: Schema):
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        raise APIValidationError(err.messages)
        
    return data

def get_object(type,id: Union[uuid.UUID, str, int], message: str):
    object = db.session.scalar(db.select(type).where(type.id == id))

    if not object:
        raise APINotFoundError(message)

    return object

def validate_role(user: User,role: str):
    if user.role.name == "admin":
        return
    
    if user.role.name != role:
        raise APIAuthError("No tienes los permisos necesarios para realizar esta acción") 