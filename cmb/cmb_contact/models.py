from django.db import models
from tinymce.models import HTMLField

from cmb_home.models import trim
from cmb_home.mockup import mockup_content


class ContactContent(models.Model):
    html = HTMLField()
    position = models.PositiveIntegerField(default=10, verbose_name="vertical position")
    default_reference = "/contact"
    reference = models.CharField(
        max_length=255,
        default=default_reference,
        verbose_name="reference")

    class Meta:
        verbose_name = "content (/contact)"
        verbose_name_plural = "content (/contact)"

    # noinspection PyUnresolvedReferences
    @classmethod
    def get_context(cls, reference=default_reference):
        return {"content": sorted(cls.objects.filter(reference=reference), key=lambda obj: obj.position)}

    @classmethod
    def mockup(cls) -> bool:
        return mockup_content(cls)

    # noinspection PyTypeChecker
    @property
    def digest(self):
        return "[NO TEXT]" if not self.html else trim(self.html)
