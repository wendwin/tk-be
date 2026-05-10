from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class AlamatSchema(Schema):
    
    alamat_lengkap = fields.Str(required=True)
    rt = fields.Str(required=True)
    rw = fields.Str(required=True)
    kelurahan = fields.Str(required=True)
    kecamatan = fields.Str(required=True)
    kabupaten = fields.Str(required=True)
    kode_pos = fields.Str(required=True)

class OrangTuaSchema(Schema):
    
    tipe = fields.Str(
        required=True,
        validate=validate.OneOf(['ayah', 'ibu'])
    )
    nama = fields.Str(required=True)
    tempat_lahir = fields.Str(required=True)
    tanggal_lahir = fields.Date(required=True)
    nik = fields.Str(
        required=True,
        validate=[
            validate.Length(equal=16),
            validate.Regexp(r'^\d+$', error='NIK hanya boleh angka')
        ]
    )
    pendidikan = fields.Str(
        required=True,
        validate=validate.OneOf(['SD','SMP','SMA','D1','D2','D3','D4','S1','S2','S3'])
    )
    pekerjaan = fields.Str(required=True)
    pendapatan = fields.Decimal(as_string=True)
    alamat_kantor = fields.Str(allow_none=True)
    no_hp = fields.Str(
        required=True,
        validate=validate.Length(min=11, max=20)
    )
    email = fields.Email(allow_none=True)

    alamat = fields.Nested(AlamatSchema, dump_only=True)

class KesehatanSchema(Schema):
    berat_badan = fields.Float(allow_none=True)
    tinggi_badan = fields.Float(allow_none=True)
    lingkar_kepala = fields.Float(allow_none=True)
    golongan_darah = fields.Str(
        allow_none=True,
        validate=validate.OneOf(['A', 'B', 'AB', 'O'])
    )
    riwayat_penyakit = fields.Str(allow_none=True)
    alergi = fields.Str(allow_none=True)
    kebutuhan_khusus = fields.Str(allow_none=True)

class InformasiSchema(Schema):
    tinggal_dengan = fields.Str(allow_none=True)
    jarak_sekolah = fields.Float(allow_none=True)
    waktu_tempuh = fields.Str(allow_none=True)
    kendaraan = fields.Str(allow_none=True)
    pernah_sekolah = fields.Boolean(required=True)
    nama_sekolah = fields.Str(allow_none=True)
    npsn = fields.Str(allow_none=True)
    nisn = fields.Str(allow_none=True)
    bakat = fields.Str(allow_none=True)
    hobi = fields.Str(allow_none=True)
    cita_cita = fields.Str(allow_none=True)
    sumber_informasi = fields.Str(allow_none=True)

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
            validate.Regexp(r'^\d+$', error='NIK hanya boleh angka')
        ]
    )
    no_kk = fields.Str(
        required=True,
        validate=[
            validate.Length(equal=16),
            validate.Regexp(r'^\d+$', error='No KK hanya boleh angka')
        ]
    )
    no_akta = fields.Str(
        required=True,
        validate=validate.Length(max=25)
    )
    agama = fields.Str(
        required=True,
        validate=validate.OneOf(['islam','kristen','katolik','hindu','buddha','konghucu'])
    )
    no_telp = fields.Str(
        allow_none=True,
        validate=[
            validate.Length(min=11, max=20),
            validate.Regexp(r'^\d+$', error='No HP hanya boleh angka')
        ]
    )
    anak_ke = fields.Int(required=True)
    jumlah_saudara = fields.Int(required=True)
    bahasa = fields.Str(required=True)

    alamat_domisili = fields.Nested(AlamatSchema, required=True)
    alamat_kk = fields.Nested(AlamatSchema, required=False, allow_none=True)
    alamat_kk_same = fields.Boolean(required=True)
    
    kesehatan = fields.Nested(KesehatanSchema,required=True)
    orang_tua = fields.Nested(OrangTuaSchema,many=True,required=True)
    informasi = fields.Nested(InformasiSchema,required=True)

    @validates_schema
    def validate_alamat(self, data, **kwargs):
        if "alamat_kk_same" not in data:
            return

        if not data.get("alamat_kk_same") and not data.get("alamat_kk"):
            raise ValidationError(
                "alamat_kk wajib diisi jika tidak sama dengan domisili",
                field_name="alamat_kk"
            )

class DokumenSchema(Schema):
    jenis_dokumen = fields.Str(
        required=True,
        validate=validate.OneOf(['kk','akta','kia','foto','surat_pernyataan']))
    file_path = fields.Str(required=True)

class GelombangSchema(Schema):
    id = fields.Int()
    nama = fields.Str()

class TahunAjaranSchema(Schema):
    id = fields.Int()
    label = fields.Method("get_label")

    def get_label(self, obj):
        return f"{obj.tahun_mulai}/{obj.tahun_selesai}"

class PendaftaranSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    no_pendaftaran = fields.Str(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    status = fields.Str(validate=validate.OneOf(['draft','submitted','verified','accepted','rejected']))
    status_pembayaran = fields.Str(validate=validate.OneOf(['unpaid','pending','paid','failed']))
    jenis = fields.Str(required=True,validate=validate.OneOf(['tk', 'kb']))
    program = fields.Str(required=True,validate=validate.OneOf(['reguler','halfday','fullday']))
    
    tahun_ajaran_id = fields.Int(required=True)
    peserta = fields.Nested(
        PesertaSchema,
        required=True
    )
    dokumen = fields.Nested(
        DokumenSchema,
        many=True
    )
    tahun_ajaran = fields.Nested(
        TahunAjaranSchema,
        dump_only=True
    )
    gelombang = fields.Nested(
        GelombangSchema,
        dump_only=True
    )
    observasi_at = fields.DateTime(
        allow_none=True
    )
    status_observasi = fields.Str(dump_only=True,validate=validate.OneOf(['belum','terjadwal','hadir','tidak_hadir']))


class PendaftaranListSchema(Schema):
    id = fields.Int()
    no_pendaftaran = fields.Str()
    created_at = fields.DateTime()
    jenis = fields.Str()
    program = fields.Str()
    status = fields.Str()
    status_pembayaran = fields.Str()
    nama_lengkap = fields.Method("get_nama")
    tahun_ajaran = fields.Method("get_tahun")

    def get_nama(self, obj):
        return obj.peserta.nama_lengkap if obj.peserta else None

    def get_tahun(self, obj):
        return (
            obj.tahun_ajaran.label
            if obj.tahun_ajaran else None
        )