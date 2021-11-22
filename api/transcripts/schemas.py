from api.transcripts.models import TranscriptModel
from app.serializer import ma
from api.users.schemas import UserSchema
from marshmallow import fields, post_load
from api.transcripts.dtos import AudioDTO


class TranscriptSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = TranscriptModel
        load_instance = True


class AudioSchema(ma.Schema):
    base64 = fields.String(required=True)
    username = fields.Email(required=True)

    @post_load
    def make_audio_dto(self, data, **kwargs):
        return AudioDTO(**data)
