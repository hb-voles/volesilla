# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, SQLAlchemyAdapter
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_nav import Nav


db = SQLAlchemy()  # pylint: disable=invalid-name


class User(db.Model, UserMixin):
    '''User data model'''
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')


class Internal(db.Model):
    '''Table for internal data'''
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    db_version = db.Column(db.Integer)


class Team(db.Model):
    '''Teams table'''
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    team_name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)


db_adapter = SQLAlchemyAdapter(db, User, Internal, Team)  # pylint: disable=invalid-name
mail = Mail()  # pylint: disable=invalid-name
bootstrap = Bootstrap()  # pylint: disable=invalid-name
nav = Nav()  # pylint: disable=invalid-name
