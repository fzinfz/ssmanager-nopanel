#!/usr/bin/env python3

import argparse
import native as web
import os

def main():

    url_json = os.environ.get('URL_JSON')
    ss_bin = os.environ.get('SS_BIN','/usr/bin/ss-server')

    parser = argparse.ArgumentParser(description='ssmanager web daemon', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a','--address',default='', nargs='?', help='listening address')
    parser.add_argument('-p','--port',default='8000', nargs='?', help='listening port')
    parser.add_argument('-t','--web-hook-token',default='update', nargs='?', help='token to trigger update()')
    args = parser.parse_args()

    print('URI for updating config: {0}:{1}/{2}'.format(args.address, args.port, args.web_hook_token))
    web.start_web_server(args.address, int(args.port), args.web_hook_token, url_json, ss_bin)


if __name__ == '__main__':
    main()
