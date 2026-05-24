from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class TahunAjaranSchema(Schema):
    id = fields.Int(dump_only=True)
    tahun_mulai = fields.Int()
    tahun_selesai = fields.Int()
    tanggal_mulai = fields.Date()
    tanggal_selesai = fields.Date()
    is_active = fields.Bool()
    label = fields.Method("get_label")

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def get_label(self, obj):
        return obj.label


class CreateTahunAjaranSchema(Schema):
    tahun_mulai = fields.Int(required=True)
    tahun_selesai = fields.Int(required=True)
    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)
    is_active = fields.Bool(required=False, load_default=False)

    @validates_schema
    def validate_range(self, data, **kwargs):
        if data["tahun_selesai"] <= data["tahun_mulai"]:
            raise ValidationError("Tahun selesai harus lebih besar dari tahun mulai")

        if data["tanggal_selesai"] <= data["tanggal_mulai"]:
            raise ValidationError("Tanggal selesai harus lebih besar dari tanggal mulai")


class UpdateTahunAjaranSchema(Schema):
    tahun_mulai = fields.Int(required=False)
    tahun_selesai = fields.Int(required=False)
    tanggal_mulai = fields.Date(required=False)
    tanggal_selesai = fields.Date(required=False)
    is_active = fields.Bool(required=False)