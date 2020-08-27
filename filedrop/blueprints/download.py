import os

from flask import Blueprint, render_template, request, abort, send_file, flash, current_app

download_bp = Blueprint("download", __name__)


@download_bp.route("/", methods=["GET"])
def download_form():
    return render_template('downloadRequest.html')


@download_bp.route('<bucket>')
@download_bp.route('downloader', methods=['POST', 'GET'])
def get_files(bucket=None):
    if bucket is None:
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
    current_app.logger.info('Downloading file {}'.format(path))
    return send_file(path, as_attachment=True)
