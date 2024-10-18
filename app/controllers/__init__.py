from .application_controller import bp as application_controller
from .auth_controller import bp as auth_controller
from .score_controller import bp as score_controller
from .student_controller import bp as student_controller

__all__ = [
    'application_controller',
    'auth_controller',
    'score_controller',
    'student_controller'
]