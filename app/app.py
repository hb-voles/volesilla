# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from flask import Flask, session
from flask_bootstrap import WebCDN

from app.settings import ProdConfig
from app.extensions import BCRYPT, DB, MAIL, BOOTSTRAP, CSRF
from app.exceptions import InvalidUsage
from app.navbar import build_navbar

from app import account
from app import voles


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    :param config_object: The configuration object to use.
    """

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_context_processots(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""

    BCRYPT.init_app(app)

    DB.init_app(app)

    MAIL.init_app(app)

    BOOTSTRAP.init_app(app)
    bootstrapcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/")
    bootswatchcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/")
    app.extensions['bootstrap']['cdns'].update(
        {'bootstrapcdn': bootstrapcdn, 'bootswatchcdn': bootswatchcdn})

    CSRF.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(account.views.BLUEPRINT)
    app.register_blueprint(voles.views.BLUEPRINT)


def register_errorhandlers(app):
    """Register error handlers."""

    def errorhandler(error):
        """Error handler."""
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_context_processots(app):
    '''Register context processors.'''

    @app.context_processor
    def inject_navbar():  # pylint: disable=unused-variable
        '''Inject our navbar to the global context'''
        return build_navbar()

    @app.context_processor
    def is_authenticated():  # pylint: disable=unused-variable
        '''Tell if user is authenticated'''
        def authenticated():
            '''Tell if user is authenticated'''
            return True if 'username' in session else False
        return dict(is_authenticated=authenticated)

    @app.context_processor
    def inject_footer_variables():  # pylint: disable=unused-variable
        '''Inject footer variable'''
        return dict(commit_hash=app.config['COMMIT_HASH'], deploy_ts=app.config['DEPLOY_TS'])
