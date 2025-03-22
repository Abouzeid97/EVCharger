from django.db import models

class Charger(models.Model):
    charger_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default="Disconnected")

class Transaction(models.Model):
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(null=True, blank=True)
