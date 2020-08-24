import os
import subprocess
import time

from flask_crontab import Crontab

crontab = Crontab()


def is_older_than(file, days=1):
    file_time = os.path.getmtime(file)
    if (time.time() - file_time) / 3600 > 24*days:
        return True
    else:
        return False


def get_all_files(folder):
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


@crontab.job(minute="*/5")
def delete_old_files():
    uploads_folder = os.environ.get('UPLOAD_PATH')
    for abs_path in get_all_files(uploads_folder):
        if is_older_than(abs_path, 30):
            os.remove(abs_path)
    subprocess.call(["find", uploads_folder, "-type", "d", "-empty", "-delete"])
