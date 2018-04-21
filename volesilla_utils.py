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
import sys
from datetime import datetime
from docopt import docopt
from flask.helpers import get_debug_flag

from app.app import create_app
from app.settings import DevConfig, ProdConfig
from app.extensions import db

from app.extensions import flask_bcrypt
from app.account.model import User


def main():
    """Entry point"""

    args = docopt(__doc__)

    if args['db_init'] and args['<db_file>']:

        config = DevConfig if get_debug_flag() else ProdConfig

        db_dir = os.path.join(config.PROJECT_ROOT, 'data')
        config.DB_NAME = args['<db_file>']
        config.DB_PATH = os.path.join(db_dir, config.DB_NAME)
        config.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_PATH)

        if os.path.isfile(config.DB_PATH):
            print('[WARNING] File [{}] already exists.'.format(config.DB_PATH))
            sys.exit(0)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        app = create_app(config_object=config)

        with app.app_context():
            db.init_app(app)
            db.create_all()

            admin = User(
                username='admin',
                password=flask_bcrypt.generate_password_hash(config.APP_ADMIN_PASS),
                email=config.APP_ADMIN_MAIL,
                confirmed_at=datetime.now(),
                active=True)

            db.session.add(admin)
            db.session.commit()

        print('[SUCCESS] File [{}] created.'.format(config.DB_PATH))
        sys.exit(0)


if __name__ == '__main__':
    main()
