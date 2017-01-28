#!/bin/sh
# Running now

if [ `id -u` -ne 0 ]; then
    echo "Please re-run ${this_file} as root."
    exit 1
fi

nohup redis-server &
nohup celery worker -A config.celery &
/usr/bin/python3 server.py 0.0.0.0 4999 NO_DEBUG