from app.extensions import db
from app.models.auth.role import Role

def seed_roles():
    roles = ['admin', 'guru', 'orangtua', 'kepsek']

    for r in roles:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r))

    db.session.commit()
    print("Seeder roles berhasil")