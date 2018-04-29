"""Server test utils"""

import os
from multiprocessing import Process

from app.app import create_app
from app.settings import TestConfig


def start_server(test_dir, db_file):  # pylint: disable=unused-argument
    """Create client"""

    vls = {}

    config = TestConfig

    config.RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    config.RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    config.DB_FILE = db_file
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(config.DB_FILE)

    vls['db_file'] = db_file

    app = create_app(config_object=config)  # pylint: disable=invalid-name

    vls['server'] = Process(target=app.run)
    vls['server'].start()

    vls['client'] = app.test_client()
    vls['session'] = vls['client'].__enter__()

    pid_file = open(os.path.join(test_dir, 'flask_server.pid'), 'w')
    pid_file.write(str(vls['server'].pid))
    pid_file.close()

    return vls

    # with context.session.session_transaction() as sess:
    #     sess['key here'] = some_value
