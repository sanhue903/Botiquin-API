from .auth_view import sign_up_view, log_in_view
from .mobile_app_view import register_mobile_app_view
from .student_view import get_students_view, post_student_view
from .score_view import get_scores_view, post_scores_view

__all__ = [
    'sign_up_view',
    'log_in_view',
    'register_mobile_app_view',
    'get_students_view',
    'post_student_view',
    'get_scores_view',
    'post_scores_view'
]