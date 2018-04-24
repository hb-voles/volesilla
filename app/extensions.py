# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

import uuid
from sqlalchemy import types

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


class UUID(types.TypeDecorator):  # pylint: disable=abstract-method
    '''UUID for SQLite'''

    impl = types.Binary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and not isinstance(value, uuid.UUID):
            raise ValueError('value {} is not a valid uuid.UUID'.format(value))
        else:
            return None

    def process_result_value(self, value, dialect=None):
        return uuid.UUID(bytes=value) if value else None

    def is_mutable(self):  # pylint: disable=no-self-use
        '''is_mutable'''
        return False


BCRYPT = Bcrypt()
DB = SQLAlchemy()
MAIL = Mail()
BOOTSTRAP = Bootstrap()
CSRF = CSRFProtect()
