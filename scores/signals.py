import importlib
from django.db.models.signals import pre_save
from django.dispatch import receiver
from scores.models import ScoreSystem
from readings.models import Reading, ScoreSystemReading

@receiver(pre_save, sender=Reading, dispatch_uid='calculate_scores')
def calculate_scores(sender, instance: Reading, raw, using, update_fields, **kwargs):
    score_systems = ScoreSystem.objects.all()
    for score_system in score_systems:
        spec = importlib.util.spec_from_file_location(score_system.name, score_system.script_path)
        score_system_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(score_system_module)
        score_result = score_system_module.main(instance.heart_rate, instance.blood_pressure, instance.temperature, instance.blood_oxygen, instance.respiratory_rate)
        ScoreSystemReading.objects.create(reading=instance, score_system=score_system, value=score_result)
