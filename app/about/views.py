# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from jinja2 import TemplateNotFound


blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/')
def index():
    return render_template('pages/about.html')
