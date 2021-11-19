from flask_restx import Api
from .users.views import api as users_api


api = Api(
    title='api_4u2',
    description='Minha primeira api da 4you2'
)


def setup(app):
    api.init_app(app)


api.add_namespace(users_api)