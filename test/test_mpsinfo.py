import common
import mpsinfo
import os


def test_dict():
    info = mpsinfo.read_info(os.path.join(common.TESTS, 'data', 'IMG.jpg'))
    assert 'size' in info
