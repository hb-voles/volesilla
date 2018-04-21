# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app as app
from flask import Blueprint, render_template, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app.account.controller import authenticate


BLUEPRINT = Blueprint('account', __name__, template_folder='templates')


class LoginForm(FlaskForm):
    '''Login form'''

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


@BLUEPRINT.route('/login', methods=('GET', 'POST'))
def login():
    '''View function'''

    form = LoginForm()

    if form.validate_on_submit():
        print('>>> ', authenticate(form.username.data, form.password.data))
        return redirect('/secret')

    return render_template(
        'account/login.html',
        form=form,
        commit_hash=app.config['COMMIT_HASH'],
        deploy_ts=app.config['DEPLOY_TS'])


@BLUEPRINT.route('/secret', methods=('GET', 'POST'))
def secret():
    '''View function'''

    return render_template(
        'account/secret.html',
        commit_hash=app.config['COMMIT_HASH'],
        deploy_ts=app.config['DEPLOY_TS'])
