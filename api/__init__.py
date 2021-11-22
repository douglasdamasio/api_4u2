from flask_restx import Api
from .users.views import api as users_api
from .transcripts.views import api as transcripts_api
from .reports.views import api as reports_api
from .auth.views import api as auth_api

api = Api(
    title='api_4u2',
    description='Minha primeira api da 4you2',
    authorizations={
        'bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
        },
    },
    security='bearer'
)


def setup(app):
    api.init_app(app)


api.add_namespace(users_api)
api.add_namespace(transcripts_api)
api.add_namespace(reports_api)
api.add_namespace(auth_api)
