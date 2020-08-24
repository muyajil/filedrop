import os

from flask import Blueprint, render_template, request, abort, send_file, flash

download_bp = Blueprint("download", __name__)


@download_bp.route("/", methods=["GET"])
def download_form():
    return render_template('downloadRequest.html')


@download_bp.route('/downloader', methods=['POST'])
def get_files():
    bucket = request.form['bucket_name']
    folder = os.path.join(os.environ.get('UPLOAD_PATH'), bucket)
    if not os.path.exists(folder):
        flash("Bucket does not exist!")
        return render_template('downloadRequest.html')
    files = os.listdir(folder)
    links = [f"/download/{bucket}/{f}" for f in files]
    return render_template('download.html', links=links, bucket=bucket)


@download_bp.route('<bucket>/<filename>', methods=['GET'])
def download_file(bucket, filename):
    path = os.path.join(os.environ.get('UPLOAD_PATH'), bucket, filename)
    if not os.path.exists(path):
        abort(404, "File does not exists!")
    return send_file(path, as_attachment=True)
