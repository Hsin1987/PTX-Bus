import requests
import base64
import hashlib
import hmac
from datetime import datetime, time
from time import mktime
from wsgiref.handlers import format_date_time
import calendar


def create_date_header():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)

"""
def create_date_header():
    # EXAMPLE x-date: Mon, 07 May 2018 13:07:30 GMT
    msg = "x-date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    return msg
"""

def create_auth_header(key_id, sign_hmac):
    # EXAMPLE: Authorization: hmac username="37ea2500589b4bfba83109e994fd4828", algorithm="hmac-sha1", headers="x-date", signature="Ad4SEp0OoFf2c594ew71bqNhIWI="

    # Set the authorization header template
    auth_header_template = 'hmac username="{}", algorithm="{}", headers="{}", signature="{}"'
    # Set the signature hash algorithm
    algorithm = 'hmac-sha1'
    headers = "x-date"

    auth_header = auth_header_template.format(key_id, algorithm, headers, sign_hmac.decode("utf-8"))
    return auth_header


def sha1_hash_base64(string_to_hash, secret):
    h = hmac.new(secret, (string_to_hash).encode('utf-8'), hashlib.sha1)
    return base64.b64encode(h.digest())


url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeByFrequency/City/Taipei?$format=JSON"
key_id = "37ea2500589b4bfba83109e994fd4828"
secret = b"wBj14ITh9YcoRY4oJlyiSwshfQQ"

msg = create_date_header()
sign_hmac = sha1_hash_base64("x-date: "+ msg, secret)
auth_header = create_auth_header(key_id, sign_hmac)
date_header = create_date_header()
print(auth_header)
print(date_header)

request_headers = {
            'Authorization': auth_header,
            'x-date': date_header
            }

print(request_headers)

r = requests.get(url, headers=request_headers)
print('Response code: %d\n' % r.status_code)
print(r.text)


# Step 1. Query all the bus line.

# Step 2. Download All the