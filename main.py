from requests_html import HTMLSession
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
        res = self.session.post(payhead.baseurl, headers=self.headers, json=payhead.login_payload)
        global resHeaders
        global folder_name
        resHeaders = res.headers
        try:
            folder_name = str(json.loads(res.content)['data']['user_name']).replace("/", "_")
            os.mkdir('data')
            os.mkdir(f"data/{folder_name}")
            os.mkdir(f"data/{folder_name}/info")
        except:
            pass
        return json.loads(res.content)

    def fetch(self):
        def get_ids():
            semesters = []
            courses = []
            with open(f"data/{folder_name}/info/studentAcademicYearSemesters.json") as json_file:
                sem_data = json.load(json_file)
                for ids in sem_data['data']["studentAcademicYearSemesters"]:
                    try:
                        sem = {}
                        sem.update({
                            'id': ids['id'],
                            'semesterName': ids['semesterName']
                        })
                        semesters.append(sem)
                    except:
                        pass
                with open(f"data/{folder_name}/info/semesters_info.json", "w") as sem_file:
                    sem_file.write(json.dumps(semesters))
                    sem_file.close()
                json_file.close()
            with open(f"data/{folder_name}/info/studentCourseEnrollments.json") as course_json:
                cor_data = json.load(course_json)
                for ids in cor_data['data']['studentCourseEnrollments']:
                    try:
                        cor = {}
                        cor.update({
                            'id': ids['id'],
                            'titleAndCode': ids['course']['titleAndCode']
                        })
                        courses.append(cor)
                    except:
                        pass
                with open(f"data/{folder_name}/info/courses_info.json", "w") as cor_file:
                    cor_file.write(json.dumps(courses))
                    cor_file.close()
                course_json.close()

            return
        
        if str(list(self.login().keys())[0]) == 'data':

            payload = payhead.fetch_payloads
            for pload in payload:
                pload.update({
                    'access-token': resHeaders['access-token'],
                    'client': resHeaders['client'],
                    'uid': resHeaders['uid']
                })
                res = self.session.post(payhead.graphs, headers=self.headers, json=pload)
                data = json.loads(res.content)
                file_name = str(list(data['data'].keys())[0])
                with open(f"data/{folder_name}/info/{file_name}.json", "w") as file:
                    file.write(json.dumps(data))
                    file.close()
            get_ids()
        return


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
