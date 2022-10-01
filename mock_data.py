import django
django.setup()
from django.utils import timezone

from doctors.models import User
from readings.models import Reading
from devices.models import Device
from pacients.models import Pacient

if not User.objects.filter(email='joaodoutor@om.pt').exists():
    user = User.objects.create_user('joaodoutor@om.pt', 'pwd123', ballot='12345')
    user.first_name = 'Joao'
    user.last_name = 'Doutor'
    user.save()
else:
    user = User.objects.get(email='joaodoutor@om.pt')

if not Pacient.objects.filter(full_name='Alexandre Serra').exists():
    pacient = Pacient.objects.create(full_name='Alexandre Serra', health_number='123456789')
else:
    pacient = Pacient.objects.get(health_number='123456789')

if not Device.objects.filter(code='TEST1').exists():
    device = Device.objects.create(code='TEST1')
else:
    device = Device.objects.get(code='TEST1')

datetime = timezone.now()
reading1 = Reading.objects.create(
    pacient=pacient,
    device=device,
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
    pacient=pacient,
    device=device,
    datetime=datetime,
    temperature=35.3,
    heart_rate=22.0,
    respiratory_rate=12.0,
    oxygen_saturation=21.0,
    blood_pressure=12.0
)

reading2.save()