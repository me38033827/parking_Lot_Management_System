import hashlib
from django.contrib.staticfiles.views import serve
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Admin, Log, Car, Parking
from django.db.models import F
from utils import dijkstra, weather, gasPrice,EmailService,SMSService
import datetime
import math
import dicttoxml
import json



# this file is the main file of our system.
# most of the server logic is handled in this file

####################################################################################################################################
#Functions used to handle requests sent by parking lot managers

#return the main page
def dashboard(request):
    adminId = request.session.get('adminId', -1)
    try:
        admin = Admin.objects.get(id=adminId)
    except ObjectDoesNotExist:
        return redirect('/park/admin/login')

    return render(request, 'parkSrc/dashboard.html', {'userName': admin.phoneNumber})


#handle the login of managers
#if login successfully, it will return the main page
#otherwise, it will return the to the login page with error message
@csrf_exempt
def adminLogin(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        password = request.POST['password']
        try:
            admin = Admin.objects.get(phoneNumber=userName)
            password = hashlib.sha256(password.encode()).hexdigest()
            if str(password) == admin.password:
                request.session.set_expiry(30 * 24 * 60 * 60)
                request.session['adminId'] = admin.id
                return redirect('/park/admin')
            else:
                return render(request, 'parkSrc/signin.html', {'errorMsg': 'Username or Password is not correct!'})
        except ObjectDoesNotExist:
            return render(request, 'parkSrc/signin.html', {'errorMsg': 'Username is invalid!'})
    else:
        adminId = request.session.get('adminId', -1)
        try:
            admin = Admin.objects.get(id=adminId)
            return render(request, 'parkSrc/dashboard.html', {'userName': admin.phoneNumber})
        except ObjectDoesNotExist:
            return render(request, 'parkSrc/adminSignin.html')

#handle the logout request
#after logout the session will be deleted from server
def adminLogout(request):
    try:
        del request.session['adminId']
    except KeyError:
        pass
    return redirect('/park/admin')


#return the current number of cars in the parking lot
#the number will be returned in the heaeders
def numberOfCar(request):
    start = request.GET['start']
    end = request.GET['end']

    if start is None or end is None:
        response = HttpResponse('please add start date and end date', content_type='plain/text')
        response.status_code = 400
    else:
        number = 0
        start = start.split('-')
        end = end.split('-')
        startdate = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        enddate = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        logs = Log.objects.all()

        for log in logs:
            if startdate <= log.date < enddate:
                number += 1
        response = HttpResponse()
        response.status_code = 200
        response['number'] = number

    return response

#return the totoal parking time and parking fee of the parking lot
#the 'totaltime' and 'income' will be returned in the heaeders
def income(request):
    start = request.GET['start']
    end = request.GET['end']

    if start is None or end is None:
        response = HttpResponse('please add start date and end date', content_type='plain/text')
        response.status_code = 400
    else:
        parkTime = 0
        income = 0
        start = start.split('-')
        end = end.split('-')
        startdate = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        enddate = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        logs = Log.objects.all()

        for log in logs:
            if startdate <= log.date < enddate:
                startDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                                  log.enterTime.hour, log.enterTime.minute, log.enterTime.second)
                endDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                                log.exitTime.hour, log.exitTime.minute, log.exitTime.second)
                hours = math.ceil((endDatetime - startDatetime).seconds / 3600)
                parkTime += hours

                income += hours * 1.5 if hours <= 3 else 4.5 + (hours - 3) * 1

        response = HttpResponse()
        response.status_code = 200
        response['totalTime'] = parkTime
        response['income'] = income

    return response

