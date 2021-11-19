from api.transcripts.models import TranscriptModel
from app.serializer import ma
from api.users.schemas import UserSchema
from marshmallow import fields


class TranscriptSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = TranscriptModel
        load_instance = True
