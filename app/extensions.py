# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

flask_bcrypt = Bcrypt()  # pylint: disable=invalid-name
db = SQLAlchemy()  # pylint: disable=invalid-name
mail = Mail()  # pylint: disable=invalid-name
bootstrap = Bootstrap()  # pylint: disable=invalid-name
csrf = CSRFProtect()  # pylint: disable=invalid-name
