
import datetime
import exceptions
import json
import mock
import pytest

import common
import import_video


@mock.patch('os.path.exists')
@mock.patch('os.makedirs')
@mock.patch('shutil.copy2')
def test_copy(copy2, makedirs, exists):
    exists.return_value = False
    import_video.copy('/some/file', '/some/folder/file')
    exists.assert_called_once_with('/some/folder')
    makedirs.assert_called_once_with('/some/folder', mode=0o755)
    copy2.assert_called_once_with('/some/file', '/some/folder/file')


@mock.patch('import_video.convert_file')
@mock.patch('import_video.copy')
def test_make_job(copy, convert_file):
    job = {'from': '/some/file', 'to': '/raw/out/2016.03.01/file',
           'converted': '/out/2016.03.01/file'}
    import_video.make_job(job, 'nexus5')
    copy.assert_called_once_with('/some/file', '/raw/out/2016.03.01/file')
    convert_file.assert_called_once_with('/some/file', '/out/2016.03.01/file',
                                         'nexus5')


@mock.patch('os.path.exists')
def test_check_job(exists):
    exists.side_effect = [True, False]
    job = {'from': '/some/file', 'to': '/raw/out/2016.03.01/file',
           'converted': '/converted/out/2016.03.01/file'}
    with pytest.raises(exceptions.RuntimeError):
        import_video.check_job(job)
    exists.assert_called_once_with('/raw/out/2016.03.01/file')
    exists.reset_mock()

    exists.side_effect = [False, True]
    job = {'from': '/some/file', 'to': '/raw/out/2016.03.01/file',
           'converted': '/converted/out/2016.03.01/file'}
    with pytest.raises(exceptions.RuntimeError):
        import_video.check_job(job)
    exists.has_calls(mock.call('/raw/out/2016.03.01/file'),
                     mock.call('/converted/out/2016.03.01/file'))
    assert exists.call_count == 2
    exists.reset_mock()

    exists.side_effect = [False, False]
    import_video.check_job(job)  # Not raises
    exists.has_calls(mock.call('/raw/out/2016.03.01/file'),
                     mock.call('/converted/out/2016.03.01/file'))
    assert exists.call_count == 2



@mock.patch('os.path.exists')
@mock.patch('os.path.isdir')
def test_create_job_description(isdir, exists):
    date = datetime.date(2016, 3, 1)
    exists.side_effect = [False, True]
    isdir.side_effect = [True, True]
    with pytest.raises(exceptions.IOError):
        import_video.create_job_description('/file', date,
                                            '/raw/out/', '/converted/out')
    exists.assert_called_once_with('/raw/out/')
    assert isdir.call_count == 0
    exists.reset_mock()
    isdir.reset_mock()

    exists.side_effect = [True, True]
    isdir.side_effect = [False, True]
    with pytest.raises(exceptions.IOError):
        import_video.create_job_description('/file', date,
                                            '/raw/out/', '/converted/out')
    exists.assert_called_once_with('/raw/out/')
    isdir.assert_called_once_with('/raw/out/')
    exists.reset_mock()
    isdir.reset_mock()

    exists.side_effect = [True, False]
    isdir.side_effect = [True, True]
    with pytest.raises(exceptions.IOError):
        import_video.create_job_description('/file', date,
                                            '/raw/out/', '/converted/out')
    exists.assert_has_calls([mock.call('/raw/out/'),
                             mock.call('/converted/out')])
    assert exists.call_count == 2
    isdir.assert_called_once_with('/raw/out/')
    exists.reset_mock()
    isdir.reset_mock()

    exists.side_effect = [True, True]
    isdir.side_effect = [True, False]
    with pytest.raises(exceptions.IOError):
        import_video.create_job_description('/file', date,
                                            '/raw/out/', '/converted/out')
    exists.assert_has_calls([mock.call('/raw/out/'),
                             mock.call('/converted/out')])
    assert exists.call_count == 2
    isdir.assert_has_calls([mock.call('/raw/out/'),
                            mock.call('/converted/out')])
    assert isdir.call_count == 2
    exists.reset_mock()
    isdir.reset_mock()

    exists.side_effect = [True, True]
    isdir.side_effect = [True, True]
    job = import_video.create_job_description('/file', date, '/raw/out/',
                                              '/converted/out')
    expected = json.dumps({'from': '/file', 'to': '/raw/out/2016.03.01/file',
                           'converted': '/converted/out/2016.03.01/file'})
    assert json.dumps(job) == expected


