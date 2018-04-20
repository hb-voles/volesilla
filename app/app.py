# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from flask_user import UserManager
from flask_bootstrap import WebCDN
from flask_nav import register_renderer
from flask_nav.elements import Navbar, Link

from app.settings import ProdConfig
from app.extensions import db, db_adapter, mail, bootstrap, nav
from app.exceptions import InvalidUsage
from app.nav import MyBootstrapRenderer
from app.user_form import MyRegisterForm, MyLoginForm, MyForgotPasswordForm, \
    MyResetPasswordForm, MyChangePasswordForm

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
    register_renderer(app, 'bootstrap', MyBootstrapRenderer)

    return app


def register_extensions(app):
    """Register Flask extensions."""

    db.init_app(app)

    UserManager(
        db_adapter,
        app,
        login_form=MyLoginForm,
        register_form=MyRegisterForm,
        forgot_password_form=MyForgotPasswordForm,
        reset_password_form=MyResetPasswordForm,
        change_password_form=MyChangePasswordForm,
    )

    mail.init_app(app)

    bootstrap.init_app(app)
    bootstrapcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/")
    bootswatchcdn = WebCDN("https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/")
    app.extensions['bootstrap']['cdns'].update(
        {'bootstrapcdn': bootstrapcdn, 'bootswatchcdn': bootswatchcdn})

    nav.init_app(app)
    nav.register_element('top', Navbar(
        Link('Hell-Bent VoleS', app.config['HOME_URL']),
    ))


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(voles.views.BLUEPRINT)


def register_errorhandlers(app):
    """Register error handlers."""

    def errorhandler(error):
        """Error handler."""
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)
