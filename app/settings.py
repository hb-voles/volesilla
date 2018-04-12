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

    COMMIT_HASH = os.environ.get('VOLESILLA_COMMIT_HASH', 'commit-hash')
    DEPLOY_TS = os.environ.get('VOLESILLA_DEPLOY_TS', 'deploy-ts')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    BOOTSTRAP_USE_MINIFIED = True
    DB_NAME = 'app_prod.db'
    HOME_URL = 'https://voles.celestian.cz/'

    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    BOOTSTRAP_USE_MINIFIED = False
    DB_NAME = 'app_dev.db'
    HOME_URL = 'http://127.0.0.1:5000/'

    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
