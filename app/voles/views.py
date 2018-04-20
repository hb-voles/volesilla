# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app as app
from flask import Blueprint, render_template

BLUEPRINT = Blueprint('voles', __name__, template_folder='templates')


@BLUEPRINT.route('/')
def index():
    '''View function'''

    return render_template(
        'pages/voles.html',
        commit_hash=app.config['COMMIT_HASH'],
        deploy_ts=app.config['DEPLOY_TS'])
