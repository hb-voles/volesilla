# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app, Blueprint, flash, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

from app.auth import login_required
from app.database import Player
from app.account.controller import get_steam_player, create_player
from app.account.controller_auth import get_logged_user


BLUEPRINT = Blueprint('profile', __name__, template_folder='templates')


@BLUEPRINT.route('/profile/me', methods=['GET'])
@login_required
def my_profile():
    """View function"""

    logged_user = get_logged_user()
    my_profiles = Player.query.filter_by(
        user_uid=logged_user.uid).order_by(
            Player.name.desc()).all()

    return render_template('profile/my_profile.html', my_profiles=my_profiles)


class CheckSteamProfileForm(FlaskForm):
    """Check Invitation form"""

    steam_id = HiddenField(
        'steam id', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})
    player_name = StringField(
        'player name', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})
    steam_profile = HiddenField(
        'steam profile', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})
    avatar = HiddenField('avatar', validators=[DataRequired()], render_kw={'readonly': 'readonly'})
    avatar_medium = HiddenField(
        'avatar_medium', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})
    avatar_full = HiddenField(
        'avatar_full', validators=[
            DataRequired()], render_kw={
                'readonly': 'readonly'})


@BLUEPRINT.route('/profile/add', methods=['GET', 'POST'])
@login_required
def add_profile():
    """View function"""

    class AddProfileForm(FlaskForm):
        """Add profile form"""

        steam_id = StringField('steam id', validators=[DataRequired()])

    with current_app.app_context():
        form = AddProfileForm()

        if form.validate_on_submit():
            player_data = get_steam_player(form.steam_id)

            profile_form = CheckSteamProfileForm()

            profile_form.steam_id.data = form.steam_id.data
            profile_form.player_name.data = player_data['personaname']
            profile_form.steam_profile.data = player_data['profileurl']
            profile_form.avatar.data = player_data['avatar']
            profile_form.avatar_medium.data = player_data['avatarmedium']
            profile_form.avatar_full.data = player_data['avatarfull']

            return render_template(
                'profile/profile_check.html',
                steam_profile=player_data['profileurl'],
                avatar=player_data['avatarfull'],
                form=profile_form)

    return render_template('profile/profile_new.html', form=form)


@BLUEPRINT.route('/profile/check', methods=['GET', 'POST'])
@login_required
def profile_check():
    """View function"""

    form = CheckSteamProfileForm()

    if form.validate_on_submit():

        if not form.errors:

            logged_user = get_logged_user()
            create_player(
                logged_user,
                form.steam_id.data,
                form.player_name.data,
                form.avatar.data,
                form.avatar_medium.data,
                form.avatar_full.data
            )

            return my_profile()

    if form.errors:
        flash('Profile is not correct!', 'error')

    return render_template(
        'profile/profile_check.html',
        steam_profile=form.steam_profile.data,
        avatar=form.avatar_full.data,
        form=form)
