import os

from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/", methods=["GET"])
def upload_form():
    return render_template('upload.html')


@upload_bp.route('/uploader', methods=['POST'])
def upload_file():
    files = request.files.getlist("file[]")
    bucket = request.form['bucket_name']
    folder = os.path.join(os.environ.get('UPLOAD_PATH'), bucket)
    if not os.path.exists(folder):
        os.makedirs(folder)

    success_files = []
    fail_files = []

    for f in files:
        try:
            path = os.path.join(folder, secure_filename(f.filename))
            current_app.logger.info('Uploading file {}'.format(path))
            fh = open(path, 'w')
            f.save(path)
            fh.close()
            success_files.append(secure_filename(f.filename))
        except:  # noqa E722
            fail_files.append(secure_filename(f.filename))
    return render_template("success.html", sucesses=success_files, fails=fail_files, bucket=bucket)
