#!/bin/sh
# Running now

if [ `id -u` -ne 0 ]; then
    echo "Please re-run ${this_file} as root."
    exit 1
fi

nohup redis-server &
nohup celery worker -A config.celery &
python3 server.py