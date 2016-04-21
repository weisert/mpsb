#!/usr/bin/env python

import os
import shutil
import subprocess
import sys

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
    for entry in os.walk(path):
        if not entry[2]:  # there is no file
            continue
        for basename in entry[2]:
            if os.path.splitext(basename)[-1].strip().lower() == '.mp4':
                entries.append(os.path.join(entry[0], basename))
    return entries


def create_thumbnail(video_file_path, thumbnail_path):
    try:
        sec = settings.THUMBNAIL_TIMESTAMP_IN_SECONDS
        assert  60 > sec > 0
        width = settings.THUMBNAIL_WIDTH
        assert width > 0
        height = settings.THUMBNAIL_HEIGHT
        assert height > 0
        command = ['ffmpeg', '-i', video_file_path, '-ss',
                   '00:00:{0:02d}'.format(sec), '-vframes', '1', '-vf',
                   'scale="\'if(gt(a,4/3),{},-1)\':\'if(gt(a,4/3),-1,{})\'"'.format(
                       width, height), thumbnail_path]
        log.info('Run: ', ' '.join(command))
        subprocess.check_call(command)
    except Exception:
        log.exception('Failed to create thumbnail for {}'.format(video_file_path))
        return False
    return True


def get_thumbnail_filename_for(video_file):
    relpath = os.path.relpath(video_file,
                              start=settings.VIDEO_FILES_PATH)
    relpath = os.path.splitext(relpath)[0]  # remove extension
    return settings.THUMBNAIL_FILES_PATH + '/' + relpath + '.png'


def main():
    if not check_ffmpeg():
        log.error('No ffmpeg executable found.')
        return 1
    if settings.THUMBNAIL_FILES_CREATION_POLICY == settings.CREATE_NEW_POLICY:
        shutil.rmtree(settings.THUMBNAIL_FILES_PATH)
    result = 0
    files = get_video_files_list(settings.VIDEO_FILES_LOCATION)
    for video_file in files:
        thumbnail_file = get_thumbnail_filename_for(video_file)
        if os.path.exists(thumbnail_file):
            continue
        os.makedirs(os.path.dirname(thumbnail_file), 0755)
        if not create_thumbnail(video_file, thumbnail_file):
            result = 1
    return result


if __name__ == '__main__':
    try:
        returncode = main()
    except:
        log.exception('Top level exception.')
        returncode = 1
    sys.exit(returncode)
