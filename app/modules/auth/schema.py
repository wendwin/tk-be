from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100),
        error_messages={"required": "Nama depan wajib diisi"}
    )

    last_name = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=100)
    )

    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email wajib diisi", 
            "invalid": "Format email tidak valid"
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password minimal 8 karakter"),
        error_messages={"required": "Password wajib diisi"}
    )

class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email wajib diisi"})
    password = fields.Str(required=True, error_messages={"required": "Password wajib diisi"})

class ForgotPasswordSchema(Schema):
    email = fields.Email(
            required=True, 
            error_messages={
            "required": "Email wajib diisi", 
            "invalid": "Format email tidak valid"
        })

class ResetPasswordSchema(Schema):
    token = fields.String(required=True)
    password = fields.String(required=True)