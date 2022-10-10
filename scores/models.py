import os
from scores.apps import ScoresConfig
from handonvitals.settings import BASE_DIR
from django.db import models

def score_scripts_path():
    return os.path.join(BASE_DIR, ScoresConfig.name, 'scripts')

class ScoreSystem(models.Model):
    name = models.CharField(max_length=50)
    spec = models.URLField()
    script = models.FilePathField(path=score_scripts_path)

    def __str__(self):
            return f"{self.name} score system"
