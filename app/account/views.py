# -*- coding: utf-8 -*-
"""User views."""

from datetime import datetime, timedelta
from flask import current_app, Blueprint, flash, render_template, redirect, \
    request, session, url_for

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from app.auth import login_required
from app.account.model import Token, TokenType
from app.account.controller import authenticate, create_account, confirm_account, \
    send_registration_mail, search_user_by_email, send_reset_password_mail, change_password
from app.account.controller_token import cancel_token_by_uid, verify_token_by_uid, \
    create_invitation_token, search_user_by_token_uid


BLUEPRINT = Blueprint('account', __name__, template_folder='templates')


@BLUEPRINT.route('/login', methods=('GET', 'POST'))
def login():
    """View function"""

    class LoginForm(FlaskForm):
        """Login form"""

        email = StringField('e-mail', validators=[DataRequired()])
        password = PasswordField('password', validators=[DataRequired()])
        recaptcha = RecaptchaField()

    if 'next' in request.args:
        target = request.args['next']
    else:
        target = '/'

    form = LoginForm()

    if form.validate_on_submit():
        if authenticate(form.email.data, form.password.data):
            return redirect(target)

    return render_template(
        'account/login.html',
        form=form,
        next=target)


@BLUEPRINT.route('/password/forgotten', methods=('GET', 'POST'))
def forgotten_password():
    """Forgotten password"""

    class ForgottenPasswordForm(FlaskForm):
        """Forgotten Password form"""

        email = StringField('e-mail', validators=[DataRequired()])
        recaptcha = RecaptchaField()

    form = ForgottenPasswordForm()

    if form.validate_on_submit():

        user = search_user_by_email(form.email.data)
        if not user:
            form.email.errors.append('Given e-mail isn\'t registered!')

        if not form.errors:
            send_reset_password_mail(user)

            return render_template(
                'account/forgotten_password_confirmation.html',
                mail=form.email.data)

    if form.errors:
        flash('Forgotten Password form isn\'t filled correctly!', 'error')

    return render_template('account/forgotten_password.html', form=form)


@BLUEPRINT.route('/password/reset/<token_uid>', methods=('GET', 'POST'))
def reset_password(token_uid):
    """Reset password form"""

    class ResetPasswordForm(FlaskForm):
        """Forgotten Password form"""

        password1 = PasswordField('new password', validators=[DataRequired()])
        password2 = PasswordField('new password again',
                                  validators=[DataRequired()])
        recaptcha = RecaptchaField()

    form = ResetPasswordForm()

    if form.validate_on_submit():

        if form.password1.data != form.password2.data:
            form.password1.errors.append(
                '<strong>Passwords</strong> should have the same value!'
            )

        if not form.errors:
            password_changed = change_password(token_uid, form.password1.data)
            user = search_user_by_token_uid(token_uid)
            confirm_account(user)
            cancel_token_by_uid(token_uid)

            return render_template('account/reset_password_final.html', result=password_changed)

    if form.errors:
        flash('Registration form isn\'t filled correctly!', 'error')

    return render_template('account/reset_password.html', form=form, reset_password_token=token_uid)


@BLUEPRINT.route('/logout')
def logout():
    """View function"""

    if 'access_token' in session:
        cancel_token_by_uid(session['access_token'])
    if 'renew_access_token' in session:
        cancel_token_by_uid(session['renew_access_token'])

    session.pop('access_token', None)
    session.pop('renew_access_token', None)
    session.pop('user_email', None)

    return redirect(url_for('voles.index'))


@BLUEPRINT.route('/registration', methods=('GET', 'POST'))
def registration():
    """View function"""

    class RegistrationForm(FlaskForm):
        """Registration form"""

        username = StringField('username', validators=[DataRequired()])
        email = StringField('email', validators=[DataRequired()])
        password1 = PasswordField('password', validators=[DataRequired()])
        password2 = PasswordField('password again',
                                  validators=[DataRequired()])
        token = StringField('invitation token', validators=[DataRequired()])
        accept_gdpr = BooleanField('I agree with GDPR Statement (v1)')
        recaptcha = RecaptchaField()

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

        if not verify_token_by_uid(form.token.data, TokenType.INVITATION):
            form.token.errors.append('Invalid invitation token!')

        if not form.errors:

            user = create_account(
                password=form.password1.data,
                email=form.email.data,
            )

            send_registration_mail(user)

            return render_template('account/registration_confirmation.html', mail=form.email.data)

    if form.errors:
        flash('Registration form isn\'t filled correctly!', 'error')

    return render_template(
        'account/registration.html',
        form=form,
        gdpr_version=current_app.config['GDPR_VERSION']
    )


@BLUEPRINT.route('/registration/final/<token_uid>')
def registration_final(token_uid):
    """View function"""

    if not verify_token_by_uid(token_uid, TokenType.REGISTRATION):
        user = search_user_by_token_uid(token_uid)
        confirm_account(user)

        # >>> Udelat profile
        return render_template('account/registration_final.html', result=True)

    return render_template('account/registration_final.html', result=False)


@BLUEPRINT.route('/invitation')
@login_required
def invitation_index():
    """View function"""

    invitations = Token.query.all()

    return render_template('account/invitation_index.html', invitations=invitations)


@BLUEPRINT.route('/invitation/new', methods=('GET', 'POST'))
@login_required
def invitation_new():
    """View function"""

    class InvitationForm(FlaskForm):
        """Invitation form"""

        created_by = StringField('created_by',
                                 render_kw={'readonly': 'readonly'})
        created = StringField('created', render_kw={'readonly': 'readonly'},
                              default=datetime.now())
        valid_until = StringField(
            'valid_until',
            render_kw={'readonly': 'readonly'},
            default=datetime.now() + timedelta(days=2)
        )
        for_user = StringField('for_user', validators=[DataRequired()])

    with current_app.app_context():
        user = search_user_by_token_uid(session['access_token'])

        form = InvitationForm(created_by=user.email)

        if form.validate_on_submit():
            token = create_invitation_token(user.uid, form.for_user.data)
            return render_template('account/invitation_final.html', invitation_token=token.uid.hex)

    return render_template('account/invitation_new.html', form=form)
