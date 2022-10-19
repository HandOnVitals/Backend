from django.db import models
from doctors.models import User

class OTP(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code_hash = models.TextField()
    validity = models.DateTimeField()

    def __str__(self):
        return f'{self.user} OTP code valid until {self.validity}'
