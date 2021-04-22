import marshmallow as ma
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models import PaymentMode, Budget, Tag


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

    return payment_mode


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

    return estimate


def get_tags(obj):

    taglist = ','.join([tag.tagname for tag in obj.tags])
    return taglist


def set_tags(data):

    return [Tag(tagname=name) for name in data.split(',')]


class ExpenseSchema(ma.Schema):
    class Meta:
        ordered = True

    id = ma.fields.Int()
    description = ma.fields.Str(required=True)
    amount = ma.fields.Decimal(required=True, as_string=True)
    date = ma.fields.Date(required=True)
    payment_mode = ma.fields.Function(
        serialize=get_mode,
        deserialize=set_mode,
        required=True
    )
    estimate = ma.fields.Function(
        serialize=get_estimate,
        deserialize=set_estimate
    )
    comments = ma.fields.Str()
    tags = ma.fields.Function(
        serialize=get_tags,
        deserialize=set_tags
    )
    created_on = ma.fields.DateTime(dump_only=True)
    updated_on = ma.fields.DateTime(dump_only=True)


class ExpenseUpdateSchema(ExpenseSchema):
    description = ma.fields.Str()
    amount = ma.fields.Decimal(as_string=True)
    date = ma.fields.Date()
    payment_mode = ma.fields.Function(
        serialize=get_mode,
        deserialize=set_mode
    )
