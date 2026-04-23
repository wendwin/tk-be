from app.seeders.asesmen_pertanyaan_seeder import seed_asesmen_pertanyaan
from app.seeders.role_seeder import seed_roles
from app.seeders.user_seeder import seed_users
from app.seeders.tahun_ajaran_seeder import seed_tahun_ajaran

def seed_all():
    seed_roles()
    seed_tahun_ajaran()
    seed_users() 
    seed_asesmen_pertanyaan()