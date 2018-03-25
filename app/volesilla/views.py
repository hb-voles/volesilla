# -*- coding: utf-8 -*-
"""User views."""

from flask import current_app as app
from flask import Blueprint, render_template

from app.extensions import db_adapter, Team

BLUEPRINT = Blueprint('volesilla', __name__, template_folder='templates')


@BLUEPRINT.route('/')
def index():
    '''View function'''

    teams = db_adapter.find_all_objects(Team)

    commit_hash = app.config['COMMIT_HASH']
    deploy_ts = app.config['DEPLOY_TS']

    return render_template(
        'pages/volesilla.html',
        base_url=app.config['HOME_URL'],
        teams=teams,
        commit_hash=commit_hash,
        deploy_ts=deploy_ts)
