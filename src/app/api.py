'''
Backend API.
'''
import json
import os
import sys
import urlparse
from flask import Flask, Response, request

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, '..'))
import settings

application = Flask(__name__)


@application.route("/video/")
def video():
    '''
    Video request handler.
    :return: list of available videos in json format.
    '''
    entries = []
    for entry in os.walk(settings.VIDEO_FILES_PATH):
        if not entry[2]:  # there is no file
            continue
        links = []
        for basename in entry[2]:
            filename = os.path.join(entry[0], basename)
            relpath = os.path.relpath(filename,
                                      start=settings.VIDEO_FILES_PATH)
            parts = list(urlparse.urlsplit(request.base_url)[:2])
            parts.append(settings.VIDEO_FILES_LOCATION + '/' + relpath)
            parts.extend(['', ''])
            links.append(urlparse.urlunsplit(parts))
        entries.append({'name': os.path.basename(entry[0]), 'files': links})

    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(entries)
    return response

if __name__ == "__main__":
    application.run()
