import os

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/", methods=["GET"])
def upload_form():
    return render_template('upload.html')


@upload_bp.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    bucket = request.form['bucket_name']
    folder = os.path.join(os.environ.get('UPLOAD_PATH'), bucket)
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, secure_filename(f.filename))
    fh = open(path, 'w')
    f.save(path)
    fh.close()
    return 'file uploaded successfully'
