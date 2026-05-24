from datetime import date
from marshmallow import Schema, fields, validate

class UmurMixin:
    def calculate_umur(self, tanggal_lahir, detail=False, with_days=False):
        if not tanggal_lahir:
            return None

        today = date.today()

        years = today.year - tanggal_lahir.year
        months = today.month - tanggal_lahir.month
        days = today.day - tanggal_lahir.day

        if days < 0:
            months -= 1

            prev_month = today.month - 1 or 12
            prev_year = today.year if today.month != 1 else today.year - 1

            if prev_month in [1, 3, 5, 7, 8, 10, 12]:
                days += 31
            elif prev_month in [4, 6, 9, 11]:
                days += 30
            else:
                is_leap = (
                    prev_year % 4 == 0
                    and (prev_year % 100 != 0 or prev_year % 400 == 0)
                )
                days += 29 if is_leap else 28

        if months < 0:
            years -= 1
            months += 12

        total_months = years * 12 + months

        if detail and with_days:
            return f"{years} Tahun {months} Bulan {days} Hari ({total_months} Bulan {days} Hari)"

        if detail:
            return f"{years} Tahun {months} Bulan ({total_months} Bulan)"

        return f"{years} Tahun"
    
class UnassignedSiswaSchema(Schema, UmurMixin):
    id = fields.Int()
    nama_lengkap = fields.Str()
    jenis_kelamin = fields.Str()
    tanggal_lahir = fields.Date()
    umur = fields.Method("get_umur")
    jenis = fields.Str()
    program = fields.Str()
    observasi = fields.Raw()

    def get_umur(self, obj):
        return self.calculate_umur(
            obj.get("tanggal_lahir"),
            detail=True
        )

class SiswaInKelasSchema(Schema, UmurMixin):
    id = fields.Int()
    nama_lengkap = fields.Str(attribute="peserta.nama_lengkap")
    jenis_kelamin = fields.Str(attribute="peserta.jenis_kelamin")
    tanggal_lahir = fields.Date(attribute="peserta.tanggal_lahir")
    nisn = fields.Str()
    umur = fields.Method("get_umur")

    def get_umur(self, obj):
        if not obj.peserta:
            return None

        return self.calculate_umur(
            obj.peserta.tanggal_lahir,
            detail=True
        )


class KelasNestedSchema(Schema):
    id = fields.Int()
    nama = fields.Str()
    jenjang = fields.Str()
    kelompok = fields.Str(allow_none=True)
    kapasitas = fields.Int()


class TahunAjaranNestedSchema(Schema):
    id = fields.Int()
    label = fields.Str()


class SiswaKelasSchema(Schema):
    id = fields.Int()
    siswa_id = fields.Int()
    kelas_id = fields.Int()
    tahun_ajaran_id = fields.Int()
    status = fields.Str()

    siswa = fields.Nested(SiswaInKelasSchema)
    kelas = fields.Nested(KelasNestedSchema)
    tahun_ajaran = fields.Nested(TahunAjaranNestedSchema)


class AssignSiswaKelasSchema(Schema):
    siswa_id = fields.Int(required=True)
    kelas_id = fields.Int(required=True)
    tahun_ajaran_id = fields.Int(required=True)


class BulkAssignSiswaKelasSchema(Schema):
    kelas_id = fields.Int(required=True)
    tahun_ajaran_id = fields.Int(required=True)
    siswa_ids = fields.List(fields.Int(), required=True)


class UpdateSiswaKelasSchema(Schema):
    kelas_id = fields.Int(required=False)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["aktif", "naik", "tinggal", "pindah", "lulus"])
    )