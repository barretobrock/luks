from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
)


class KeyGenForm(FlaskForm):
    """KeyGen form"""
    n_phrases = IntegerField(
        label='Number of Secrets to Generate',
        validators=[DataRequired()],
        description='The maximum number of possible passwords (secrets) to generate.',
        default=50
    )
    n_words = IntegerField(
        label='Max Number of Words Per Secret',
        validators=[DataRequired()],
        description='Maximum number of words per secret',
        default=6
    )
    char_limit = IntegerField(
        label='Max Characters',
        validators=[DataRequired()],
        default=64
    )
    joiner_char = StringField(
        label='Character to Join Words',
        validators=[
            DataRequired(),
            Length(min=1, max=1, message='Must be a single character.')
        ],
        default='-'
    )
    symbols = StringField(
        label='Acceptable Symbols to Pepper in Secret',
        default='!@#$%^&*'
    )
    submit = SubmitField('Submit')
