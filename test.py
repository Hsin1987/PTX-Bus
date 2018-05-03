import requests
import base64
import hashlib
import hmac
from datetime import datetime

def sha1_hash_base64(string_to_hash, secret):
    #string_to_hash = "x-date: Thu, 03 May 2018 16:07:13 GMT"
    h = hmac.new(secret, (string_to_hash).encode('utf-8'), hashlib.sha1)
    return base64.b64encode(h.digest())


url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeByFrequency/City/Taipei?$format=JSON"
key_id = "37ea2500589b4bfba83109e994fd4828"
secret = b"wBj14ITh9YcoRY4oJlyiSwshfQQ"



msg = "x-date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

sign_hmac = sha1_hash_base64(msg, secret)
# Set the authorization header template
auth_header_template = 'hmac username="{}",algorithm="{}",headers="{}",signature="{}"'
# Set the signature hash algorithm
algorithm = 'hmac-sha1'

headers =  "x-date"
auth_header = auth_header_template.format(key_id, algorithm, headers, sign_hmac.decode("utf-8"))
request_headers = {
            'Authorization': auth_header,
            'Date': msg
            }


print(request_headers)
r = requests.get(url, headers=request_headers)

print ('Response code: %d\n' % r.status_code)
print (r.text)