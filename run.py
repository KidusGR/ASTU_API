import main
import payhead

idnumber = "ugr/23346/13"  # input("Enter Your ID: ")
password = "Strong098"  # input("Enter Your Password: ")

pload = {
    'user_name': idnumber,
    'password': password,
}

payhead.login_payload.update(pload)

inst1 = main.Stalker()
inst1.login()

inst1.asses("805627")
