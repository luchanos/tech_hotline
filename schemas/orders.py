from marshmallow import Schema, fields


class NewOrderSchema(Schema):
    user_id = fields.Int(required=True, allow_none=False)
    text_message = fields.Str()
