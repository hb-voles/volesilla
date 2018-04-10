# -*- coding: utf-8 -*-
"""User views."""
from flask import current_app as app
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound


blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/')
def index():

    commit_hash = app.config['COMMIT_HASH']
    commit_ts = app.config['COMMIT_TS']
    deploy_ts = app.config['DEPLOY_TS']

    return render_template(
        'pages/about.html',
        commit_hash=commit_hash,
        commit_ts=commit_ts,
        deploy_ts=deploy_ts)
