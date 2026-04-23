from app.extensions import db

class AsesmenPertanyaan(db.Model):
    __tablename__ = 'asesmen_pertanyaan'

    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)

    tipe = db.Column(
        db.Enum('text', 'textarea', 'radio', 'checkbox', 'select', 'number', name='tipe_asesmen_enum'),
        default='text'
    )

    is_required = db.Column(db.Boolean, default=True)
    urutan = db.Column(db.Integer)


    options = db.Column(db.JSON, nullable=True)