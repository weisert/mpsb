
import exceptions
import exifread
import hashlib
import os


def _get_exif_data(raw_file):
    keys = [
        # 'EXIF MakerNote',
        'GPS GPSDate',
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
        'Image DateTime',
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
        'Image ResolutionUnit',
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


def _get_md5(raw_data):
    md5 = hashlib.md5()
    md5.update(raw_data)
    return {'md5': md5.hexdigest()}


def get_tags(prefix, path):
    assert path.startswith(prefix)
    dirname = os.path.dirname(path)
    location = dirname.replace(prefix, '')
    if location.startswith('/'):
        location = location[1:]
    return {'tags': map(lambda x: x.lower(),
                        location.decode('UTF8').split('/')),
            'basename': os.path.basename(path),
            'location': location}


def read_info(path):
    if not os.path.exists(path):
        raise exceptions.IOError('No such file or directory: ' + path)
    with open(path, 'rb') as f:
        result = _get_exif_data(f)
        f.seek(0)
        data = f.read()
        result['size'] = len(data)
        result.update(_get_md5(data))
    return result
