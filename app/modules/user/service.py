from datetime import datetime
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.auth.user import User
from app.models.auth.role import Role


def get_all_users(
    role=None,
    search=None,
    status="active",
    page=1,
    per_page=10
):
    allowed_status = ["active", "inactive", "all"]

    if status not in allowed_status:
        raise ValueError("Status tidak valid")

    query = User.query.join(User.role)

    if status == "active":
        query = query.filter(User.is_active == True)

    elif status == "inactive":
        query = query.filter(User.is_active == False)

    if role:
        query = query.filter(Role.name == role)

    if search:
        query = query.filter(
            db.or_(
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
            )
        )

    return (
        query
        .order_by(User.created_at.desc())
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    )


def get_user_by_id(id):
    user = db.session.get(User, id)

    if not user:
        raise ValueError("User tidak ditemukan")

    return user


def create_user(data):
    exists = User.query.filter_by(
        email=data["email"]
    ).first()

    if exists:
        raise ValueError("Email sudah digunakan")

    role = db.session.get(Role, data["role_id"])

    if not role:
        raise ValueError("Role tidak ditemukan")

    user = User(
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role_id=data["role_id"],
        is_verified=data.get("is_verified", True),
    )

    db.session.add(user)
    db.session.commit()

    return user


def update_user(id, data):
    user = get_user_by_id(id)

    if "first_name" in data:
        user.first_name = data["first_name"]

    if "last_name" in data:
        user.last_name = data["last_name"]

    if "email" in data:
        exists = User.query.filter(
            User.id != id,
            User.email == data["email"]
        ).first()

        if exists:
            raise ValueError("Email sudah digunakan")

        user.email = data["email"]

    if "role_id" in data:
        if user.role and user.role.name == "orang_tua":
            raise ValueError("Role orang tua tidak dapat diubah")

        role = db.session.get(Role, data["role_id"])

        if not role:
            raise ValueError("Role tidak ditemukan")

        user.role_id = data["role_id"]

    if "is_verified" in data:
        user.is_verified = data["is_verified"]

    if "password" in data:
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    return user


def delete_user(id):
    user = get_user_by_id(id)

    user.is_active = False
    user.deleted_at = datetime.utcnow()

    db.session.commit()

    return True

def restore_user(id):
    user = get_user_by_id(id)

    user.is_active = True
    user.deleted_at = None

    db.session.commit()

    return user