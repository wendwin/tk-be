from app.seeders.role_seeder import seed_roles
from app.seeders.user_seeder import seed_users
from app.seeders.tahun_ajaran_seeder import seed_tahun_ajaran

def seed_all():
    seed_roles()
    seed_tahun_ajaran()
    seed_users() 