from requests_html import HTMLSession
import json
import os

baseurl = "https://estudent.astu.edu.et/api/auth/sign_in"
graphs = "https://estudent.astu.edu.et/api//graphql"


class Stalker:
    def __init__(self):
        self.session = HTMLSession()
        self.pdata = json.load(open('payhead.json'))
        self.headers = self.pdata['main_header']
        self.baseurl = baseurl
        self.graphs = graphs

    def login(self, username, password):
        self.pdata['login_payload']['user_name'] = username
        self.pdata['login_payload']['password'] = password
        res = self.session.post(baseurl, headers=self.headers, json=self.pdata['login_payload'])
        self.pdata.update({
            "resHeaders": res.headers
        })
        print(f"{json.loads(res.content)}")
        try:
            self.pdata.update({
                "folder_name": str(json.loads(res.content)['data']['user_name']).replace("/", "_")
            })
            os.mkdir('data')
            os.mkdir(f"data/{self.pdata['folder_name']}")
            os.mkdir(f"data/{self.pdata['folder_name']}/info")
            data = json.loads(res.content)
            with open(f"data/{self.pdata['folder_name']}/info/Login_info.json", "w") as login_file:
                login_file.write(json.dumps(data))
        except:
            pass

        return

    def fetch(self):
        
        try:
            with open(f"data/{self.pdata['folder_name']}/info/Login_info.json") as log_file:
                log_info = json.load(log_file)
                log_file.close()
        except:
            log_info = {None: None}
        if str(list(log_info.keys())[0]) == 'data':

            payload = self.pdata['fetch_payloads']
            for pload in payload:
                pload.update({
                    'access-token': self.pdata["resHeaders"]['access-token'],
                    'client': self.pdata["resHeaders"]['client'],
                    'uid': self.pdata["resHeaders"]['uid']
                })

                if pload['operationName'] == "gradeReport":
                    sems = []
                    with open(f"data/{self.pdata['folder_name']}/info/studentAcademicYearSemesters.json") as sem_file:
                        infos = json.load(sem_file)
                        for info in infos['data']["studentAcademicYearSemesters"]:
                            pload['variables']['id'] = f"{info['id']}"
                            res = self.session.post(graphs, headers=self.headers, json=pload)
                            sems.append(json.loads(res.content))
                        sem_file.close()
                    data = json.loads(res.content)
                    file_name = str(list(data['data'].keys())[0])
                    data = sems

                elif pload['operationName'] == "assessmentResultForEnrollment":
                    cors = []
                    with open(f"data/{self.pdata['folder_name']}/info/studentCourseEnrollments.json") as ass_file:
                        infos = json.load(ass_file)
                        for info in infos['data']['studentCourseEnrollments']:
                            pload['variables']['id'] = f"{info['id']}"
                            res = self.session.post(graphs, headers=self.headers, json=pload)
                            cors.append(json.loads(res.content))
                        ass_file.close()
                    data = json.loads(res.content)
                    file_name = str(list(data['data'].keys())[0])
                    data = cors

                else:
                    res = self.session.post(graphs, headers=self.headers, json=pload)
                    data = json.loads(res.content)
                    if b'"data":null,' in res.content:
                        continue
                    else:
                        file_name = str(list(data['data'].keys())[0])

                if file_name == "getPerson":
                    pic_name = f"{data['data']['getPerson']['firstName']}_{data['data']['getPerson']['fatherName']}_{data['data']['getPerson']['grandFatherName']}"
                    image = self.session.get(
                        f"https://estudent.astu.edu.et{data['data']['getPerson']['photoUrl']}",
                        headers=self.headers
                    )
                    with open(f"data/{self.pdata['folder_name']}/info/{pic_name}.jpeg", "wb") as pic:
                        pic.write(image.content)
                        pic.close()

                with open(f"data/{self.pdata['folder_name']}/info/{file_name}.json", "w") as file:
                    file.write(json.dumps(data))
                    file.close()

        return
