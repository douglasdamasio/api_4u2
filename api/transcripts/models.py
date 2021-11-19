from datetime import datetime

from app.database import db


class TranscriptModel(db.Model):
    __tablename__ = 'transcript'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    create_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        ), nullable=False)

    user = db.relationship(
        'UserModel',
        backref=db.backref('transcript')
    )

    def __repr__(self) -> str:
        return f'<Transcript {self.id}>'
