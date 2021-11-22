from api.transcripts.models import TranscriptModel
from api.transcripts.schemas import TranscriptSchema
from api.users.models import UserModel
from api.users.views import user_payload
from flask import current_app
from flask_restx import Namespace, Resource, fields

api = Namespace('transcript', description='Users text transcript')

transcript_payload = api.model('TranscriptPayload', {
    'id': fields.Integer,
    'text': fields.String,
    'user': fields.Nested(user_payload),
    'create_at': fields.DateTime(dt_format='iso8601')
})


@api.route('/')
class TranscriptList(Resource):
    @api.marshal_with(transcript_payload, as_list=True, code=200)
    def get(self):
        transcripts = TranscriptModel.query.all()
        return TranscriptSchema(many=True).dump(transcripts), 200

    def post(self):
        ...


@api.route('/<int:id>')
class TranscriptDetail(Resource):
    @api.response(404, 'Transcript not found')
    @api.response(200, 'Success', transcript_payload)
    def get(self, id: int):
        transcript = TranscriptModel.query.filter_by(id=id).first()
        if not transcript:
            return {'message': 'Transcript not found'}, 404

        return TranscriptSchema().dump(transcript), 200

    @api.response(404, 'Transcript not found')
    @api.response(204, 'Success')
    def delete(self, id: int):
        transcript = TranscriptModel.query.filter_by(id=id).delete()
        if not transcript:
            return {'message': 'Transcript not found'}, 404

        current_app.db.session.commit()

        return {}, 204


@api.route('/<string:username>')
class TranscriptUserDetail(Resource):
    @api.response(404, 'Transcript not found')
    @api.response(200, 'Success')
    def get(self, username: str):
        transcripts = TranscriptModel.query.join(UserModel).\
            filter(UserModel.username == username).all()

        if not transcripts:
            return {'message': 'Transcripts not found'}, 404

        return TranscriptSchema(many=True).dump(transcripts), 200
