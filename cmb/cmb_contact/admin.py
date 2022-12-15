from django.contrib import admin
from cmb_home.admin import ContentAdmin
from cmb_home.models import Content


class ContactContent(Content):
    REFERENCE = "contact"

    class Meta:
        proxy = True
        verbose_name = "content"
        verbose_name_plural = "content"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.REFERENCE
        return super().save(*args, **kwargs)


class ContactContentAdmin(ContentAdmin):
    filter_queryset_prefix = ContactContent.REFERENCE


admin.site.register(ContactContent, ContactContentAdmin)
