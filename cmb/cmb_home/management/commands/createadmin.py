import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates admin with default password only for development purposes'

    def handle(self, *args, **options):
        password = os.environ.get("ADMIN_DEFAULT_PW")
        if password:
            try:
                user_model = get_user_model()
                manager = user_model.objects.create_user('manager', '', password)
                manager.is_staff = True
                manager.save()
                user_model.objects.create_superuser('admin', '', password)
                self.stdout.write(self.style.SUCCESS(
                    "Created superuser 'admin'"))
            except Exception as ex:
                self.stderr.write(f"Could not create superuser:\n{ex}")
        else:
            self.stdout.write(self.style.ERROR("No default pw provided"))
