#!/usr/bin/env bash

su -m fuser -c "gunicorn -b 0.0.0.0:8000 bse:app"