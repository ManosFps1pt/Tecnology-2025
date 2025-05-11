#!/bin/bash

pkill -f flask_server.py
sleep 3
nohup python3 flask_server.py > server.log 2>&1 &
