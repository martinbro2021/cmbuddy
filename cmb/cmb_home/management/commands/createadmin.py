import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    creator_name = "creator"
    help = \
        'Creates admin with default password and a content creator ' \
        f'with name "{creator_name}" ' \
        'only for development purposes'

    def handle(self, *args, **options):
        password = os.environ.get("ADMIN_DEFAULT_PW")
        creator_pw = get_random_secret_key()[:10]
        if password:
            try:
                user_model = get_user_model()

                creator = user_model.objects.create_user(self.creator_name, '', creator_pw)  # type: ignore
                creator.is_staff = True
                creator.save()
                self.stdout.write(self.style.SUCCESS(f"Created user '{self.creator_name}' with password: {creator_pw}"))

                user_model.objects.create_superuser('admin', '', password)  # type: ignore
                self.stdout.write(self.style.SUCCESS(
                    "Created superuser 'admin'"))
            except Exception as ex:
                self.stderr.write(f"Could not create superuser and/or manager:\n{ex}")
        else:
            self.stdout.write(self.style.ERROR("No default pw provided"))
