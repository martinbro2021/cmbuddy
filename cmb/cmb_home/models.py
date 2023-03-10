import logging

from django.db import models

from tinymce.models import HTMLField

from cmb_home.mockup import (mockup_content, mockup_files, mockup_links,
                             mockup_menu_entries, mockup_settings,
                             mockup_snippets)
from cmb_utils.markdown_wrapper import md
from cmb_utils.mixins import ContentContextMixin, DigestMixin, trim

MEDIA_URL = "media/"


logger = logging.getLogger(__name__)


class Snippet(models.Model):
    key = models.CharField(max_length=127, primary_key=True)
    value = models.TextField(max_length=4095)
    html = models.TextField(max_length=8191)

    @classmethod
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
    html = HTMLField(verbose_name="text")  # type: ignore
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


class Link(models.Model):
    target = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255, blank=True)

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
    position = models.IntegerField(primary_key=True, default=10)

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
            "menu_entries": cls.objects.all()
        }


class File(models.Model):
    identifier = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(max_length=1023, blank=True)
    description_html = models.CharField(max_length=2047, blank=True)
    file = models.FileField(null=True, blank=True, upload_to="home/files")

    def save(self, *args, **kwargs) -> None:
        self.description_html = md.convert(self.description)
        super().save(*args, **kwargs)

    @ classmethod
    def get_context(cls) -> dict:
        return {
            "files":
                {file.identifier: {
                    "url": file.file.url,
                    "description": file.description_html,
                } for file in cls.objects.all()}
        }

    @ classmethod
    def mockup(cls) -> bool:
        return mockup_files(cls)
