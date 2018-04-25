# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    DB_VERSION = 2
    GDPR_VERSION = 1

    HOME_URL = os.environ.get('VLS_BASE_URL', 'http://127.0.0.1:5000/')

    SECRET_KEY = os.environ.get('VLS_SECRET_KEY', '')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = False

    # USER_PASSWORD_HASH = 'bcrypt'
    # USER_PASSWORD_HASH_MODE = 'passlib'
    # SECURITY_PASSWORD_SALT = 'aaaaa'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('VLS_MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('VLS_MAIL_PASSWORD', '')

    MAIL_DEFAULT_SENDER = os.getenv('VLS_DEFAULT_SENDER',
                                    '"VoleS" <noreply@gmail.com>')

    APP_ADMIN_MAIL = os.environ.get('VLS_APP_ADMIN_MAIL', '')

    USER_APP_NAME = 'Hell-Bent VoleS'

    RECAPTCHA_PUBLIC_KEY = os.environ.get('VLS_RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('VLS_RECAPTCHA_PRIVATE_KEY', '')

    # RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

    COMMIT_HASH = os.environ.get('VLS_COMMIT_HASH', 'commit-hash')
    DEPLOY_TS = os.environ.get('VLS_DEPLOY_TS', 'deploy-ts')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'production_env'
    DEBUG = False
    BOOTSTRAP_USE_MINIFIED = True

    # Put the db file in project root
    DB_NAME = 'volesilla.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'data', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class DevConfig(Config):
    """Development configuration."""

    ENV = 'development_env'
    DEBUG = True
    BOOTSTRAP_USE_MINIFIED = False

    # Put the db file in project root
    DB_NAME = 'volesilla_dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'data', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
