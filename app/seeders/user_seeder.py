import os
from app.extensions import db
from app.models.auth.user import User
from app.models.auth.role import Role
from werkzeug.security import generate_password_hash

def seed_users():
    admin_role = Role.query.filter_by(name="admin").first()

    if not admin_role:
        print("Role admin tidak ditemukan!")
        return
    
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    existing = User.query.filter_by(email=email).first()
    if existing:
        print("User admin sudah ada")
        return

    user = User(
        email=email,
        password=generate_password_hash(password),
        role_id=admin_role.id,
        is_verified=True
    )

    db.session.add(user)
    db.session.commit()
    print("Seeder user berhasil")