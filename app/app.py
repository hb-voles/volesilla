# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from flask_user import UserManager
from flask_bootstrap import WebCDN
from flask_nav import register_renderer
from flask_nav.elements import Navbar, Link, View

from app.extensions import db, db_adapter, bootstrap, nav
from app.settings import ProdConfig
from app.exceptions import InvalidUsage
from app.nav import MyBootstrapRenderer

from app import about
from app import secret


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
    register_renderer(app, 'bootstrap', MyBootstrapRenderer)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)

    user_manager = UserManager(db_adapter, app)     # Initialize Flask-User

    bootstrap.init_app(app)
    bootstrapcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/")
    bootswatchcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/")
    app.extensions['bootstrap']['cdns'].update(
        {'bootstrapcdn': bootstrapcdn, 'bootswatchcdn': bootswatchcdn})

    nav.init_app(app)
    nav.register_element('top', Navbar(
        Link('Hell-Bent VoleS', app.config['HOME_URL']),
        View('About', 'about.index'),
        View('Secret', 'secret.index'),
    ))


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
