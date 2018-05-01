from kong_hmac import generate_request_headers
import requests


url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeByFrequency/City/Taipei?$format=JSON"
key_id = "b30cc9bf581d48e6bf2cf9cc10d0aa19"
secret = b"JXU_hVy_NpApRP2VPMwqSAqLV7s"


get_request_headers = generate_request_headers(key_id, secret, url)
r = requests.get(url, headers=get_request_headers)
print ('Response code: %d\n' % r.status_code)
print (r.text)