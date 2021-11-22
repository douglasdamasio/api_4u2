from api import setup as setup_api
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from settings import Settings

from .database import setup as setup_db
from .serializer import setup as setup_ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)

    setup_db(app)
    setup_ma(app)
    setup_api(app)

    Migrate(app, app.db)
    JWTManager(app)

    return app
