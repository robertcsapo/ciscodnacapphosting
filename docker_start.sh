#!/bin/sh
set -m
/usr/local/bin/dockerd-entrypoint.sh &>/dev/null &
/bin/sh