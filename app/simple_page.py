from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@simple_page.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        form = MyForm()
        return render_template('pages/%s.html' % page,form=form)
    except TemplateNotFound:
        abort(404)
