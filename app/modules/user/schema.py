from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    full_name = fields.Method("get_full_name")

    email = fields.Email()
    role_id = fields.Int()
    is_verified = fields.Bool()
    is_active = fields.Bool()

    role = fields.Method("get_role")

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    def get_full_name(self, obj):
        return obj.full_name

    def get_role(self, obj):
        if not obj.role:
            return None

        return {
            "id": obj.role.id,
            "name": obj.role.name,
        }


class UpdateUserSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    last_name = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    email = fields.Email(required=False)
    role_id = fields.Int(required=False)
    is_verified = fields.Bool(required=False)
    password = fields.Str(required=False)


class CreateUserSchema(Schema):
    first_name = fields.Str(required=False, validate=validate.Length(min=2, max=100))
    last_name = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role_id = fields.Int(required=True)
    is_verified = fields.Bool(required=False, load_default=True)