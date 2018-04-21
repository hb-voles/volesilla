"""Data model for user"""

from app.extensions import db


class User(db.Model):
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
