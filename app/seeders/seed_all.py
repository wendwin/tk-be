from app.seeders.asesmen_pertanyaan_seeder import seed_asesmen_pertanyaan
from app.seeders.gpph_pertanyaan_seeder import seed_gpph_pertanyaan
from app.seeders.role_seeder import seed_roles
from app.seeders.siswa_kelas_seeder import seed_siswa_kelas
from app.seeders.guru_kelas_seeder import seed_guru_kelas
from app.seeders.user_seeder import seed_users
from app.seeders.tahun_ajaran_seeder import seed_tahun_ajaran
from app.seeders.gelombang_seeder import seed_gelombang
from app.seeders.kpsp_pertanyaan_seeder import seed_kpsp_pertanyaan
from app.seeders.kelas_seeder import seed_kelas
from app.seeders.pendaftaran_seeder import seed_pendaftaran
from app.seeders.mon_mingguan_seeder import seed_monitoring_mingguan
from app.seeders.mon_siswa_seeder import seed_monitoring_siswa

def seed_all():
    seed_roles()
    seed_tahun_ajaran()
    seed_users() 
    seed_asesmen_pertanyaan()
    seed_gelombang()
    seed_gpph_pertanyaan()
    seed_kpsp_pertanyaan()
    seed_kelas()
    seed_pendaftaran()
    seed_siswa_kelas()
    seed_guru_kelas()
    seed_monitoring_mingguan()
    seed_monitoring_siswa()