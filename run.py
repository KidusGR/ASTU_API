import main

idnumber = input("Enter Your ID: ")
password = input("Enter Your Password: ")

inst1 = main.Stalker()
inst1.login(idnumber, password)

inst1.fetch()
