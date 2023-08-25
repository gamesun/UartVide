#!/bin/bash
python3 -m pip download -d ../wheels -r ../requirements.txt --platform win_amd64 --python-version 3.8.9 --only-binary=:all: