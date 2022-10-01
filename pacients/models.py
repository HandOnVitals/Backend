from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

HEALTH_NUMBER_DIGITS = 9

# Create your models here.
class Pacient(models.Model):
    full_name = models.TextField(null=False, blank=False)
    health_number = models.CharField(max_length=9, unique=True, validators=[
        MaxLengthValidator(9),
        MinLengthValidator(9),
        RegexValidator(r'^\d{1,10}$')
    ])

    def __str__(self) -> str:
        return f'{self.health_number} - {self.full_name}'

