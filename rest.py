from flask import Flask, Blueprint, request
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
        return db.query_users(), 200


@api_checkins.route('/')
class Checkins(Resource):
    """Checkins."""

    @auth.login_required
    @api_users.doc('query all checkin data')
    @api_checkins.marshal_with(checkins)
    def get(self, **kwargs):
        return db.query_checkins(), 200

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

    @auth.login_required
    @api_users.doc('query all user data')
    @api_cards.marshal_with(cards)
    def get(self, **kwargs):
        return db.query_cards(), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
