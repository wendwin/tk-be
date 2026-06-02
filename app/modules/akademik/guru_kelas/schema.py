from marshmallow import Schema, fields, validate


class GuruNestedSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    role = fields.Str(attribute="role.name")
    full_name = fields.Method("get_full_name")

    def get_full_name(self, obj):
        first = obj.first_name or ""
        last = obj.last_name or ""

        return f"{first} {last}".strip()


class KelasNestedSchema(Schema):
    id = fields.Int()
    nama = fields.Str()
    jenjang = fields.Str()
    kelompok = fields.Str(allow_none=True)


class TahunAjaranNestedSchema(Schema):
    id = fields.Int()
    label = fields.Str()


class GuruKelasSchema(Schema):
    id = fields.Int(dump_only=True)

    guru_id = fields.Int()
    kelas_id = fields.Int()
    tahun_ajaran_id = fields.Int()
    peran = fields.Str()

    guru = fields.Nested(GuruNestedSchema)
    kelas = fields.Nested(KelasNestedSchema)
    tahun_ajaran = fields.Nested(TahunAjaranNestedSchema)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CreateGuruKelasSchema(Schema):
    guru_id = fields.Int(required=True)
    kelas_id = fields.Int(required=True)
    tahun_ajaran_id = fields.Int(required=True)
    peran = fields.Str(
        required=True,
        validate=validate.OneOf(["wali kelas", "pendamping"])
    )


class UpdateGuruKelasSchema(Schema):
    guru_id = fields.Int(required=False)
    kelas_id = fields.Int(required=False)
    tahun_ajaran_id = fields.Int(required=False)
    peran = fields.Str(
        required=False,
        validate=validate.OneOf(["wali kelas", "pendamping"])
    )