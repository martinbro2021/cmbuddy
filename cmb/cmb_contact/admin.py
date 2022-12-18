from django.contrib import admin
from cmb_home.admin import ContentAdmin
from cmb_home.models import LocatedContent


class ContactContent(LocatedContent):
    locate = "contact"

    class Meta:
        proxy = True
        verbose_name = "content (/contact)"
        verbose_name_plural = "content (/contact)"


class ContactContentAdmin(ContentAdmin):
    locate = ContactContent.locate


admin.site.register(ContactContent, ContactContentAdmin)
