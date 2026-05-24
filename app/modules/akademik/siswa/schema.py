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

class SiswaAlamatSchema(Schema):
    alamat_lengkap = fields.Str()
    rt = fields.Str()
    rw = fields.Str()
    kelurahan = fields.Str()
    kecamatan = fields.Str()
    kabupaten = fields.Str()
    kode_pos = fields.Str()


class SiswaKesehatanSchema(Schema):
    berat_badan = fields.Float()
    tinggi_badan = fields.Float()
    lingkar_kepala = fields.Float()
    golongan_darah = fields.Str()
    riwayat_penyakit = fields.Str()
    alergi = fields.Str()
    kebutuhan_khusus = fields.Raw()


class SiswaInformasiSchema(Schema):
    tinggal_dengan = fields.Str()
    jarak_sekolah = fields.Float()
    waktu_tempuh = fields.Str()
    kendaraan = fields.Str()
    pernah_sekolah = fields.Bool()
    nama_sekolah = fields.Str()
    npsn = fields.Str()
    nisn = fields.Str()
    bakat = fields.Str()
    hobi = fields.Str()
    cita_cita = fields.Str()
    sumber_informasi = fields.Str()


class SiswaOrangTuaSchema(Schema):
    tipe = fields.Str()
    nama = fields.Str()
    tempat_lahir = fields.Str()
    tanggal_lahir = fields.Date()
    nik = fields.Str()
    pendidikan = fields.Str()
    pekerjaan = fields.Str()
    pendapatan = fields.Decimal(as_string=True)
    alamat_kantor = fields.Str()
    no_hp = fields.Str()
    email = fields.Str()
    alamat = fields.Nested(SiswaAlamatSchema)


class SiswaPesertaDetailSchema(Schema):
    nama_lengkap = fields.Str()
    nama_panggilan = fields.Str()
    tempat_lahir = fields.Str()
    tanggal_lahir = fields.Date()
    jenis_kelamin = fields.Str()
    kewarganegaraan = fields.Str()
    nik = fields.Str()
    no_kk = fields.Str()
    no_akta = fields.Str()
    agama = fields.Str()
    no_telp = fields.Str()
    anak_ke = fields.Int()
    jumlah_saudara = fields.Int()
    bahasa = fields.Str()

    alamat_domisili = fields.Nested(SiswaAlamatSchema)
    alamat_kk = fields.Nested(SiswaAlamatSchema)
    kesehatan = fields.Nested(SiswaKesehatanSchema)
    informasi = fields.Nested(SiswaInformasiSchema)
    orang_tua = fields.Nested(SiswaOrangTuaSchema, many=True)


class SiswaDetailSchema(Schema, UmurMixin):
    id = fields.Int(dump_only=True)
    peserta_id = fields.Int(dump_only=True)
    nisn = fields.Str(allow_none=True)
    tanggal_masuk = fields.Date(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    umur = fields.Method("get_umur")
    peserta = fields.Nested(SiswaPesertaDetailSchema)
    pendaftaran = fields.Method("get_pendaftaran")
    kelas_aktif = fields.Method("get_kelas_aktif")

    def get_umur(self, obj):
        if not obj or not obj.peserta:
            return None

        return self.calculate_umur(
            obj.peserta.tanggal_lahir,
            detail=True,
            with_days=True
        )

    def get_pendaftaran_accepted(self, obj):
        if not obj.peserta:
            return None

        accepted = [
            item for item in obj.peserta.pendaftaran
            if item.status == "accepted"
        ]

        if not accepted:
            return None

        return sorted(
            accepted,
            key=lambda item: item.created_at,
            reverse=True
        )[0]

    def get_pendaftaran(self, obj):
        pendaftaran = self.get_pendaftaran_accepted(obj)

        if not pendaftaran:
            return None

        return {
            "id": pendaftaran.id,
            "no_pendaftaran": pendaftaran.no_pendaftaran,
            "jenis": pendaftaran.jenis,
            "program": pendaftaran.program,
            "status": pendaftaran.status,
            "tahun_ajaran": {
                "id": pendaftaran.tahun_ajaran.id,
                "label": pendaftaran.tahun_ajaran.label,
                "tahun_mulai": pendaftaran.tahun_ajaran.tahun_mulai,
                "tahun_selesai": pendaftaran.tahun_ajaran.tahun_selesai,
            } if pendaftaran.tahun_ajaran else None,
            "gelombang": {
                "id": pendaftaran.gelombang.id,
                "nama": pendaftaran.gelombang.nama,
            } if pendaftaran.gelombang else None,
        }

    def get_kelas_aktif(self, obj):
        aktif = next(
            (
                item for item in getattr(obj, "riwayat_kelas", [])
                if item.status == "aktif"
            ),
            None
        )

        if not aktif:
            return None

        return {
            "id": aktif.id,
            "status": aktif.status,
            "kelas": {
                "id": aktif.kelas.id,
                "nama": aktif.kelas.nama,
                "jenjang": aktif.kelas.jenjang,
                "kelompok": aktif.kelas.kelompok,
            } if aktif.kelas else None,
            "tahun_ajaran": {
                "id": aktif.tahun_ajaran.id,
                "label": aktif.tahun_ajaran.label,
            } if aktif.tahun_ajaran else None,
        }
class SiswaListSchema(Schema):
    id = fields.Int(dump_only=True)
    nisn = fields.Str(allow_none=True)
    status = fields.Str()
    tanggal_masuk = fields.Date()

    nama_lengkap = fields.Method("get_nama_lengkap")
    jenis_kelamin = fields.Method("get_jenis_kelamin")
    jenis = fields.Method("get_jenis")
    program = fields.Method("get_program")
    kelas = fields.Method("get_kelas")
    tahun_ajaran = fields.Method("get_tahun_ajaran")

    def get_nama_lengkap(self, obj):
        return obj.peserta.nama_lengkap if obj.peserta else None

    def get_jenis_kelamin(self, obj):
        return obj.peserta.jenis_kelamin if obj.peserta else None

    def get_pendaftaran_accepted(self, obj):
        if not obj.peserta:
            return None

        accepted = [
            item for item in obj.peserta.pendaftaran
            if item.status == "accepted"
        ]

        if not accepted:
            return None

        return sorted(
            accepted,
            key=lambda item: item.created_at,
            reverse=True
        )[0]

    def get_jenis(self, obj):
        pendaftaran = self.get_pendaftaran_accepted(obj)
        return pendaftaran.jenis if pendaftaran else None

    def get_program(self, obj):
        pendaftaran = self.get_pendaftaran_accepted(obj)
        return pendaftaran.program if pendaftaran else None

    def get_kelas(self, obj):
        aktif = next(
            (
                item for item in getattr(obj, "riwayat_kelas", [])
                if item.status == "aktif"
            ),
            None
        )

        if not aktif or not aktif.kelas:
            return None

        return aktif.kelas.nama

    def get_tahun_ajaran(self, obj):
        aktif = next(
            (
                item for item in getattr(obj, "riwayat_kelas", [])
                if item.status == "aktif"
            ),
            None
        )

        if aktif and aktif.tahun_ajaran:
            return aktif.tahun_ajaran.label

        pendaftaran = self.get_pendaftaran_accepted(obj)

        if pendaftaran and pendaftaran.tahun_ajaran:
            return pendaftaran.tahun_ajaran.label

        return None


class UpdateSiswaSchema(Schema):
    nisn = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )

    status = fields.Str(
        required=False,
        validate=validate.OneOf([
            "aktif",
            "lulus",
            "keluar"
        ])
    )