"""Data model for user"""

from app.extensions import db


class Invite(db.Model):
    '''User data model'''
    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name
    token = db.Column(db.Integer, nullable=False, unique=True)
    valid_until = db.Column(db.DateTime(), nullable=False)
    created_by = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    for_user = db.Column(db.String(50), nullable=False)
