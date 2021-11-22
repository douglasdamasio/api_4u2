from marshmallow import ValidationError
from api.users.schemas import UserSchema
from api.users.models import UserModel
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token

api = Namespace('auth', description='Authentication route')

auth_payload = api.model('AuthPayload', {
    'username': fields.String,
    'password': fields.String
})

jwt_payload = api.model('JwtPayload', {
    'access_token': fields.String,
})


@api.route('/')
class Authentication(Resource):
    @api.expect(auth_payload)
    @api.response(400, 'Fail')
    @api.response(200, 'Success', jwt_payload)
    def post(self):
        try:
            user = UserSchema().load(api.payload)
        except ValidationError as error:
            return error.args, 400

        user = UserModel.query.filter_by(username=user.username).first()

        if user and user.verify_password(api.payload['password']):
            return {
                'access_token': f'Bearer {create_access_token(identity=user.id)}',
            }, 200

        return {'message': 'Invalid Credentials'}, 400
