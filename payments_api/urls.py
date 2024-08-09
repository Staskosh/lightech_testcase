from django.urls import path
from . import views


app_name = 'payments_api'


urlpatterns = [
    path('balance/', views.get_balance, name='balance'),
    path('deposit/', views.deposit, name='deposit'),
    path('transfer/', views.transfer, name='transfer'),
]
