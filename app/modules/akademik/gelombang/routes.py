from flask import Blueprint, request
from marshmallow import ValidationError

from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required
from app.modules.akademik.gelombang.schema import GelombangSchema, GelombangUpdateSchema
from app.modules.akademik.gelombang.service import (
    get_active_gelombang,
    get_gelombang_by_tahun_ajaran,
    get_gelombang_by_id,
    create_gelombang,
    update_gelombang,
    delete_gelombang,
)

bp_gelombang = Blueprint("gelombang", __name__)


@bp_gelombang.route("/tahun-ajaran/<int:tahun_ajaran_id>", methods=["GET"])
@role_required("admin")
def index_by_tahun_ajaran(tahun_ajaran_id):
    try:
        data = get_gelombang_by_tahun_ajaran(tahun_ajaran_id)
        schema = GelombangSchema(many=True)

        return success_response(
            message="Berhasil mengambil data gelombang",
            data=schema.dump(data),
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_gelombang.route("/<int:id>", methods=["GET"])
@role_required("admin")
def show(id):
    try:
        data = get_gelombang_by_id(id)
        schema = GelombangSchema()

        return success_response(
            message="Berhasil mengambil detail gelombang",
            data=schema.dump(data),
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_gelombang.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = GelombangSchema()
        data = schema.load(request.get_json())

        result = create_gelombang(data)

        return success_response(
            message="Gelombang berhasil dibuat",
            data=schema.dump(result),
            code=201,
        )

    except ValidationError as e:
        return error_response("Validation error", errors=e.messages, code=422)

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_gelombang.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = GelombangUpdateSchema()
        data = schema.load(request.get_json())

        result = update_gelombang(id, data)

        return success_response(
            message="Gelombang berhasil diupdate",
            data=GelombangSchema().dump(result),
        )

    except ValidationError as e:
        return error_response("Validation error", errors=e.messages, code=422)

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_gelombang.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_gelombang(id)

        return success_response(
            message="Gelombang berhasil dihapus"
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)
    
@bp_gelombang.route("/active", methods=["GET"])
def active():
    try:
        data = get_active_gelombang()

        return success_response(
            message="Berhasil mengambil gelombang aktif",
            data=GelombangSchema(many=True).dump(data),
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)