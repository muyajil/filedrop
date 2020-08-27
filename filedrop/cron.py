import os
import time

from flask_crontab import Crontab
from flask import current_app

crontab = Crontab()


def is_older_than(file, days):
    file_time = os.path.getmtime(file)
    if (time.time() - file_time) / 3600 > 24*days:
        return True
    else:
        return False


def get_all_files(folder):
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def get_all_dirs(folder):
    for dirpath, dirs, _ in os.walk(folder):
        for d in dirs:
            yield os.path.abspath(os.path.join(dirpath, d))


@crontab.job(minute="0")
def delete_old_files():
    current_app.logger.info('------------------------------------')
    current_app.logger.info('Starting cleanup job...')
    uploads_folder = os.environ.get('UPLOAD_PATH')
    for abs_path in get_all_files(uploads_folder):
        if is_older_than(abs_path, 30):
            current_app.logger.info('Deleting file {}'.format(abs_path))
            os.remove(abs_path)

    for abs_path in get_all_dirs(uploads_folder):
        if not os.listdir(abs_path):
            current_app.logger.info('Deleting bucket {}'.format(abs_path))
            os.remove(abs_path)
