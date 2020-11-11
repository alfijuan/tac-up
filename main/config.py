import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "RandomSecurePassword"
    DEBUG = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "TheLongWayToTheOthers"
    # JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SQLALCHEMY_BINDS = {
        'users': 'postgres://dev:dev@localhost:5432/tap_users',
        'products': 'postgres://dev:dev@localhost:5432/tap_products',
        'sales': 'postgres://dev:dev@localhost:5432/tap_sales'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

config = configs[os.environ.get('CONFIG_MODE', 'development')]