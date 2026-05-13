from marshmallow import Schema, fields, validate


class GPPHJawabanItemSchema(Schema):
    pertanyaan_id = fields.Integer(required=True)

    nilai = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=3)
    )


class CreateGPPHSchema(Schema):
    pendaftaran_id = fields.Integer(required=True)

    jawaban = fields.List(
        fields.Nested(GPPHJawabanItemSchema),
        required=True,
        validate=validate.Length(equal=10)
    )