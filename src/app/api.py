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
import settings  # pylint: disable=wrong-import-position

application = Flask(__name__)  # pylint: disable=invalid-name


@application.route("/api/video/")
def video():
    '''
    Video request handler.
    :return: list of available videos in json format.
    '''
    entries = []
    for entry in os.walk(settings.VIDEO_FILES_PATH):
        if not entry[2]:  # there is no file
            continue
        date = os.path.basename(entry[0])
        for basename in entry[2]:
            filename = os.path.join(entry[0], basename)
            relpath = os.path.relpath(filename,
                                      start=settings.VIDEO_FILES_PATH)
            parts = list(urlparse.urlsplit(request.base_url)[:2])
            parts.append(settings.VIDEO_FILES_LOCATION + '/' + relpath)
            parts.extend(['', ''])
            url = urlparse.urlunsplit(parts)
            parts[2] = settings.THUMBNAIL_FILES_LOCATION + '/'
            parts[2] += os.path.splitext(relpath)[0] + '.png'
            thumbnail = urlparse.urlunsplit(parts)
            entries.append({'date': date, 'url': url, 'thumbnail': thumbnail})
    entries.sort(reverse=True, key=lambda x: x['date'])

    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(entries)
    return response

if __name__ == "__main__":
    application.run()
