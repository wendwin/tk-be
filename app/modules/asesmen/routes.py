from flask import Blueprint, request
from marshmallow import ValidationError
from app.utils.responses import success_response, error_response
from app.modules.asesmen.services import *
from app.modules.asesmen.schema import *
from app.utils.decorators import role_required
from app.extensions import db

bp_asesmen = Blueprint('asesmen', __name__)


@bp_asesmen.route('/pertanyaan', methods=['GET'])
@role_required('admin', 'orang_tua', 'guru')
def index_pertanyaan():
    active_only = request.args.get("active_only", "false") == "true"

    data = get_all_pertanyaan_service(active_only=active_only)
    schema = AsesmenPertanyaanSchema(many=True)

    return success_response(
        data=schema.dump(data),
        message="Data pertanyaan berhasil diambil"
    )


@bp_asesmen.route('/pertanyaan/<int:id>', methods=['GET'])
@role_required('admin', 'orang_tua', 'guru')
def show_pertanyaan(id):
    data = get_pertanyaan_by_id_service(id)

    if not data:
        return error_response("Data tidak ditemukan", code=404)

    schema = AsesmenPertanyaanSchema()

    return success_response(
        data=schema.dump(data),
        message="Detail pertanyaan berhasil diambil"
    )


@bp_asesmen.route('/pertanyaan', methods=['POST'])
@role_required('admin')
def store_pertanyaan():
    try:
        data = request.get_json()

        schema = AsesmenPertanyaanSchema()
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        result = create_pertanyaan_service(data)

        return success_response(
            message="Pertanyaan berhasil dibuat",
            data=schema.dump(result),
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_asesmen.route('/pertanyaan/bulk', methods=['POST'])
@role_required('admin')
def bulk_store_pertanyaan():
    try:
        data = request.get_json()

        schema = AsesmenPertanyaanSchema(many=True)

        try:
            data = schema.load(data)
        except ValidationError as err:
            return error_response(
                "Validation error",
                errors=err.messages,
                code=422
            )

        result = bulk_create_pertanyaan_service(data)

        return success_response(
            message="Bulk pertanyaan berhasil dibuat",
            data=schema.dump(result),
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_asesmen.route('/pertanyaan/<int:id>', methods=['PUT'])
@role_required('admin')
def update_pertanyaan(id):
    try:
        data = request.get_json()

        schema = AsesmenPertanyaanSchema(partial=True)
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        result = update_pertanyaan_service(id, data)

        if not result:
            return error_response("Data tidak ditemukan", code=404)

        return success_response(
            message="Pertanyaan berhasil diupdate",
            data=schema.dump(result)
        )

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_asesmen.route('/pertanyaan/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_pertanyaan(id):
    success = delete_pertanyaan_service(id)

    if not success:
        return error_response("Data tidak ditemukan", code=404)

    return success_response(
        message="Pertanyaan berhasil dinonaktifkan"
    )


@bp_asesmen.route('/pertanyaan/<int:id>/restore', methods=['PUT'])
@role_required('admin')
def restore_pertanyaan(id):
    success = restore_pertanyaan_service(id)

    if not success:
        return error_response("Data tidak ditemukan", code=404)

    return success_response(
        message="Pertanyaan berhasil diaktifkan"
    )


@bp_asesmen.route('/jawaban/<int:id_pendaftaran>', methods=['GET'])
@role_required('admin', 'orang_tua', 'guru')
def get_jawaban(id_pendaftaran):
    data = get_jawaban_by_pendaftaran(id_pendaftaran)

    result = []

    for item in data:
        result.append({
            "id": item.id,
            "id_pertanyaan": item.id_pertanyaan,
            "pertanyaan": item.snapshot_pertanyaan,
            "jawaban": item.jawaban
        })

    return success_response(
        data=result,
        message="Jawaban asesmen berhasil diambil"
    )


@bp_asesmen.route('/jawaban', methods=['POST'])
@role_required('admin', 'orang_tua', 'guru')
def store_jawaban():
    try:
        data = request.get_json()

        schema = AsesmenSubmitSchema()
        errors = schema.validate(data)

        if errors:
            return error_response("Validation error", errors=errors, code=422)

        create_jawaban_service(data)

        return success_response(
            message="Jawaban asesmen berhasil disimpan",
            code=201
        )

    except ValueError as e:
        db.session.rollback()
        return error_response(str(e), code=404)

    except Exception as e:
        db.session.rollback()
        return error_response(str(e), code=500)


@bp_asesmen.route('/jawaban/<int:id_pendaftaran>', methods=['DELETE'])
@role_required('admin')
def delete_jawaban(id_pendaftaran):
    delete_jawaban_service(id_pendaftaran)

    return success_response(
        message="Jawaban berhasil dihapus"
    )