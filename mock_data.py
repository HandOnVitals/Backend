from os import read
import django
from django.utils import timezone
django.setup()
from users.models import User
from readings.models import Reading

if not User.objects.filter(username='johnsmith').exists():
    user = User.objects.create_user('johnsmith', 'john@smith.com', 'pwd123', citizen_id='12345678')
    user.first_name = 'John'
    user.last_name = 'Smith'
    user.save()
else:
    user = User.objects.get(username='johnsmith')

datetime = timezone.now()
reading1 = Reading.objects.create(
    user=user,
    datetime=datetime,
    temperature=37.3,
    heart_rate=23.0,
    respiratory_rate=13.0,
    oxygen_saturation=22.0,
    blood_pressure=13.0
)

reading1.save()


datetime = timezone.now()
reading2 = Reading.objects.create(
    user=user,
    datetime=datetime,
    temperature=35.3,
    heart_rate=22.0,
    respiratory_rate=12.0,
    oxygen_saturation=21.0,
    blood_pressure=12.0
)

reading2.save()