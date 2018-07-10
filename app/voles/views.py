# -*- coding: utf-8 -*-
"""User views."""

from flask import Blueprint, render_template

from app.database import Player

BLUEPRINT = Blueprint('voles', __name__, template_folder='templates')


@BLUEPRINT.route('/')
def index():
    """View function"""

    players = Player.query.order_by(Player.name.desc()).all()

    return render_template('voles/voles.html', players=players)
