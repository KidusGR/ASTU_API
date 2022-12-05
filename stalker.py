import requests
import json
from bs4 import BeautifulSoup
from lxml import html
import urllib
import os
import pprint

'''user = input("Enter your user name: ")
passw = input("ENter your password: ")'''

headers2 = {}
headers1 = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

payload = {
    'user_name': 'ugr/23346/13',
    'password': 'Strong098',
}

payload2 = {
    'operationName': "assessmentResultForEnrollment",
    'query': "query assessmentResultForEnrollment($id: ID!) {\n  assessmentResultForEnrollment(id: $id) {\n    id\n    instructorName\n    sumOfMaximumMark\n    sumOfResults\n    course {\n      id\n      courseTitle\n      courseCode\n      __typename\n    }\n    studentGrade {\n      id\n      letterGrade\n      __typename\n    }\n    assessmentResults {\n      id\n      result\n      assessment {\n        id\n        assessmentName\n        maximumMark\n        assessmentType\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    'variables': {'id': "904628"}
}

payload3 = {
    'operationName': None,
    'query': "{\n  headerProfile {\n    id\n    idNumber\n    classYear\n    dormitoryView\n    section\n    program {\n      id\n      name\n      __typename\n    }\n    applicant {\n      id\n      person {\n        id\n        photoUrl\n        fullName\n        __typename\n      }\n      admissionYear\n      admission {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    'variables': {}
}


with requests.Session() as s:
    res = s.post('https://estudent.astu.edu.et/api/auth/sign_in', json=payload, headers=headers1)
    # print(f"{json.loads(res.content)}\n{res.status_code}\n")
    s_main = s.get('https://estudent.astu.edu.et/student_profile', headers=headers1)
    # print(f"{s_main.status_code}\n{s_main.content}\n")
    login_headers = res.headers
    tree = html.fromstring(html=s_main.content)
    main_html = BeautifulSoup(s_main.content, 'html.parser')
    payload3.update({
        'access-token': login_headers['access-token'],
        'client': login_headers['client'],
        # 'expiry': login_headers['expiry'],
        'uid': login_headers['uid']
    })

    # graphs = s.post('https://estudent.astu.edu.et/api//graphql', headers=headers1, json=payload2)
    # print(f"{json.loads(graphs.content)}\n\nStatus Code {graphs.status_code}\n")
    # data = json.loads(graphs.content)

    image = s.post('https://estudent.astu.edu.et/api//graphql', headers=headers1, json=payload3)
    image_dict = json.loads(image.content)
    pprint.pprint(image_dict)
    image_url = image_dict['data']['headerProfile']['applicant']['person']['photoUrl']
    name = image_dict['data']['headerProfile']['applicant']['person']['fullName']
    get_image = s.get(f'https://estudent.astu.edu.et{image_url}', headers=headers1)
    with open(f"{name}.jpeg", "wb") as file:
        file.write(get_image.content)
