#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


def get_default_binary_path():
    """Auto detect ss binary location"""

    bin_names = ['ss-server', 'ssserver']
    sys.path.append(os.getcwd())
    path_binary = None
    for cmd in bin_names:
        result = subprocess.run(['which', cmd], stdout=subprocess.PIPE)
        if result.returncode == 0:
            path_binary = result.stdout.decode().rstrip()
            print("detected " + cmd + ": " + path_binary)
            break
    return path_binary


def main():
    url_json_default = "https://raw.githubusercontent.com/fzinfz/ssmanager-nopanel/master/servers-example.json"
    # Change to your own url, or pass it from command line by `-u` switch.

    parser = argparse.ArgumentParser(description='ssmanager web daemon',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-b', '--path-binary', default=get_default_binary_path(), nargs='?',
                        help='path for ss binary file')
    parser.add_argument('-a', '--address', default='', nargs='?', help='listening address')
    parser.add_argument('-p', '--port', default='8000', nargs='?', type=int, help='listening port')

    parser.add_argument('-u', '--url-json', default=url_json_default, nargs='?',
                        help='url for ss servers json file, use `-c` for auth')
    parser.add_argument('-c', '--user-password', default=None, nargs='?', help='user:password for url_json')
    parser.add_argument('-t', '--web-hook-token', default='update', nargs='?', help='token to trigger update()')

    parser.add_argument('-d', '--url-db', nargs='?', help='db url for syncing traffic')
    parser.add_argument('-i', '--interval-sync', default=10, nargs='?', help='sync traffic interval(seconds)')
    parser.add_argument('--verbose', '-v', action='count', help="-v: traffic log; -vv: connections also")

    args = parser.parse_args()

    print(args)
    print('visit URI to trigger updating servers: {0}:{1}/{2}'.format(args.address, args.port, args.web_hook_token))

    from ssmanager_nopanel import httpd_native as web
    ws = web.WebServer(**args.__dict__)
    ws.start_server()


if __name__ == '__main__':
    main()
