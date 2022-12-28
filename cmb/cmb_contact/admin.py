from django.contrib import admin

from cmb_contact.models import ContactContent
from cmb_utils.mixins import PreviewMixin


class ContactContentAdmin(admin.ModelAdmin, PreviewMixin):
    list_display = ("digest",)
    readonly_fields = ("preview",)


admin.site.register(ContactContent, ContactContentAdmin)
