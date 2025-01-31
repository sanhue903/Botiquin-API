from .auth_controller import bp as auth_bp
from .mobile_app_controller import bp as mobile_app_bp
from .score_controller import bp as score_bp
from .student_controller import bp as student_bp
from .main_controller import bp as main_bp

__all__ = [
    'auth_bp',
    'mobile_app_bp',
    'score_bp',
    'student_bp',
    'main_bp'
    ]