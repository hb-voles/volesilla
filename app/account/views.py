# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app, Blueprint, flash, render_template, redirect, \
    request, session, url_for

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired

from app.authen import login_required
from app.database import Token, TokenType
from app.account.controller import send_invitation_mail, search_user_by_email, \
    send_reset_password_mail, get_steam_player, create_player
from app.account.controller_account import create_account, change_password, confirm_account
from app.account.controller_authen import authenticate, get_logged_user
from app.account.controller_token import cancel_token_by_uid, verify_token_by_uid, \
    create_invitation_token, search_user_by_token_uid
from app.profile.views import CheckSteamProfileForm

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


@BLUEPRINT.route('/registration/token/<invitation_token_uid>', methods=('GET', 'POST'))
def registration_via_token(invitation_token_uid):
    """View function"""

    class RegistrationForm(FlaskForm):
        """Registration form"""

        email = StringField('email', validators=[DataRequired()])
        password1 = PasswordField('password', validators=[DataRequired()])
        password2 = PasswordField('password again',
                                  validators=[DataRequired()])
        accept_gdpr = BooleanField(
            'I agree with GDPR Statement (v{})'.format(
                current_app.config['GDPR_VERSION']))
        recaptcha = RecaptchaField()

    if not verify_token_by_uid(invitation_token_uid, TokenType.INVITATION):
        flash('Invalid invitation token!', 'error')
        return redirect(url_for('voles.index'))

    user = search_user_by_token_uid(invitation_token_uid)

    form = RegistrationForm()
    form.email.data = user.email

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

        if not form.errors:
            confirm_account(user)
            change_password(invitation_token_uid, form.password1.data)
            return render_template('account/registration_final.html', result=True)

    if form.errors:
        flash('Registration form isn\'t filled correctly!', 'error')

    return render_template(
        'account/registration.html',
        form=form,
        gdpr_version=current_app.config['GDPR_VERSION'],
        invitation_token_uid=invitation_token_uid
    )


@BLUEPRINT.route('/invitation')
@login_required
def invitation_index():
    """View function"""

    invitations = Token.query.all()

    return render_template('account/invitation_index.html', invitations=invitations)


class CheckInvitationForm(CheckSteamProfileForm):
    """Check Invitation form"""

    new_user_email = HiddenField(
        'email', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})


@BLUEPRINT.route('/invitation/new', methods=('GET', 'POST'))
@login_required
def invitation_new():
    """View function"""

    class InvitationForm(FlaskForm):
        """Invitation form"""

        email = StringField('email', validators=[DataRequired()])
        steam_id = StringField('steam id', validators=[DataRequired()])

    with current_app.app_context():
        form = InvitationForm()

        if form.validate_on_submit():
            player_data = get_steam_player(form.steam_id)

            check_form = CheckInvitationForm()

            check_form.new_user_email.data = form.email.data
            check_form.steam_id.data = form.steam_id.data
            check_form.player_name.data = player_data['personaname']
            check_form.steam_profile.data = player_data['profileurl']
            check_form.avatar.data = player_data['avatar']
            check_form.avatar_medium.data = player_data['avatarmedium']
            check_form.avatar_full.data = player_data['avatarfull']

            return render_template(
                'account/invitation_check.html',
                steam_profile=player_data['profileurl'],
                avatar=player_data['avatarfull'],
                form=check_form)

    return render_template('account/invitation_new.html', form=form)


@BLUEPRINT.route('/invitation/check', methods=('GET', 'POST'))
@login_required
def invitation_check():
    """View function"""

    form = CheckInvitationForm()

    if form.validate_on_submit():

        if not form.errors:

            new_user = create_account(form.new_user_email.data)
            invitation_token = create_invitation_token(new_user, get_logged_user())
            invitation_token_hex = invitation_token.uid.hex
            player = create_player(
                new_user,
                form.steam_id.data,
                form.player_name.data,
                form.avatar.data,
                form.avatar_medium.data,
                form.avatar_full.data)
            send_invitation_mail(new_user, player.name, invitation_token_hex)

            return render_template('account/invitation_final.html', mail=new_user.email)

    if form.errors:
        flash('Profile is not correct!', 'error')

    return render_template(
        'account/invitation_check.html',
        steam_profile=form.steam_profile.data,
        avatar=form.avatar_full.data,
        form=form)
