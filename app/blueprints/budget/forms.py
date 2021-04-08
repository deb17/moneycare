from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, IntegerField,
                     TextAreaField, SubmitField)
from wtforms.validators import DataRequired


class BudgetForm(FlaskForm):

    item = StringField('Brief description', validators=[DataRequired()])
    estimate = IntegerField('Estimated year total')
    due = StringField('Frequency or due date (optional)',
                      render_kw={'placeholder': 'When is the expense due?'})
    comments = TextAreaField('Comments (optional)')
    active = BooleanField('Active', default="checked")
    submit = SubmitField('Create')
