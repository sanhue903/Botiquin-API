from flask import Blueprint, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.extensions import db

error_bp = Blueprint('error', __name__)

__all__ = [
    'APIError', 
    'APIBadRequestError', 
    'APIUnauthorizedError', 
    'APIAuthError', 
    'APINotFoundError',
    'APIConflictError',
    'APIValidationError'
]

class APIError(Exception):
    """custom API Exceptions"""
    def __init__(self, code: int, description: str, *args):
        self.code = code
        self.description = description
        self.args = args

class APIBadRequestError(APIError):
    """Bad request error exception"""
    def __init__(self, *args):
        super().__init__(400, 'Bad request error', *args)

class APIUnauthorizedError(APIError):
    """Unauthorized error exception"""
    def __init__(self, *args):
        super().__init__(401, 'Unauthorized error', *args)

class APIAuthError(APIError):
    """Auth error exception"""
    def __init__(self, *args):
        super().__init__(403, 'Authentication error', *args)

class APINotFoundError(APIError):
    """Not found error exception"""
    def __init__(self, *args):
        super().__init__(404, 'Not found error', *args)

class APIConflictError(APIError):
    """Conflict error exception"""
    def __init__(self, *args):
        super().__init__(409, 'Conflict error', *args)

class APIValidationError(APIError):
    """Validation error exception"""
    def __init__(self, *args):
        super().__init__(422, 'Validation error', *args)



@error_bp.app_errorhandler(APIError)
def handle_api_exception(err):
    """Handle API exceptions"""
    return handler_error(err)

@error_bp.app_errorhandler(SQLAlchemyError)
def handle_sql_exception(err):
    """Handle SQLAlchemy exceptions"""
    err = APIError(500, "Lo sentimos, ocurrio un error en la base de datos", *err.args)
    
    db.session.rollback()
    return handler_error(err)

@error_bp.app_errorhandler(ValidationError)
def handle_validation_error(err):
    """Handle validation exceptions"""
    err = APIBadRequestError("Lo sentimos, los datos enviados no son validos", *err.args)
    return handler_error(err)

@error_bp.app_errorhandler(400)
def handle_bad_request(err):
    """Handle bad request errors"""
    err = APIBadRequestError("Lo sentimos, la solicitud es incorrecta", err.description)
    return handler_error(err)

@error_bp.app_errorhandler(404)
def handle_not_found(err):
    """Handle not found errors"""
    err = APINotFoundError("Lo sentimos, la ruta solicitada no existe")
    return handler_error(err)

@error_bp.app_errorhandler(405)
def handle_not_allowed(err):
    """Handle not allowed errors"""
    err = APIError(405, "Method not allowed error", "Lo sentimos, el metodo solicitado no esta permitido")
    return handler_error(err)


@error_bp.app_errorhandler(500)
def handle_server_exception(err):
    """Handle server errors"""
    err = APIError(500, "Server error", "Lo sentimos, ocurrio un error inesperado", err.description if current_app.config['DEBUG'] else []) ## no funciona si DEBUG = True o False
    return handler_error(err)

def handler_error(err):
    """Return a custom JSON response"""
    response = {"error": err.description}
    
    response["messages"] = [arg for arg in err.args if len(arg) > 0] 
        
    return jsonify(response), err.code