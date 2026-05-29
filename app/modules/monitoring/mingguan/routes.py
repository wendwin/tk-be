from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination

from .schema import MonitoringMingguanSchema, MonitoringMingguanListSchema, MonitoringMingguanDetailSchema
from .service import (
    get_all_mingguan,
    get_mingguan_by_id,
    create_mingguan,
    update_mingguan,
    publish_mingguan,
)

bp_monitoring_mingguan = Blueprint("monitoring_mingguan", __name__)


@bp_monitoring_mingguan.route("", methods=["GET"])
@role_required("admin", "guru")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        kelas_id = request.args.get("kelas_id", type=int)
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
        semester = request.args.get("semester", type=int)
        status = request.args.get("status")

        pagination = get_all_mingguan(
            page=page,
            per_page=per_page,
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id,
            semester=semester,
            status=status,
        )

        data = MonitoringMingguanListSchema(many=True).dump(pagination.items)

        return success_response(
            message="Daftar monitoring mingguan berhasil diambil",
            data=data,
            meta=format_pagination(pagination),
        )

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring_mingguan.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru")
def show(id):
    try:
        monitoring = get_mingguan_by_id(id)

        return success_response(
            message="Detail monitoring mingguan berhasil diambil",
            data=MonitoringMingguanDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        return error_response(str(e), code=404)

    except Exception as e:
        return error_response(str(e), code=500)


@bp_monitoring_mingguan.route("", methods=["POST"])
@role_required("admin", "guru")
def store():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()

        schema = MonitoringMingguanSchema()
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = create_mingguan(data, user_id)

        return success_response(
            message="Monitoring mingguan berhasil dibuat",
            data=MonitoringMingguanDetailSchema().dump(monitoring),
            code=201,
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring_mingguan.route("/<int:id>", methods=["PUT"])
@role_required("admin", "guru")
def update(id):
    try:
        data = request.get_json()

        schema = MonitoringMingguanSchema(partial=True)
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        monitoring = update_mingguan(id, data)

        return success_response(
            message="Monitoring mingguan berhasil diperbarui",
            data=MonitoringMingguanDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_monitoring_mingguan.route("/<int:id>/publish", methods=["PUT"])
@role_required("admin", "guru")
def publish(id):
    try:
        monitoring = publish_mingguan(id)

        return success_response(
            message="Monitoring mingguan berhasil dipublikasikan",
            data=MonitoringMingguanDetailSchema().dump(monitoring),
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)