import common
import mpsinfo
import os


def test_dict():
    test_filename = os.path.join(common.TESTS, 'data', 'IMG.jpg')
    info = mpsinfo.read_info(test_filename)
    assert 'size' in info
    assert os.stat(test_filename).st_size == info['size']
    assert 'md5' in info
    assert info['md5'] == '1f92dd4c463ac03beb8b4838eb96e352'
