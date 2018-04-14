# -*- coding: utf-8 -*-
"""User views."""
from flask import current_app as app
from flask import Blueprint, render_template

from flask_user import login_required


BLUEPRINT = Blueprint('secret', __name__, template_folder='templates')


@BLUEPRINT.route('/secret')
@login_required
def index():

    commit_hash = app.config['COMMIT_HASH']
    deploy_ts = app.config['DEPLOY_TS']

    return render_template(
        'pages/secret.html',
        commit_hash=commit_hash,
        deploy_ts=deploy_ts)
