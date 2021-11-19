from app.serializer import ma
from marshmallow import fields

from .models import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

    id = fields.Integer(dump_only=True)
    password = fields.Str(load_only=True)
