# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template

BLUEPRINT = Blueprint('voles', __name__, template_folder='templates')


@BLUEPRINT.route('/')
def index():
    '''View function'''

    return render_template('voles/voles.html')
