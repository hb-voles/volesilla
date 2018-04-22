"""Data model for user"""

import uuid
from app.extensions import db

from app.invitation.model import Invite


def create_invite_token(valid_until, created_by, for_user):
    '''Save invite_token into DB'''

    invite = Invite(
        token=uuid.uuid4().hex,
        valid_until=valid_until,
        created_by=created_by,
        for_user=for_user)

    db.session.add(invite)
    db.session.commit()
