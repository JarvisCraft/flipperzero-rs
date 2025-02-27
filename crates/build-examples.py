#!/usr/bin/env python3
# Helper script for building/installing all examples.

import argparse
import logging
import os
from pathlib import Path, PurePosixPath
from subprocess import run

FLIPPERZERO_FIRMWARE = Path(os.environ.get('FLIPPERZERO_FIRMWARE', '../../flipperzero-firmware'))
PYTHON = 'python'
STORAGE_SCRIPT = FLIPPERZERO_FIRMWARE / 'scripts' / 'storage.py'
INSTALL_PATH = PurePosixPath('/ext/apps/Examples')
EXAMPLES = ["dialog", "gpio", "gui", "hello-rust", "notification"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install', action='store_true', help='Copy built projects to device')

    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(level=logging.INFO)

    for example in EXAMPLES:
        logging.info('Building %s', example)
        run(['cargo', 'build', '--package', 'flipperzero', '--example', example, '--all-features', '--release'], check=True)

        if args.install:
            # Assume that the binary has the name as the 
            binary = Path.cwd() / 'target' / 'thumbv7em-none-eabihf' / 'release' / 'examples' / example
            target = INSTALL_PATH / f'{example}.fap'

            logging.info('Copying %s to %s', binary, target)
            run([PYTHON, STORAGE_SCRIPT, 'send', os.fspath(binary), os.fspath(target)], check=True)


if __name__ == '__main__':
    main()
