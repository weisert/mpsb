
import json
import common
from app import application
from mock import patch
import settings

@patch('os.walk')
def test_video(walk):
    walk.return_value = (('/some/path/2013.03.05', [], ['video.mp4']),
                         ('/some/path/2009.08.01', [], ['video_00.mp4',
                                                        'video_02.mp4']),
                         ('/some/path/2014.12.25', [], ['video.mp4']))
    settings.VIDEO_FILES_PATH = '/some/path'
    settings.VIDEO_FILES_LOCATION = '/static/video'

    client = application.test_client()
    resp = client.get('/api/video/')

    walk.assert_called_with('/some/path')
    assert resp.status_code == 200
    assert resp.mimetype == 'application/json'
    expected = [{'name': '2013.03.05',
                 'files': ['http://localhost/static/video/2013.03.05/' +
                           'video.mp4']},
                {'name': '2009.08.01',
                 'files': ['http://localhost/static/video/2009.08.01/' +
                           'video_00.mp4',
                           'http://localhost/static/video/2009.08.01/' +
                           'video_02.mp4']},
                {'name': '2014.12.25',
                 'files': ['http://localhost/static/video/2014.12.25/' +
                           'video.mp4']}]
    assert json.dumps(expected) == resp.data
