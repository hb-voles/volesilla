from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from app.simple_page import simple_page


app = Flask(__name__)
Bootstrap(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

app.register_blueprint(simple_page)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run()
