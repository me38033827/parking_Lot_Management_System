import json
from datetime import date,time,datetime,timedelta
import random
from django.core.serializers.json import DjangoJSONEncoder

logJson=[]

cars = json.load(open('./cardb.json', 'r'))
carsId=[car['pk'] for car in cars ]


# history log
for i in range(400):
    year=random.randint(2017,2019)

    if year==2019:
        month=random.randint(1,2)
    else:
        month=random.randint(1,12)

    if month in [1,3,5,7,8,10,12]:
        day=random.randint(1,31)
    elif month in [4,6,9,11]:
        day=random.randint(1,30)
    else:
        day=random.randint(1,28)

    startHour=random.randint(6,22)
    startMinute=random.randint(0,59)
    startSecond=random.randint(0,59)

    parkHour=random.randint(0,8)
    parkMinute=random.randint(0,59)
    parkSecond=random.randint(0,59)

    startDatetime=datetime(year,month,day,startHour,startMinute,startSecond)
    parkTime=timedelta(hours=parkHour,minutes=parkMinute,seconds=parkSecond)

    carId=carsId[random.randint(0,9)]

    logJson.append({'date':startDatetime.date(),'enterTime':startDatetime.time(),
                    'exitTime':str((startDatetime+parkTime).time()),'car_id':carId})

    print("date:"+str(startDatetime.date())+" start time:"+str(startDatetime.time())+" exit time:"+str((startDatetime+parkTime).time()))


# realtime log (start==exit)
for i in range(10):
    startHour=random.randint(6,13)
    startMinute=random.randint(0,59)
    startSecond=random.randint(0,59)

    startDatetime = datetime(2019, 3, 18, startHour, startMinute, startSecond)

    carId = carsId[i]

    logJson.append({'date': startDatetime.date(), 'enterTime': startDatetime.time(),
                    'exitTime': startDatetime.time(), 'car_id': carId})

    print("date:" + str(startDatetime.date()) + " start time:" + str(startDatetime.time()) + " exit time:" + str(startDatetime.time()))




json.dump(logJson, open('./log.json', 'w'),
              indent=4, separators=(',', ': '),
          cls=DjangoJSONEncoder)
