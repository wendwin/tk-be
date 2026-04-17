from marshmallow import Schema, fields, validate

class AlamatSchema(Schema):
    alamat_lengkap = fields.Str()
    rt = fields.Str()
    rw = fields.Str()
    desa = fields.Str()
    kecamatan = fields.Str()
    kabupaten = fields.Str()
    kode_pos = fields.Str()

class OrangTuaSchema(Schema):
    tipe = fields.Str()
    nama = fields.Str()
    tempat_lahir = fields.Str()
    tanggal_lahir = fields.Date()
    nik = fields.Str()
    pendidikan = fields.Str()
    pekerjaan = fields.Str()
    pendapatan = fields.Float()
    alamat_kantor = fields.Str()
    no_hp = fields.Str()
    email = fields.Email()

    alamat = fields.Nested(AlamatSchema)

class KesehatanSchema(Schema):
    berat_badan = fields.Float()
    tinggi_badan = fields.Float()
    lingkar_kepala = fields.Float()
    golongan_darah = fields.Str()
    riwayat_penyakit = fields.Str()
    alergi = fields.Str()
    kebutuhan_khusus = fields.Str()

class InformasiSchema(Schema):
    tinggal_dengan = fields.Str()
    jarak_sekolah = fields.Float()
    waktu_tempuh = fields.Str()
    kendaraan = fields.Str()
    pernah_sekolah = fields.Boolean()
    nama_sekolah = fields.Str()
    npsn = fields.Str()
    nisn = fields.Str()
    bakat = fields.Str()
    hobi = fields.Str()
    cita_cita = fields.Str()

class PesertaSchema(Schema):
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

    alamat_domisili = fields.Nested(AlamatSchema)
    alamat_kk = fields.Nested(AlamatSchema)

    kesehatan = fields.Nested(KesehatanSchema)
    orang_tua = fields.Nested(OrangTuaSchema, many=True)
    informasi = fields.Nested(InformasiSchema)

class DokumenSchema(Schema):
    jenis_dokumen = fields.Str()
    file_path = fields.Str()
    uploaded_at = fields.DateTime()

class PendaftaranSchema(Schema):
    id = fields.Int()
    no_pendaftaran = fields.Str()
    tanggal_daftar = fields.DateTime()

    jenis_pendaftaran = fields.Str()
    program = fields.Str()

    peserta = fields.Nested(PesertaSchema)
    dokumen = fields.Nested(DokumenSchema, many=True)