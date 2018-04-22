import requests
import hashlib
import hmac
import base64
from datetime import datetime


#url = 'http://graph.facebook.com/v2.3/123435'
url = "http://ptx.transportdata.tw/MOTC/v2/Rail/TRA/Station?$top=10&$format=JSON"
id = "b30cc9bf581d48e6bf2cf9cc10d0aa19"
key = b"JXU_hVy_NpApRP2VPMwqSAqLV7s"

msg = "x-date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
msg_byte = msg.encode()
m = hmac.new(key, msg_byte, hashlib.sha1)
signature = base64.b64encode(m.digest())

headers = {
    'hmac username': id,
    'algorithm': "hmac-sha1",
    "headers": "x-date",
    'signature': signature
}


ret = requests.get(url, headers=headers)
# Error code 401 : Unauthorized
print(ret.status_code)
print(ret)
