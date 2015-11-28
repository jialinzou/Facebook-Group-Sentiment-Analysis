#!/usr/bin/env bash

celery -A celery_main worker --concurrency=1 --loglevel=info