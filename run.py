import main
import payhead
import json
import os

idnumber = "ugr/23346/13"  # input("Enter Your ID: ")
password = "Strong098"  # input("Enter Your Password: ")

pload = {
    'user_name': idnumber,
    'password': password,
}

payhead.login_payload.update(pload)
inst1 = main.Stalker()
data = inst1.login()


print("--- fetching ---\n")
for pload in payhead.fetch_payloads:
    data = inst1.fetch(pload)

# tests

print(inst1.get_ids())

