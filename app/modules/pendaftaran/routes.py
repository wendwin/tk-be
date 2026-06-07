import os
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.extensions import db
from flask import Blueprint, request, redirect, send_from_directory, json, current_app, send_file

from app.models.pendaftaran.tahun_ajaran import TahunAjaran
from .schema import PendaftaranSchema, PendaftaranListSchema, TahunAjaranSchema
from .service import get_all, create, get_by_id, get_by_user_id, upload_berkas_service, update_status_berkas_service, update_status_pembayaran_service , update_status_pendaftaran_service,upload_pembayaran_service, update_pendaftaran_service
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response
from app.utils.pagination import format_pagination
from app.utils.formulir import generate_formulir_pendaftaran
from app.utils.surat_pernyataan import generate_surat_pernyataan

import traceback

bp_pendaftaran = Blueprint('pendaftaran', __name__)

# get all
@bp_pendaftaran.route('', methods=['GET'])
@role_required('admin', 'orang_tua', 'guru')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    jenis = request.args.get("jenis")
    program = request.args.get("program")
    tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)
    search = request.args.get('search')
    status = request.args.get('status')
    status_pembayaran = request.args.get('status_pembayaran')

    pagination = get_all(page, per_page,search, status, status_pembayaran, jenis, program, tahun_ajaran_id)

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
        # data = json.loads(request.form.get("data"))
        data = request.get_json()
        # files = request.files
        user_id = get_jwt_identity()

        schema = PendaftaranSchema()
        errors = schema.validate(data)
        if errors:
            return error_response("Validation error", errors=errors, code=422)

        pendaftaran = create(data, user_id)

        return success_response(
            message="Data pendaftaran berhasil disimpan",
            data=schema.dump(pendaftaran),
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e), code=500)
    
# get by id
@bp_pendaftaran.route('/<int:id>', methods=['GET'])
@role_required('admin', 'orang_tua', 'guru')
def show(id):
    user_id = get_jwt_identity()
    role = get_jwt().get("role")

    pendaftaran = get_by_id(
        id=id,
        user_id=user_id if role == "orang_tua" else None
    )

    if not pendaftaran:
        return error_response("Data tidak ditemukan", code=404)

    schema = PendaftaranSchema()
    return success_response(
        data=schema.dump(pendaftaran),
        message="Data pendaftaran berhasil diambil",
        code=200
    )

# update 
@bp_pendaftaran.route('/<int:id>', methods=['PUT'])
@role_required('admin', 'orang_tua')
def update(id):
    try:
        data = request.get_json()

        if not data:
            return error_response("Data tidak boleh kosong", code=400)

        pendaftaran = get_by_id(id)
        if not pendaftaran:
            return error_response("Data tidak ditemukan", code=404)

        schema = PendaftaranSchema()
        errors = schema.validate(data, partial=True)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        updated = update_pendaftaran_service(pendaftaran, data)

        return success_response(
            message="Data pendaftaran berhasil diupdate",
            data=schema.dump(updated),
            code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(message=str(e), code=500)
    
# upload berkas
@bp_pendaftaran.route('/<int:id>/upload-berkas', methods=['POST'])
@role_required('orang_tua')
def upload_berkas(id):
    try:
        user_id = get_jwt_identity()
        files = request.files

        if not files:
            return error_response("File wajib diupload", code=400)

        result = upload_berkas_service(id, user_id, files)

        return success_response(
            message="Berkas berhasil diupload",
            data=result
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)

# update status pendaftaran
@bp_pendaftaran.route('/<int:id>/status', methods=['PATCH'])
@role_required('admin')
def update_status_pendaftaran(id):
    try:
        data = request.get_json()
        status = data.get("status")

        result = update_status_pendaftaran_service(id, status)

        return success_response(
            message="Status pendaftaran berhasil diupdate",
            data=result
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)
    
# update status berkas
@bp_pendaftaran.route('/<int:id>/status-berkas', methods=['PATCH'])
@role_required('admin')
def update_status_berkas(id):
    try:
        data = request.get_json()
        status = data.get("status_berkas")

        result = update_status_berkas_service(id, status)

        return success_response(
            message="Status berkas berhasil diupdate",
            data=result
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)

# upload bukti pembayaran
@bp_pendaftaran.route('/<int:id>/upload-pembayaran', methods=['POST'])
@role_required('orang_tua')
def upload_bukti(id):
    try:
        user_id = get_jwt_identity()

        file = request.files.get('bukti_tf')

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

# verifikasi pembayaran
@bp_pendaftaran.route('/<int:id>/status-pembayaran', methods=['PATCH'])
@role_required('admin')
def update_status_pembayaran(id):
    try:
        data = request.get_json()
        status = data.get("status_pembayaran")

        result = update_status_pembayaran_service(id, status)

        return success_response(
            message="Status pembayaran berhasil diupdate",
            data=result
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)
    
# akses file
@bp_pendaftaran.route('/uploads/<path:filename>', methods=['GET'])
@jwt_required()
@role_required('admin')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'uploads'), filename)

# download formulir
@bp_pendaftaran.route('/<int:id>/download', methods=['GET'])
@role_required('admin')
def download_formulir(id):
    try:
        file_path = generate_formulir_pendaftaran(id)

        return send_file(
            file_path,
            as_attachment=False,
            download_name="formulir_pendaftaran.pdf"
        )

    except Exception as e:
        return error_response(str(e), code=500)
    
# download surat pernyataan
@bp_pendaftaran.route('/download-surat-pernyataan', methods=['GET'])
@role_required('orang_tua')
def download_surat_pernyataan():
    try:
        user_id = get_jwt_identity()

        file_path = generate_surat_pernyataan(user_id)

        return send_file(
            file_path,
            as_attachment=True,
            download_name='surat_pernyataan.pdf'
        )

    except Exception as e:
        return error_response(str(e), code=500)
    
# me
@bp_pendaftaran.route('/me', methods=['GET'])
@role_required('admin', 'orang_tua')
def get_me():
    user_id = get_jwt_identity()

    pendaftaran = get_by_user_id(user_id)

    if not pendaftaran:
        return success_response(
            data=[],
            message="Belum ada pendaftaran",
            code=200
        )

    schema = PendaftaranSchema(many=True)

    return success_response(
        data=schema.dump(pendaftaran),
        message="Data pendaftaran berhasil diambil",
        code=200
    )