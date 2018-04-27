# -*- coding: utf-8 -*-
"""volesilla_utils
Usage:
  volesilla_utils.py db_init [-t <testing_path>] <db_file>
  volesilla_utils.py (-h | --help)
Options:
  -t                Testing environment
  -h --help         Show this screen.
  db_file           <file> in schema sqlite:////PROJECT_ROOT/data/<file>
"""

import os
import sys
import uuid
from docopt import docopt
from flask.helpers import get_debug_flag

from app.app import create_app
from app.settings import DevConfig, ProdConfig, TestConfig
from app.extensions import DB, BCRYPT

from app.account.model import User


def main():
    """Entry point"""

    args = docopt(__doc__)

    if args['db_init'] and args['<db_file>']:

        if args['-t']:
            config = TestConfig
            config.PROJECT_ROOT = args['<testing_path>']

        else:
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
            DB.init_app(app)
            DB.create_all()

            admin = User(
                email=config.APP_ADMIN_MAIL,
                password=BCRYPT.generate_password_hash(uuid.uuid4().hex),
                gdpr_version=config.GDPR_VERSION,
                is_active=False
            )

            DB.session.add(admin)
            DB.session.commit()

        print('[SUCCESS] File [{}] created.'.format(config.DB_PATH))
        sys.exit(0)


if __name__ == '__main__':
    main()
