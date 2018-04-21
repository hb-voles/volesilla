# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app
from flask import Blueprint, render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from app.account.controller import authenticate
from app.auth import login_required

BLUEPRINT = Blueprint('account', __name__, template_folder='templates')


class LoginForm(FlaskForm):
    '''Login form'''

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


@BLUEPRINT.route('/login', methods=('GET', 'POST'))
def login():
    '''View function'''

    if 'next' in request.args:
        target = request.args['next']
    else:
        target = '/secret'

    form = LoginForm()

    if form.validate_on_submit() and authenticate(form.username.data, form.password.data):
        return redirect(target)

    return render_template(
        'account/login.html',
        form=form,
        next=target,
        commit_hash=current_app.config['COMMIT_HASH'],
        deploy_ts=current_app.config['DEPLOY_TS'])


@BLUEPRINT.route('/secret', methods=('GET', 'POST'))
@login_required
def secret():
    '''View function'''

    return render_template(
        'account/secret.html',
        commit_hash=current_app.config['COMMIT_HASH'],
        deploy_ts=current_app.config['DEPLOY_TS'])


@BLUEPRINT.route('/secret2', methods=('GET', 'POST'))
@login_required
def secret2():
    '''View function'''

    return render_template(
        'account/secret2.html',
        commit_hash=current_app.config['COMMIT_HASH'],
        deploy_ts=current_app.config['DEPLOY_TS'])
