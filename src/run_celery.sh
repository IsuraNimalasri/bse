#!/usr/bin/env bash

su -m fuser -c "celery -A tasks worker -l info"