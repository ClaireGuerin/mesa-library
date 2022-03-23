#!/bin/bash

env/bin/python3 -m pip install --upgrade pip
python3 -m pip install --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install -e . # install mesa from setup.py (in root), in edit mode
python -m pip install pysimplegui
source env/bin/activate