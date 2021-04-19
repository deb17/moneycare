from calendar import month_abbr

from flask_wtf import FlaskForm
from wtforms import (StringField, DateField, SelectField, SelectMultipleField,
                     DecimalField, BooleanField, SubmitField)
from wtforms.validators import Length, Optional, ValidationError
from wtforms.widgets import Select, html_params, HTMLString


class MultiSelectWidget(Select):
    def __init__(self):
        super().__init__(multiple=True)

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)
        kwargs['multiple'] = True
        html = []
        html.append('<select {}>'.format(
            html_params(name=field.name, **kwargs)
        ))
        html.append("<option disabled value=''>Choose one or more</option>")
        for val, label, selected in field.iter_choices():
            html.append(
                '<option {}>{}</option>'.format(
                    html_params(selected=selected, value=val),
                    label
                )
            )
        html.append('</select>')
        return HTMLString('\n'.join(html))


class CustomMultiSelect(SelectMultipleField):
    widget = MultiSelectWidget()


class SearchForm(FlaskForm):
    year = StringField('Year',
                       validators=[Optional(False), Length(min=4, max=4)],
                       render_kw={'placeholder': 'yyyy'})

    month = CustomMultiSelect(
        'Month',
        coerce=int,
        choices=[(i, month_abbr[i]) for i in range(1, 13)]
    )
    exact_date = DateField('Exact date',
                           validators=[Optional()],
                           render_kw={'type': 'date'})
    from_date = DateField('From date',
                          validators=[Optional()],
                          render_kw={'type': 'date'})
    to_date = DateField('To date',
                        validators=[Optional()],
                        render_kw={'type': 'date'})
    amt_cond = SelectField(
        choices=[('==', 'Equal to'),
                 ('>', 'Greater than'),
                 ('<', 'Less than'),
                 ('>=', 'Greater than or equal to'),
                 ('<=', 'Less than or equal to')]
    )
    amount = DecimalField(validators=[Optional()],
                          render_kw={'placeholder': 'Value'})
    amt_min = DecimalField(validators=[Optional()],
                           render_kw={'placeholder': 'Min value'})
    amt_max = DecimalField(validators=[Optional()],
                           render_kw={'placeholder': 'Max value'})
    text = StringField('Description or comments contains')
    simple_search = BooleanField('Search as a string of characters')
    payment_modes = CustomMultiSelect('Payment modes', coerce=int)
    tags = CustomMultiSelect('Tags', coerce=int)
    submit = SubmitField('Search')

    def validate_year(form, field):

        try:
            int(field.data)
        except Exception:
            raise ValidationError('Not a valid year.')

    def validate_exact_date(form, field):

        if field.data:
            if form.from_date.data or form.to_date.data:
                raise ValidationError('Both exact and from/to dates cannot '
                                      'be specified.')

    def validate_from_date(form, field):

        if field.data:
            if form.exact_date.data:
                raise ValidationError('Both exact and from dates cannot '
                                      'be specified.')

    def validate_to_date(form, field):

        if field.data:
            if form.exact_date.data:
                raise ValidationError('Both exact and to dates cannot '
                                      'be specified.')

    def validate_amount(form, field):

        if field.data:
            if form.amt_min.data or form.amt_max.data:
                raise ValidationError('Both amount and min/max cannot '
                                      'be specified.')

    def validate_amt_min(form, field):

        if field.data:
            if form.amount.data:
                raise ValidationError('Both amount and min amount cannot '
                                      'be specified.')

    def validate_amt_max(form, field):

        if field.data:
            if form.amount.data:
                raise ValidationError('Both amount and max amount cannot '
                                      'be specified.')
