#!/usr/bin/env python
'''
Script for converting and storing video files.
'''
import argparse
import datetime
import exceptions
import os
import re
import shutil
import sys

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_CURRENT_DIR, '..'))
import settings

log = settings.get_logger('import_video')


def copy(source, destination):
    '''
    Copies file. In case destination directory not exist it is created.
    :param source: Source filename.
    :param destination: Destination filename.
    :return: None.
    '''
    destdir = os.path.dirname(destination)
    if not os.path.exists(destdir):
        os.makedirs(destdir, mode=0o755)
    shutil.copy2(source, destination)
    print 'Copy from: \t' + source + ' to ' + destination


def convert_file_nexus5(source, destination):
    '''
    Since Nexus5 produces MP4(AAC, H264) this function just copies source file
    to destionation.
    :param source: Source filename.
    :param destination: Destination filename.
    :return: None.
    '''
    copy(source, destination)


def convert_file(source, destination, device):
    '''
    Converts the given file to MP4(AAC, H264)
    :param source: Source filename.
    :param destination: Destination filename.
    :param device: name of device that shot the video.
    :return: None.
    '''
    if device == 'nexus5':
        return convert_file_nexus5(source, destination)
    else:
        raise exceptions.NotImplementedError('Unknown device: ' + device)


def make_job(job, device):
    '''
    Copies source file to the reliable storage and makes converted copy for
    the app.
    :param job: Job description.
    :param device: name of device that shot the video.
    :return: None.
    '''
    copy(job['from'], job['to'])
    convert_file(job['from'], job['converted'], device)


def check_job(job):
    '''
    Checks whenever the job can be done without errors. If any error is found
    raises exception with error description.
    :param job: Job description.
    :return: None.
    '''
    if os.path.exists(job['to']):
        # TODO(weisert): Check file equality.
        raise exceptions.RuntimeError('Target file exists: ' + job['to'])
    if os.path.exists(job['converted']):
        raise exceptions.RuntimeError('Converted file exists: ' +
                                      job['converted'])


def create_job_description(filename, date, raw_out_dir, converted_out_dir):
    '''
    Returns description of the job to be done.
    :param filename: Input file name.
    :param date: Date retrieved from input file.
    :param raw_out_dir: Path to the reliable storage to save raw file.
    :param converted_out_dir: Path to www directory.
    :return: job description dictionary.
    '''
    if not os.path.exists(raw_out_dir):
        raise exceptions.IOError('No such directory: ' + raw_out_dir)
    if not os.path.isdir(raw_out_dir):
        raise exceptions.IOError(raw_out_dir + ' is not a directory.')
    if not os.path.exists(converted_out_dir):
        raise exceptions.IOError('No such directory: ' + converted_out_dir)
    if not os.path.isdir(converted_out_dir):
        raise exceptions.IOError(converted_out_dir + ' is not a directory.')
    datestr = date.strftime('%Y.%m.%d')
    return {'from': filename,
            'to': os.path.join(raw_out_dir, datestr,
                               os.path.basename(filename)),
            'converted': os.path.join(converted_out_dir, datestr,
                                      os.path.basename(filename))}


def parse_date_nexus5(filename):
    '''
    Retrieves shot date from filename like 'VID_20150614_160042.mp4'
    :param filename: Name of the file.
    :return: datetime.date object.
    '''
    basename = os.path.basename(filename)
    pattern = r'VID_(\d{4})(\d\d)(\d\d)_\d{6}\.mp4'
    date_re = re.compile(pattern)
    match = date_re.match(basename)
    if not match:
        raise exceptions.RuntimeError('File "' + basename + '" did not match '
                                      'Nexus\'s video files pattern: "' +
                                      pattern + '"')
    return datetime.date(int(match.group(1)),  # year
                         int(match.group(2)),  # month
                         int(match.group(3)))  # day of month


def get_date_for_device(device, filename):
    '''
    Retrieves date from file using device dependent algorithm.
    :param device: name of device that shot the video.
    :param filename: name of the file.
    :return: datetime.date object.
    '''
    if device == 'nexus5':
        return parse_date_nexus5(filename)
    else:
        raise exceptions.NotImplementedError('Unknown device: ' + device)


def get_input_files_list(input_dir):
    '''
    Return list of *.mp4 files in directory. Look up is made recursively.
    :param input_dir: Path to the directory.
    :return: list of *.mp4 files.
    '''
    if not os.path.exists(input_dir):
        raise exceptions.IOError('No such directory: ' + input_dir)
    if not os.path.isdir(input_dir):
        raise exceptions.IOError(input_dir + ' is not a directory.')
    result = []
    for entry in os.walk(input_dir):
        result.extend([os.path.join(entry[0], name) for name in entry[2]])
    return [filename for filename in result if filename.endswith('.mp4')]


def parse_command_line_options(opt):
    """
    Parses command line options
    :param opt: sys.argv[1:]
    :return: parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Run video import procedure.',
        epilog='Example:\n\t./import_video --device=nexus5 --input=/raw/path '
               '--raw-output=/path/to/storage --converted-output=/path/to/www',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--device',
                        help='Device that produced video files.',
                        choices=['nexus5', ], default='nexus5',
                        metavar='DEVICE')
    # TODO(weisert): Consider using positional arguments.
    parser.add_argument('-i', '--input',
                        help='Path to the files copied from device.',
                        type=str)
    parser.add_argument('-s', '--raw-output',
                        help='Path to the reliable storage to save raw files.',
                        type=str)
    parser.add_argument('-o', '--converted-output',
                        help='Path to the www folder.',
                        type=str)
    return parser.parse_args(opt)


def main():
    '''
    :return: status code.
    '''
    args = parse_command_line_options(sys.argv[1:])
    files = get_input_files_list(args.input)
    if not files:
        return 0
    jobs = []
    for filename in files:
        date = get_date_for_device(args.device, filename)
        job = create_job_description(filename, date, args.raw_output,
                                     args.converted_output)
        check_job(job)
        jobs.append(job)

    for job in jobs:
        make_job(job, args.device)


if __name__ == '__main__':
    try:
        returncode = main()
    except:
        log.exception('Top level exception.')
        returncode = 1
    sys.exit(returncode)
