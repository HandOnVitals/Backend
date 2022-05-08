from curses.ascii import US
from django.db import models
from users.models import User

class Reading(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    # Values
    temperature = models.FloatField()
    heart_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    oxygen_saturation = models.FloatField()
    blood_pressure = models.FloatField()

    class Meta:
        unique_together = ['user', 'datetime']