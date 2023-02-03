from marshmallow import Schema, fields, ValidationError

class NoteSchema(Schema):
    name = fields.String(required=True, error_messages={"required": "Name is required."})
    description = fields.String()

    class Meta:
        strict = True

class UserSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Name is required."})
    password = fields.String(required=True, error_messages={"required": "Password is required."})

    class Meta:
        strict = True