from django.urls import path
from . import views

#this py file shows our path mapping
#the detailed documentation of each call is shown in the views.py


urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup),
    path('login', views.login),
    path('addUser', views.addUser),
    path('logout', views.logout),
    path('admin/login',views.adminLogin),
    path('admin/logout',views.adminLogout),
    path('admin',views.dashboard),
    path('navigation',views.navigation),
    path('recommend',views.recommend),

    path('positions',views.position),
    path('weather',views.getWeather),
    path('gas',views.getGasPrice),


    path('delete',views.deleteUser),
    path('change',views.changePassword),

    path('number',views.numberOfCar),
    path('income',views.income),
    path('usage',views.rateOfUsage),
    path('parktime',views.parkTime),
    path('record',views.getRecord),

    path('checkin',views.checkin),
    path('checkout',views.checkout),

    path('af7ae505a9eed503f8b8e6982036873e.woff2',views.woff2),
    path('a1ecc3b826d01251edddf29c3e4e1e97.woff',views.woff1),
    path('fee66e712a8a08eef5805a46892932ad.woff',views.woff3),
    path('e23a7dcaefbde4e74e263247aa42ecd7.ttf',views.ttf1),
    path('b06871f281fee6b241d60582ae9369b9.ttf',views.ttf2),


    path('api',views.api)

]
