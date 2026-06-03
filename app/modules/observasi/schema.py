from marshmallow import Schema, fields, validate

class CreateGPPHPertanyaanSchema(Schema):
    nomor = fields.Integer(required=True)
    pertanyaan = fields.String(required=True)

class UpdateGPPHPertanyaanSchema(Schema):
    nomor = fields.Integer(required=True)
    pertanyaan = fields.String(required=True)
    
class GPPHJawabanItemSchema(Schema):
    pertanyaan_id = fields.Integer(required=True)

    nilai = fields.Integer(
        required=True,
        validate=validate.Range(min=0, max=3)
    )

class CreateGPPHSchema(Schema):
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
    is_active = fields.Boolean(load_default=True)


class UpdateKPSPPertanyaanSchema(Schema):
    usia_bulan = fields.Integer(required=True)
    aspek_perkembangan = fields.String(required=True)
    kemampuan_anak = fields.String(required=True)
    urutan = fields.Integer(required=True)
    is_active = fields.Boolean(load_default=True)

class KPSPJawabanItemSchema(Schema):
    pertanyaan_id = fields.Integer(required=True)
    jawaban = fields.String(required=True,validate=validate.OneOf(['ya', 'tidak']))
    keterangan = fields.String(allow_none=True)


class CreateKPSPSchema(Schema):
    catatan = fields.String(allow_none=True)
    jawaban = fields.List(fields.Nested(KPSPJawabanItemSchema),required=True)