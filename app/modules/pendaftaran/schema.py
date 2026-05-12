import json
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class AlamatSchema(Schema):
    
    alamat_lengkap = fields.Str(required=True, validate=validate.Length(min=5, max=255))
    rt = fields.Str(required=True,validate=[
            validate.Length(max=3),
            validate.Regexp(r'^\d+$', error="RT harus angka")
        ])
    rw = fields.Str(required=True,validate=[
            validate.Length(max=3),
            validate.Regexp(r'^\d+$', error="RW harus angka")
        ])
    kelurahan = fields.Str(required=True)
    kecamatan = fields.Str(required=True)
    kabupaten = fields.Str(required=True)
    kode_pos = fields.Str(required=True, validate=[
            validate.Length(equal=5),
            validate.Regexp(r'^\d+$', error="Kode pos harus angka")
        ])

class OrangTuaSchema(Schema):
    tipe = fields.Str(
        required=True,
        validate=validate.OneOf(['ayah', 'ibu', 'wali'])
    )
    nama = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    tempat_lahir = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    tanggal_lahir = fields.Date(required=True)
    nik = fields.Str(
        required=True,
        validate=[
            validate.Length(equal=16),
            validate.Regexp(r'^\d{16}$', error='NIK harus 16 digit angka')
        ]
    )
    pendidikan = fields.Str(
        required=True,
        validate=validate.OneOf(['SD','SMP','SMA','D1','D2','D3','D4','S1','S2','S3'])
    )
    pekerjaan = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    pendapatan = fields.Decimal(
        as_string=True,
        required=False,
        allow_none=True
    )
    alamat_kantor = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=255)
    )
    no_hp = fields.Str(
        required=True,
        validate=[
            validate.Length(min=10, max=20),
            validate.Regexp(r'^\d+$', error='No HP hanya boleh angka')
        ]
    )
    email = email = fields.Email(required=True)
    alamat = fields.Nested(AlamatSchema, dump_only=True)

class KesehatanSchema(Schema):
    berat_badan = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=300)
    )
    tinggi_badan = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=250)
    )
    lingkar_kepala = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=100)
    )
    golongan_darah = fields.Str(
        required=True,
        validate=validate.OneOf(['A', 'B', 'AB', 'O'])
    )
    riwayat_penyakit = fields.Str(required=True)
    alergi = fields.Str(required=True)
    kebutuhan_khusus = fields.List(
        fields.Str(),
        required=True,
        validate=validate.Length(min=1)
    )

class InformasiSchema(Schema):
    tinggal_dengan = fields.Str(
        required=True,
        validate=validate.OneOf(["orang tua", "wali", "asrama"])
    )
    jarak_sekolah = fields.Float(
        required=True,
        validate=validate.Range(min=0)
    )
    waktu_tempuh = fields.Str(
        required=True,
        validate=validate.Length(max=50)
    )
    kendaraan = fields.Str(
        required=True,
        validate=validate.OneOf(["jalan kaki","sepeda","sepeda motor","mobil","angkutan umum"
        ])
    )
    pernah_sekolah = fields.Boolean(required=True)

    nama_sekolah = fields.Str(allow_none=True, validate=validate.Length(max=150))
    npsn = fields.Str(allow_none=True, validate=validate.Length(max=20))
    nisn = fields.Str(allow_none=True, validate=validate.Length(max=20))

    bakat = fields.Str(allow_none=True, validate=validate.Length(max=100))
    hobi = fields.Str(allow_none=True, validate=validate.Length(max=100))
    cita_cita = fields.Str(allow_none=True, validate=validate.Length(max=100))
    sumber_informasi = fields.Str(allow_none=True, validate=validate.Length(max=100))

    @validates_schema
    def validate_kondisional(self, data, **kwargs):
        if data.get("pernah_sekolah"):
            required_if_true = ["nama_sekolah", "npsn", "nisn"]

            for field in required_if_true:
                if not data.get(field):
                    raise ValidationError(
                        {field: "Wajib diisi jika pernah sekolah"}
                    )

