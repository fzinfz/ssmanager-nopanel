#!/usr/bin/env python3

import argparse
import native as web
import os,sys
import subprocess

def main():

    bin_names = ['ss-server','ssserver']
    sys.path.append(os.getcwd())
    for cmd in bin_names:
        result = subprocess.run(['which', cmd], stdout=subprocess.PIPE)
        if result.returncode == 0:
            path_binary = result.stdout.decode().rstrip()
            break
    if not 'path_binary' in locals():
        path_binary = None

    parser = argparse.ArgumentParser(description='ssmanager web daemon', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a','--address',default='', nargs='?', help='listening address')
    parser.add_argument('-p','--port',default='8000', nargs='?', help='listening port')
    parser.add_argument('-t','--web-hook-token',default='update', nargs='?', help='token to trigger update()')
    parser.add_argument('-u','--url-json', default='http://127.0.0.1/ss_servers.json', help='url for ss servers json file')
    parser.add_argument('-b','--path-binary', default=path_binary, help='path for ss binary file')
    args = parser.parse_args()

    print('ss location: ' + args.path_binary)
    print('get json file from: ' + args.url_json)
    print('visit URI to update servers: {0}:{1}/{2}'.format(args.address, args.port, args.web_hook_token))
    web.start_web_server(args.address, int(args.port), args.web_hook_token, args.url_json, args.path_binary)


if __name__ == '__main__':
    main()
