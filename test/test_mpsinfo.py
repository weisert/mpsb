import exceptions
import os

import pytest
import common
import mpsinfo


def test_read_info_error_handling():
    with pytest.raises(exceptions.IOError):
        mpsinfo.read_info(os.path.join(common.TESTS, 'foo.jpg'))


def test_dict():
    test_filename = os.path.join(common.TESTS, 'data', 'IMG.jpg')
    info = mpsinfo.read_info(test_filename)
    assert 'EXIF ExifVersion' in info
    assert info['Image Make'] == 'LGE'
    assert info['Image Model'] == 'Nexus 5'
    assert info['datetime'] == '2016:02:14 23:17:20'
    assert info['height'] == 720
    assert info['md5'] == '1f92dd4c463ac03beb8b4838eb96e352'
    assert info['orientation'] == 'Horizontal (normal)'
    assert info['size'] == os.stat(test_filename).st_size
    assert round(info['timestamp'] - 1455470240, 5) == 0
    assert info['width'] == 1280


def test_get_tags_error_handling():
    with pytest.raises(exceptions.AssertionError):
        mpsinfo.get_tags(os.path.join(common.TESTS, 'foo'),
                         os.path.join(common.TESTS, 'bar'))


def test_get_tags():
    tags = mpsinfo.get_tags(common.TESTS,
                            os.path.join(common.TESTS, 'foo', 'bar', 'baz.jpg'))
    assert tags['basename'] == 'baz.jpg'
    assert tags['location'] == 'foo/bar'
    assert len(tags['tags']) == 2
    assert u'foo' in tags['tags']
    assert u'bar' in tags['tags']
