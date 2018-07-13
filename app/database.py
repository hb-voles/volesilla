"""Data model for user"""

from enum import Enum, unique
import uuid

from app.extensions import DB, UUID


class Internal(DB.Model):
    """User data model"""

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    db_version = DB.Column(DB.Integer, nullable=False)
    updated_at = DB.Column(DB.DateTime())


class User(DB.Model):
    """User data model"""

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    email = DB.Column(DB.String(255), nullable=False, unique=True)
    password = DB.Column(DB.String(255), nullable=False, server_default='')
    confirmed_at = DB.Column(DB.DateTime())
    gdpr_version = DB.Column(DB.Integer, nullable=False)
    is_active = DB.Column(DB.Boolean(), nullable=False, server_default='0')


class Player(DB.Model):
    """User data model"""

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    user_uid = DB.Column(UUID, DB.ForeignKey('user.uid'), nullable=False)
    steam_id = DB.Column(DB.Integer, nullable=False)
    name = DB.Column(DB.String(50), nullable=False, unique=True)
    avatar = DB.Column(DB.String(300), nullable=False, unique=True)
    avatar_medium = DB.Column(DB.String(300), nullable=False, unique=True)
    avatar_full = DB.Column(DB.String(300), nullable=False, unique=True)

    user = DB.relationship('User', back_populates='players', lazy='select')


User.players = DB.relationship('Player', order_by=Player.name, back_populates='user', lazy='select')


@unique
class TokenType(Enum):
    """Type of tokens"""

    INVITATION = 1
    RESET_PASSWORD = 2
    ACCESS = 3
    RENEW_ACCESS = 4


class Token(DB.Model):
    """Token data model"""

    uid = DB.Column(UUID, primary_key=True, default=uuid.uuid4)
    token_type = DB.Column(DB.Integer, nullable=False)
    created_at = DB.Column(DB.DateTime(), nullable=False)
    valid_until = DB.Column(DB.DateTime(), nullable=False)
    is_active = DB.Column(DB.Boolean(), nullable=False, server_default='1')
    user_uid = DB.Column(UUID, DB.ForeignKey('user.uid'), nullable=False)
    note = DB.Column(DB.String(20), nullable=False, server_default='')

    user = DB.relationship('User', back_populates='tokens', lazy='select')


User.tokens = DB.relationship(
    'Token',
    order_by=Token.created_at,
    back_populates='user',
    lazy='select')
