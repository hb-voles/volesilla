# -*- coding: utf-8 -*-
"""User views."""

from datetime import datetime, timedelta
from flask import current_app, Blueprint, flash, render_template, redirect, \
    request, session, url_for

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from app.auth import login_required
from app.account.model import Token
from app.account.controller import authenticate, create_invite_token, \
    validate_invite_token, create_account, send_confirmation_mail


BLUEPRINT = Blueprint('account', __name__, template_folder='templates')


class RegistrationForm(FlaskForm):
    '''Registration form'''

    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password1 = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password again', validators=[DataRequired()])
    token = StringField('invitation token', validators=[DataRequired()])
    accept_gdpr = BooleanField('I agree with GDPR Statement (v1)')
    recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
    '''Login form'''

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    recaptcha = RecaptchaField()


class InvitationForm(FlaskForm):
    '''Invitation form'''

    created_by = StringField('created_by', render_kw={'readonly': 'readonly'})
    created = StringField('created', render_kw={'readonly': 'readonly'}, default=datetime.now())
    valid_until = StringField(
        'valid_until',
        render_kw={'readonly': 'readonly'},
        default=datetime.now() + timedelta(days=2)
    )
    for_user = StringField('for_user', validators=[DataRequired()])


@BLUEPRINT.route('/login', methods=('GET', 'POST'))
def login():
    '''View function'''

    if 'next' in request.args:
        target = request.args['next']
    else:
        target = '/'

    form = LoginForm()

    if form.validate_on_submit() and authenticate(form.username.data, form.password.data):
        return redirect(target)

    return render_template(
        'account/login.html',
        form=form,
        next=target)


@BLUEPRINT.route('/logout')
def logout():
    '''View function'''

    session.pop('username', None)
    return redirect(url_for('voles.index'))


@BLUEPRINT.route('/registration', methods=('GET', 'POST'))
def registration():
    '''View function'''

    form = RegistrationForm()

    if form.validate_on_submit():

        if form.password1.data != form.password2.data:
            form.password1.errors.append(
                '<strong>Passwords</strong> should have the same value!'
            )

        if not form.accept_gdpr.data:
            form.accept_gdpr.errors.append(
                '<strong>Agreement on GDPR Statement</strong> is '
                '<strong>mandatory</strong> for successful registration!'
            )

        if not validate_invite_token(form.token.data):
            form.token.errors.append('Invalid invitation token!')

        if not form.errors:

            create_account(
                username=form.username.data,
                password=form.password1.data,
                email=form.email.data,
                invite_token=form.token.data,
                confirmed_at=datetime.now()
            )
            return redirect(url_for('voles.index'))

    if form.errors:
        flash('Registration form isn\'t filled correctly!', 'error')

    return render_template('account/registration.html', form=form)


@BLUEPRINT.route('/invitation')
@login_required
def invitation_index():
    '''View function'''

    invites = Token.query.all()

    return render_template('account/invitation_index.html', invites=invites)


@BLUEPRINT.route('/invitation/new', methods=('GET', 'POST'))
@login_required
def invitation_new():
    '''View function'''

    with current_app.app_context():
        form = InvitationForm(created_by=session['username'])

        if form.validate_on_submit():
            create_invite_token(
                valid_until=datetime.now() + timedelta(days=2),
                created_by=session['username'],
                for_user=form.for_user.data
            )
            return redirect(url_for('account.invitation_index'))

    return render_template('account/invitation_new.html', form=form)
