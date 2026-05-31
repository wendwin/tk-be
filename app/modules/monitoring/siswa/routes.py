import os
import json
from flask import Blueprint, request, send_from_directory
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination

from .schema import (
    MonitoringSiswaSchema,
    MonitoringSiswaListSchema,
    MonitoringSiswaDetailSchema,
)

from .service import (
    get_all_siswa_monitoring,
    get_siswa_monitoring_by_id,
    create_siswa_monitoring,
    update_siswa_monitoring,
    publish_siswa_monitoring,
)

bp_monitoring_siswa = Blueprint("monitoring_siswa", __name__)


def parse_monitoring_request():
    data_raw = request.form.get("data")

    if not data_raw:
        raise ValueError("Data monitoring wajib diisi")

    return json.loads(data_raw), request.files


@bp_monitoring_siswa.route("", methods=["GET"])
@role_required("admin", "guru", "orang_tua")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        monitoring_mingguan_id = request.args.get("monitoring_mingguan_id", type=int)
        siswa_kelas_id = request.args.get("siswa_kelas_id", type=int)
        status = request.args.get("status")

        pagination = get_all_siswa_monitoring(
            page=page,
            per_page=per_page,
            monitoring_mingguan_id=monitoring_mingguan_id,
            siswa_kelas_id=siswa_kelas_id,
            status=status,
        )

        return success_response(
            message="Daftar monitoring siswa berhasil diambil",
            data=MonitoringSiswaListSchema(many=True).dump(pagination.items),
            meta=format_pagination(pagination),
        )

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring_siswa.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru", "orang_tua")
def show(id):
    try:
        monitoring = get_siswa_monitoring_by_id(id)

        return success_response(
            message="Detail monitoring siswa berhasil diambil",
            data=MonitoringSiswaDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        return error_response(str(e), code=404)

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring_siswa.route("", methods=["POST"])
@role_required("admin", "guru")
def store():
    try:
        user_id = get_jwt_identity()

        data, files = parse_monitoring_request()
        print("DATA MASUK:", data)
        
        schema = MonitoringSiswaSchema()
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = create_siswa_monitoring(data, user_id, files)

        return success_response(
            message="Monitoring siswa berhasil dibuat",
            data=MonitoringSiswaDetailSchema().dump(monitoring),
            code=201,
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=422)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring_siswa.route("/<int:id>", methods=["PUT"])
@role_required("admin", "guru")
def update(id):
    try:
        data, files = parse_monitoring_request()

        schema = MonitoringSiswaSchema(partial=True)
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = update_siswa_monitoring(id, data, files)

        return success_response(
            message="Monitoring siswa berhasil diperbarui",
            data=MonitoringSiswaDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=422)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring_siswa.route("/<int:id>/publish", methods=["PUT"])
@role_required("admin", "guru")
def publish(id):
    try:
        monitoring = publish_siswa_monitoring(id)

        return success_response(
            message="Monitoring siswa berhasil dipublikasikan",
            data=MonitoringSiswaDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)
    

@bp_monitoring_siswa.route("/file/karya/<path:filename>", methods=["GET"])
@role_required("admin", "guru", "orang_tua")
def show_karya_file(filename):
    try:
        folder = os.path.join(
            os.getcwd(),
            "uploads",
            "monitoring",
            "karya"
        )

        return send_from_directory(folder, filename)

    except Exception as e:
        return error_response(str(e), code=404)