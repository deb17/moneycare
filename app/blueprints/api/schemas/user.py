import marshmallow as ma

from app.models import User


class LoginSchema(ma.Schema):
    class Meta:
        ordered = True

    username = ma.fields.String(required=True)
    password = ma.fields.String(required=True)


def validate_username(name):

    user = User.query.filter_by(uname=name).first()
    if user:
        raise ma.ValidationError('That username is taken.')


def validate_email(email):

    user = User.query.filter_by(email=email).first()
    if user:
        raise ma.ValidationError('That email is taken.')


class UserSchema(ma.Schema):
    class Meta:
        ordered = True

    username = ma.fields.String(required=True,
                                validate=[ma.validate.Length(min=3, max=64),
                                          validate_username])
    email = ma.fields.Email(required=True, validate=validate_email)
    password = ma.fields.String(required=True,
                                load_only=True,
                                validate=[ma.validate.Length(min=6)])
    role = ma.fields.String(dump_only=True)
    limit = ma.fields.Int(dump_only=True)
    country_code = ma.fields.String(dump_only=True)
    currency_code = ma.fields.String(attribute='ccy_iso', dump_only=True)
    currency_override = ma.fields.String(attribute='ccy_override',
                                         dump_only=True)
    locale = ma.fields.String(dump_only=True)
    allow_decimals = ma.fields.Bool(dump_only=True)
