from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required

from app.modules.akademik.kelas.schema import  KelasSchema, KelasDetailSchema, CreateKelasSchema, UpdateKelasSchema
from app.modules.akademik.kelas.service import get_all_kelas, get_kelas_by_id, create_kelas, update_kelas, delete_kelas

bp_kelas = Blueprint("kelas", __name__)


@bp_kelas.route("", methods=["GET"])
@role_required("admin", "guru", "kepsek")
def index():
    try:
        kelas = get_all_kelas()

        schema = KelasSchema(many=True)
        data = schema.dump(kelas)

        return success_response(
            message="Berhasil mengambil data kelas",
            data=data
        )

    except Exception as e:
        return error_response(str(e), 500)


@bp_kelas.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru")
def show(id):
    try:
        kelas = get_kelas_by_id(id)

        data = KelasDetailSchema().dump(kelas)

        return success_response(
            message="Berhasil mengambil detail kelas",
            data=data
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_kelas.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = CreateKelasSchema()
        data = schema.load(request.json)

        kelas = create_kelas(data)

        result = KelasSchema().dump(kelas)

        return success_response(
            message="Kelas berhasil dibuat",
            data=result,
            code=201
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_kelas.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateKelasSchema()
        data = schema.load(request.json)

        kelas = update_kelas(id, data)

        result = KelasSchema().dump(kelas)

        return success_response(
            message="Kelas berhasil diupdate",
            data=result
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_kelas.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_kelas(id)

        return success_response(
            message="Kelas berhasil dihapus"
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)