# edited script to run with two arguments in cmd
# arguments should be passed 

import os
import requests
from json import loads
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="Input file list")
ap.add_argument("-o", "--order", required=True,
	help="Order name")
ap.add_argument("-p", "--processor", required=True,
	help="Processor: coh, card_bs, sen2cor or download")
ap.add_argument("-b", "--baseline", required=False,
	help="Temporal baseline for coherence", default=6)
args = vars(ap.parse_args())

creodias_user='{CREODIAS_ID}'
creodias_password='{CREODIAS_PW}'

input_data = {'order_name': 'Sen2cor_newTest',
        'priority': 1,
        'identifier_list': open('S2-L2_test_190710.txt').read().split('\n'),
        'processor': 'sen2cor-dev'
        }

def get_keycloak_token():
    h = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    d = {
        'client_id': 'CLOUDFERRO_PUBLIC',
        'password': creodias_password,
        'username': creodias_user,
        'grant_type': 'password'
    }
    resp = requests.post('https://auth.creodias.eu/auth/realms/dias/protocol/openid-connect/token', data=d, headers=h)
    return loads(resp.content.decode('utf-8'))['access_token']


headers = {'content-type': 'application/json', 'accept': 'application/json', 'Keycloak-Token': get_keycloak_token()}
session = requests.Session()
query = f'''https://finder.creodias.eu/api/order/'''
response = session.post(query, json=input_data, headers=headers)
response.close()
print(response.status_code)
print(response.text)
