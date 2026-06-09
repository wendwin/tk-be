from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required

from app.modules.akademik.tahun_ajaran.schema import TahunAjaranSchema, CreateTahunAjaranSchema, UpdateTahunAjaranSchema

from app.modules.akademik.tahun_ajaran.service import get_all_tahun_ajaran,get_tahun_ajaran_by_id,create_tahun_ajaran,update_tahun_ajaran,delete_tahun_ajaran


bp_tahun_ajaran = Blueprint("tahun_ajaran", __name__)

@bp_tahun_ajaran.route("", methods=["GET"])
@role_required("admin", "guru", "kepsek")
def index():
    try:
        tahun_ajaran = get_all_tahun_ajaran()

        return success_response(
            message="Berhasil mengambil data tahun ajaran",
            data=TahunAjaranSchema(many=True).dump(tahun_ajaran)
        )

    except Exception as e:
        return error_response(str(e), 500)


@bp_tahun_ajaran.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru", "kepsek")
def show(id):
    try:
        tahun_ajaran = get_tahun_ajaran_by_id(id)

        return success_response(
            message="Berhasil mengambil detail tahun ajaran",
            data=TahunAjaranSchema().dump(tahun_ajaran)
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_tahun_ajaran.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = CreateTahunAjaranSchema()
        data = schema.load(request.json)

        tahun_ajaran = create_tahun_ajaran(data)

        return success_response(
            message="Tahun ajaran berhasil dibuat",
            data=TahunAjaranSchema().dump(tahun_ajaran),
            code=201
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_tahun_ajaran.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateTahunAjaranSchema()
        data = schema.load(request.json)

        tahun_ajaran = update_tahun_ajaran(id, data)

        return success_response(
            message="Tahun ajaran berhasil diupdate",
            data=TahunAjaranSchema().dump(tahun_ajaran)
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_tahun_ajaran.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_tahun_ajaran(id)

        return success_response(
            message="Tahun ajaran berhasil dihapus"
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)