# Monitoring Perkembangan Anak - Backend

Backend API untuk Sistem Monitoring Perkembangan Anak berbasis web yang dikembangkan menggunakan **Flask**. Aplikasi ini menyediakan REST API untuk autentikasi, pengelolaan data pengguna, siswa, observasi, jurnal perkembangan, dan fitur pendukung lainnya.

## Tech Stack

- Python 3.12+
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask JWT Extended
- Flask Mail
- Flask Limiter
- MySQL
- Alembic

---

## Requirements

Pastikan telah menginstal:

- Python 3.12 atau lebih baru
- pip

---

## Installation

### 1. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Linux / macOS:

```bash
python3 -m venv venv
```

---

### 2. Activate Virtual Environment

Windows (CMD):

```cmd
venv\Scripts\activate
```

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Copy file `.env.example` menjadi `.env`.

Linux / macOS:

```bash
cp .env.example .env
```

Windows CMD:

```cmd
copy .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Kemudian isi konfigurasi pada file `.env`

---

## Database Configuration

Buat database MySQL terlebih dahulu.

Contoh:

```sql
CREATE DATABASE monitoring_db;
```

Sesuaikan konfigurasi database pada file `.env`.

---

## Database Migration

Jalankan migration untuk membuat tabel database:

```bash
flask db upgrade
```

Jika terdapat perubahan pada model dan ingin membuat migration baru:

```bash
flask db migrate -m "migration message"
flask db upgrade
```

---

## Database Commands

### Seed Database

Mengisi database dengan data awal:

```bash
flask db:seed
```

> Pastikan email dan password default telah diisi pada file `.env`.

### Fresh Database

Menghapus seluruh tabel, menjalankan ulang migration, kemudian mengisi kembali data awal:

```bash
flask db:fresh
```

> **Warning:** Perintah ini akan menghapus seluruh data database. Gunakan hanya pada lingkungan development.

---

## Run Development Server

Jalankan aplikasi:

```bash
python run.py
```

atau:

```bash
flask run
```

Backend akan berjalan pada:

```
http://localhost:5000
```

---

## Main Features

- JWT Authentication
- Role Based Access Control (RBAC)
- Student Management
- Teacher Management
- Parent Management
- School Year Management
- Observation Management
- Weekly Monitoring Journal
- File Upload
- Email Service
- Rate Limiting
- RESTful API

---

## User Roles

- Admin
- Kepala Sekolah
- Guru
- Orang Tua

## API Base URL

```
http://localhost:5000/api
```

---

## Environment Variables

Seluruh environment variable yang dibutuhkan dapat dilihat pada file:

```
.env.example
```

---

## License

This project is developed for educational purposes.
