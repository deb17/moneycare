from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError
)

from app.models import User


class LoginForm(FlaskForm):
    identity = StringField(
        'Username or email',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Enter either username or email'}
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError('This username is already taken.')

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')
