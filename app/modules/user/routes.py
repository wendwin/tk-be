from flask import Blueprint, request

from app.utils.pagination import format_pagination
from app.utils.responses import success_response, error_response
from app.utils.decorators import role_required

from app.modules.user.schema import (
    UserSchema,
    CreateUserSchema,
    UpdateUserSchema,
)

from app.modules.user.service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    restore_user
)


bp_user = Blueprint("user", __name__)


@bp_user.route("", methods=["GET"])
@role_required("admin", "kepsek")
def index():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        status = request.args.get("status", "active")
        role = request.args.get("role")
        search = request.args.get("search")

        pagination = get_all_users(
            role=role,
            search=search,
            status=status,
            page=page,
            per_page=per_page
        )

        schema = UserSchema(many=True)
        data = schema.dump(pagination.items)

        return success_response(
            message="Berhasil mengambil data user",
            data=data,
            meta=format_pagination(pagination)
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_user.route("/<int:id>", methods=["GET"])
@role_required("admin")
def show(id):
    try:
        user = get_user_by_id(id)

        return success_response(
            message="Berhasil mengambil detail user",
            data=UserSchema().dump(user)
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)


@bp_user.route("", methods=["POST"])
@role_required("admin")
def store():
    try:
        schema = CreateUserSchema()
        data = schema.load(request.json)

        user = create_user(data)

        return success_response(
            message="User berhasil dibuat",
            data=UserSchema().dump(user),
            code=201
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_user.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update(id):
    try:
        schema = UpdateUserSchema()
        data = schema.load(request.json)

        user = update_user(id, data)

        return success_response(
            message="User berhasil diupdate",
            data=UserSchema().dump(user)
        )

    except ValueError as e:
        return error_response(str(e), 422)

    except Exception as e:
        return error_response(str(e), 500)


@bp_user.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def destroy(id):
    try:
        delete_user(id)

        return success_response(
            message="User berhasil dinonaktifkan"
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)
    

@bp_user.route("/<int:id>/restore", methods=["PATCH"])
@role_required("admin")
def restore(id):
    try:
        user = restore_user(id)

        return success_response(
            message="User berhasil diaktifkan kembali",
            data=UserSchema().dump(user)
        )

    except ValueError as e:
        return error_response(str(e), 404)

    except Exception as e:
        return error_response(str(e), 500)