from flask import Flask, Blueprint, request, render_template
from flask_restplus import Api, Resource, fields

import db
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.url_map.strict_slashes = False
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')  # doc=False
app.register_blueprint(blueprint)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password_candidate):
    """Verify basic auth credentials."""
    return db.verify_login(username, password_candidate)


api.namespaces.clear()  # get rid of default namespace
api_users = api.namespace('users', description='USER operations')
api_checkins = api.namespace('checkins', description='CHECKIN operations')
api_cards = api.namespace('cards', description='CARD operations')

users = api.model('Model', {
    'user_uid': fields.Integer,
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


@app.route('/')
def index():
    return render_template('index.html')


@api_users.route('/')
class UserList(Resource):
    """Shows a list of all users and lets you POST to add new users"""

    @auth.login_required
    @api_users.doc('list_users')
    @api_users.marshal_with(users)
    def get(self):
        """List all users"""
        return db.query_users(), 200


@api_users.route('/<int:id>')
class User(Resource):
    """Show a single user."""

    @auth.login_required
    @api_users.doc('get_user')
    @api_users.marshal_with(users)
    def get(self, id):
        """List user by id"""
        return db.query_user_by_id(id), 200


@api_checkins.route('/')
class CheckinList(Resource):
    """Checkins."""

    @auth.login_required
    @api_users.doc('query all checkin data')
    @api_checkins.marshal_with(checkins)
    def get(self, **kwargs):
        """List all checkins"""
        return db.query_checkins(), 200

    @api_checkins.doc('create_checkin')
    @api_checkins.expect(checkins)
    # @api_checkins.marshal_with(checkins, code=201)
    def post(self):
        """Create new checkin"""
        checkin_uid = db.create_checkin(api.payload['user_uid'])
        return {'checkin_uid': checkin_uid, 'result': 'Checkin added'}, 201
        # TODO return new checkin object, missing payload / argument


@api_checkins.route('/<int:checkin_uid>')
class Checkin(Resource):
    """Show a single checkin."""

    @auth.login_required
    @api_checkins.doc('get_user_card')
    @api_checkins.marshal_with(checkins)
    def get(self, checkin_uid):
        """Fetch chekin by id"""
        return db.query_checkin_by_id(checkin_uid), 200


@api_cards.route('/')
class CardList(Resource):
    """Cards."""

    @auth.login_required
    @api_users.doc('query all card data')
    @api_cards.marshal_with(cards)
    def get(self, **kwargs):
        """List all cards"""
        return db.query_cards(), 200


@api_cards.route('/<card_uid>')
class Card(Resource):
    """Show a single card."""

    @auth.login_required
    @api_cards.doc('get_card_user')
    @api_cards.marshal_with(cards)
    def get(self, card_uid):
        """Fetch card by card_uid"""
        return db.query_card_by_id(card_uid), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
