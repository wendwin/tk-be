from marshmallow import Schema, fields, validate

class AsesmenPertanyaanSchema(Schema):
    id = fields.Int(dump_only=True)
    pertanyaan = fields.Str(required=True)
    urutan = fields.Int()


class AsesmenJawabanItemSchema(Schema):
    id_pertanyaan = fields.Int(required=True)
    jawaban = fields.Raw(required=True)


class AsesmenSubmitSchema(Schema):
    id_pendaftaran = fields.Int(required=True)
    jawaban = fields.List(fields.Nested(AsesmenJawabanItemSchema), required=True)