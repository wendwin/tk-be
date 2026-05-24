from flask import Blueprint, request

from .schema import SiswaListSchema,SiswaDetailSchema, UpdateSiswaSchema
from .service import get_all_siswa, get_siswa_by_id, update_siswa

from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination


bp_siswa = Blueprint("siswa", __name__)

@bp_siswa.route("", methods=["GET"])
@role_required("admin", "guru")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = request.args.get("search")
        status = request.args.get("status")
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
        kelas_id = request.args.get("kelas_id", type=int)

        pagination = get_all_siswa(
            page=page,
            per_page=per_page,
            search=search,
            status=status,
            tahun_ajaran_id=tahun_ajaran_id,
            kelas_id=kelas_id,
        )

        schema = SiswaListSchema(many=True)
        data = schema.dump(pagination.items)

        return success_response(
            message="Berhasil mengambil data siswa",
            data=data,
            meta=format_pagination(pagination),
        )

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru")
def show(id):
    try:
        siswa = get_siswa_by_id(id)

        schema = SiswaDetailSchema()
        data = schema.dump(siswa)

        return success_response(
            message="Berhasil mengambil detail siswa",
            data=data,
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_siswa.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateSiswaSchema()
        data = schema.load(request.json)

        siswa = update_siswa(id, data)

        result_schema = SiswaDetailSchema()
        result = result_schema.dump(siswa)

        return success_response(
            message="Data siswa berhasil diupdate",
            data=result,
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)