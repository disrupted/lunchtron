"""Lunchtron REST API."""
import logging

from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

from passlib.hash import sha256_crypt
from flask_httpauth import HTTPBasicAuth
from lunchtron.models import Card, User, Admin, Checkin
from lunchtron.database import db_session

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

_LOGGER = logging.getLogger(__name__)

application = Flask(__name__)

# application.config.from_object(__name__)
# application.config.update(dict(
#     JSONIFY_PRETTYPRINT_REGULAR=False
# ))
# application.config.from_envvar('FLASK_SERVER_SETTINGS', silent=True)

application.url_map.strict_slashes = False
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')  # doc=False
application.register_blueprint(blueprint)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password_candidate):
    """Verify basic auth credentials."""
    admin = db_session.query(Admin).filter_by(username=username).first()
    if not admin:
        return False
    return sha256_crypt.verify(password_candidate, admin.password_hash)


api.namespaces.clear()  # get rid of default namespace
api_users = api.namespace('users', description='USER operations')
api_checkins = api.namespace('checkins', description='CHECKIN operations')
api_cards = api.namespace('cards', description='CARD operations')
api_admins = api.namespace('admins', description='ADMIN operations')


users = api.model('Model', {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Fixed(description='fixed-precision decimal', decimals=2),
    'balance': fields.Fixed(description='fixed-precision decimal', decimals=2)
})

checkins = api.model('Model', {
    'checkin_uid': fields.Integer,
    'user_uid': fields.Integer,
    'when': fields.DateTime(dt_format='rfc822')
})

cards = api.model('Model', {
    'card_uid': fields.String,
    'user_uid': fields.Integer
})

admins = api.model('Model', {
    'username': fields.String,
    'password_hash': fields.String
})


@application.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()


@application.route('/about')
def index():
    return 'ProVeg International'


@api_users.route('/')
class UserList(Resource):
    """Shows a list of all users and lets you POST to add new users"""

    @auth.login_required
    @api_users.marshal_with(users)
    def get(self):
        """List all users"""
        return db_session.query(User).all(), 200


@api_users.route('/<int:id>')
class UserDetail(Resource):
    """Show a single user."""

    @auth.login_required
    @api_users.doc('get_user')
    @api_users.marshal_with(users)
    def get(self, id):
        """List user by id"""
        return db_session.query(User).filter_by(id=id).one(), 200


@api_checkins.route('/')
class CheckinList(Resource):
    """Checkins."""

    @auth.login_required
    @api_checkins.doc('query all checkin data')
    @api_checkins.marshal_with(checkins)
    def get(self):
        """List all checkins"""
        return db_session.query(Checkin).all(), 200

    @api_checkins.doc('create_checkin')
    @api_checkins.expect(checkins)
    # @api_checkins.marshal_with(checkins, code=201)
    def post(self):
        """Create new checkin"""
        user_uid = api.payload['user_uid']
        print(user_uid)
        new_checkin = Checkin(user_uid=user_uid)
        db_session.add(new_checkin)
        db_session.flush()
        # return new_checkin.to_dict(), 201
        return 201
        # return {'checkin_uid': checkin_uid, 'result': 'Checkin added'}, 201
        # TODO return new checkin object, missing payload / argument


@api_checkins.route('/<int:checkin_uid>')
class CheckinDetail(Resource):
    """Show a single checkin."""

    @auth.login_required
    @api_checkins.doc('checkin_detail')
    @api_checkins.marshal_with(checkins)
    def get(self, checkin_uid):
        """Fetch chekin by id"""
        return db_session.query(Checkin).filter_by(checkin_uid=checkin_uid).one(), 200


@api_cards.route('/')
class CardList(Resource):
    """Cards."""

    @auth.login_required
    @api_cards.doc('list_all_cards')
    @api_cards.marshal_with(cards)
    def get(self):
        """List all cards"""
        return db_session.query(Card).all(), 200


@api_cards.route('/<card_uid>')
class CardDetail(Resource):
    """Show a single card."""

    @auth.login_required
    @api_cards.doc('card_detail')
    @api_cards.marshal_with(cards)
    def get(self, card_uid):
        """Fetch card by card_uid"""
        return db_session.query(Card).filter_by(card_uid=card_uid).one(), 200


@api_admins.route('/')
class AdminList(Resource):
    """Admins."""

    @auth.login_required
    @api_admins.doc('list_all_admins')
    @api_admins.marshal_with(admins)
    def get(self):
        """List all admins"""
        return db_session.query(Admin).all(), 200


@api_admins.route('/<username>')
class AdminDetail(Resource):
    """Show a single admin."""

    @auth.login_required
    @api_admins.doc('admin_detail')
    @api_admins.marshal_with(admins)
    def get(self, username):
        """Fetch admin by username"""
        return db_session.query(Admin).filter_by(username=username).one(), 200
