from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination
from app.utils.decorators import role_required

from .schema import MonitoringSchema, MonitoringListSchema, MonitoringDetailSchema
from .service import (
    get_all_monitoring,
    get_monitoring_by_id,
    create_monitoring,
    update_monitoring,
    publish_monitoring,
)

bp_monitoring = Blueprint("monitoring", __name__)


@bp_monitoring.route("", methods=["GET"])
@role_required("admin", "guru", "orang_tua")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        siswa_id = request.args.get("siswa_id", type=int)
        kelas_id = request.args.get("kelas_id", type=int)
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
        semester = request.args.get("semester", type=int)
        status = request.args.get("status")

        user_id = get_jwt_identity()

        pagination = get_all_monitoring(
            page=page,
            per_page=per_page,
            siswa_id=siswa_id,
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id,
            semester=semester,
            status=status,
            user_id=user_id,
        )

        schema = MonitoringListSchema(many=True)

        return success_response(
            message="Daftar monitoring berhasil diambil",
            data=schema.dump(pagination.items),
            meta=format_pagination(pagination),
        )

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru", "orang_tua")
def show(id):
    try:
        monitoring = get_monitoring_by_id(id)

        schema = MonitoringDetailSchema()

        return success_response(
            message="Detail monitoring berhasil diambil",
            data=schema.dump(monitoring),
        )

    except ValueError as e:
        return error_response(str(e), code=404)

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring.route("", methods=["POST"])
@role_required("admin", "guru")
def store():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()

        schema = MonitoringSchema()
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = create_monitoring(data, user_id)

        return success_response(
            message="Monitoring berhasil dibuat",
            data=MonitoringDetailSchema().dump(monitoring),
            code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring.route("/<int:id>", methods=["PUT"])
@role_required("admin", "guru")
def update(id):
    try:
        data = request.get_json()

        schema = MonitoringSchema(partial=True)
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = update_monitoring(id, data)

        return success_response(
            message="Monitoring berhasil diperbarui",
            data=MonitoringDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring.route("/<int:id>/publish", methods=["PUT"])
@role_required("admin", "guru")
def publish(id):
    try:
        monitoring = publish_monitoring(id)

        return success_response(
            message="Monitoring berhasil dipublikasikan",
            data=MonitoringDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)