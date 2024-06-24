from django.urls import include, path
from customer.views import *

urlpatterns = [
    path('login/', check_credentials, name='login'),
    path('new_user/', new_user, name='new_user'),
]