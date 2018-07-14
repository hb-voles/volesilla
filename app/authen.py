"""Decorators for authentication"""

from functools import wraps

from flask import request, redirect, url_for

from app.account.controller_token import verify_authentication


def login_required(func):
    """Decorator login_required"""

    @wraps(func)
    def decorated_view(*args, **kwargs):
        """Switch between requested page and login form"""

        if not verify_authentication():
            return redirect(url_for('account.login', next=request.url))
        return func(*args, **kwargs)

    return decorated_view
