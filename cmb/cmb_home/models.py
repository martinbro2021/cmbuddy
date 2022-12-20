import logging

from django.db import models
from tinymce.models import HTMLField

from cmb_home.mockup import mockup_content, mockup_files, mockup_links, mockup_settings, mockup_snippets
from cmb_home.my_markdown import md
from cmb_sample.settings import MEDIA_URL


logger = logging.getLogger(__name__)
MAX_DIGEST_LEN = 100


def trim(_str: str) -> str:
    return _str[:MAX_DIGEST_LEN] + (" [...]" if len(_str) > MAX_DIGEST_LEN else "")


class Snippet(models.Model):
    key = models.CharField(max_length=127, primary_key=True)
    value = models.TextField(max_length=4095)
    html = models.TextField(max_length=8191)

    # noinspection PyUnresolvedReferences
    @classmethod
    def get_context(cls):
        return {
            "snippets": {obj.key: obj.html for obj in cls.objects.all()}
        }

    @classmethod
    def mockup(cls) -> bool:
        return mockup_snippets(cls)

    def save(self, *args, **kwargs):
        self.html = md.convert(self.value)
        return super().save(*args, **kwargs)


class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.CharField(max_length=255)

    @classmethod
    def mockup(cls) -> bool:
        return mockup_settings(cls)

    def __str__(self) -> str:
        return f"Setting: <{self.key}>"


class HomeContent(models.Model):
    html = HTMLField()
    position = models.PositiveIntegerField(default=10, verbose_name="vertical position")

    class Meta:
        verbose_name = "content (/home)"
        verbose_name_plural = "content (/home)"

    # noinspection PyUnresolvedReferences
    @classmethod
    def get_context(cls):
        return {"content": sorted(cls.objects.all(), key=lambda obj: obj.position)}

    @classmethod
    def mockup(cls) -> bool:
        return mockup_content(cls)

    # noinspection PyTypeChecker
    @property
    def digest(self):
        return "[NO TEXT]" if not self.html else trim(self.html)


# noinspection PyTypeChecker
# noinspection PyUnresolvedReference
class Link(models.Model):
    target = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255, blank=True)

    # noinspection PyUnresolvedReferences
    def save(self, *args, **kwargs):
        if self.url:
            if self.url.count("@"):
                self.url = "mailto:" + self.url
            elif not self.url.startswith("http"):
                self.url = "http://" + self.url
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        _str = f"Link: {self.target} -> {self.url if self.url else '?'}"
        return trim(_str)

    # noinspection PyUnresolvedReferences
    @ classmethod
    def get_context(cls):
        return {
            "links":
                {
                    link.target: link.url for link in cls.objects.all()}
        }

    @ classmethod
    def mockup(cls) -> bool:
        return mockup_links(cls)


# noinspection PyUnresolvedReferences
class File(models.Model):
    identifier = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(max_length=4095, blank=True)
    description_html = models.TextField(max_length=8191, blank=True)
    file = models.FileField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.description_html = md.convert(self.description)
        return super().save(*args, **kwargs)

    @ classmethod
    def get_context(cls):
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
    def url(self):
        return "/" + MEDIA_URL + self.file.name if self.file else ""
