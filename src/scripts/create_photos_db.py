#!/usr/bin/env python
'''
Scans all the source directories, collects image information and stores it in MongoDB. 
'''

import os
import yaml
import sys

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(_CURRENT_DIR))
import settings  # pylint: disable=import-error, wrong-import-position

log = settings.get_logger('create_photos_db')  # pylint: disable=invalid-name


def get_config(path):
    ''' Parses configuration file.
    :param path: the path to config.yaml
    :return: dictionary with configuration
    '''
    log.debug('Get configuration from: ' + path)
    assert os.path.exists(path)
    with open(path) as f:
        return yaml.load(f)


def main():
    '''
    :return: status code.
    '''
    config_path = os.path.join(os.path.dirname(_CURRENT_DIR), 'config.yaml')
    config = get_config(config_path)
    print config
    return 0


if __name__ == '__main__':
    try:
        EXIT_CODE = main()
    except Exception:  # pylint: disable=broad-except
        log.exception('Top level exception.')
        EXIT_CODE = 1
    sys.exit(EXIT_CODE)
