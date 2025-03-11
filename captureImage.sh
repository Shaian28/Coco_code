#!/bin/bash

pkill stream_server
cd ~/git/Coco_code
libcamera-still -o "$1"
python3 ~/svn/robobot/stream_server/stream_server.py