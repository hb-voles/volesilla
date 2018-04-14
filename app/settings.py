# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('VOLESILLA_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('VOLES_MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('VOLES_MAIL_PASSWORD', '')

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER',
                                    '"VoleS" <noreply@gmail.com>')

    USER_APP_NAME = 'VoleS'

    RECAPTCHA_PUBLIC_KEY = os.environ.get('VOLES_RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('VOLES_RECAPTCHA_PRIVATE_KEY', '')

    RECAPTCHA_API_SERVER = 'https://www.google.com/recaptcha/api/siteverify'

    COMMIT_HASH = os.environ.get('VOLESILLA_COMMIT_HASH', 'commit-hash')
    DEPLOY_TS = os.environ.get('VOLESILLA_DEPLOY_TS', 'deploy-ts')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'production_env'
    DEBUG = False
    BOOTSTRAP_USE_MINIFIED = True
    HOME_URL = 'https://voles.celestian.cz/'

    # Put the db file in project root
    DB_NAME = 'volesilla.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'data', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class DevConfig(Config):
    """Development configuration."""

    ENV = 'development_env'
    DEBUG = True
    BOOTSTRAP_USE_MINIFIED = False
    HOME_URL = 'http://127.0.0.1:5000/'

    # Put the db file in project root
    DB_NAME = 'volesilla_dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, 'data', DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
