#!/usr/bin/env python

import os
import sys
import subprocess

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, '..'))
import settings

log = settings.get_logger('create_video_thumbnails')


def check_ffmpeg():
    try:
        subprocess.check_call(['ffmpeg', '-version'])
    except Exception:
        return False
    return True


def get_video_files_list(path):
    entries = []
    for entry in os.walk(settings.VIDEO_FILES_PATH):
        if not entry[2]:  # there is no file
            continue
        for basename in entry[2]:
            if os.path.splitext(basename)[-1].strip().lower() == '.mp4':
                entries.append(os.path.join(entry[0], basename))
    return entries


def create_thumbnail(video_file_path, thumbnail_path):
    pass


def main():
    if not check_ffmpeg():
        log.error('No ffmpeg executable found.')
        return 1
    return 0


if __name__ == '__main__':
    try:
        returncode = main()
    except:
        log.exception('Top level exception.')
        returncode = 1
    sys.exit(returncode)
