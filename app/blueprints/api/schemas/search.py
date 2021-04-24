import calendar

import marshmallow as ma
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from .expense import ExpenseUpdateSchema
from app.models import PaymentMode, Budget


def get_mode(obj):
    return obj.payment_mode.mode


def set_mode(data):

    verify_jwt_in_request()
    user_id = get_jwt_identity()
    mode = data
    payment_mode = PaymentMode.query \
        .filter_by(user_id=user_id, mode=mode).first()

    if not payment_mode:
        raise ma.ValidationError('Payment mode does not exist.')

    return payment_mode.id


def get_estimate(obj):

    if obj.budget_id:
        return obj.estimate.item
    return None


def set_estimate(data):

    if not data:
        return None
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    item = data
    estimate = Budget.query \
        .filter_by(user_id=user_id, item=item).first()

    if not estimate:
        raise ma.ValidationError('Estimate does not exist.')

    return estimate.id


def get_tags(obj):

    taglist = ','.join([tag.tagname for tag in obj.tags])
    return taglist


def set_month(data):

    month_list = list(calendar.month_abbr)
    month_names = data.split(',')

    try:
        month_indexes = [month_list.index(name.title()) for name in
                         month_names]
    except Exception:
        raise ma.ValidationError('Month name should be abbreviated.')

    return month_indexes


def validate_year(year_str):

    try:
        year = int(year_str)
        if not (1900 < year < 2100):
            raise ValueError
    except Exception:
        raise ma.ValidationError('Year is invalid')


class SearchSchema(ExpenseUpdateSchema):

    payment_mode = ma.fields.Function(
        serialize=get_mode,
        deserialize=set_mode
    )
    estimate = ma.fields.Function(
        serialize=get_estimate,
        deserialize=set_estimate
    )
    tags = ma.fields.Function(
        serialize=get_tags
    )
    year = ma.fields.Str(validate=[ma.validate.Length(min=4, max=4),
                                   validate_year])
    month = ma.fields.Function(deserialize=set_month)
    exact_date = ma.fields.Date()
    from_date = ma.fields.Date()
    to_date = ma.fields.Date()
    amt_cond = ma.fields.Str(missing='==')
    amt_min = ma.fields.Decimal(as_string=True)
    amt_max = ma.fields.Decimal(as_string=True)
    text = ma.fields.Str(validate=ma.validate.Length(max=512))
    simple_search = ma.fields.Bool(missing=False)

    @ma.validates_schema
    def validate_amt_min(self, data, **kwargs):

        if data.get('amount') and data.get('amt_min'):
            raise ma.ValidationError('Both amount and amt_min cannot be '
                                     'specified.')

    @ma.validates_schema
    def validate_amt_max(self, data, **kwargs):

        if data.get('amount') and data.get('amt_max'):
            raise ma.ValidationError('Both amount and amt_max cannot be '
                                     'specified.')

    @ma.validates_schema
    def validate_from_date(self, data, **kwargs):

        if data.get('exact_date') and data.get('from_date'):
            raise ma.ValidationError('Both exact date and from-date cannot be '
                                     'specified.')

    @ma.validates_schema
    def validate_to_date(self, data, **kwargs):

        if data.get('exact_date') and data.get('to_date'):
            raise ma.ValidationError('Both exact date and to-date cannot be '
                                     'specified.')
