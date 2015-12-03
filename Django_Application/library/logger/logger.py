# logger.py includes functions and variables to enable logging

import logging
import logging.config

# Read the logger.conf file, and create a logger
logging.config.fileConfig('./library/logger/logger.conf')
logger = logging.getLogger('root')