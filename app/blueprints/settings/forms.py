from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from flask_login import current_user
from app.models import PaymentMode, Tag


class SettingsForm(FlaskForm):

    limit = IntegerField('Transaction limit', validators=[DataRequired()])
    allow_decimals = BooleanField('Allow decimals')
    country_code = StringField('2 letter country code (to set locale)',
                               validators=[DataRequired(),
                                           Length(min=2, max=2)])
    ccy_iso = StringField('3 letter currency code',
                          validators=[DataRequired(), Length(min=3, max=3)])
    ccy_override = StringField('Override currency symbol',
                               validators=[Optional(), Length(min=1, max=6)])
    submit = SubmitField('Save')


class PaymentModeAddForm(FlaskForm):

    mode = StringField('Payment mode', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_mode(form, field):

        PM = PaymentMode
        mode = PM.query.filter(
            PM.user_id == current_user.id, PM.mode == field.data).first()

        if mode:
            raise ValidationError('This mode is already present.')


class PaymentModeEditForm(FlaskForm):

    mode = StringField('Payment mode', validators=[DataRequired()])
    submit = SubmitField('Save')

    def validate_mode(form, field):

        PM = PaymentMode
        mode = PM.query.filter(
            PM.user_id == current_user.id, PM.mode == field.data).first()

        if mode and mode.id != request.view_args['id']:
            raise ValidationError('This mode is already present.')


class TagForm(FlaskForm):

    tagname = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_tagname(form, field):

        tag = Tag.query.filter(
            Tag.user_id == current_user.id,
            Tag.tagname == field.data.lower()
        ).first()

        if tag:
            raise ValidationError('This tag is already present.')
