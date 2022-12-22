from hashlib import _BlakeHash
import logging

from django.db import models
from tinymce.models import HTMLField
from cmb_utils.mixins import DigestMixin, ContentContextMixin, trim

from cmb_home.mockup import mockup_content, mockup_files, mockup_links, mockup_settings, mockup_snippets, mockup_menu_entries
from cmb_utils.markdown_wrapper import md
MEDIA_URL = "media/"


logger = logging.getLogger(__name__)


class Snippet(models.Model):
    key = models.CharField(max_length=127, primary_key=True)
    value = models.TextField(max_length=4095)
    html = models.TextField(max_length=8191)

    @classmethod
    # noinspection PyUnresolvedReferences
    def get_context(cls) -> dict:
        return {
            "snippets": {obj.key: obj.html for obj in cls.objects.all()}
        }

    @classmethod
    def mockup(cls) -> bool:
        return mockup_snippets(cls)

    def save(self, *args, **kwargs) -> None:
        self.html = md.convert(self.value)
        super().save(*args, **kwargs)


class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)

    @classmethod
    def mockup(cls) -> bool:
        return mockup_settings(cls)

    def __str__(self) -> str:
        return f"Setting <{self.key}>"


class HomeContent(models.Model, DigestMixin, ContentContextMixin):
    html = HTMLField()
    position = models.PositiveIntegerField(default=10, verbose_name="vertical position")

    class Meta:
        verbose_name = "content (/home)"
        verbose_name_plural = "content (/home)"

    def __str__(self) -> str:
        return f"<{self.digest[:10]}...>"

    @classmethod
    def get_context(cls) -> dict:
        return cls._get_context(cls.objects.all())

    @classmethod
    def mockup(cls) -> bool:
        return mockup_content(cls)


# noinspection PyTypeChecker
# noinspection PyUnresolvedReference
class Link(models.Model):
    target = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255, blank=True)

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs) -> None:
        if self.url:
            if self.url.count("@"):
                self.url = "mailto:" + self.url
            elif not self.url.startswith("http"):
                self.url = "http://" + self.url
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        _str = f"Link<{self.target} -> {self.url if self.url else '?'}>"
        return trim(_str)

    # noinspection PyUnresolvedReferences
    @ classmethod
    def get_context(cls) -> dict:
        return {
            "links":
                {
                    link.target: link.url for link in cls.objects.all()}
        }

    @ classmethod
    def mockup(cls) -> bool:
        return mockup_links(cls)


class MenuEntry(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Menu entry"
        verbose_name_plural = "Menu entries"

    def __str__(self) -> str:
        return f"<{self.name}:{self.url}>"

    @classmethod
    def mockup(cls) -> bool:
        return mockup_menu_entries(cls)

    @classmethod
    def get_context(cls) -> dict:
        return {
            "menu_entries": baefwef
        }

# noinspection PyUnresolvedReferences


class File(models.Model):
    identifier = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(max_length=1023, blank=True)
    description_html = models.CharField(max_length=2047, blank=True)
    file = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        self.description_html = md.convert(self.description)
        super().save(*args, **kwargs)

    @ classmethod
    def get_context(cls) -> dict:
        return {
            "files":
                {file.identifier: {
                    "url": file.url,
                    "description": file.description_html,
                } for file in cls.objects.all()}
        }

    @ classmethod
    def mockup(cls) -> bool:
        return mockup_files(cls)

    @ property
    def url(self) -> str:
        return ("/" + MEDIA_URL + self.file.name) if self.file else ""
