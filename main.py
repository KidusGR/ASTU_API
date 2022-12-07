from requests_html import HTMLSession
import pandas as pd
import json
import payhead
import os

class Stalker:
    def __init__(self):
        self.session = HTMLSession()
        self.headers = payhead.main_header
        self.baseurl = payhead.baseurl
        self.graphs = payhead.graphs

    def login(self):
        print("--- Logging in ---")
        res = self.session.post(payhead.baseurl, headers=self.headers, json=payhead.login_payload)
        global resHeaders
        resHeaders = res.headers
        data = json.loads(res.content)
        global folder_name
        folder_name = str(data['data']['user_name']).replace("/", "_")
        print(f"{data}\n")

    def fetch(self, payload):
        self.payload = payload
        payload.update({
            'access-token': resHeaders['access-token'],
            'client': resHeaders['client'],
            'uid': resHeaders['uid']
        })
        response = self.session.post(payhead.graphs, headers=self.headers, json=payload)
        return json.loads(response.content)

    def asses(self, courseID):
        print("--- Loading ---")
        self.courseID = courseID
        assPload = payhead.assessment
        assPload.update({
            'access-token': resHeaders['access-token'],
            'client': resHeaders['client'],
            'uid': resHeaders['uid']
        })
        assPload['variables']['id'] = f"{courseID}"
        assessmentRes = self.session.post(payhead.graphs, headers=self.headers, json=assPload)
        print(f"\n{json.loads(assessmentRes.content)}\n")
    def grade(self, semesterID):
        print("--- Loading ---")
        self.semesterID = semesterID
        semPload = payhead.gradeReport
        semPload.update({
            'access-token': resHeaders['access-token'],
            'client': resHeaders['client'],
            'uid': resHeaders['uid']
        })
        semPload['variables']['id'] = f"{semesterID}"
        semesterRes = self.session.post(payhead.graphs, headers=self.headers, json=semPload)
        print(f"\n{json.loads(semesterRes.content)}\n")
