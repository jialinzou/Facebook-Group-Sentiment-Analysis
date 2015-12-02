import sys
import os
from celery import Celery

# celery_main.py starts up celery

# Need to move up a few directories up
sys.path.insert(0, os.path.abspath("../.."))

# Sets up the celery object, and loads configuration from celery_configurations folder
task_queue = Celery()
task_queue.config_from_object('workload_distribution.celery_configurations.celery_config')