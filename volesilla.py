# -*- coding: utf-8 -*-
"""Entrypoint"""

from flask.helpers import get_debug_flag
from app.app import create_app
from app.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig
app = create_app(config_object=CONFIG)  # pylint: disable=invalid-name
