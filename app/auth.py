"""Decorators for authentication"""

from functools import wraps

from flask import request, redirect, session, url_for


def login_required(func):
    '''
    Decorator login_required
    '''

    @wraps(func)
    def decorated_view(*args, **kwargs):
        '''
        Switch between requested page and login form
        '''

        if 'username' not in session:
            return redirect(url_for('account.login', next=request.url))
        return func(*args, **kwargs)

    return decorated_view
