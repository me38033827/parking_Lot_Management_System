import json
import cv2
import numpy as np


def find_near(type, index):
    if type == 'space':
        if 1 < index < 7:
            return 32 + index - 2
        if 6 < index < 13:
            return 42 + index - 7
        if 12 < index < 19:
            return 42 + index - 13 + 100 * (48 + index - 13)
        if 18 < index < 24:
            return 37 + index - 19
        if 23 < index < 30:
            return 48 + index - 24
    elif type == 'enter':
        if index == 30:
            return 32
        else:
            return 41
    elif type == 'exit':
        if index == 32:
            return 37
        else:
            return 36
    elif type == 'first_v':
        temp = index - 2
        if index == 2:
            temp += 100 * 28 + 10000 * 42 + 10**6 * 33
        elif index == 3:
            temp += 100 * 32 + 10000 * 34 + 10**6 * 42
        elif index == 4:
            temp += 100 * 33 + 10000 * 35 + 10**6 * 42
        elif index == 5:
            temp += 100 * 34 + 10000 * 36
        elif index == 6:
            temp += 100 * 35 + 10000 * 48 + 10**6 * 31
        return temp
    elif type == 'second_v':
        temp = index - 2
        if index == 19:
            temp += 100 * 38 + 10000 * 30 + 10 ** 6 * 47
        elif index == 20:
            temp += 100 * 37 + 10000 * 39 + 10 ** 6 * 47
        elif index == 21:
            temp += 100 * 38 + 10000 * 40 + 10 ** 6 * 47
        elif index == 22:
            temp += 100 * 39 + 10000 * 41
        elif index == 23:
            temp += 100 * 40 + 10000 * 53 + 10 ** 6 * 29
        return temp
    elif type == 'first_h':
        temp = index - 2
        if index == 7:
            temp += 100 * 13 + 10000 * 43 + 10 ** 6 * 32 + 10**8 * 33 + 10**10 * 34
        elif 7 < index < 12:
            temp += 100 * (index + 6) + 10000 * (42 + index - 8) + 10 ** 6 * (42 + index - 6)
        elif index == 12:
            temp += 100 * 18 + 10000 * 46 + 10 ** 6 * 37 + 10**8 * 38 + 10**10 * 39
        return temp
    elif type == 'second_h':
        temp = index - 2
        if index == 13:
            temp += 100 * 24 + 10000 * 49 + 10 ** 6 * 36
        elif 13 < index < 18:
            temp += 100 * (index + 11) + 10000 * (48 + index - 14) + 10 ** 6 * (48 + index - 12)
        elif index == 18:
            temp += 100 * 29 + 10000 * 52 + 10 ** 6 * 41
        return temp


if __name__ == '__main__':
    parking_lot = json.load(open('./parking.json', 'rb'))
    print(parking_lot.keys())
    parking_lot_json = []
    count = 0

    tempArray = parking_lot['parking_lot']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for parking_space in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": True,
                "isEnter": False,
                "isExit": False,
                "nearPoint": find_near('space', parking_space[2]),
                "xCoord": parking_space[0],
                "yCoord": parking_space[1]
            }
        })
        count += 1

    tempArray = parking_lot['enter']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for enter in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": True,
                "isExit": False,
                "nearPoint": find_near('enter', enter[2]),
                "xCoord": enter[0],
                "yCoord": enter[1]
            }
        })
        count += 1

    tempArray = parking_lot['exit']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for exit_ in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": False,
                "isExit": True,
                "nearPoint": find_near('exit', exit_[2]),
                "xCoord": exit_[0],
                "yCoord": exit_[1]
            }
        })
        count += 1

    tempArray = parking_lot['first_v']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for r in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": False,
                "isExit": False,
                "nearPoint": find_near('first_v', r[2]),
                "xCoord": r[0],
                "yCoord": r[1]
            }
        })
        count += 1

    tempArray = parking_lot['second_v']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for r in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": False,
                "isExit": False,
                "nearPoint": find_near('second_v', r[2]),
                "xCoord": r[0],
                "yCoord": r[1]
            }
        })
        count += 1

    tempArray = parking_lot['first_h']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for r in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": False,
                "isExit": False,
                "nearPoint": find_near('first_h', r[2]),
                "xCoord": r[0],
                "yCoord": r[1]
            }
        })
        count += 1

    tempArray = parking_lot['second_h']
    tempArray = sorted(tempArray, key=lambda x: x[2])
    for r in tempArray:
        parking_lot_json.append({
            "model": "parkManagement.Parking",
            "pk": count,
            "fields": {
                "isParkingLot": False,
                "isEnter": False,
                "isExit": False,
                "nearPoint": find_near('second_h', r[2]),
                "xCoord": r[0],
                "yCoord": r[1]
            }
        })
        count += 1

    json.dump(parking_lot_json, open('./parkingdb.json', 'w'),
              indent=4, separators=(',', ': '))
