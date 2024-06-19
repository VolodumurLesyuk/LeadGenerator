from django.urls import include, path
from customer.views import *

urlpatterns = [
    path('login/', check_credentials, name='login'),
]