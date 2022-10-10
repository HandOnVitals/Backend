import os
import os
from scores.models import ScoreSystem, score_scripts_path

if not ScoreSystem.objects.filter(name='News2').exists():
    name = 'News2'
    spec = 'https://www.rcplondon.ac.uk/projects/outputs/national-early-warning-score-news-2'
    script = os.path.join(score_scripts_path, 'news2.py')
    ScoreSystem.objects.create(name=name, spec=spec, script=script)