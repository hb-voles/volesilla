# -*- coding: utf-8 -*-
"""volesilla_utils
Usage:
  volesilla_utils.py db_init <db_file>
  volesilla_utils.py check <db_file>
  volesilla_utils.py db_add_user <db_file> <user_mail>
  volesilla_utils.py rights_import <db_file> <rights_file>
  volesilla_utils.py (-h | --help)
Options:
  -t                Testing environment
  -h --help         Show this screen.
  db_file           Absolute path to the DB file
  rights_file       .yaml file with rights and roles definitions
"""

import os
import sys
import uuid
from datetime import datetime
from docopt import docopt
import yaml
from flask.helpers import get_debug_flag

from app.app import create_app
from app.settings import DevConfig, ProdConfig, TestConfig
from app.extensions import DB, BCRYPT
from app.author import get_rights_name

from app.database import Internal, Rights, User


def db_init(config):
    """Creation of database"""

    if os.path.isfile(config.DB_FILE):
        print('[WARNING] File [{}] already exists.'.format(config.DB_FILE))
        sys.exit(0)

    if not os.path.exists(os.path.dirname(config.DB_FILE)):
        os.makedirs(os.path.dirname(config.DB_FILE))

    app = create_app(config_object=config)

    with app.app_context():
        DB.init_app(app)
        DB.create_all()

        internal = Internal(
            db_version=config.DB_VERSION,
            updated_at=datetime.now()
        )

        DB.session.add(internal)
        DB.session.commit()

    print('[SUCCESS] File [{}] created.'.format(config.DB_FILE))


def db_check(config):
    """Check of database"""

    if not os.path.isfile(config.DB_FILE):
        print('[WARNING] File [{}] doesn\'t exist.'.format(config.DB_FILE))
        sys.exit(1)

    app = create_app(config_object=config)

    with app.app_context():
        DB.init_app(app)

        internal = Internal.query.order_by(Internal.db_version.desc()).first()

        if internal.db_version != config.DB_VERSION:
            print(
                '[WARNING] Schema version [{}] in file [{}] differs from proper [{}].'.format(
                    internal.db_version, config.DB_FILE, config.DB_VERSION)
            )
            sys.exit(0)

    print('[SUCCESS] Schema in [{}] file is in correct version [{}].'.format(
        config.DB_FILE, config.DB_VERSION))


def db_add_user(config, user_email):
    """Adding user"""

    if not os.path.isfile(config.DB_FILE):
        print('[WARNING] File [{}] doesn\'t exist.'.format(config.DB_FILE))
        sys.exit(1)

    app = create_app(config_object=config)

    with app.app_context():
        DB.init_app(app)

        user = User.query.filter_by(email=user_email).first()
        if user:
            print('[WARNING] User [{}] is already added. '.format(user_email))
            sys.exit(0)

        admin = User(
            email=user_email,
            password=BCRYPT.generate_password_hash(uuid.uuid4().hex),
            gdpr_version=config.GDPR_VERSION,
            is_active=True
        )

        DB.session.add(admin)
        DB.session.commit()

    print(
        '[SUCCESS] Admin user was set. For activation, you should reset password.')


def import_rights(config, rights_file):
    """Import rights to database

    :param config: Configuration object
    :param rights_file: File with rights and roles definitions
    :return:
    """

    with open(rights_file, 'r') as stream:
        roles_rights = yaml.load(stream)

    if not os.path.isfile(config.DB_FILE):
        print('[WARNING] File [{}] doesn\'t exist.'.format(config.DB_FILE))
        sys.exit(1)

    app = create_app(config_object=config)

    with app.app_context():
        DB.init_app(app)

        for group in roles_rights['rights']:
            for rule in roles_rights['rights'][group]:

                rights = Rights(
                    name=get_rights_name(group, rule['permission']),
                    group=group,
                    permission=rule['permission'],
                    description=rule['description']
                )

                DB.session.add(rights)

        DB.session.commit()

    print('[SUCCESS] Rights imported to [{}] file'.format(
        config.DB_FILE))


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
        db_init(config)
        sys.exit(0)

    if args['check']:
        db_check(config)
        sys.exit(0)

    if args['db_add_user']:
        db_add_user(config, args['<user_mail>'])
        sys.exit(0)

    if args['rights_import'] and args['<rights_file>']:
        import_rights(config, args['<rights_file>'])
        sys.exit(0)


if __name__ == '__main__':
    main()
