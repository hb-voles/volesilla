# -*- coding: utf-8 -*-
"""User views."""
from flask import current_app as app
from flask import Blueprint, render_template

blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/')
def index():

    commit_hash = app.config['COMMIT_HASH']
    deploy_ts = app.config['DEPLOY_TS']

    return render_template(
        'pages/about.html',
        commit_hash=commit_hash,
        deploy_ts=deploy_ts)
