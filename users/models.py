from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator

class User(AbstractUser):
    citizen_id = models.IntegerField(unique=True, validators=[
        MaxLengthValidator(8),
        MinLengthValidator(8)
    ])
    # TODO: Remove other fields and make citizenId Primary Key