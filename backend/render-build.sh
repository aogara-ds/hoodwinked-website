#!/usr/bin/env bash
set -e # exit on error

pip3 install -r requirements.txt

python manage.py makemigrations hoodwinked --no-input

python manage.py migrate --no-input