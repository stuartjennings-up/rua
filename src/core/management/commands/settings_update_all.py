import os
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = "Run 'python manage.py settings_update_all' to update or create setting models from master.json. USE WITH CAUTION- could replace all settings e.g. email text on a live installation of Rua if applied to a live update command."

    def handle(self, *args, **options):
        file = os.path.join(settings.BASE_DIR, 'core/fixtures/settings/master.json')

        with open(file) as json_data:
            default_data = json.load(json_data)

            for setting in default_data:
                group = models.SettingGroup.objects.get(pk=int(setting['fields']['group']))
                defaults = {
                    'types': setting['fields']['types'],
                    'value': setting['fields']['value'],
                    'description': setting['fields']['description'],
                    'group': group,
                }

                s, created = models.Setting.objects.update_or_create(
                    name=setting['fields']['name'],
                    defaults=defaults
                )

                if created:
                    print 'Created setting {0}'.format(s.name)
