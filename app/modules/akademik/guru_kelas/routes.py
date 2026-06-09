from flask import Blueprint, request

from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity

from app.modules.akademik.guru_kelas.schema import (
    GuruKelasSchema,
    CreateGuruKelasSchema,
    UpdateGuruKelasSchema,
)

from app.modules.akademik.guru_kelas.service import (
    get_all_guru_kelas,
    get_guru_kelas_by_id,
    create_guru_kelas,
    update_guru_kelas,
    delete_guru_kelas,
    get_my_guru_kelas,
)


bp_guru_kelas = Blueprint("guru_kelas", __name__)


@bp_guru_kelas.route("", methods=["GET"])
@role_required("admin", "guru", "kepsek")
def index():
    try:
        guru_kelas = get_all_guru_kelas()

        schema = GuruKelasSchema(many=True)
        data = schema.dump(guru_kelas)

        return success_response(
            message="Berhasil mengambil data guru kelas",
            data=data,
        )

    except Exception as e:
        return error_response(str(e), 500)


@bp_guru_kelas.route("/<int:id>", methods=["GET"])
@role_required("admin", "guru")
def show(id):
    try:
        guru_kelas = get_guru_kelas_by_id(id)

        schema = GuruKelasSchema()
        data = schema.dump(guru_kelas)

        return success_response(
            message="Berhasil mengambil detail guru kelas",
            data=data,
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_guru_kelas.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = CreateGuruKelasSchema()
        data = schema.load(request.json)

        guru_kelas = create_guru_kelas(data)

        result = GuruKelasSchema().dump(guru_kelas)

        return success_response(
            message="Guru berhasil ditambahkan ke kelas",
            data=result,
            code=201,
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_guru_kelas.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateGuruKelasSchema()
        data = schema.load(request.json)

        guru_kelas = update_guru_kelas(id, data)

        result = GuruKelasSchema().dump(guru_kelas)

        return success_response(
            message="Data guru kelas berhasil diupdate",
            data=result,
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_guru_kelas.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_guru_kelas(id)

        return success_response(
            message="Guru berhasil dihapus dari kelas",
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)
    

@bp_guru_kelas.route("/me", methods=["GET"])
@role_required("guru")
def me():
    try:
        user_id = get_jwt_identity()

        guru_kelas = get_my_guru_kelas(user_id)

        schema = GuruKelasSchema(many=True)
        data = schema.dump(guru_kelas)

        return success_response(
            message="Berhasil mengambil data kelas guru",
            data=data,
        )

    except Exception as e:
        return error_response(str(e), 500)