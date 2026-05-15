import os
from flask import Blueprint, request
from app.models.observasi.gpph import GPPHPertanyaan
from ..pendaftaran.schema import PendaftaranSchema
from .schema import CreateGPPHPertanyaanSchema, UpdateGPPHPertanyaanSchema, CreateKPSPPertanyaanSchema, UpdateKPSPPertanyaanSchema, CreateGPPHSchema, CreateKPSPSchema
from .service import (
set_jadwal_observasi, 
update_status_observasi, 
get_all_gpph_pertanyaan, 
get_detail_gpph_pertanyaan, 
create_gpph_pertanyaan, 
update_gpph_pertanyaan, 
delete_gpph_pertanyaan, 
create_gpph, get_gpph_result, 
get_kpsp_pertanyaan_by_pendaftaran, 
create_kpsp, get_kpsp_result, 
get_all_kpsp_pertanyaan_service, 
get_detail_kpsp_pertanyaan, 
create_kpsp_pertanyaan, 
update_kpsp_pertanyaan, 
delete_kpsp_pertanyaan
)

from app.utils.decorators import role_required
from app.utils.responses import success_response, error_response

bp_observasi = Blueprint('observasi', __name__)

# set jadwal observasi
@bp_observasi.route('/set-jadwal', methods=['PUT'])
@role_required('admin')
def set_observasi():
    try:
        data = request.get_json()

        ids = data.get("pendaftaran_ids", [])
        observasi_at = data.get("observasi_at")

        if not ids:
            return error_response("Pendaftaran wajib dipilih", 400)
        
        if not observasi_at:
            return error_response("Jadwal observasi wajib diisi", 400)

        set_jadwal_observasi(ids, observasi_at)

        return success_response(
            message="Jadwal observasi berhasil diset"
        )

    except Exception as e:
        return error_response(str(e), 500)
    
# update status observasi
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


""" GPPH """
# get all master pertanyaan gpph
@bp_observasi.route('/gpph/pertanyaan', methods=['GET'])
@role_required('admin', 'guru')
def get_all_gpph_pertanyaan_route():
    try:
        result = get_all_gpph_pertanyaan()

        return success_response(
            message='Berhasil mengambil master pertanyaan GPPH',
            data=result
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )

# detail master pertanyaan gpph
@bp_observasi.route('/gpph/pertanyaan/<int:id>', methods=['GET'])
@role_required('admin', 'guru')
def detail_gpph_pertanyaan_route(id):
    try:
        result = get_detail_gpph_pertanyaan(id)

        return success_response(
            message='Berhasil mengambil detail pertanyaan GPPH',
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

# create master pertanyaan gpph
@bp_observasi.route('/gpph/pertanyaan', methods=['POST'])
@role_required('admin')
def store_gpph_pertanyaan():
    try:
        schema = CreateGPPHPertanyaanSchema()
        data = schema.load(request.json)
        pertanyaan = create_gpph_pertanyaan(data)

        return success_response(
            message='Pertanyaan GPPH berhasil dibuat',
            data={
                'id': pertanyaan.id
            },
            code=201
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            code=422
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )

# update master pertanyaan gpph
@bp_observasi.route('/gpph/pertanyaan/<int:id>', methods=['PUT'])
@role_required('admin')
def update_gpph_pertanyaan_route(id):
    try:
        schema = UpdateGPPHPertanyaanSchema()
        data = schema.load(request.json)
        pertanyaan = update_gpph_pertanyaan(id, data)

        return success_response(
            message='Pertanyaan GPPH berhasil diupdate',
            data={
                'id': pertanyaan.id
            }
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            code=422
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )

# delete master pertanyaan gpph
@bp_observasi.route('/gpph/pertanyaan/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_gpph_pertanyaan_route(id):
    try:
        delete_gpph_pertanyaan(id)

        return success_response(
            message='Pertanyaan GPPH berhasil dihapus'
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

# create jawaban gpph
@bp_observasi.route('/<int:pendaftaran_id>/gpph', methods=['POST'])
@role_required('admin', 'guru')
def store_gpph(pendaftaran_id):
    try:
        schema = CreateGPPHSchema()

        data = schema.load(request.json)

        create_gpph(pendaftaran_id,data)

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

# detail hasil gpph
@bp_observasi.route('/<int:pendaftaran_id>/gpph', methods=['GET'])
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



""" KPSP """
# get all master pertanyaan kpsp
@bp_observasi.route('/kpsp/pertanyaan', methods=['GET'])
@role_required('admin', 'guru')
def get_all_kpsp_pertanyaan():
    try:
        result = get_all_kpsp_pertanyaan_service()

        return success_response(
            message='Berhasil mengambil master pertanyaan KPSP',
            data=result
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )

# detail master pertanyaan kpsp
@bp_observasi.route('/kpsp/pertanyaan/<int:id>', methods=['GET'])
@role_required('admin', 'guru')
def detail_kpsp_pertanyaan(id):
    try:
        result = get_detail_kpsp_pertanyaan(id)

        return success_response(
            message='Berhasil mengambil detail pertanyaan KPSP',
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

# create master pertanyaan kpsp
@bp_observasi.route('/kpsp/pertanyaan', methods=['POST'])
@role_required('admin')
def store_kpsp_pertanyaan():
    try:
        schema = CreateKPSPPertanyaanSchema()
        data = schema.load(request.json)
        pertanyaan = create_kpsp_pertanyaan(data)

        return success_response(
            message='Pertanyaan KPSP berhasil dibuat',
            data={
                'id': pertanyaan.id
            },
            code=201
        )

    except Exception as e:
        return error_response(
            message='Terjadi kesalahan',
            errors=str(e),
            code=500
        )

# update master pertanyaan kpsp
@bp_observasi.route('/kpsp/pertanyaan/<int:id>', methods=['PUT'])
@role_required('admin')
def update_kpsp_pertanyaan_route(id):
    try:
        schema = UpdateKPSPPertanyaanSchema()
        data = schema.load(request.json)
        pertanyaan = update_kpsp_pertanyaan(id, data)

        return success_response(
            message='Pertanyaan KPSP berhasil diupdate',
            data={
                'id': pertanyaan.id
            }
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

# delete master pertanyaan kpsp
@bp_observasi.route('/kpsp/pertanyaan/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_kpsp_pertanyaan_route(id):
    try:
        delete_kpsp_pertanyaan(id)

        return success_response(
            message='Pertanyaan KPSP berhasil dihapus'
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


# get pertanyaan kpsp berdasarkan usia
@bp_observasi.route('/<int:pendaftaran_id>/kpsp/soal', methods=['GET'])
@role_required('admin')
def get_kpsp_pertanyaan(pendaftaran_id):
    try:
        result = get_kpsp_pertanyaan_by_pendaftaran(pendaftaran_id)

        return success_response(
            message='Berhasil mengambil pertanyaan KPSP',
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
    
# create jawaban kpsp
@bp_observasi.route('/<int:pendaftaran_id>/kpsp', methods=['POST'])
@role_required('admin', 'guru')
def store_kpsp(pendaftaran_id):
    try:
        schema = CreateKPSPSchema()
        data = schema.load(request.json)

        create_kpsp(pendaftaran_id, data)

        return success_response(
            message='Observasi KPSP berhasil disimpan',
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
    
# detail hasil kpsp
@bp_observasi.route('/<int:pendaftaran_id>/kpsp',methods=['GET'])
@role_required('admin')
def detail_kpsp(pendaftaran_id):
    try:
        result = get_kpsp_result(
            pendaftaran_id
        )
        return success_response(
            message='Berhasil mengambil hasil KPSP',
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