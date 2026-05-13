import os
from flask import Blueprint, request
from app.models.observasi.gpph import GPPHPertanyaan
from ..pendaftaran.schema import PendaftaranSchema
from .schema import CreateGPPHSchema
from .service import set_jadwal_observasi, update_status_observasi,create_gpph, get_gpph_result

from flask import Blueprint, jsonify, request
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
@role_required('admin', 'guru')
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
    

# get pertanyaan
@bp_observasi.route('/gpph/pertanyaan', methods=['GET'])
@role_required('admin', 'guru')
def get_pertanyaan():

    pertanyaan = (
        GPPHPertanyaan.query
        .order_by(GPPHPertanyaan.nomor.asc())
        .all()
    )

    result = []

    for item in pertanyaan:
        result.append({
            'id': item.id,
            'nomor': item.nomor,
            'pertanyaan': item.pertanyaan
        })

    return success_response(
        message='Berhasil mengambil pertanyaan GPPH',
        data=result
    )


# create/update jawaban
@bp_observasi.route('/gpph', methods=['POST'])
@role_required('admin', 'guru')
def store_gpph():
    try:
        schema = CreateGPPHSchema()

        data = schema.load(request.json)

        create_gpph(data)

        return success_response(
            message='Observasi GPPH berhasil disimpan',
            code=201
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            code=404
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )


# detail hasil
@bp_observasi.route('/gpph/<int:pendaftaran_id>', methods=['GET'])
@role_required('admin', 'guru')
def detail_gpph(pendaftaran_id):
    try:
        result = get_gpph_result(pendaftaran_id)

        return success_response(
            message='Berhasil mengambil hasil GPPH',
            data=result
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            code=404
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )