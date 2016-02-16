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
    assert 'LGE' == info['Image Make']
    assert 'Nexus 5' == info['Image Model']
    assert '2016:02:14 23:17:20' == info['datetime']
    assert 720 == info['height']
    assert '1f92dd4c463ac03beb8b4838eb96e352' == info['md5']
    assert 'Horizontal (normal)' == info['orientation']
    assert os.stat(test_filename).st_size == info['size']
    assert 0 == round(info['timestamp'] - 1455470240, 5)
    assert 1280 == info['width']


def test_get_tags_error_handling():
    with pytest.raises(exceptions.AssertionError):
        mpsinfo.get_tags(os.path.join(common.TESTS, 'foo'),
                         os.path.join(common.TESTS, 'bar'))


def test_get_tags():
    tags = mpsinfo.get_tags(common.TESTS,
                            os.path.join(common.TESTS, 'foo', 'bar', 'baz.jpg'))
    assert 'baz.jpg' == tags['basename']
    assert 'foo/bar' == tags['location']
    assert 2 == len(tags['tags'])
    assert u'foo' in tags['tags']
    assert u'bar' in tags['tags']
