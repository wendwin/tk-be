import os
import uuid
from app.extensions import db
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.pendaftaran.dokumen import Dokumen

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
UPLOAD_FOLDER = 'uploads/pembayaran'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

MONITORING_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MONITORING_MAX_FILE_SIZE = 5 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file):
    if not allowed_file(file.filename):
        raise Exception("Format file tidak diizinkan (png, jpg, jpeg)")

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file_length = file.tell()
    file.seek(0)

    if file_length > MAX_FILE_SIZE:
        raise Exception("Ukuran file maksimal 2MB")
    
    if size == 0:
        raise Exception("File kosong")


def generate_filename(original_filename):
    ext = original_filename.rsplit(".", 1)[1].lower()
    return f"{uuid.uuid4().hex}.{ext}"


def save_file(file, subfolder):
    base_folder = os.path.join(os.getcwd(), "uploads", subfolder)
    os.makedirs(base_folder, exist_ok=True)

    filename = generate_filename(file.filename)

    filepath = os.path.join(base_folder, filename)
    file.save(filepath)

    return f"/uploads/{subfolder}/{filename}"

def delete_file_if_exists(file_path):
    if not file_path:
        return

    real_path = file_path.replace("/uploads/", "uploads/")
    if os.path.exists(real_path):
        os.remove(real_path)

def upload_dokumen(pendaftaran, file, jenis, folder):
    validate_file(file)

    file_url = save_file(file, folder)

    existing = Dokumen.query.filter_by(
        pendaftaran_id=pendaftaran.id,
        jenis_dokumen=jenis
    ).first()

    if existing:
        delete_file_if_exists(existing.file_path)
        existing.file_path = file_url
    else:
        db.session.add(Dokumen(
            pendaftaran_id=pendaftaran.id,
            jenis_dokumen=jenis,
            file_path=file_url
        ))

    return file_url

def allowed_monitoring_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in MONITORING_IMAGE_EXTENSIONS
    )

def validate_monitoring_image(file):
    if not file or file.filename == "":
        raise Exception("Foto kegiatan wajib dipilih")

    if not allowed_monitoring_image(file.filename):
        raise Exception("Format foto harus png, jpg, jpeg, atau webp")

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length == 0:
        raise Exception("File foto kosong")

    if file_length > MONITORING_MAX_FILE_SIZE:
        raise Exception("Ukuran foto maksimal 5MB")