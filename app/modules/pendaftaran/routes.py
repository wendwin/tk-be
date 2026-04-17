import os
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from flask import Blueprint, request, redirect, send_from_directory, json
from .schema import PendaftaranSchema, PendaftaranListSchema
from .service import get_all, create, get_by_id, upload_pembayaran_service
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination

bp_pendaftaran = Blueprint('pendaftaran', __name__)

# get all
@bp_pendaftaran.route('', methods=['GET'])
@role_required('admin', 'orang_tua',)
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search')

    pagination = get_all(page, per_page, search)

    schema = PendaftaranListSchema(many=True)
    data = schema.dump(pagination.items)

    return success_response(
        data=data,
        code=200,
        message="Daftar pendaftaran berhasil diambil",
        meta=format_pagination(pagination)
    )

# create
@bp_pendaftaran.route('', methods=['POST'])
@role_required('admin', 'orang_tua')
def store():
    try:
        data = json.loads(request.form.get("data"))
        files = request.files
        user_id = get_jwt_identity()

        schema = PendaftaranSchema()
        errors = schema.validate(data)
        if errors:
            return error_response("Validation error", errors=errors, code=422)

        pendaftaran = create(data, user_id, files)

        return success_response(
            message="Pendaftaran berhasil dibuat",
            data=schema.dump(pendaftaran),
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e), code=500)
    
# get by id
@bp_pendaftaran.route('/<int:id>', methods=['GET'])
@role_required('admin', 'orang_tua')
def show(id):
    pendaftaran = get_by_id(id)

    if not pendaftaran:
        return error_response("Data tidak ditemukan", code=404)

    schema = PendaftaranSchema()
    return success_response(data=schema.dump(pendaftaran), message="Data pendaftaran berhasil diambil", code=200)

# upload bukti pembayaran
@bp_pendaftaran.route('/<int:id>/upload-pembayaran', methods=['POST'])
@role_required('orang_tua')
def upload_bukti(id):
    try:
        user_id = get_jwt_identity()

        file = request.files.get('file')

        if not file:
            return error_response("File wajib diupload", code=400)

        result = upload_pembayaran_service(id, user_id, file)

        return success_response(
            message="Bukti pembayaran berhasil diupload",
            data=result
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)
    
@bp_pendaftaran.route('/uploads/<path:filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)