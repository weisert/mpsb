
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
    walk.assert_called_once_with('/some/path')
    expected = ['/some/path/2013.03.05/video.mp4',
                '/some/path/2009.08.01/video_00.mp4',
                '/some/path/2009.08.01/video_02.mp4']
    assert len(expected) == len(actual)
    for index in xrange(len(expected)):
        assert expected[index] == actual[index]


@patch('subprocess.check_call')
def test_check_ffmpeg(check_call):
    check_call.return_value = ''
    assert cvt.check_ffmpeg()
    check_call.assert_called_once_with(['ffmpeg', '-version'])
    check_call.reset_mock()
    check_call.side_effect = Exception('No ffmpeg')
    assert not cvt.check_ffmpeg()
    check_call.assert_called_once_with(['ffmpeg', '-version'])


@patch('subprocess.check_call')
def test_create_thumbnail(check_call):
    check_call.return_value = ''
    assert cvt.create_thumbnail('VID_20160415_223123.mp4',
                                'output_320x240_boxed.png')
    check_call.assert_called_once_with([
        'ffmpeg',
        '-i',
        'VID_20160415_223123.mp4',
        '-ss',
        '00:00:02',
        '-vframes',
        '1',
        '-vf',
        'scale="\'if(gt(a,4/3),320,-1)\':\'if(gt(a,4/3),-1,240)\'"',
        'output_320x240_boxed.png'])
    check_call.reset_mock()
    check_call.side_effect = Exception('No ffmpeg')
    assert not cvt.create_thumbnail('VID_20160415_223123.mp4',
                                    'output_320x240_boxed.png')
    check_call.assert_called_once_with([
        'ffmpeg',
        '-i',
        'VID_20160415_223123.mp4',
        '-ss',
        '00:00:02',
        '-vframes',
        '1',
        '-vf',
        'scale="\'if(gt(a,4/3),320,-1)\':\'if(gt(a,4/3),-1,240)\'"',
        'output_320x240_boxed.png'])
