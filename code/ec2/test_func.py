#!/usr/bin/env python

import argparse
import os
import requests

# Disable urllib3 warnings:
# https://github.com/shazow/urllib3/issues/497
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def _assert_vote(base_url, candidate):
	url = '{}/votes'.format(base_url)
	r = requests.post(url=url, json={'candidate': candidate})
	assert r.status_code == 201, r.text
	print('Vote for {} POSTed successfully'.format(candidate))

def _assert_simulation(base_url):
    url = '{}/simulation'.format(base_url)
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    print('/simulation test successful')
    
def _assert_candidates(base_url):
    url = '{}/candidates'.format(base_url)
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    resp_json = r.json()
    assert 'candidates' in resp_json, 'candidates not in json: {}'.format(resp_json)
#     assert resp_json['candidates'] == expected_message, r.text
    print('/candidates test successful')
    
def _assert_resultvotes(base_url):
    url = '{}/results/votes'.format(base_url)
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    resp_json = r.json()
    assert 'votes' in resp_json, 'votes not in json: {}'.format(resp_json)
#     assert resp_json['candidates'] == expected_message, r.text
    print('/results/votes test successful')

def _assert_winners(base_url):
    url = '{}/winners'.format(base_url)
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    resp_json = r.json()
    assert 'results' in resp_json, 'results not in json: {}'.format(resp_json)
#     assert resp_json['candidates'] == expected_message, r.text
    print('/winners test successful')

def _assert_winnervotes(base_url):
    url = '{}/winners/votes'.format(base_url)
    r = requests.get(url=url)
    assert r.status_code == 200, r.text
    resp_json = r.json()
    assert 'votes' in resp_json, 'votes not in json: {}'.format(resp_json)
#     assert resp_json['candidates'] == expected_message, r.text
    print('/winners/votes test successful')


if __name__ == '__main__':

    # Parse arguments
	parser = argparse.ArgumentParser(
		description='Script for functional testing the voting app',
	)
	parser.add_argument(
        '-u', '--baseURL',
#        default='localhost',
        help='APP URL including the port (http://<some-host>:/<some-port>',
        required=True,
	)
	args = parser.parse_args()
	
	BASE_URL = args.baseURL	

# Test Add a vote
	_assert_vote(
		base_url=BASE_URL,
		candidate='Jill Stein')


# Test Simulation
	_assert_simulation (
		base_url=BASE_URL)

# Test Candidates
	_assert_candidates(
		base_url=BASE_URL)
		
# Test Result votes
	_assert_resultvotes(
		base_url=BASE_URL)

# Test Winners		
	_assert_winners(
		base_url=BASE_URL)
		
# Test Winner votes
	_assert_winnervotes(
		base_url=BASE_URL)
	
	print('')
	print('*' * 75)
	print('Functional tests were successful!')
	print('*' * 75)
