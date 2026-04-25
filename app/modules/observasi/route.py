import os
from flask import Blueprint, request
from ..pendaftaran.schema import PendaftaranSchema
from .service import set_jadwal_observasi, update_status_observasi
from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response

bp_observasi = Blueprint('observasi', __name__)

@bp_observasi.route('/<int:id>', methods=['PUT'])
@role_required('admin')
def set_observasi(id):
    
    try:
        data = request.get_json()

        pendaftaran = set_jadwal_observasi(id, data)

        if not pendaftaran:
            return error_response("Data tidak ditemukan", 404)

        schema = PendaftaranSchema()
        return success_response(
            message="Jadwal observasi berhasil diset",
            data=schema.dump(pendaftaran)
        )

    except Exception as e:
        return error_response(str(e), 500)
    
@bp_observasi.route('/<int:id>/status', methods=['PUT'])
@role_required('admin')
def update_status(id):
    try:
        data = request.get_json()

        pendaftaran = update_status_observasi(id, data.get("status_observasi"))

        if not pendaftaran:
            return error_response("Data tidak ditemukan", 404)

        return success_response(
            message="Status observasi berhasil diupdate"
        )

    except Exception as e:
        return error_response(str(e), 500)