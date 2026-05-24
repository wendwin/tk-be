from marshmallow import Schema, fields, validate

from app.modules.akademik.guru_kelas.schema import GuruKelasSchema
from app.modules.akademik.siswa_kelas.schema import SiswaKelasSchema

class KelasSchema(Schema):
    id = fields.Int(dump_only=True)
    tahun_ajaran_id = fields.Int(required=True)
    nama = fields.Str(required=True)
    jenjang = fields.Str(
        required=True,
        validate=validate.OneOf(["kb", "tk"])
    )
    kelompok = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["a", "b"])
    )
    kapasitas = fields.Int(required=True)

    tahun_ajaran = fields.Method("get_tahun_ajaran")
    total_guru = fields.Method("get_total_guru")

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def get_tahun_ajaran(self, obj):
        if not obj.tahun_ajaran:
            return None

        return {
            "id": obj.tahun_ajaran.id,
            "label": obj.tahun_ajaran.label,
            "tahun_mulai": obj.tahun_ajaran.tahun_mulai,
            "tahun_selesai": obj.tahun_ajaran.tahun_selesai,
        }
    
    def get_total_guru(self, obj):
        return len([
            item for item in obj.guru_kelas
            if item.tahun_ajaran_id == obj.tahun_ajaran_id
        ])

class KelasDetailSchema(KelasSchema):
    jumlah_siswa = fields.Method("get_jumlah_siswa")
    guru_kelas = fields.Method("get_guru_kelas")
    siswa_kelas = fields.Method("get_siswa_kelas")

    def get_jumlah_siswa(self, obj):
        return len([
            item for item in obj.siswa_kelas
            if item.tahun_ajaran_id == obj.tahun_ajaran_id
            and item.status == "aktif"
        ])

    def get_guru_kelas(self, obj):
        guru_kelas = [
            item for item in obj.guru_kelas
            if item.tahun_ajaran_id == obj.tahun_ajaran_id
        ]

        return GuruKelasSchema(many=True).dump(guru_kelas)

    def get_siswa_kelas(self, obj):
        siswa_kelas = [
            item for item in obj.siswa_kelas
            if item.tahun_ajaran_id == obj.tahun_ajaran_id
            and item.status == "aktif"
        ]

        return SiswaKelasSchema(many=True).dump(siswa_kelas)

class CreateKelasSchema(Schema):
    tahun_ajaran_id = fields.Int(required=True)
    nama = fields.Str(required=True)
    jenjang = fields.Str(
        required=True,
        validate=validate.OneOf(["kb", "tk"])
    )
    kelompok = fields.Str(
        allow_none=True,
        validate=validate.OneOf(["a", "b"])
    )
    kapasitas = fields.Int(required=True)



class UpdateKelasSchema(Schema):
    tahun_ajaran_id = fields.Int(required=False)
    nama = fields.Str(required=False)
    jenjang = fields.Str(
        required=False,
        validate=validate.OneOf(["kb", "tk"])
    )
    kelompok = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.OneOf(["a", "b"])
    )
    kapasitas = fields.Int(required=False)