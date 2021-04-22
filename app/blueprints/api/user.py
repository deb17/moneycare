from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

from app.extensions import db
from app.models import User
from .schemas.user import UserSchema, LoginSchema

bp = Blueprint('api.user', __name__, url_prefix='/api',
               description='Auth routes')


@bp.route('/login', methods=['POST'])
@bp.arguments(LoginSchema)
def login(args):
    '''Login to the MoneyCare app with username and password.

    Returns JWT token.
    '''

    username = args.get('username')
    password = args.get('password')

    user = User.query.filter_by(uname=username).first()
    if user:
        if user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token)

    return jsonify(msg='Bad username or password'), 401


@bp.route('/user')
class UserResource(MethodView):

    @bp.response(200, UserSchema)
    @bp.doc(security=[{'bearerAuth': []}])
    @jwt_required()
    def get(self):
        '''Get details of signed-in user.'''

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, message='User not found')
        return user

    @bp.arguments(UserSchema)
    def post(self, args):
        '''Register a new user with the MoneyCare app.'''

        username = args.get('username')
        email = args.get('email')
        password = args.get('password')

        new_user = User(uname=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(msg=f'User {username} created.'), 201
