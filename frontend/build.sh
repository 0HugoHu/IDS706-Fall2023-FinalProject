#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt

flask db init
flask db migrate
flask db upgrade
flask gen_api
