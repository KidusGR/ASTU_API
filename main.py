from requests_html import HTMLSession
import pandas as pd
import json
import payhead


class Stalker:
    def __init__(self):
        self.session = HTMLSession()
        self.headers = payhead.main_header

    def login(self):
        print("--- test ---")
        res = self.session.post(payhead.baseurl, headers=self.headers, json=payhead.login_payload)
        resHeaders = res.headers
        payhead.yearSemesters.update({
            'access-token': resHeaders['access-token'],
            'client': resHeaders['client'],
            'uid': resHeaders['uid']
        })
        print(json.loads(res.content))
        test = self.session.post(payhead.graphs, headers=self.headers, json=payhead.yearSemesters)
        print(json.loads(test.content))
