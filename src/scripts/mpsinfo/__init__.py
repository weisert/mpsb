"""
Module to retrieve auxiliary information from image file.
"""
from datetime import datetime
import calendar
import exceptions
import hashlib
import os
import sys

import exifread
import pytz

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, '..', '..'))
from settings import TIMEZONE


def _get_exif_data(raw_file):
    """
    :param raw_file: File object to be analyzed.
    :return: Dictionary that contains exif info of given file.
    """
    keys = [
        # 'EXIF MakerNote',
        # 'GPS GPSDate',
        # 'EXIF ApertureValue',
        # 'MakerNote Tag 0x000E',
        # 'Image ExifOffset',
        # 'EXIF LensMake',
        # 'GPS GPSDestBearingRef',
        # 'MakerNote Tag 0x0001',
        # 'MakerNote Tag 0x0002',
        # 'MakerNote Tag 0x0003',
        # 'MakerNote Tag 0x0004',
        # 'GPS GPSLatitudeRef',
        # 'MakerNote Tag 0x0006',
        # 'GPS GPSAltitudeRef',
        # 'Image DateTime',
        # 'EXIF ShutterSpeedValue',
        # 'EXIF ColorSpace',
        # 'EXIF MeteringMode',
        'EXIF ExifVersion',
        'Image Software',
        # 'EXIF ISOSpeedRatings',
        # 'Thumbnail YResolution',
        # 'GPS GPSSpeed',
        'GPS GPSLongitude',
        'Image Orientation',
        'EXIF DateTimeOriginal',
        # 'Image YCbCrPositioning',
        # 'MakerNote Tag 0x0005',
        # 'Thumbnail JPEGInterchangeFormat',
        # 'EXIF ComponentsConfiguration',
        # 'MakerNote Tag 0x0008',
        # 'GPS GPSSpeedRef',
        'Image Model',
        'EXIF ExifImageLength',
        'EXIF SceneType',
        # 'Image ResolutionUnit',
        # 'EXIF ExposureTime',
        # 'Thumbnail XResolution',
        # 'GPS GPSDestBearing',
        # 'Image GPSInfo',
        # 'EXIF ExposureProgram',
        # 'Thumbnail JPEGInterchangeFormatLength',
        # 'EXIF Flash',
        # 'Thumbnail Compression',
        # 'MakerNote Tag 0x0009',
        # 'GPS GPSImgDirectionRef',
        # 'EXIF ExposureMode',
        # 'EXIF FocalLengthIn35mmFilm',
        # 'EXIF FlashPixVersion',
        'EXIF ExifImageWidth',
        'GPS GPSLatitude',
        # 'EXIF SceneCaptureType',
        # 'JPEGThumbnail',
        'GPS GPSTimeStamp',
        # 'EXIF SubjectArea',
        # 'EXIF LensSpecification',
        # 'EXIF SubSecTimeOriginal',
        # 'EXIF BrightnessValue',
        # 'EXIF LensModel',
        # 'EXIF DateTimeDigitized',
        # 'EXIF FocalLength',
        # 'GPS GPSImgDirection',
        # 'Image XResolution',
        'Image Make',
        # 'EXIF WhiteBalance',
        # 'EXIF SubSecTimeDigitized',
        # 'Thumbnail ResolutionUnit',
        # 'Image YResolution',
        # 'MakerNote Tag 0x0007',
        # 'GPS GPSLongitudeRef',
        # 'EXIF FNumber',
        # 'EXIF ExposureBiasValue',
        # 'EXIF SensingMethod',
        # 'GPS GPSAltitude',
    ]
    tags = exifread.process_file(raw_file)
    return {k: str(v) for k, v in tags.items() if k in keys}


def _get_sha384(raw_data):
    """
    :param raw_data: bytes to calculate sha384 hash.
    :return: hex representation of sha384 hash.
    """
    sha384 = hashlib.sha384(raw_data)
    return {'sha384': sha384.hexdigest()}


def get_tags(prefix, path):
    """
    :param prefix: Root path of image storage.
    :param path: Path to certain file.
    :return: List that contains dir names in unicode.
    """
    assert path.startswith(prefix)
    dirname = os.path.dirname(path)
    location = dirname.replace(prefix, '')
    if location.startswith('/'):
        location = location[1:]
    return {'tags': [x.lower() for x in location.decode('UTF8').split('/')],
            'basename': os.path.basename(path),
            'location': location}


def read_info(path):
    """
    :param path: File to be analyzed
    :return: Dictionary that contains meta info of given file.
    """
    if not os.path.exists(path):
        raise exceptions.IOError('No such file or directory: ' + path)
    with open(path, 'rb') as image:
        result = _get_exif_data(image)
        image.seek(0)
        data = image.read()
        result['size'] = len(data)
        result.update(_get_sha384(data))
    key_mapper = {'EXIF DateTimeOriginal': 'datetime',
                  'EXIF ExifImageWidth': 'width',
                  'EXIF ExifImageLength': 'height',
                  'Image Orientation': 'orientation'}
    for k in key_mapper:
        if k in result:
            result[key_mapper[k]] = result[k]
            del result[k]
    tzone = pytz.timezone(TIMEZONE)
    date = datetime.strptime(result['datetime'], '%Y:%m:%d %H:%M:%S')
    result['timestamp'] = calendar.timegm(tzone.localize(date).utctimetuple())
    result['width'] = int(result['width'])
    result['height'] = int(result['height'])
    return result
