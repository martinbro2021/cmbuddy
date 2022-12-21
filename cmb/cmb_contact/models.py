from django.db import models
from tinymce.models import HTMLField

from cmb_utils.mixins import DigestMixin
from cmb_home.models import trim
from cmb_home.mockup import mockup_content
from cmb_utils.mixins import ContentContextMixin


class ContactContent(models.Model, ContentContextMixin, DigestMixin):
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

    def __str__(self) -> str:
        return f"<{self.digest[:10]}...>"

    # noinspection PyUnresolvedReferences
    @classmethod
    def get_context(cls, reference=default_reference) -> dict:
        return cls._get_context(cls.objects.filter(reference=reference))

    @classmethod
    def mockup(cls) -> bool:
        return mockup_content(cls)
