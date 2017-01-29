#!/bin/sh
# Run this file for installation!

if [ `id -u` -ne 0 ]; then
    echo "Please re-run ${this_file} as root."
    exit 1
fi

docker build -f docker/Dependencies -t aiplay/serverbase:v1 --no-cache=true .