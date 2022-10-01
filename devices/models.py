from django.db import models

# Represents a device
class Device(models.Model):
    code = models.CharField(max_length=50)
    # location = 
    # serial_number =
    # active = models.BooleanField
    # installed_at = models.Datetime