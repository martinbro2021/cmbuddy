from cmb_contact.models import ContactContent
from django.contrib import admin
from cmb_utils.misc import ImplicitModelAdmin


class ContactContentAdmin(admin.ModelAdmin):
    list_display = ("digest",)


admin.site.register(ContactContent, ContactContentAdmin)
