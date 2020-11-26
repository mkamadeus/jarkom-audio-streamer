#!/bin/bash

source ./venv/bin/activate

echo -e "$1\n$2\n" | py server.py