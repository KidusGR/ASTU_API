import main
import payhead
import json

idnumber = "ugr/23346/13"  # input("Enter Your ID: ")
password = "Strong098"  # input("Enter Your Password: ")

pload = {
    'user_name': idnumber,
    'password': password,
}

payhead.login_payload.update(pload)
inst1 = main.Stalker()
inst1.login()

print("--- fetching ---\n")
for pload in payhead.fetch_payloads:
    data = inst1.fetch(pload)
    file_name = str(list(data['data'].keys())[0])
    with open(f"data/{file_name}.json", "w") as file:
        file.write(json.dumps(data))
        file.close()


semesters = []
courses = []
with open(f"data/studentAcademicYearSemesters.json") as json_file:
    sem_data = json.load(json_file)
    for ids in sem_data['data']["studentAcademicYearSemesters"]:
        try:
            semesters.append(ids['id'])
        except:
            pass
    json_file.close()
with open(f"data/studentCourseEnrollments.json") as course_json:
    cor_data = json.load(course_json)
    for ids in cor_data['data']['studentCourseEnrollments']:
        try:
            courses.append(ids['id'])
        except:
            pass
    course_json.close()

print(semesters)
print(courses)
