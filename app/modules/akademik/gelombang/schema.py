from marshmallow import Schema, fields


class GelombangSchema(Schema):
    id = fields.Int(dump_only=True)
    tahun_ajaran_id = fields.Int(required=True)
    nama = fields.Str(required=True)
    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class GelombangUpdateSchema(Schema):
    nama = fields.Str(required=True)
    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)