#!/usr/bin/env python

import os
import sys

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, '..'))
import settings

log = settings.get_logger('create_video_thumbnails')


def get_video_files_list(path):
    entries = []
    for entry in os.walk(settings.VIDEO_FILES_PATH):
        if not entry[2]:  # there is no file
            continue
        for basename in entry[2]:
            print os.path.splitext(basename)
            if os.path.splitext(basename)[-1].strip().lower() == '.mp4':
                entries.append(os.path.join(entry[0], basename))
    return entries


def main():
    return 0


if __name__ == '__main__':
    try:
        returncode = main()
    except:
        log.exception('Top level exception.')
        returncode = 1
    sys.exit(returncode)
