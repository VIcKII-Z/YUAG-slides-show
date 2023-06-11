#!/usr/bin/env python

from sys import argv, exit, stderr
from midterm import app
import argparse

def main():
    parser = argparse.ArgumentParser(description='An object slideshow application.')
    parser.add_argument('port', type=int, help='the port at which the server should listen')
    args = parser.parse_args()

    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[1])
    except Exception:
        print('Port must be an integer.', file=stderr)
        exit(1)

    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=stderr)
        exit(1)

if __name__ == '__main__':
    main()
