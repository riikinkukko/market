from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('registration/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('basket/', basket_view, name='basket'),
]