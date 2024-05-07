from django.contrib import admin
from django.urls import path,include
from api.views import *
from User.views import *

urlpatterns = [
    path('tanglegram/', tanglegram, name='tanglegram'),
    path('tree/', tree, name='tree'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),
]