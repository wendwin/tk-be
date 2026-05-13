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

class CreateKPSPPertanyaanSchema(Schema):
    usia_bulan = fields.Integer(required=True)
    aspek_perkembangan = fields.String(required=True)
    kemampuan_anak = fields.String(required=True)
    urutan = fields.Integer(required=True)


class UpdateKPSPPertanyaanSchema(Schema):
    usia_bulan = fields.Integer(required=True)
    aspek_perkembangan = fields.String(required=True)
    kemampuan_anak = fields.String(required=True)
    urutan = fields.Integer(required=True)

class KPSPJawabanItemSchema(Schema):
    pertanyaan_id = fields.Integer(required=True)
    jawaban = fields.String(required=True,validate=validate.OneOf(['ya', 'tidak']))
    keterangan = fields.String(allow_none=True)


class CreateKPSPSchema(Schema):
    pendaftaran_id = fields.Integer(required=True)
    catatan = fields.String(allow_none=True)
    jawaban = fields.List(fields.Nested(KPSPJawabanItemSchema),required=True)