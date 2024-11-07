from .auth_controller import bp as auth_bp
from .mobile_app_controller import bp as mobile_app_bp

__all__ = [
    'auth_bp',
    'mobile_app_bp'
    ]