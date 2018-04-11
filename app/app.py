# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from flask_bootstrap.nav import BootstrapRenderer

from app.extensions import db, nav

from flask_bootstrap import Bootstrap
from flask_bootstrap import WebCDN

from flask_user import UserManager, SQLAlchemyAdapter

from app import about
from app import secret
from app.settings import ProdConfig
from app.exceptions import InvalidUsage

from app.user import User

from flask_nav import register_renderer


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_bootsrap(app)
    configure_flask_user(app)
    register_renderer(app, 'bootstrap', BootstrapRenderer)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    bootstrap = Bootstrap(app)
    nav.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(about.views.blueprint)
    app.register_blueprint(secret.views.blueprint)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def configure_bootsrap(app):
    bootstrapcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/")
    bootswatchcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/")
    app.extensions['bootstrap']['cdns'].update(
        {'bootstrapcdn': bootstrapcdn, 'bootswatchcdn': bootswatchcdn})


def configure_flask_user(app):
    db_adapter = SQLAlchemyAdapter(db, User)        # Register the User model
    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User
