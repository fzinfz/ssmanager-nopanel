#!/usr/bin/env python3

import argparse
import native as web
import os,sys
import subprocess

def main():

    # change to your own url, or pass it from command line by `-u` switch
    url_json_default = "https://raw.githubusercontent.com/fzinfz/ssmanager-nopanel/master/servers.json"

    # Auto detect ss binary location
    bin_names = ['ss-server','ssserver']  # TODO: ss-server libev version can't work yet
    sys.path.append(os.getcwd())
    for cmd in bin_names:
        result = subprocess.run(['which', cmd], stdout=subprocess.PIPE)
        if result.returncode == 0:
            path_binary = result.stdout.decode().rstrip()
            break
    if not 'path_binary' in locals():
        path_binary = None

    # args parse
    parser = argparse.ArgumentParser(description='ssmanager web daemon', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a','--address',default='', nargs='?', help='listening address')
    parser.add_argument('-p','--port',default='8000', nargs='?', help='listening port')
    parser.add_argument('-t','--web-hook-token',default='update', nargs='?', help='token to trigger update()')
    parser.add_argument('-u','--url-json', default=url_json_default, help='url for ss servers json file')
    parser.add_argument('-b','--path-binary', default=path_binary, help='path for ss binary file')
    args = parser.parse_args()

    # start web server
    print('ss location: ' + args.path_binary)
    print('get json file from: ' + args.url_json)
    print('visit URI to trigger updating servers: {0}:{1}/{2}'.format(args.address, args.port, args.web_hook_token))
    web.start_web_server(args.address, int(args.port), args.web_hook_token, args.url_json, args.path_binary)


if __name__ == '__main__':
    main()
