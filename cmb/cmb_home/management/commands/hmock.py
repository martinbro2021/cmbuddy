from cmb_home.models import Content, Link, File, Snippet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populates DB with some test data'

    def handle(self, *args, **options):
        for cls in (Snippet, Content, File, Link):
            try:
                if cls.mockup():
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully added mock up data for table {cls.__name__}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Did not add mock-up data for table {cls.__name__} since db table is not empty.'))
            except Exception as ex:
                self.stdout.write(self.style.ERROR(
                    f'An error ocurred while adding mockup data:\n{ex}'))
