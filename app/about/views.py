# -*- coding: utf-8 -*-
"""User views."""
from flask import current_app as app
from flask import Blueprint, render_template

from app.extensions import db_adapter, Team


BLUEPRINT = Blueprint('about', __name__, template_folder='templates')


@BLUEPRINT.route('/')
def index(team_url):
    '''View function'''

    team_obj = db_adapter.find_first_object(Team, url=team_url)

    commit_hash = app.config['COMMIT_HASH']
    deploy_ts = app.config['DEPLOY_TS']

    return render_template(
        'pages/about.html',
        team_name=team_obj.name,
        commit_hash=commit_hash,
        deploy_ts=deploy_ts)
