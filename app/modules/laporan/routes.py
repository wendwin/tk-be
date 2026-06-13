from flask import Blueprint, request, send_file
from app.utils.responses import error_response
from app.utils.decorators import role_required

from app.modules.laporan.service import generate_laporan_pdf

bp_laporan = Blueprint("laporan", __name__)

@bp_laporan.route("/export-pdf", methods=["GET"])
@role_required("kepsek", "admin")
def export_pdf():
    try:
        tahun_ajaran_id = request.args.get("tahun_ajaran_id", type=int)

        file_path = generate_laporan_pdf(tahun_ajaran_id)

        return send_file(
            file_path,
            mimetype="application/pdf",
            as_attachment=False,
            download_name="laporan_kepsek.pdf"
        )

    except Exception as e:
        return error_response(str(e), 500)