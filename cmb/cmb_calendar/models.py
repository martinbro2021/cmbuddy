from datetime import date

from django.db import models

from tinymce.models import HTMLField

from cmb_home.mockup import mockup_calendar_entries


class CalendarEntry(models.Model):
    html = HTMLField(verbose_name="text")
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to="calendar/img")

    class Meta:
        verbose_name = "Calendar entry"
        verbose_name_plural = "Calendar entries"

    @classmethod
    def get_context(cls, year: int) -> dict:
        jan_01 = date(year, month=1, day=1)
        dec_31 = date(year, month=12, day=31)
        return {"content": cls.objects.filter(date__gte=jan_01, date__lte=dec_31).order_by("date")}

    @classmethod
    def mockup(cls) -> bool:
        return mockup_calendar_entries(cls)
