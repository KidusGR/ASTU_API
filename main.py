from requests_html import HTMLSession
import pandas as pd
import json
import payhead


class Stalker:
    def __init__(self):
        self.session = HTMLSession()
        self.headers = payhead.main_header
        self.baseurl = payhead.baseurl
        self.graphs = payhead.graphs

    def login(self):
        print("--- test ---")
        res = self.session.post(payhead.baseurl, headers=self.headers, json=payhead.login_payload)
        global resHeaders
        resHeaders = res.headers
        print(f"\n{json.loads(res.content)}\n")

    def fetch(self, payload):
        print("--- Fetching ---")
        self.payload = payload
        payload.update({
            'access-token': resHeaders['access-token'],
            'client': resHeaders['client'],
            'uid': resHeaders['uid']
        })
        response = self.session.post(payhead.graphs, headers=self.headers, json=payload)
        print(f"\n{json.loads(response.content)}\n")
