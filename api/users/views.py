from flask import current_app

from api.users.models import UserModel
from api.users.schemas import UserSchema
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

api = Namespace('users', description='Usuários da API')

user_create_payload = api.model('UserCreatePayload', {
    'username': fields.String,
    'password': fields.String
})

user_payload = api.model('UserPayload', {
    'id': fields.Integer,
    'username': fields.String
})


@api.route('/')
class UserList(Resource):
    @api.marshal_with(user_payload, as_list=True, code=200)
    def get(self):
        users = UserModel.query.all()
        return UserSchema(many=True).dump(users), 200

    @api.expect(user_create_payload)
    def post(self):
        try:
            user = UserSchema().load(api.payload)
        except ValidationError as error:
            return error.args, 400

        user.generator_hash()

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return UserSchema().dump(user), 201


@api.route('/<int:id>')
class UserDetails(Resource):
    @api.response(404, 'User not found')
    @api.response(200, 'Success', user_payload)
    def get(self, id: int):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return {'message': 'User not found'}, 404

        return UserSchema().dump(user), 200

    @api.expect(user_payload)
    @api.response(404, 'User not found')
    @api.response(204, 'Success', user_payload)
    def put(self, id: int):
        user = UserModel.query.filter_by(id=id)
        if not user:
            return {'message': 'User not found'}, 404

        user.update(api.payload)
        current_app.db.session.commit()

        return UserSchema().dump(user), 204

    @api.response(404, 'User not found')
    @api.response(204, 'Success')
    def delete(self, id: int):
        user = UserModel.query.filter_by(id=id)
        if not user:
            return {'message': 'User not found'}, 404

        user.delete()

        current_app.db.session.commit()
        return {}, 204
