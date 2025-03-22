from django.urls import path
from .views import *

urlpatterns = [
    path('charger/', ChargerView.as_view(), name="chargers"),
    path('transactions/', TransactionView.as_view(), name='transactions')
    
]