class PesertaSchema(Schema):
    nama_lengkap = fields.Str(required=True)
    nama_panggilan = fields.Str(required=True)
    tempat_lahir = fields.Str(required=True)
    tanggal_lahir = fields.Date(required=True)
    jenis_kelamin = fields.Str(
        required=True,
        validate=validate.OneOf(['L', 'P'])
    )
    kewarganegaraan = fields.Str(required=True)
    nik = fields.Str(
        required=True,
        validate=[
            validate.Length(equal=16),
            validate.Regexp(r'^\d{16}$', error='NIK harus 16 digit angka')
        ]
    )
    no_kk = fields.Str(
        required=True,
        validate=[
            validate.Length(equal=16),
            validate.Regexp(r'^\d{16}$', error='No KK harus 16 digit angka')
        ]
    )
    no_akta = fields.Str(required=True, validate=validate.Length(max=25))
    agama = fields.Str(
        required=True,
        validate=validate.OneOf([
            'islam','kristen','katolik','hindu','buddha','konghucu'
        ])
    )
    no_telp = fields.Str(
        required=True,
        validate=[
            validate.Length(min=10, max=20),
            validate.Regexp(r'^\+?\d+$', error='No HP hanya boleh angka')
        ]
    )
    anak_ke = fields.Int(required=True)
    jumlah_saudara = fields.Int(required=True)
    bahasa = fields.Str(required=True)
    alamat_domisili = fields.Nested(AlamatSchema, required=True)
    alamat_kk = fields.Nested(AlamatSchema, required=False, allow_none=True)

    alamat_kk_same = fields.Boolean(required=True)

    kesehatan = fields.Nested(KesehatanSchema, required=True)
    orang_tua = fields.Nested(OrangTuaSchema, many=True, required=True)
    informasi = fields.Nested(InformasiSchema, required=True)

    @validates_schema
    def validate_alamat(self, data, **kwargs):
        same = data.get("alamat_kk_same")

        if same is False and not data.get("alamat_kk"):
            raise ValidationError(
                "Alamat KK wajib diisi jika tidak sama dengan domisili",
                field_name="alamat_kk"
            )

class DokumenSchema(Schema):
    jenis_dokumen = fields.Str(
        required=True,
        validate=validate.OneOf(['kk','akta','kia','foto','surat_pernyataan','bukti_pembayaran'])
    )
    file_path = fields.Str(
        required=True,
        validate=validate.Length(max=500)
    )

class GelombangSchema(Schema):
    id = fields.Int(dump_only=True)
    tahun_ajaran_id = fields.Int(required=True)
    nama = fields.Str(
        required=True,
        validate=validate.Length(max=50)
    )
    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)

    @validates_schema
    def validate_tanggal(self, data, **kwargs):
        if data['tanggal_selesai'] < data['tanggal_mulai']:
            raise ValidationError(
                "Tanggal selesai tidak boleh sebelum tanggal mulai",
                field_name="tanggal_selesai"
            )

class TahunAjaranSchema(Schema):
    id = fields.Int(dump_only=True)
    tahun_mulai = fields.Int(dump_only=True)
    tahun_selesai = fields.Int(dump_only=True)
    label = fields.Method("get_label", dump_only=True)

    def get_label(self, obj):
        if not obj:
            return None
        return f"{obj.tahun_mulai}/{obj.tahun_selesai}"

class PendaftaranSchema(Schema):
    id = fields.Int(dump_only=True)
    no_pendaftaran = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    status = fields.Str(
        dump_only=True,
        validate=validate.OneOf(['draft','pending','verified','accepted','rejected'])
    )
    status_pembayaran = fields.Str(
        dump_only=True,
        validate=validate.OneOf(['unpaid','pending','paid','failed'])
    )
    jenis = fields.Str(
        required=True,
        validate=validate.OneOf(['tk', 'kb'])
    )
    program = fields.Str(
        required=True,
        validate=validate.OneOf(['reguler','halfday','fullday'])
    )
    tahun_ajaran_id = fields.Int(required=True)
    peserta = fields.Nested(
        PesertaSchema,
        required=True
    )
    dokumen = fields.Nested(
        DokumenSchema,
        many=True,
        dump_only=True
    )
    tahun_ajaran = fields.Nested(
        TahunAjaranSchema,
        dump_only=True
    )
    gelombang = fields.Nested(
        GelombangSchema,
        dump_only=True
    )
    observasi_at = fields.DateTime(allow_none=True)
    status_observasi = fields.Str(
        dump_only=True,
        validate=validate.OneOf(['belum','terjadwal','hadir','tidak_hadir'])
    )


class PendaftaranListSchema(Schema):
    id = fields.Int(dump_only=True)
    no_pendaftaran = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    jenis = fields.Str(dump_only=True)
    program = fields.Str(dump_only=True)

    status = fields.Str(dump_only=True)
    status_pembayaran = fields.Str(dump_only=True)

    nama_lengkap = fields.Method("get_nama", dump_only=True)
    tahun_ajaran = fields.Method("get_tahun", dump_only=True)

    def get_nama(self, obj):
        if not obj or not obj.peserta:
            return None
        return obj.peserta.nama_lengkap

    def get_tahun(self, obj):
        if not obj or not obj.tahun_ajaran:
            return None
        return getattr(obj.tahun_ajaran, "label", None)