'''Data model for user'''

from enum import Enum, unique
import uuid

from app.extensions import DB, UUID


class User(DB.Model):
    '''User data model'''

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    email = DB.Column(DB.String(255), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False, server_default='')
    confirmed_at = DB.Column(DB.DateTime())
    gdpr_version = DB.Column(DB.Integer, nullable=False)
    is_active = DB.Column(DB.Boolean(), nullable=False, server_default='0')


@unique
class TokenType(Enum):
    '''Type of tokens'''

    INVITATION = 1
    REGISTRATION = 2
    RESET_PASSWORD = 3
    ACCESS = 4
    RENEW_ACCESS = 5


class Token(DB.Model):
    '''Token data model'''

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    token_type = DB.Column(DB.Integer, nullable=False)
    created_at = DB.Column(DB.DateTime(), nullable=False)
    valid_until = DB.Column(DB.DateTime(), nullable=False)
    is_active = DB.Column(DB.Boolean(), nullable=False, server_default='1')
    user_uid = DB.Column(UUID, DB.ForeignKey('user.uid'), nullable=False)
    note = DB.Column(DB.String(20), nullable=False, server_default='')

    user = DB.relationship('User', back_populates='tokens')


User.tokens = DB.relationship('Token', order_by=Token.created_at, back_populates='user')
