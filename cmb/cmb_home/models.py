import logging
from django.db import models
from cmb_home.my_markdown import md
from cmb_home.mockup import mockup_content, mockup_files, mockup_links, mockup_snippets, mockup_reference
from cmb_sample.settings import MEDIA_URL

logger = logging.getLogger(__name__)
MAX_DIGEST_LEN = 50


def trim(_str: str) -> str:
    return _str[:MAX_DIGEST_LEN] + (" [...]" if len(_str) > MAX_DIGEST_LEN else "")


# noinspection PyUnresolvedReferences
class Snippet(models.Model):
    key = models.CharField(max_length=127, primary_key=True)
    value = models.TextField(max_length=4095)
    html = models.TextField(max_length=8191)

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


# noinspection PyUnresolvedReferences
class Content(models.Model):
    text = models.TextField(max_length=32767, blank=True)
    html = models.TextField(max_length=65535)
    header = models.CharField(max_length=255, blank=True)
    position = models.IntegerField(default=0)
    reference = models.TextField(max_length=255)
    published = models.DateField(verbose_name="Date published", null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.html = md.convert(self.text)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Content"

    @classmethod
    def get_context(cls, reference: str):  # todo implement key
        return {"content": sorted(cls.objects.filter(reference=reference), key=lambda obj: obj.position)}

    @classmethod
    def mockup(cls) -> bool:
        return mockup_content(cls)

    @property
    def digest(self):
        return "[NO TEXT]" if not self.text else trim(self.text)


# noinspection PyTypeChecker
# noinspection PyUnresolvedReference
class Link(models.Model):
    objects = None
    target = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.url:
            if self.url.count("@"):
                self.url = "mailto:" + self.url
            elif not self.url.startswith("http"):
                self.url = "http://" + self.url
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        _str = f"{self.target} -> {self.url}"
        return trim(_str)

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
