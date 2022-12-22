from django.core.management.base import BaseCommand

from cmb_home.models import File, Link, Setting, Snippet, HomeContent, MenuEntry
from cmb_contact.models import ContactContent
from cmb_home.mockup import NoMockupException


class Command(BaseCommand):
    help = 'Populates DB with some test data'

    def handle(self, *args, **options):
        for cls in (HomeContent, ContactContent, Snippet, File, Link, Setting, MenuEntry):
            try:
                if cls.mockup():
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully added mock up data for table {cls.__name__}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Did not add mock-up data for table {cls.__name__} since db table is not empty.'))
            except NoMockupException:
                self.stdout.write(self.style.ERROR(
                    f'Did not add mock-up data for table {cls.__name__} because no mockups where found.'))
            except Exception as ex:
                self.stdout.write(self.style.ERROR(
                    f'An error ocurred while adding mockup data:\n{ex}'))
                raise ex
