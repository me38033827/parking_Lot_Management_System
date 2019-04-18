import json

logs = json.load(open('./log.json', 'rb'))

for i in range(len(logs)):
    temp = {
        "model": "parkManagement.Log",
        "pk": i,
        "fields": logs[i]
    }
    logs[i] = temp

json.dump(logs, open("./logdb.json", 'w'), indent=4, separators=(',', ': '))
