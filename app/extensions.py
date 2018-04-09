# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_sqlalchemy import SQLAlchemy, Model
from flask_nav import Nav
from flask_nav.elements import *


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


db = SQLAlchemy(model_class=CRUDMixin)

nav = Nav()
nav.register_element('top', Navbar(
    View('About', 'about.index'),
    View('Something', 'about.index'),
    #Link('Seznam.cz', 'https://www.seznam.cz/'),
))


from dominate import tags
from flask_nav.renderers import Renderer

class JustDivRenderer(Renderer):
    # def visit_Navbar(self, node):
    #     print(">>> A: ", node.items)
    #     sub = []
    #     for item in node.items:
    #         sub.append(self.visit(item))
    #
    #     return tags.div('Navigation:', *sub)
    #
    # def visit_View(self, node):
    #     print(">>> B: ", node.text)
    #     return tags.div('{} ({})'.format(node.text, node.get_url()))
    #
    # def visit_Subgroup(self, node):
    #     print(">>> C: ", node.text)
    #     # almost the same as visit_Navbar, but written a bit more concise
    #     return tags.div(node.title,
    #                     *[self.visit(item) for item in node.items])

    def visit_object(self, node):
        print('>>> ', node)