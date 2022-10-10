from curses.ascii import US
from django.db import models
from devices.models import Device
from pacients.models import Pacient
from scores.models import ScoreSystem

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

    scores = models.ManyToManyField(ScoreSystem, through='ScoreSystemReadingValue')

    class Meta:
        unique_together = ['pacient', 'datetime']

    def __str__(self):
        return f"Reading from {self.pacient} at {self.datetime}"


class ScoreSystemReadingValue(models.Model):
    reading = models.ForeignKey(Reading, on_delete=models.CASCADE)
    score_system = models.ForeignKey(ScoreSystem, on_delete=models.CASCADE)
    
    value = models.FloatField()

    def __str__(self):
        return f"Score of {self.value} using {self.score_system} - {self.reading}"
