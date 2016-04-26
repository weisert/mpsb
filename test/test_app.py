
import json
import common
from app import application
from mock import patch
import settings

@patch('os.walk')
def test_video(walk):
    walk.return_value = (('/some/path/2013.03.05', [], ['video.mp4']),
                         ('/some/path/2009.08.01', [], ['video_0.mp4',
                                                        'video_2.mp4']),
                         ('/some/path/2014.12.25', [], ['video.mp4']))
    settings.VIDEO_FILES_PATH = '/some/path'
    settings.VIDEO_FILES_LOCATION = '/static/video'
    settings.THUMBNAIL_FILES_LOCATION = '/thumbnails/video'

    client = application.test_client()
    resp = client.get('/api/video/')

    walk.assert_called_with('/some/path')
    assert resp.status_code == 200
    assert resp.mimetype == 'application/json'
    expected = [{
        'date': '2014.12.25',
        'url': 'http://localhost/static/video/2014.12.25/video.mp4',
        'thumbnail': 'http://localhost/thumbnails/video/2014.12.25/video.png'
    }, {
        'date': '2013.03.05',
        'url': 'http://localhost/static/video/2013.03.05/video.mp4',
        'thumbnail': 'http://localhost/thumbnails/video/2013.03.05/video.png'
    }, {
        'date': '2009.08.01',
        'url': 'http://localhost/static/video/2009.08.01/video_0.mp4',
        'thumbnail': 'http://localhost/thumbnails/video/2009.08.01/video_0.png'
    }, {
        'date': '2009.08.01',
        'url': 'http://localhost/static/video/2009.08.01/video_2.mp4',
        'thumbnail': 'http://localhost/thumbnails/video/2009.08.01/video_2.png'
    }]
    assert json.dumps(expected) == resp.data
