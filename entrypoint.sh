#!/bin/bash

/etc/init.d/cron start
gunicorn --log-level INFO --timeout 6000 --workers 4 --bind 0.0.0.0:5000 "filedrop.app:create_app()"