#return the usage rate of the parkinglot
#the 'usage' will be returned in the headers
def rateOfUsage(request):
    start = request.GET['start']
    end = request.GET['end']

    if start == None or end == None:
        response = HttpResponse('please add start date and end date', content_type='plain/text')
        response.status_code = 400
    else:
        parkTime = 0
        start = start.split('-')
        end = end.split('-')
        startdate = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        enddate = datetime.date(int(end[0]), int(end[1]), int(end[2]))
        logs = Log.objects.all()

        for log in logs:
            if log.date > startdate and log.date < enddate:
                startDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                                  log.enterTime.hour, log.enterTime.minute, log.enterTime.second)
                endDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                                log.exitTime.hour, log.exitTime.minute, log.exitTime.second)
                minutes = (endDatetime - startDatetime).seconds / 60

        response = HttpResponse()
        response.status_code = 200
        response['usage'] = minutes / (28 * 24 * 60)

    return response

#return the car's information, such as coordination and plate number
#the data will be returned in json format
def position(request):
    cars = Car.objects.all()
    data = []

    for car in cars:
        if car.xCoord != -1:
            data.append(
                {"carId": car.plateNumber, "xCoord": int(car.xCoord), "yCoord": int(car.yCoord), "rot": car.rot})

    positions = json.dumps(data)
    print (positions)

    return JsonResponse(positions, safe=False)

####################################################################################################################################
# The following part is to handle requests sent by users


#return the signup page
def signup(request):
    return render(request, 'parkSrc/signup.html')

#handle the register request
#after registering successfully, the login page will be returned
@csrf_exempt
def addUser(request):
    phone = request.POST['userName']
    password = request.POST['password']
    email = request.POST['email']
    password = hashlib.sha256(password.encode()).hexdigest()
    newuser = User(phoneNumber=phone, password=password, xCoord=-1, yCoord=-1, email=email)
    newuser.save()
    return render(request, 'parkSrc/signin.html')


#return the main page to users
def index(request):
    userId = request.session.get('userId', -1)
    try:
        user = User.objects.get(id=userId)
    except ObjectDoesNotExist:
        return redirect('/park/login')

    return render(request, 'parkSrc/index.html', {'userName': user.phoneNumber})

#handle login request
#if login successfully, it will return the main page
#otherwise, it will return the to the login page with error message
@csrf_exempt
def login(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        password = request.POST['password']
        try:
            user = User.objects.get(phoneNumber=userName)
            password = hashlib.sha256(password.encode()).hexdigest()
            if str(password) == user.password:
                request.session.set_expiry(30 * 24 * 60 * 60)
                request.session['userId'] = user.id
                return redirect('/park')
            else:
                return render(request, 'parkSrc/signin.html', {'errorMsg': 'Username or Password is not correct!'})
        except ObjectDoesNotExist:
            return render(request, 'parkSrc/signin.html', {'errorMsg': 'Username is invalid!'})
    else:
        userId = request.session.get('userId', -1)
        try:
            user = User.objects.get(id=userId)
            return render(request, 'parkSrc/index.html', {'userName': user.phoneNumber})
        except ObjectDoesNotExist:
            return render(request, 'parkSrc/signin.html')

#handle the logout process
def logout(request):
    try:
        del request.session['userId']
    except KeyError:
        pass
    return redirect('/park/login')

#handle the delete urser process
@csrf_exempt
def deleteUser(request):
    if request.method == "DELETE":
        userId = request.session.get('userId', -1)
        try:
            user = User.objects.get(id=userId)
            password = request.META.get('HTTP_PASSWORD')
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                user.delete()
                del request.session['userId']
            else:
                return HttpResponse(status=400)
        except ObjectDoesNotExist:
            return redirect('/park/login')
    return redirect('/park/login')

#handle the password updating process
@csrf_exempt
def changePassword(request):
    if request.method == "PUT":
        userId = request.session.get('userId', -1)
        try:
            user = User.objects.get(id=userId)
            newPassword = request.META.get('HTTP_NEWPASSWORD')
            oldPassword = request.META.get('HTTP_OLDPASSWORD')
            if user.password == hashlib.sha256(oldPassword.encode()).hexdigest():
                user.password = hashlib.sha256(newPassword.encode()).hexdigest()
                user.save()

        except ObjectDoesNotExist:
            return render(request, 'parkSrc/signin.html')

    return render(request, 'parkSrc/index.html', {'userName': user.phoneNumber})

#return the totle parking time of a user
#the 'meantime' will be returned in headers.
def parkTime(request):
    userId = request.session.get('userId')
    carId = Car.objects.get(owner=userId).plateNumber
    totalParkTime = 0
    logs = Log.objects.filter(car=carId)
    for log in logs:
        startDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                          log.enterTime.hour, log.enterTime.minute, log.enterTime.second)
        endDatetime = datetime.datetime(log.date.year, log.date.month, log.date.day,
                                        log.exitTime.hour, log.exitTime.minute, log.exitTime.second)
        minutes = (endDatetime - startDatetime).seconds / 60
        totalParkTime += minutes

    days = (datetime.datetime.now() - datetime.datetime(2017, 1, 1, 0, 0, 0)).days

    response = HttpResponse()
    response.status_code = 200
    response['meantime'] = totalParkTime / days

    return response

