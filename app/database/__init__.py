from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup(app):
    db.init_app(app)
    app.db = db

    from api.users.models import UserModel
    from api.transcripts.models import TranscriptModel
