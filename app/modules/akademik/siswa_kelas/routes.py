from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required

from app.modules.akademik.siswa_kelas.schema import (
    SiswaKelasSchema,
    AssignSiswaKelasSchema,
    BulkAssignSiswaKelasSchema,
    UpdateSiswaKelasSchema,
    UnassignedSiswaSchema,
)

from app.modules.akademik.siswa_kelas.service import (
    get_unassigned_siswa,
    get_siswa_by_kelas,
    get_rekomendasi_siswa_kelas,
    assign_siswa_kelas,
    bulk_assign_siswa_kelas,
    update_siswa_kelas,
    delete_siswa_kelas,
)


bp_siswa_kelas = Blueprint("siswa_kelas", __name__)


@bp_siswa_kelas.route("/unassigned", methods=["GET"])
@role_required("admin")
def unassigned():
    try:
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
        kelas_id = request.args.get("kelas_id", type=int)
        program = request.args.get("program")

        data = get_unassigned_siswa(
            tahun_ajaran_id=tahun_ajaran_id,
            kelas_id=kelas_id,
            program=program,
        )

        data = UnassignedSiswaSchema(many=True).dump(data)

        return success_response(
            message="Berhasil mengambil siswa belum masuk kelas",
            data=data
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("/rekomendasi", methods=["GET"])
@role_required("admin")
def rekomendasi():
    try:
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
        kelas_id = request.args.get("kelas_id", type=int)
        jenjang = request.args.get("jenjang")
        program = request.args.get("program")

        data = get_rekomendasi_siswa_kelas(
            tahun_ajaran_id=tahun_ajaran_id,
            kelas_id=kelas_id,
            program=program,
        )
        
        data = UnassignedSiswaSchema(many=True).dump(data)
        
        return success_response(
            message="Berhasil mengambil rekomendasi siswa",
            data=data
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("", methods=["GET"])
@role_required("admin", "guru")
def index():
    try:
        kelas_id = request.args.get("kelas_id", type=int)
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)

        siswa_kelas = get_siswa_by_kelas(
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id
        )

        schema = SiswaKelasSchema(many=True)
        data = schema.dump(siswa_kelas)

        return success_response(
            message="Berhasil mengambil siswa kelas",
            data=data
        )

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = AssignSiswaKelasSchema()
        data = schema.load(request.json)

        siswa_kelas = assign_siswa_kelas(data)

        result = SiswaKelasSchema().dump(siswa_kelas)

        return success_response(
            message="Siswa berhasil dimasukkan ke kelas",
            data=result,
            code=201
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("/bulk", methods=["POST"])
@role_required("admin")
def bulk_store():
    try:
        schema = BulkAssignSiswaKelasSchema()
        data = schema.load(request.json)

        result = bulk_assign_siswa_kelas(data)

        return success_response(
            message="Siswa berhasil dimasukkan ke kelas",
            data=SiswaKelasSchema(many=True).dump(result),
            code=201
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateSiswaKelasSchema()
        data = schema.load(request.json)

        siswa_kelas = update_siswa_kelas(id, data)

        return success_response(
            message="Data siswa kelas berhasil diupdate",
            data=SiswaKelasSchema().dump(siswa_kelas)
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa_kelas.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_siswa_kelas(id)

        return success_response(
            message="Siswa berhasil dikeluarkan dari kelas"
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)