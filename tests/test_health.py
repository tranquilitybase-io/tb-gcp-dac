import requests
import json
import os

def test_health():

    GCP_DAC_URL=os.environ['GCP_DAC_URL']
    url = f"{GCP_DAC_URL}/api/health"

    resp = requests.get(url) 
    resp_json = resp.json()
    # Validate Response
    assert resp.status_code == 200
    assert resp_json['status'] == 'Healthy'
