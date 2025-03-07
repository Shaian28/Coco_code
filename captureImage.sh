#!/bin/bash

pkill stream_server
libcamera-still -o "$1"
python3 ~/svn/robobot/stream_server/stream_server.py