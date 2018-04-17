# -*- coding: utf-8 -*-
"""User forms"""
from flask_user.forms import RegisterForm, LoginForm, ForgotPasswordForm,\
    ResetPasswordForm, ChangePasswordForm
from flask_wtf import RecaptchaField


class MyRegisterForm(RegisterForm):
    '''Register form'''
    recaptcha = RecaptchaField()


class MyLoginForm(LoginForm):
    '''Login form'''
    recaptcha = RecaptchaField()


class MyForgotPasswordForm(ForgotPasswordForm):
    '''Forgot password form'''
    recaptcha = RecaptchaField()


class MyResetPasswordForm(ResetPasswordForm):
    '''Reset password form'''
    recaptcha = RecaptchaField()


class MyChangePasswordForm(ChangePasswordForm):
    '''Change password form'''
    recaptcha = RecaptchaField()
