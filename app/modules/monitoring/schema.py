from marshmallow import Schema, fields, validate


class MonitoringKKTPInputSchema(Schema):
    key = fields.Str(required=False)
    deskripsi = fields.Str(required=True)


class MonitoringTPInputSchema(Schema):
    key = fields.Str(required=False)
    elemen = fields.Str(
        required=True,
        validate=validate.OneOf(["kesyuhadaan", "nabp", "jd", "ddlmstrs"])
    )
    tujuan = fields.Str(required=True)
    kktp = fields.List(fields.Nested(MonitoringKKTPInputSchema), required=True)


class MonitoringKegiatanInputSchema(Schema):
    nama = fields.Str(required=True)
    media = fields.Str(allow_none=True)


class MonitoringAsesmenAwalInputSchema(Schema):
    teknik = fields.Str(required=True)
    rancangan_kegiatan = fields.Str(required=True)
    hasil = fields.Str(allow_none=True)


class MonitoringKaryaInputSchema(Schema):
    kktp_id = fields.Int(required=False)
    kktp_key = fields.Str(required=False)
    kegiatan = fields.Str(required=True)
    foto = fields.Str(allow_none=True)
    deskripsi = fields.Str(required=True)
    analisa = fields.Str(required=True)


class MonitoringAnekdotInputSchema(Schema):
    kktp_id = fields.Int(required=False)
    kktp_key = fields.Str(required=False)
    waktu = fields.DateTime(required=True)
    catatan = fields.Str(required=True)


class MonitoringIndikatorInputSchema(Schema):
    kktp_id = fields.Int(required=False)
    kktp_key = fields.Str(required=False)
    muncul = fields.Bool(required=True)
    kejadian_teramati = fields.Str(allow_none=True)


class MonitoringRekomendasiInputSchema(Schema):
    elemen = fields.Str(
        required=True,
        validate=validate.OneOf(["kesyuhadaan", "nabp", "jd", "ddlmstrs"])
    )
    tips = fields.Str(required=True)


class MonitoringSchema(Schema):
    id = fields.Int(dump_only=True)

    siswa_kelas_id = fields.Int(required=True)

    semester = fields.Int(required=True)
    minggu = fields.Int(required=True)

    topik = fields.Str(required=True)
    sub_topik = fields.Str(required=True)

    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)

    ringkasan = fields.Str(allow_none=True)

    status = fields.Str(validate=validate.OneOf(["draft", "published"]))

    replace_detail = fields.Bool(required=False)

    tujuan_pembelajaran = fields.List(
        fields.Nested(MonitoringTPInputSchema),
        required=True
    )

    kegiatan = fields.List(
        fields.Nested(MonitoringKegiatanInputSchema),
        required=True
    )

    asesmen_awal = fields.Nested(
        MonitoringAsesmenAwalInputSchema,
        required=False
    )

    karya = fields.List(
        fields.Nested(MonitoringKaryaInputSchema),
        required=False
    )

    anekdot = fields.List(
        fields.Nested(MonitoringAnekdotInputSchema),
        required=False
    )

    indikator = fields.List(
        fields.Nested(MonitoringIndikatorInputSchema),
        required=False
    )

    rekomendasi = fields.List(
        fields.Nested(MonitoringRekomendasiInputSchema),
        required=False
    )


class SiswaKelasMiniSchema(Schema):
    id = fields.Int()
    siswa = fields.Method("get_siswa")
    kelas = fields.Method("get_kelas")
    tahun_ajaran = fields.Method("get_tahun_ajaran")

    def get_siswa(self, obj):
        if not obj.siswa:
            return None

        return {
            "id": obj.siswa.id,
            "nama_lengkap": obj.siswa.peserta.nama_lengkap if obj.siswa.peserta else None,
            "nama_panggilan": obj.siswa.peserta.nama_panggilan if obj.siswa.peserta else None,
        }

    def get_kelas(self, obj):
        if not obj.kelas:
            return None

        return {
            "id": obj.kelas.id,
            "nama": obj.kelas.nama,
            "jenjang": obj.kelas.jenjang,
            "kelompok": obj.kelas.kelompok,
        }

    def get_tahun_ajaran(self, obj):
        if not obj.tahun_ajaran:
            return None

        return {
            "id": obj.tahun_ajaran.id,
            "label": obj.tahun_ajaran.label,
        }


class MonitoringListSchema(Schema):
    id = fields.Int()
    semester = fields.Int()
    minggu = fields.Int()
    topik = fields.Str()
    sub_topik = fields.Str()
    tanggal_mulai = fields.Date()
    tanggal_selesai = fields.Date()
    status = fields.Str()
    siswa_kelas = fields.Nested(SiswaKelasMiniSchema)


class MonitoringKKTPDetailSchema(Schema):
    id = fields.Int()
    deskripsi = fields.Str()


class MonitoringTPDetailSchema(Schema):
    id = fields.Int()
    elemen = fields.Str()
    tujuan = fields.Str()
    kktp = fields.Nested(MonitoringKKTPDetailSchema, many=True)


class MonitoringKegiatanDetailSchema(Schema):
    id = fields.Int()
    nama = fields.Str()
    media = fields.Str()


class MonitoringAsesmenAwalDetailSchema(Schema):
    id = fields.Int()
    teknik = fields.Str()
    rancangan_kegiatan = fields.Str()
    hasil = fields.Str()


class MonitoringKaryaDetailSchema(Schema):
    id = fields.Int()
    kegiatan = fields.Str()
    foto = fields.Str()
    deskripsi = fields.Str()
    analisa = fields.Str()
    kktp = fields.Nested(MonitoringKKTPDetailSchema)


class MonitoringAnekdotDetailSchema(Schema):
    id = fields.Int()
    waktu = fields.DateTime()
    catatan = fields.Str()
    kktp = fields.Nested(MonitoringKKTPDetailSchema)


class MonitoringIndikatorDetailSchema(Schema):
    id = fields.Int()
    muncul = fields.Bool()
    kejadian_teramati = fields.Str()
    kktp = fields.Nested(MonitoringKKTPDetailSchema)


class MonitoringRekomendasiDetailSchema(Schema):
    id = fields.Int()
    elemen = fields.Str()
    tips = fields.Str()


class MonitoringDetailSchema(Schema):
    id = fields.Int()

    siswa_kelas = fields.Nested(SiswaKelasMiniSchema)

    semester = fields.Int()
    minggu = fields.Int()
    topik = fields.Str()
    sub_topik = fields.Str()
    tanggal_mulai = fields.Date()
    tanggal_selesai = fields.Date()
    ringkasan = fields.Str()
    status = fields.Str()

    tujuan_pembelajaran = fields.Nested(
        MonitoringTPDetailSchema,
        many=True,
        attribute="tp"
    )

    kegiatan = fields.Nested(MonitoringKegiatanDetailSchema, many=True)
    asesmen_awal = fields.Nested(MonitoringAsesmenAwalDetailSchema)

    karya = fields.Nested(MonitoringKaryaDetailSchema, many=True)
    anekdot = fields.Nested(MonitoringAnekdotDetailSchema, many=True)
    indikator = fields.Nested(MonitoringIndikatorDetailSchema, many=True)
    rekomendasi = fields.Nested(MonitoringRekomendasiDetailSchema, many=True)   