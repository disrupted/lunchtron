from flask import Flask, request
from flask_restplus import Api, Resource, fields

import db

app = Flask(__name__)
api = Api(app)

ns_users = api.namespace('users', description='USER operations')
ns_checkins = api.namespace('checkins', description='CHECKIN operations')
ns_cards = api.namespace('cards', description='CARD operations')

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


@ns_users.route('/')
class Users(Resource):
    """Users."""

    @ns_users.marshal_with(users)
    def get(self, **kwargs):
        return db.query_users()


@ns_checkins.route('/')
class Checkins(Resource):
    """Checkins."""

    @ns_checkins.marshal_with(checkins)
    def get(self, **kwargs):
        return db.query_checkins()

    @ns_checkins.expect(fields=checkins)
    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        user_uid = json_data['user_uid']
        db.add_checkin(user_uid)
        return {'result': 'Checkin added'}, 201


@ns_cards.route('/')
class Cards(Resource):
    """Cards."""

    @ns_cards.marshal_with(cards)
    def get(self, **kwargs):
        return db.query_cards()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
