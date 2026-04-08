import os
from typing import Dict, Type

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security Headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'dev.db')
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Proxy Fix toggle for Vercel/Render
    ENABLE_PROXY_FIX = True
    
    # Ensure SECRET_KEY is set in production
    @classmethod
    def init_app(cls, app):
        # Base config initialization
        pass
        if not os.environ.get('SECRET_KEY'):
            import secrets
            os.environ['SECRET_KEY'] = secrets.token_hex(24)

config: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
