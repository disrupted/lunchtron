from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

from lunchtron.models import User
from lunchtron.database import db_session

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

api.namespaces.clear()  # get rid of default namespace
api_users = api.namespace('users', description='USER operations')

users = api.model('Model', {
    'user_uid': fields.Integer,
    'name': fields.String,
    'price': fields.Fixed(description='fixed-precision decimal', decimals=2),
    'balance': fields.Fixed(description='fixed-precision decimal', decimals=2)
})


@application.teardown_appcontext
def shutdown_dbsession(exception=None):
    db_session.remove()


@application.route('/about')
def index():
    return 'ProVeg International'


# @application.route('/api/users')
# def users():
#     users = db_session.query(User).all()
#     return json.jsonify([user.to_dict() for user in users])

@api_users.route('/')
class UserList(Resource):
    """Shows a list of all users and lets you POST to add new users"""

    @api_users.marshal_with(users)
    def get(self):
        """List all users"""
        return db_session.query(User).all(), 200


@api_users.route('/<int:id>')
class UserDetail(Resource):
    """Show a single user."""

    # @auth.login_required
    @api_users.doc('get_user')
    @api_users.marshal_with(users)
    def get(self, id):
        """List user by id"""
        return db_session.query(User).filter(User.user_uid == id).one(), 200
