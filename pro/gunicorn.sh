#!/bin/bash

source /home/x/apps/pro/env/bin/activate
gunicorn -c /home/x/apps/pro/gunicorn.py pro.wsgi
