# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

from flask import Flask
from flask_bootstrap import WebCDN

from app.settings import ProdConfig
from app.extensions import flask_bcrypt, db, mail, bootstrap, csrf
from app.exceptions import InvalidUsage

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

    return app


def register_extensions(app):
    """Register Flask extensions."""

    flask_bcrypt.init_app(app)

    db.init_app(app)

    mail.init_app(app)

    bootstrap.init_app(app)
    bootstrapcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/")
    bootswatchcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/")
    app.extensions['bootstrap']['cdns'].update(
        {'bootstrapcdn': bootstrapcdn, 'bootswatchcdn': bootswatchcdn})

    csrf.init_app(app)


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
