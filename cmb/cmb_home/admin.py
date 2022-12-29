import logging

from django.apps import apps as applications
from django.contrib import admin
from django.utils.safestring import mark_safe

from cmb_contact.admin import *  # do not remove - force to register first  # noqa: F40
from cmb_home.models import File, HomeContent, Link, Snippet
from cmb_utils.misc import ImplicitModelAdmin
from cmb_utils.mixins import PreviewMixin

logger = logging.getLogger(__name__)


class FileAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("description_html",)
    exclude_in_list = ("description_html", "__str__")
    readonly_fields = ("preview",)

    def preview(self, obj) -> str:
        html = f'<img style="width:400px;" src={obj.url} />'
        return mark_safe(html)

    preview.short_description = "Current file"


class LinkAdmin(admin.ModelAdmin):
    pass


class SnippetAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("html",)
    exclude_in_list = ("html", "__str__")


class HomeContentAdmin(admin.ModelAdmin, PreviewMixin):
    list_display = ("digest",)
    readonly_fields = ("preview",)


def register_automatically(model_admin) -> None:
    """Registers all yet unregistered models to the admin site."""
    models = applications.get_models()
    for model in models:
        try:
            admin.site.register(model, model_admin)
        except admin.sites.AlreadyRegistered:
            pass


admin.site.register(HomeContent, HomeContentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Snippet, SnippetAdmin)

register_automatically(ImplicitModelAdmin)

admin.sites.AdminSite.site_header = 'CMBuddy admin'
admin.sites.AdminSite.site_title = 'CMBuddy admin'
admin.sites.AdminSite.index_title = 'Index'
