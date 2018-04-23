# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template, redirect, request, session, url_for

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from app.account.controller import authenticate


BLUEPRINT = Blueprint('account', __name__, template_folder='templates')


class LoginForm(FlaskForm):
    '''Login form'''

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    recaptcha = RecaptchaField()


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
