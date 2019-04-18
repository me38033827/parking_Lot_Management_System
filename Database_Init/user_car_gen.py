import binascii
import hashlib
import json

phone_numbers = [5823447919,
                 7748187599,
                 9298687511,
                 8047290211,
                 4124343018,
                 3708700556,
                 2506857347,
                 3504513683,
                 8438722004,
                 4292759106]

email = [(str(phone_numbers[i]) + "@gmail.com") for i in range(9)]
email.append("jzynoter@gmail.com")

users = []
for i in range(10):
    user = {'model': "parkManagement.User", 'pk': i, 'fields': {}}
    user['fields']['phoneNumber'] = phone_numbers[i]
    user['fields']['xCoord'] = 0
    user['fields']['yCoord'] = 0
    user['fields']['password'] = hashlib.sha256(str(phone_numbers[i]).encode()).hexdigest()
    user['fields']['email'] = email[i]
    users.append(user)

json.dump(users, open('./userdb.json', 'w'),
          indent=4, separators=(',', ': '))

admin_phone = 2974556594
admin = [{
    "model": "parkManagement.Admin",
    "pk": 0,
    "fields": {
        "phoneNumber": admin_phone,
        "password": hashlib.sha256(str(admin_phone).encode()).hexdigest()
    }
}]
json.dump(admin, open('./admindb.json', 'w'),
          indent=4, separators=(',', ': '))

cars = []
plateNumbers = ["558AKV", "975AMF", "266AGJ", "899AFK", "644AJT", "144AAR ", "975APR", "910ANP", "298AHU", "584ARY"]
parkingPos = json.load(open("./parkingdb.json"))

for i in range(10):
    car = {
        "model": "parkManagement.Car",
        "pk": plateNumbers[i],
        "fk": i,
        "fields": {
            "xCoord": parkingPos[i]['fields']['xCoord'],
            "yCoord": parkingPos[i]['fields']['yCoord'],
            "rot": 0 if i < 5 else 90,
            "owner_id": i
        }
    }
    cars.append(car)

json.dump(cars, open('./cardb.json', 'w'),
          indent=4, separators=(',', ': '))
