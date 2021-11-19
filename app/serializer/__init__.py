from flask_marshmallow import Marshmallow

ma = Marshmallow()


def setup(app):
    ma.init_app(app)
