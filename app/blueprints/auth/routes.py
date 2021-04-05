from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

from app.models import User, Social
from app.extensions import db
from app.blueprints.auth.forms import (
    LoginForm,
    RegistrationForm,
    PasswordResetRequestForm,
    PasswordResetForm
)
from app.blueprints.auth.email import send_email


bp = Blueprint('auth', __name__)
google_blueprint = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'],
    redirect_to='auth.google_login'
)
twitter_blueprint = make_twitter_blueprint(redirect_to='auth.twitter_login')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        identity = form.identity.data
        user = User.query.filter(
            (User.uname == identity) | (User.email == identity)).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(
                    request.args.get('next', url_for('main.dashboard'))
                )
        flash('Invalid credentials.', 'danger')

    return render_template('auth/login.html', form=form, title='Sign in')


@bp.route('/logout')
def logout():
    logout_user()
    try:
        del google_blueprint.token
    except Exception:
        pass
    try:
        del twitter_blueprint.token
    except Exception:
        pass
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if new user has already made a social login
        u = User.query.join(User.social) \
            .filter((Social.gmail == form.email.data) |
                    (Social.tmail == form.email.data)) \
            .first()

        if u:
            u.username = form.username.data
            u.email = form.email.data
        else:
            u = User(
                uname=form.username.data,
                email=form.email.data
            )

        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('You have registered successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Sign in')


@bp.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get('/oauth2/v1/userinfo')
    retval = resp.json()

    user = User.query.outerjoin(Social) \
        .filter(
            (Social.gmail == retval['email']) |
            (Social.tmail == retval['email']) |
            (User.email == retval['email'])).first()

    if not user:
        user = User()
        user.social = Social(gname=retval['name'], gmail=retval['email'])
        db.session.add(user)
        db.session.commit()
    elif not user.social:
        user.social = Social(gname=retval['name'], gmail=retval['email'])
        db.session.commit()
    else:
        user.social.gname = retval['name']
        user.social.gmail = retval['email']
        db.session.commit()

    login_user(user)

    return redirect(request.args.get('next', url_for('main.dashboard')))


@bp.route('/twitter-login')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    resp = twitter.get('account/verify_credentials.json?include_email=true')
    retval = resp.json()  # Note - email may not be present

    user = User.query.outerjoin(Social) \
        .filter(
            (Social.gmail == retval['email']) |
            (Social.tmail == retval['email']) |
            (User.email == retval['email'])).first()

    if not user:
        user = User()
        user.social = Social(handle=retval['screen_name'],
                             tmail=retval.get('email'))
        db.session.add(user)
        db.session.commit()
    elif not user.social:
        user.social = Social(handle=retval['screen_name'],
                             tmail=retval.get('email'))
        db.session.commit()
    else:
        user.social.handle = retval['screen_name']
        user.social.tmail = retval.get('email')
        db.session.commit()

    login_user(user)

    return redirect(request.args.get('next', url_for('main.dashboard')))


@bp.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',
                           form=form, title='Reset password')


@bp.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.home'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.verify_reset_token(token)
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been updated.', 'info')
            return redirect(url_for('auth.login'))

        flash('Password could not be updated', 'danger')

    return render_template('auth/reset_password.html',
                           form=form, title='Reset password')