def test_parse_date_nexus5():
    invalid_files = ['VVID_20150614_160042.mp4', 'VID20150913_212655.mp4',
                     'VID_0151025_204016.mp4', 'VID_220151106_093315.mp4',
                     'VID_20151227_1110548.mp4']
    for filename in invalid_files:
        with pytest.raises(exceptions.RuntimeError):
            import_video.parse_date_nexus5(filename)
    valid_files = [['VID_20150614_160042.mp4', datetime.date(2015, 6, 14)],
                   ['VID_20150913_212655.mp4', datetime.date(2015, 9, 13)],
                   ['VID_20151025_204016.mp4', datetime.date(2015, 10, 25)],
                   ['VID_20151106_093315.mp4', datetime.date(2015, 11, 6)],
                   ['VID_20151227_111548.mp4', datetime.date(2015, 12, 27)],
                   ['VID_20150801_162045.mp4', datetime.date(2015, 8, 1)],
                   ['VID_20150915_141219.mp4', datetime.date(2015, 9, 15)],
                   ['VID_20151105_103531.mp4', datetime.date(2015, 11, 5)],
                   ['VID_20151106_124508.mp4', datetime.date(2015, 11, 6)],
                   ['VID_20160227_175256.mp4', datetime.date(2016, 02, 27)],
                   ['VID_20150801_172023.mp4', datetime.date(2015, 8, 1)],
                   ['VID_20150926_134132.mp4', datetime.date(2015, 9, 26)],
                   ['VID_20151105_112827.mp4', datetime.date(2015, 11, 5)],
                   ['VID_20151227_110453.mp4', datetime.date(2015, 12, 27)],
                   ['VID_20160227_175356.mp4', datetime.date(2016, 2, 27)],
                   ['VID_20150823_200939.mp4', datetime.date(2015, 8, 23)],
                   ['VID_20151023_160026.mp4', datetime.date(2015, 10, 23)],
                   ['VID_20151106_093005.mp4', datetime.date(2015, 11, 6)],
                   ['VID_20151227_111200.mp4', datetime.date(2015, 12, 27)],
                   ['VID_20160227_180455.mp4', datetime.date(2016, 2, 27)]]
    for item in valid_files:
        assert item[1] == import_video.parse_date_nexus5(item[0])


@mock.patch('os.path.exists')
@mock.patch('os.path.isdir')
@mock.patch('os.walk')
def test_get_input_files_list(walk, isdir, exists):
    exists.return_value = False
    isdir.return_value = True
    with pytest.raises(exceptions.IOError):
        import_video.get_input_files_list('/some/path')
    exists.return_value = True
    isdir.return_value = False
    with pytest.raises(exceptions.IOError):
        import_video.get_input_files_list('/some/path')
    isdir.return_value = True
    walk.return_value = (('/some/path/2013.03.05', [], ['video.mp4']),
                         ('/some/path/2009.08.01', [], ['video_00.mp4',
                                                        'video_02.mp4']),
                         ('/some/path/2014.12.25', [], ['video.mp4']),
                         ('/some/path/2013.03.05', [], ['video.mp3']))
    files = import_video.get_input_files_list('/some/path')
    assert len(files) == 4
    assert files[0] == '/some/path/2013.03.05/video.mp4'
    assert files[1] == '/some/path/2009.08.01/video_00.mp4'
    assert files[2] == '/some/path/2009.08.01/video_02.mp4'
    assert files[3] == '/some/path/2014.12.25/video.mp4'


def test_parse_command_line_options():
    args = import_video.parse_command_line_options([
        '--device=nexus5', '--input=/raw/path',
        '--raw-output=/path/to/storage', '--converted-output=/path/to/www'])
    assert args.device == 'nexus5'
    assert args.input == '/raw/path'
    assert args.raw_output == '/path/to/storage'
    assert args.converted_output == '/path/to/www'
    args1 = import_video.parse_command_line_options([
        '--device', 'nexus5', '--input', '/raw/path', '--raw-output',
        '/path/to/storage', '--converted-output', '/path/to/www'])
    assert args1.device == 'nexus5'
    assert args1.input == '/raw/path'
    assert args1.raw_output == '/path/to/storage'
    assert args1.converted_output == '/path/to/www'
    args2 = import_video.parse_command_line_options([
        '-d', 'nexus5', '-i', '/raw/path', '-s', '/path/to/storage', '-o',
        '/path/to/www'])
    assert args2.device == 'nexus5'
    assert args2.input == '/raw/path'
    assert args2.raw_output == '/path/to/storage'
    assert args2.converted_output == '/path/to/www'
