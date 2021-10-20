from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class KeyGenForm(FlaskForm):
    """KeyGen form"""
    n_phrases = IntegerField(
        'Number of Secrets',
        [DataRequired()],
        default=10
    )
    n_words = IntegerField(
        'Max Number of Words Per Secret',
        [DataRequired()],
        default=6
    )
    char_limit = IntegerField(
        'Character Limit',
        [DataRequired()],
        default=32
    )
    joiner_char = StringField(
        'Character to Join Words',
        [
            DataRequired(),
            Length(min=1, max=1, message='Must be a single character.')
        ],
        default='-'
    )
    symbols = StringField(
        'Acceptable Symbols to Add to Secret',
        default='!@#$%^&*'
    )
    submit = SubmitField('Submit')
