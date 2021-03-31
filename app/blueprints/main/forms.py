from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class DashboardYearForm(FlaskForm):
    year = SelectField('Year', validators=[DataRequired()])
    submit = SubmitField('Get data')
