#!/bin/bash

echo nohup python3 flask_server.py > server.log 2>&1 &
