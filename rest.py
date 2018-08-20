from flask import Flask, Blueprint, request
from flask_restplus import Api, Resource, fields

import db
from passlib.hash import sha256_crypt
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')  # doc=False
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password_candidate):
    if username and password_candidate:
        password_hash = db.get_password_hash(username)
        if password_hash:
            return sha256_crypt.verify(password_candidate, password_hash)
    return False


app.register_blueprint(blueprint)

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
    'user_uid': fields.Integer,
    'when': fields.DateTime(dt_format='rfc822')
})

cards = api.model('Model', {
    'card_uid': fields.String,
    'user_uid': fields.Integer
})


@api_users.route('/')
class Users(Resource):
    """Users."""

    @auth.login_required
    @api_users.doc('query all user data')
    @api_users.marshal_with(users)
    def get(self, **kwargs):
        return db.query_users()


@api_checkins.route('/')
class Checkins(Resource):
    """Checkins."""

    @api_checkins.marshal_with(checkins, code=201)
    def get(self, **kwargs):
        return db.query_checkins(), 201

    @api_checkins.doc('create_checkin')
    @api_checkins.expect(fields=checkins, code=201)
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        user_uid = json_data['user_uid']
        db.add_checkin(user_uid)
        return {'result': 'Checkin added'}, 201


@api_cards.route('/')
class Cards(Resource):
    """Cards."""

    @api_cards.marshal_with(cards)
    def get(self, **kwargs):
        return db.query_cards()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
