from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('paymentCallback/', payment_callback, name='paymentCallback'),
    path('registrationForm/', registrationForm, name='registrationForm'),
    path('testScore/', testScore, name='testScore'),

]
