import logging
import os
from logging.handlers import RotatingFileHandler

# Timezone used by image analyzer to calculate timestamp.
TIMEZONE = 'Asia/Novosibirsk'

# Path to video files.
VIDEO_FILES_PATH = ''

# Locations of video files without ending /. Example: '/static/video'
VIDEO_FILES_LOCATION = ''

# Levels of logging
CONSOLE_LOGGING_LEVEL = logging.CRITICAL
FILE_LOGGING_LEVEL = logging.DEBUG

# Time point to create thumbnail. Must be less than 60 seconds.
THUMBNAIL_TIMESTAMP_IN_SECONDS = 2
THUMBNAIL_WIDTH = 320
THUMBNAIL_HEIGHT = 240
THUMBNAIL_FILES_PATH = ''
CREATE_NEW_POLICY, ADD_NEW_POLICY = range(1,3)
THUMBNAIL_FILES_CREATION_POLICY = CREATE_NEW_POLICY


def get_logger(process_type):
    logger = logging.getLogger(process_type)
    pid_str = str(os.getpid())
    formatter = logging.Formatter('%(asctime)s %(name)s(' + pid_str +
                                  ') %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LOGGING_LEVEL)
    console_handler.setFormatter(formatter)
    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_file_name = os.path.join(root_dir, 'log', 'mpsb.log')
    file_handler = RotatingFileHandler(log_file_name, mode='a',
                                       maxBytes=1048576, backupCount=10,
                                       encoding='UTF8', delay=False)
    file_handler.setLevel(FILE_LOGGING_LEVEL)
    file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
