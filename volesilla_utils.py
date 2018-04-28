# -*- coding: utf-8 -*-
"""volesilla_utils
Usage:
  volesilla_utils.py db_init <db_file>
  volesilla_utils.py db_add_user <db_file> <user_mail>
  volesilla_utils.py (-h | --help)
Options:
  -t                Testing environment
  -h --help         Show this screen.
  db_file           Absolute path to the DB file
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

    testing = os.environ.get('VLS_TESTING', 0)
    if testing:
        config = TestConfig
    else:
        config = DevConfig if get_debug_flag() else ProdConfig

    config.DB_FILE = args['<db_file>']
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_FILE)

    if args['db_init']:

        if os.path.isfile(config.DB_FILE):
            print('[WARNING] File [{}] already exists.'.format(config.DB_FILE))
            sys.exit(0)

        if not os.path.exists(os.path.dirname(config.DB_FILE)):
            os.makedirs(os.path.dirname(config.DB_FILE))

        app = create_app(config_object=config)

        with app.app_context():
            DB.init_app(app)
            DB.create_all()

        print('[SUCCESS] File [{}] created.'.format(config.DB_FILE))
        sys.exit(0)

    if args['db_add_user']:

        if not os.path.isfile(config.DB_FILE):
            print('[WARNING] File [{}] doesn\'t exist.'.format(config.DB_FILE))
            sys.exit(1)

        app = create_app(config_object=config)

        with app.app_context():
            DB.init_app(app)

            admin = User(
                email=args['<user_mail>'],
                password=BCRYPT.generate_password_hash(uuid.uuid4().hex),
                gdpr_version=config.GDPR_VERSION,
                is_active=False
            )

            DB.session.add(admin)
            DB.session.commit()

        print(
            '[SUCCESS] Admin user was set. For activation, you should reset password.')
        sys.exit(0)


if __name__ == '__main__':
    main()
