import requests, json, time, hashlib
import hmac
import base64
from datetime import datetime


def sign(key, msg):
    new_hmac = hmac.new(key, msg.encode('utf-8'), hashlib.sha1)
    signature_base64 = base64.b64encode(new_hmac.digest())
    return signature_base64


"""
    Generates the REST API headers used to authenticate requests:
    HMAC機制：以HMAC簽章驗證使用者的身份，用戶在請求API服務時，將APP Key 與當下時間(格式請使用GMT時間)
    做 HMAC-SHA1 運算後轉成 Base64 格式，帶入 signature屬性欄位，服務器端將驗證用戶請求時的header欄位(詳如第四點)，
    驗證使用者的身份及請求服務的時效性。
"""


url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeByFrequency/City/Taipei?$format=JSON"
id = "b30cc9bf581d48e6bf2cf9cc10d0aa19"
key = b"JXU_hVy_NpApRP2VPMwqSAqLV7s"

if __name__ == '__main__':

    msg = "x-date: " + datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    sign_hmac = sign(key, msg)

    headers = {
        'hmac username': id,
        'algorithm': "hmac-sha1",
        "headers": "x-date",
        'signature': sign_hmac
    }


    ret = requests.get(url, headers=headers)
    # Error code 401 : Unauthorized
    print(ret.status_code)
    print(ret)
