from marshmallow import validate, Schema, fields, post_load

from database import *


class User_valid(Schema):
    id = fields.Integer()
    email = fields.String(validate=validate.Email())
    username = fields.String(required=True)
    password = fields.String()
    phone = fields.String()
    role = fields.String()

    @post_load
    def get_user(self, data, **kwargs):
        return User(**data)


class Article_valid(Schema):
    id = fields.Integer()
    title = fields.String()
    text = fields.String()
    author_id = fields.Integer()
    create_date = fields.String()
    last_edit_date = fields.String()
    ready = fields.String()

    @post_load
    def get_note(self, data, **kwargs):
        return Article(**data)


class Request_valid(Schema):
    id = fields.Integer()
    title = fields.String()
    text = fields.String()
    article_id = fields.Integer()
    user_id = fields.Integer()
    DateTimeOfRequest = fields.String()
    status = fields.String()

    @post_load
    def get_edit(self, data, **kwargs):
        return Request(**data)
