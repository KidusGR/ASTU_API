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

for pload in payhead.fetch_payloads:
    data = inst1.fetch(pload)
    file_name = str(list(data['data'].keys())[0])
    with open(f"{file_name}.json", "w") as file:
        file.write(json.dumps(data))



'''inst1.asses("805627")
inst1.grade("36")'''

