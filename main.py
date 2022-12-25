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
        global resHeaders
        global folder_name
        resHeaders = res.headers
        print(f"{json.loads(res.content)}")
        try:
            folder_name = str(json.loads(res.content)['data']['user_name']).replace("/", "_")
            os.mkdir('data')
            os.mkdir(f"data/{folder_name}")
            os.mkdir(f"data/{folder_name}/info")
            data = json.loads(res.content)
            with open(f"data/{folder_name}/info/Login_info.json", "w") as login_file:
                login_file.write(json.dumps(data))
        except:
            pass

        return

    def fetch(self):
        semesters = []
        courses = []

        def grade():
            semesters = []
            semPload = self.pdata["gradeReport"]
            semPload.update({
                'access-token': resHeaders['access-token'],
                'client': resHeaders['client'],
                'uid': resHeaders['uid']
            })
            with open(f"data/{folder_name}/info/semesters.json") as sem_file:
                infos = json.load(sem_file)
                for info in infos:
                    semPload['variables']['id'] = f"{info['id']}"
                    semesterRes = self.session.post(graphs, headers=self.headers, json=semPload)
                    semesters.append(json.loads(semesterRes.content))
                sem_file.close()
            with open(f"data/{folder_name}/info/semesters_info.json", "w") as grade_info:
                grade_info.write(json.dumps(semesters))
                grade_info.close()

        def asses():
            courses = []
            assPload = self.pdata["assessment"]
            assPload.update({
                'access-token': resHeaders['access-token'],
                'client': resHeaders['client'],
                'uid': resHeaders['uid']
            })
            with open(f"data/{folder_name}/info/courses.json") as ass_file:
                infos = json.load(ass_file)
                for info in infos:
                    assPload['variables']['id'] = f"{info['id']}"
                    assessmentRes = self.session.post(graphs, headers=self.headers, json=assPload)
                    courses.append(json.loads(assessmentRes.content))
                ass_file.close()
            with open(f"data/{folder_name}/info/courses_info.json", "w") as cor_info:
                cor_info.write(json.dumps(courses))
                cor_info.close()

        try:
            with open(f"data/{folder_name}/info/Login_info.json") as log_file:
                log_info = json.load(log_file)
                log_file.close()
        except:
            log_info = {None: None}
        if str(list(log_info.keys())[0]) == 'data':

            payload = self.pdata['fetch_payloads']
            for pload in payload:
                pload.update({
                    'access-token': resHeaders['access-token'],
                    'client': resHeaders['client'],
                    'uid': resHeaders['uid']
                })
                res = self.session.post(graphs, headers=self.headers, json=pload)
                data = json.loads(res.content)
                file_name = str(list(data['data'].keys())[0])

                if file_name == "getPerson":
                    pic_name = f"{data['data']['getPerson']['firstName']}_{data['data']['getPerson']['fatherName']}_{data['data']['getPerson']['grandFatherName']}"
                    image = self.session.get(
                        f"https://estudent.astu.edu.et{data['data']['getPerson']['photoUrl']}",
                        headers=self.headers
                    )
                    with open(f"data/{folder_name}/info/{pic_name}.jpeg", "wb") as pic:
                        pic.write(image.content)
                        pic.close()

                elif file_name == "studentAcademicYearSemesters":
                    for ids in data['data']["studentAcademicYearSemesters"]:
                        try:
                            sem = {}
                            sem.update({
                                'id': ids['id'],
                                'semesterName': ids['semesterName']
                            })
                            semesters.append(sem)
                        except:
                            pass
                    with open(f"data/{folder_name}/info/semesters.json", "w") as sem_file:
                        sem_file.write(json.dumps(semesters))
                        sem_file.close()

                elif file_name == "studentCourseEnrollments":
                    for ids in data['data']['studentCourseEnrollments']:
                        try:
                            cor = {}
                            cor.update({
                                'id': ids['id'],
                                'titleAndCode': ids['course']['titleAndCode']
                            })
                            courses.append(cor)
                        except:
                            pass
                    with open(f"data/{folder_name}/info/courses.json", "w") as cor_file:
                        cor_file.write(json.dumps(courses))
                        cor_file.close()

                with open(f"data/{folder_name}/info/{file_name}.json", "w") as file:
                    file.write(json.dumps(data))
                    file.close()


            grade()
            asses()
        return
