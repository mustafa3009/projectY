#!/usr/bin/env python

import argparse
import os
import requests

# Disable urllib3 warnings:
# https://github.com/shazow/urllib3/issues/497
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def _assert_health(base_url):
    url = '{}/{}'.format(base_url, 'health')
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    print('{} Health test is passed'.format(url))

def _assert_info(base_url):
    url = '{}/{}'.format(base_url, 'info')
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    print('{} Info test is passed'.format(url))


if __name__ == '__main__':

    # Parse arguments
	parser = argparse.ArgumentParser(
		description='Script for smoke testing the voting app',
	)
	parser.add_argument(
        '-u', '--baseURL',
#        default='localhost',
        help='APP URL including the port (http://<some-host>:/<some-port>',
        required=True,
	)
	args = parser.parse_args()
	
	BASE_URL = args.baseURL	

# Health test
	_assert_health(BASE_URL)

# Info test
	_assert_info(BASE_URL)


	print('')
	print('*' * 75)
	print('Smoke test was successful!')
	print('*' * 75)
