# -*- coding: utf-8 -*-
"""volesilla_utils
Usage:
  volesilla_utils.py db_check <db_file>
  volesilla_utils.py db_init <db_file>
  volesilla_utils.py (-h | --help)
Options:
  -h --help         Show this screen.
  db_file           <file> in schema sqlite:////PROJECT_ROOT/data/<file>
"""

import os
import sys
from docopt import docopt
from flask.helpers import get_debug_flag

from app.app import create_app
from app.settings import DevConfig, ProdConfig
from app.extensions import db, db_adapter, Internal


def main():
    """Entry point"""

    args = docopt(__doc__)

    if args['db_check'] and args['<db_file>']:

        config = DevConfig if get_debug_flag() else ProdConfig

        db_dir = os.path.join(config.PROJECT_ROOT, 'data')
        config.DB_NAME = args['<db_file>']
        config.DB_PATH = os.path.join(db_dir, config.DB_NAME)
        config.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_PATH)

        if not os.path.isfile(config.DB_PATH):
            print('[ERROR] File [{}] doesn\'t exist!'.format(config.DB_PATH))
            sys.exit(2)

        app = create_app(config_object=config)
        db_version_from_conf = app.config['DB_VERSION']

        with app.app_context():
            db.init_app(app)
            db_version_from_file = db_adapter.get_object(Internal, 1).db_version

        if db_version_from_conf == db_version_from_file:
            print(
                '[SUCCESS] File [{}] has the same version as is needed. [version: {}]'.format(
                    config.DB_PATH,
                    db_version_from_conf))
            sys.exit(0)
        else:
            print('[WARNING] File [{}] has different version [{}] as is needed [{}].'.format(
                config.DB_PATH, db_version_from_file, db_version_from_conf))
            sys.exit(1)

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

            internal = Internal(db_version=config.DB_VERSION)

            from app.extensions import Team
            team = Team(name='Hell-Bent VoleS', url='voles')
            db.session.add(team)

            db.session.add(internal)
            db.session.commit()

        print('[SUCCESS] File [{}] created.'.format(config.DB_PATH))
        sys.exit(0)


if __name__ == '__main__':
    main()