#send the history record email to the users
#because it costs, so we commented this sending function, and print it out instead.
def getRecord(request):
    userId = request.session.get('userId')
    car = Car.objects.get(owner=userId)
    user=User.objects.get(id=userId)
    email=user.email
    carId = car.plateNumber
    logs = Log.objects.filter(car=carId)
    record = []

    for log in logs:
        record.append([str(log.date), str(log.enterTime), str(log.exitTime)])


    print(record)
    # EmailService.sendEmail(email,record)

    response = HttpResponse()
    response.status_code = 200

    return response

#handle the navigation process
# return the shortes path to an exit for a user
def navigation(request):
    userId = request.session.get('userId')
    distance = 0
    path = []
    coords = []

    try:
        request.GET['user']
        user = User.objects.get(id=userId)
        xCoord = user.xCoord
        yCoord = user.yCoord
        [distance, path] = dijkstra.shortestPath(int(xCoord), int(yCoord), type='user')
        coords.append([int(xCoord), int(yCoord)])
        for point in path:
            parking = Parking.objects.get(id=point)
            coords.append([int(parking.xCoord), int(parking.yCoord)])
    except:
        car = Car.objects.get(owner=userId)
        xCoord = car.xCoord
        yCoord = car.yCoord
        [distance, path] = dijkstra.shortestPath(int(xCoord), int(yCoord))
        coords.append([int(xCoord), int(yCoord)])
        for point in path:
            parking = Parking.objects.get(id=point)
            coords.append([int(parking.xCoord), int(parking.yCoord)])

    response = HttpResponse(json.dumps(coords).encode("utf-8"), content_type='plain/text')
    response.status_code = 200

    return response

