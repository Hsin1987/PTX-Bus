import hmac
import hashlib
import base64
import requests
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

key_id = "37ea2500589b4bfba83109e994fd4828"
secret = b"wBj14ITh9YcoRY4oJlyiSwshfQQ"


class header_generator():

    def create_date_header(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def create_auth_header(self, key_id, sign_hmac):
        # Set the authorization header template
        auth_header_template = 'hmac username="{}", algorithm="{}", headers="{}", signature="{}"'
        # Set the signature hash algorithm
        algorithm = 'hmac-sha1'
        headers = "x-date"
        auth_header = auth_header_template.format(key_id, algorithm, headers, sign_hmac.decode("utf-8"))
        return auth_header

    def sha1_hash_base64(self, string_to_hash, secret):
        h = hmac.new(secret, (string_to_hash).encode('utf-8'), hashlib.sha1)
        return base64.b64encode(h.digest())


class xml2DataFrame():
    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self):
        return [self.parse_element(child) for child in iter(self.root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)

        if element.text:
            parsed[element.tag] = element.text

        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root()
        return pd.DataFrame(structure_data)

def df2sqlite(dataframe, db_name, tbl_name):
# Reference:http://yznotes.com/write-pandas-dataframe-to-sqlite/
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    wildcards = ','.join(['?'] * len(dataframe.columns))
    data = [tuple(x) for x in dataframe.values]

    cur.execute("drop table if exists %s" % tbl_name)

    col_str = '"' + '","'.join(dataframe.columns) + '"'
    cur.execute("create table %s (%s)" % (tbl_name, col_str))

    cur.executemany("insert into %s values(%s)" % (tbl_name, wildcards), data)

    conn.commit()
    conn.close()


# Laterly Need a URI generator
request_uri = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei?$format=XML"

header_gen = header_generator()
msg = header_gen.create_date_header()
sign_hmac = header_gen.sha1_hash_base64("x-date: " + msg, secret)
auth_header = header_gen.create_auth_header(key_id, sign_hmac)
date_header = header_gen.create_date_header()

request_headers = {
            'Authorization': auth_header,
            'x-date': date_header
            }

xml_data = requests.get(request_uri, headers=request_headers)
print('Response code: %d\n' % xml_data.status_code)

# Step 1. Query all the bus line from XML and save it into a sqlite DB.
xml2df = xml2DataFrame(xml_data.content)
xml_dataframe = xml2df.process_data()
df2sqlite(xml_dataframe, "bus_routes.sqlite", "Taipei")
xml_dataframe.to_csv("routes.csv", sep='\t', encoding='utf-8')
# Step 2. Download All the