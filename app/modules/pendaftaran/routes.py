from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from flask import Blueprint, request, redirect
from .schema import PendaftaranSchema
from .service import get_all, create
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination

bp_pendaftaran = Blueprint('pendaftaran', __name__)

@bp_pendaftaran.route('', methods=['GET'])
@role_required('admin', 'orang_tua',)
def show():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search')

    pagination = get_all(page, per_page, search)

    schema = PendaftaranSchema(many=True)
    data = schema.dump(pagination.items)

    return success_response(
        data=data,
        code=200,
        message="Daftar pendaftaran berhasil diambil",
        meta=format_pagination(pagination)
    )

@bp_pendaftaran.route('', methods=['POST'])
@role_required('admin', 'orang_tua')
def store():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()

        schema = PendaftaranSchema()
        errors = schema.validate(data)
        if errors:
            return error_response("Validation error", errors=errors, code=422)

        pendaftaran = create(data, user_id)

        return success_response(
            message="Pendaftaran berhasil dibuat",
            data=schema.dump(pendaftaran),
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e), code=500)
