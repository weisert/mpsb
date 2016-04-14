
import common
import create_video_thumbnails as cvt
from mock import patch

@patch('os.walk')
def test_get_video_files_list(walk):
    walk.return_value = (('/some/path/2013.03.05', [], ['video.mp4']),
                         ('/some/path/2009.08.01', [], ['video_00.mp4',
                                                        'video_02.mp4',
                                                        'video_00.png',
                                                        'some_file']))
    actual = cvt.get_video_files_list('/some/path')
    expected = ['/some/path/2013.03.05/video.mp4',
                '/some/path/2009.08.01/video_00.mp4',
                '/some/path/2009.08.01/video_02.mp4']
    assert len(expected) == len(actual)
    for index in xrange(len(expected)):
        assert expected[index] == actual[index]
