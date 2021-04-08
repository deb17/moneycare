from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, DecimalField, SelectField,
                     TextAreaField, SubmitField)
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
    comments = TextAreaField('Comments (if any)', validators=[Length(max=512)])
    taglist = StringField(
        'Add tags (optional)',
        render_kw={'class': 'tagsinput'}
    )
    submit = SubmitField('Save')
