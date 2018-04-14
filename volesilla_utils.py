# -*- coding: utf-8 -*-
"""volesilla_utils
Usage:
  volesilla_utils.py db_init <db_file>
  volesilla_utils.py (-h | --help)
Options:
  -h --help         Show this screen.
  db_file           <file> in schema sqlite:////PROJECT_ROOT/data/<file>
"""

import os
from docopt import docopt
from flask.helpers import get_debug_flag

from app.app import create_app
from app.settings import DevConfig, ProdConfig
from app.extensions import db


def main():
    """Entry point"""

    args = docopt(__doc__)

    if args['db_init'] and args['<db_file>']:

        CONFIG = DevConfig if get_debug_flag() else ProdConfig

        db_dir = os.path.join(CONFIG.PROJECT_ROOT, 'data')
        CONFIG.DB_NAME = args['<db_file>']
        CONFIG.DB_PATH = os.path.join(db_dir, CONFIG.DB_NAME)
        CONFIG.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(CONFIG.DB_PATH)

        if os.path.isfile(CONFIG.DB_PATH):
            print('[WARNING] File [{}] already exists.'.format(CONFIG.DB_PATH))
            return

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        db.create_all(app=create_app(config_object=CONFIG))
        print('[SUCCESS] File [{}] created.'.format(CONFIG.DB_PATH))


if __name__ == '__main__':
    main()
