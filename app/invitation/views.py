# -*- coding: utf-8 -*-
"""User views."""

from datetime import datetime, timedelta
from flask import current_app, Blueprint, render_template, session, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.auth import login_required
from app.invitation.model import Invite
from app.invitation.controller import create_invite_token


BLUEPRINT = Blueprint('invitation', __name__, template_folder='templates')


class InvitationForm(FlaskForm):
    '''Login form'''

    created_by = StringField('created_by', render_kw={'disabled': 'disabled'})
    created = StringField('created', render_kw={'disabled': 'disabled'}, default=datetime.now())
    valid_until = StringField(
        'valid_until',
        render_kw={'disabled': 'disabled'},
        default=datetime.now() + timedelta(days=2)
    )
    for_user = StringField('for_user', validators=[DataRequired()])


@BLUEPRINT.route('/invitation')
@login_required
def index():
    '''View function'''

    invites = Invite.query.all()

    return render_template('invitation/index.html', invites=invites)


@BLUEPRINT.route('/invitation/new', methods=('GET', 'POST'))
@login_required
def new():
    '''View function'''

    with current_app.app_context():
        form = InvitationForm(created_by=session['username'])

        if form.validate_on_submit():
            create_invite_token(
                valid_until=datetime.now() + timedelta(days=2),
                created_by=session['username'],
                for_user=form.for_user.data
            )
            return redirect(url_for('invitation.index'))

    return render_template('invitation/new.html', form=form)
