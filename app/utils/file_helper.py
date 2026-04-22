import os
from app.extensions import db
from werkzeug.utils import secure_filename
from datetime import datetime
from app.models.pendaftaran.dokumen import Dokumen

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
UPLOAD_FOLDER = 'uploads/pembayaran'
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file):
    if not allowed_file(file.filename):
        raise Exception("Format file tidak diizinkan (png, jpg, jpeg)")

    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)

    if file_length > MAX_FILE_SIZE:
        raise Exception("Ukuran file maksimal 2MB")

def save_file(file, subfolder):
    base_folder = os.path.join(os.getcwd(), "uploads", subfolder)
    os.makedirs(base_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{filename}"

    filepath = os.path.join(base_folder, filename)
    file.save(filepath)

    return f"/uploads/{subfolder}/{filename}"

def upload_dokumen(pendaftaran, file, jenis, folder):
    validate_file(file)
    file_url = save_file(file, folder)

    existing = Dokumen.query.filter_by(
        id_pendaftaran=pendaftaran.id,
        jenis_dokumen=jenis
    ).first()

    if existing:
        old_path = existing.file_path.replace("/uploads/", "uploads/")
        if os.path.exists(old_path):
            os.remove(old_path)

        existing.file_path = file_url
    else:
        db.session.add(Dokumen(
            id_pendaftaran=pendaftaran.id,
            jenis_dokumen=jenis,
            file_path=file_url
        ))

    return file_url