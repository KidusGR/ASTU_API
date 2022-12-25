import main

idnumber = "ugr/23346/13"  # input("Enter Your ID: ")
password = "Strong098"  # input("Enter Your Password: ")

inst1 = main.Stalker()
inst1.login(idnumber, password)

print("--- fetching ---\n")

# tests

inst1.fetch()
