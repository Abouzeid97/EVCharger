from rest_framework.generics import ListAPIView
from OcppApp.models import Charger, Transaction
from .serializers import ChargerSerializer, TransactionSerializer

class ChargerView(ListAPIView):
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializer

class TransactionView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
