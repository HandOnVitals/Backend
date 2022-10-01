from curses.ascii import US
from django.db import models
from devices.models import Device
from pacients.models import Pacient

class Reading(models.Model):
    pacient = models.ForeignKey(to=Pacient, on_delete=models.CASCADE)
    device = models.ForeignKey(to=Device, on_delete=models.SET_NULL, null=True)

    datetime = models.DateTimeField()
    # Values
    temperature = models.FloatField()
    heart_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    blood_oxygen = models.FloatField()
    blood_pressure = models.FloatField()

    class Meta:
        unique_together = ['pacient', 'datetime']

    def __str__(self) -> str:
        return f"Reading from {self.pacient} at {self.datetime}"