#handle the recommend process
# return the path to the recommended parking lot to a user
def recommend(request):
    userId = request.session.get('userId')
    car = Car.objects.get(owner=userId)
    xCoord = car.xCoord
    yCoord = car.yCoord
    coords = []

    lotsState = [0] * 28
    cars = Log.objects.filter(enterTime=F('exitTime'))
    lots = Parking.objects.filter(id__range=[0, 27])
    passways = Parking.objects.filter(id__range=[32, 53])

    for car in cars:
        carId = car.car_id
        carInfo = Car.objects.get(plateNumber=carId)
        carXCoord = carInfo.xCoord
        carYCoord = carInfo.yCoord
        for lot in lots:
            lotXCoord = lot.xCoord
            lotYCoord = lot.yCoord
            if dijkstra.distance([int(carXCoord), int(carYCoord)], [int(lotXCoord), int(lotYCoord)]) < 80:
                lotsState[lot.id] = 1

    availableIndex = [i for i in range(28) if lotsState[i] == 0]
    minDis = 2000
    nearest = availableIndex[0]
    for available in availableIndex:
        lot = lots.get(id=available)
        if dijkstra.distance([int(lot.xCoord), int(lot.yCoord)], [int(xCoord), int(yCoord)]) < minDis:
            minDis = dijkstra.distance([int(lot.xCoord), int(lot.yCoord)], [int(xCoord), int(yCoord)])
            nearest = available

    minDis = 2000
    nearestPassway = passways[0].id
    for passway in passways:
        if dijkstra.distance([int(xCoord), int(yCoord)], [int(passway.xCoord), int(passway.yCoord)]) < minDis:
            minDis = dijkstra.distance([int(xCoord), int(yCoord)], [int(passway.xCoord), int(passway.yCoord)])
            nearestPassway = passway.id

    mapping = {0: 32, 1: 33, 2: 34, 3: 35, 4: 36, 5: 42, 6: 43, 7: 44, 8: 45, 9: 46, 10: 47,
               11: [42, 48], 12: [43, 49], 13: [44, 50], 14: [45, 51], 15: [46, 52], 16: [47, 53],
               17: 37, 18: 38, 19: 39, 20: 40, 21: 41, 22: 48, 23: 49, 24: 50, 25: 51, 26: 52, 27: 53}

    if nearest <= 10 or nearest >= 17:
        [distance, path] = dijkstra.recommend(nearestPassway, mapping[nearest])
        path.append(nearest)
    else:
        [distance1, path1] = dijkstra.recommend(nearestPassway, mapping[nearest][0])
        [distance2, path2] = dijkstra.recommend(nearestPassway, mapping[nearest][1])
        path = path1 if distance1 <= distance2 else path2
        path.append(nearest)

    for point in path:
        parking = Parking.objects.get(id=point)
        coords.append([int(parking.xCoord), int(parking.yCoord)])

    response = HttpResponse(str(coords).encode('utf-8'), content_type='plain/text')
    response.status_code = 200

    return response


def checkin(request):
    carId = request.META.get('HTTP_CARID')
    current = datetime.datetime.now()
    log = Log(date=current.date(), enterTime=current.time(), exitTime=current.time(), car=carId)
    log.save()

    response = HttpResponse()
    response.status_code = 201
    return response


def checkout(request):
    carId = request.META.get('HTTP_CARID')
    current = datetime.datetime.now()
    logs = Log.objects.filter(car=carId)
    log = logs[0]
    for ele in logs:
        if ele.date == current.date():
            log = ele

    log.exitTime = current.time()
    log.save()

    response = HttpResponse()
    response.status_code = 202

    return response

####################################################################################################################################
# Common part


def woff2(request):
    response = HttpResponse('parkSrc/af7ae505a9eed503f8b8e6982036873e.woff2', content_type='application/font-woff2')
    return response


def woff1(request):
    return serve(request, 'a1ecc3b826d01251edddf29c3e4e1e97.woff')
    # response = HttpResponse('a1ecc3b826d01251edddf29c3e4e1e97.woff',content_type='application/font-woff')
    # return response


def woff3(request):
    response = HttpResponse('fee66e712a8a08eef5805a46892932ad.woff', content_type='application/font-woff')
    return response


def ttf1(request):
    response = HttpResponse('e23a7dcaefbde4e74e263247aa42ecd7.ttf', content_type='application/x-font-ttf')
    return response


def ttf2(request):
    response = HttpResponse('b06871f281fee6b241d60582ae9369b9.ttf', content_type='application/x-font-ttf')
    return response


def getWeather(request):
    data = weather.weather()

    if data==[]:
        response=HttpResponse()
        response.status_code=404
        return response
    else:
        return JsonResponse(data)


def getGasPrice(request):
    data = gasPrice.price()

    if data==[]:
        response=HttpResponse()
        response.status_code=404

    else:
        prices = {'regPrice': data['details']['reg_price'],
                  'midPrice': data['details']['mid_price'],
                  'prePrice': data['details']['pre_price']}

        xml = dicttoxml.dicttoxml(prices, custom_root='gasPrices')

        response = HttpResponse(xml, content_type='text/xml')
    return response


def api(request):
    return render(request, 'parkSrc/basic-table.html')
