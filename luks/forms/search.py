from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
)


class SearchForm(FlaskForm):
    choices = [('tag', 'tag'), ('entry', 'entry')]
    select = SelectField('Search for entries: ', choices=choices)
    search = StringField('')
