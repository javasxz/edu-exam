import os

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads fixture data into the database."

    def handle(self, *args, **options):
        fixture_files = []

        for app_config in apps.get_app_configs():
            fixtures_dir = os.path.join(app_config.path, "fixtures")
            if os.path.isdir(fixtures_dir):
                for file_name in os.listdir(fixtures_dir):
                    if file_name.endswith(".json"):
                        fixture_files.append(os.path.join(fixtures_dir, file_name))

        un_done_fixture_files = []  # TODO: need to correct
        for fixture_file in fixture_files:
            try:
                call_command("loaddata", fixture_file)
            except:
                un_done_fixture_files.append(fixture_file)

        for fixture_file_new in un_done_fixture_files:
            call_command("loaddata", fixture_file_new)

        self.stdout.write(self.style.SUCCESS("Fixture data loaded successfully."))
