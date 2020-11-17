import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "RandomSecurePassword"
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "TheLongWayToTheOthers"
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_BINDS = {
        'users': 'postgres://dev:dev@localhost:5432/tap_users',
        'products': 'postgres://dev:dev@localhost:5432/tap_products',
        'sales': 'postgres://dev:dev@localhost:5432/tap_sales'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///' + os.path.join(basedir, 'app_users.db'),
        'products': 'sqlite:///' + os.path.join(basedir, 'app_products.db'),
        'sales': 'sqlite:///' + os.path.join(basedir, 'app_sales.db')
    }
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_BINDS = {
        'users': os.environ.get('DB_USERS') or 'sqlite:///' + os.path.join(basedir, 'app_users.db'),
        'products': os.environ.get('DB_PRODUCTS') or 'sqlite:///' + os.path.join(basedir, 'app_products.db'),
        'sales': os.environ.get('DB_SALES') or 'sqlite:///' + os.path.join(basedir, 'app_sales.db')
    }


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}