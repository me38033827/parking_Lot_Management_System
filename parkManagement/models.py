from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import threading
import time
import datetime

#
#this py file is used to define the models of our system,
#there are five main models
#After the defination and migration, these models will be added automatically into the SQLite database.
#Besides the models, the final part of the file is a thread running periodically to dectect the parking time of
#cars which is 10 minutes before 3 hours.
#
#


#this model is used to represent users of the system, such as the drivers.
#the main key is the auto incremented id
class User(models.Model):
    phoneNumber = models.IntegerField()
    xCoord = models.DecimalField(decimal_places=4, max_digits=10)
    yCoord = models.DecimalField(decimal_places=4, max_digits=10)
    password = models.CharField(max_length=64)
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=64)

    def __str__(self):
        return str(self.phoneNumber)

#this model is used to represent the manager of the system
#the key is the auto incremented id
class Admin(models.Model):
    phoneNumber = models.IntegerField()
    password = models.CharField(max_length=64)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.phoneNumber)


#this model is used to represent the car
#the key is the plate number of cars.

class Car(models.Model):
    plateNumber = models.CharField(max_length=6, primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, )
    xCoord = models.DecimalField(decimal_places=4, max_digits=10)
    yCoord = models.DecimalField(decimal_places=4, max_digits=10)
    rot = models.IntegerField(default=0, validators=[MaxValueValidator(179), MinValueValidator(-180)])

    def __str__(self):
        return self.plateNumber

#this model is used to represent the parking lot
#the key is the auto incremented id
class Parking(models.Model):
    isParkingLot = models.BooleanField()
    isEnter = models.BooleanField()
    isExit = models.BooleanField()
    id = models.IntegerField(primary_key=True)
    nearPoint = models.IntegerField(default=0)
    xCoord = models.DecimalField(decimal_places=4, max_digits=10)
    yCoord = models.DecimalField(decimal_places=4, max_digits=10)

    def __str__(self):
        return self.id

#this model is used to represent the parking log information
#the key is the auto incremented key
class Log(models.Model):
    date = models.DateField()
    enterTime = models.TimeField()
    exitTime = models.TimeField(default=enterTime)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)




#this is a function to run a new thread which calculates the parking time of each car
#
def checkParkTime():

    sent={}
    date1 = '2019-03-01'
    date2 = '2029-12-31'
    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.datetime.strptime(date2, '%Y-%m-%d')
    step = datetime.timedelta(days=1)
    while start <= end:

        sent[str(start.date())]=[]
        start += step



    while True:
        time.sleep(60)
        current=datetime.datetime.now()
        year=current.date().year
        month=current.date().month
        day=current.date().day

        logs=Log.objects.all()
        for log in logs:
            if log.enterTime==log.exitTime:
                enterHour=log.enterTime.hour
                enterMinute=log.enterTime.minute
                enterSecond=log.enterTime.second
                if (datetime.datetime(year,month,day,
                                     current.hour,current.minute,current.second)-
                    datetime.datetime(year,month,day,enterHour,enterMinute,enterSecond)).seconds/60 >=170 and not(log.car in sent[str(current.date())]):
                    carId=log.car
                    car=Car.objects.get(plateNumber=carId)
                    userId=car.owner.id
                    user=User.objects.get(id=userId)
                    phoneNumber=user.phoneNumber
                    sent[str(current.date())].append(log.car)




t=threading.Thread(target=checkParkTime)
t.start()
