from flask import current_app, send_from_directory
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from api.reports.services import ReportService
from api.users.models import UserModel

api = Namespace('reports', description='.pdf reports')


@api.route('/users/')
class ReportUserList(Resource):
    @jwt_required()
    def get(self):
        ReportService.make_report_users()

        return send_from_directory(
            current_app.config['REPORT_FOLDER'],
            'all_users.pdf',
            as_attachment=True
        )


@api.route('/transcripts/')
class ReportTranscriptList(Resource):
    @jwt_required()
    def get(self):
        ReportService.make_report_transcripts()

        return send_from_directory(
            current_app.config['REPORT_FOLDER'],
            'all_transcripts.pdf',
            as_attachment=True
        )


@api.route('/user/detail/<string:username>')
class ReportUserDetail(Resource):
    @jwt_required()
    def get(self, username: str):
        user = UserModel.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        ReportService.make_report_user_detail(user)

        return send_from_directory(
            current_app.config['REPORT_FOLDER'],
            username + '.pdf',
            as_attachment=True
        )
