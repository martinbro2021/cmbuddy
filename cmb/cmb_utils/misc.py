import re
from html.parser import HTMLParser
from django.contrib import admin


class ImplicitModelAdmin(admin.ModelAdmin):
    """Implicitly registers all fields except for the id field for displaying and editing."""
    exclude_in_list = ("id",)
    exclude_in_editor = ("id",)

    # noinspection PyProtectedMember
    def __init__(self, model, admin_site) -> None:
        super().__init__(model, admin_site)
        self.exclude = self.exclude_in_editor
        self.list_display = self.list_display + tuple(field.name for field in model._meta.fields)
        self.list_display = tuple(filter(lambda name: name not in self.exclude_in_list, self.list_display))


class HTMLFilterInnerText(HTMLParser):
    """Filters the inner text from a string containing html code"""
    inner_text = ""

    def handle_data(self, data) -> None:
        self.inner_text += data


def to_snake_case_upper(camel: str) -> str:
    """converts camelCase to CAMEL_CASE - which is actually SNAKE_CASE ;-)"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel).upper()
