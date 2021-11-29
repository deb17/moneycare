from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, SelectField,
                     TextAreaField, SubmitField)
from wtforms.fields.html5 import DecimalField
from wtforms.validators import DataRequired, Length


class ExpenseForm(FlaskForm):

    description = StringField(
        'Briefly describe the expense',
        validators=[DataRequired()],
        render_kw={'autocomplete': 'off'}
    )
    date = DateField(
        'When was it made?',
        validators=[DataRequired()],
        render_kw={'type': 'date'}
    )
    amount = DecimalField(
        'Transaction amount',
        places=None,
        validators=[DataRequired()],
        render_kw={'autocomplete': 'off'}
    )
    pay_mode = SelectField('Payment mode', validators=[DataRequired()])
    estimate_entry = SelectField('Related estimate')
    comments = TextAreaField('Comments', validators=[Length(max=512)])
    taglist = StringField(
        'Add tags',
        render_kw={'class': 'tagsinput'}
    )
    submit = SubmitField('Save')
