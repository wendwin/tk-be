import os
from app.extensions import db
from app.models.auth.user import User
from app.models.auth.role import Role
from werkzeug.security import generate_password_hash

def seed_users():
    import os

    users = [
        {
            "first_name": "Super",
            "last_name": "Admin",
            "email": os.getenv("ADMIN_EMAIL"),
            "password": os.getenv("ADMIN_PASSWORD"),
            "role": "admin",
        },

        {
            "first_name": "Amelia",
            "last_name": "Sari, S.Pd.",
            "email": os.getenv("GURU1_EMAIL"),
            "password": os.getenv("GURU1_PASSWORD"),
            "role": "guru",
        },

        {
            "first_name": "Siti",
            "last_name": "Aminah, S.Pd.",
            "email": os.getenv("GURU2_EMAIL"),
            "password": os.getenv("GURU2_PASSWORD"),
            "role": "guru",
        },

        {
            "first_name": "Putri",
            "last_name": "Lestari, S.Pd.",
            "email": os.getenv("GURU3_EMAIL"),
            "password": os.getenv("GURU3_PASSWORD"),
            "role": "guru",
        },
        {
            "first_name": "Dewi",
            "last_name": "Kartika, S.Pd.",
            "email": os.getenv("GURU4_EMAIL"),
            "password": os.getenv("GURU4_PASSWORD"),
            "role": "guru",
        },      

        {
            "first_name": "Rina",
            "last_name": "Maharani, S.Pd.",
            "email": os.getenv("GURU5_EMAIL"),
            "password": os.getenv("GURU5_PASSWORD"),
            "role": "guru",
        },      

        {
            "first_name": "Yuni",
            "last_name": "Safitri, S.Pd.",
            "email": os.getenv("GURU6_EMAIL"),
            "password": os.getenv("GURU6_PASSWORD"),
            "role": "guru",
        },      

        {
            "first_name": "Fitri",
            "last_name": "Anggraini, S.Pd.",
            "email": os.getenv("GURU7_EMAIL"),
            "password": os.getenv("GURU7_PASSWORD"),
            "role": "guru",
        },      

        {
            "first_name": "Nanda",
            "last_name": "Pratiwi, S.Pd.",
            "email": os.getenv("GURU8_EMAIL"),
            "password": os.getenv("GURU8_PASSWORD"),
            "role": "guru",
        },
        {
            "first_name": "Suci",
            "last_name": "Eka Handayani, S.Pd., M.Pd.",
            "email": os.getenv("KEPSEK_EMAIL"),
            "password": os.getenv("KEPSEK_PASSWORD"),
            "role": "kepsek",
        },
    ]
    for item in users:
        role = Role.query.filter_by(
            name=item["role"]
        ).first()

        if not role:
            print(f"Role {item['role']} tidak ditemukan!")
            continue

        existing = User.query.filter_by(
            email=item["email"]
        ).first()

        if existing:
            print(f"User {item['email']} sudah ada")
            continue

        user = User(
            first_name=item["first_name"],
            last_name=item["last_name"],
            email=item["email"],
            password=generate_password_hash(item["password"]),
            role_id=role.id,
            is_verified=True,
            is_active=True,
        )

        db.session.add(user)

    db.session.commit()

    print("Seeder user berhasil")