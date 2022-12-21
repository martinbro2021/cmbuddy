import logging

from django.apps import apps as applications
from django.contrib import admin
from django.template import loader
from django.utils.safestring import mark_safe

from cmb_home.models import File, Link, Snippet, HomeContent

logger = logging.getLogger(__name__)


class PreviewMixin:
    # todo check usage
    def preview(self, obj):
        template = loader.get_template("previews/description.html")
        temp = template.render({"preview": obj.html}).replace("\"", "'")
        html = f'<iframe style="width:75%; hight: 350px;" srcdoc="{temp}"></iframe>'
        return mark_safe(html)
    preview.short_description = "Preview"


class ImplicitModelAdmin(admin.ModelAdmin):
    """Implicitly registers all fields except for the id field for displaying and editing."""
    exclude_in_list = ("id",)
    exclude_in_editor = ("id",)

    # noinspection PyProtectedMember
    def __init__(self, model, admin_site) -> None:
        super().__init__(model, admin_site)
        self.exclude = self.exclude_in_editor
        self.list_display = self.list_display + tuple(field.name for field in model._meta.fields)
        self.list_display = tuple(filter(lambda name: name not in self.exclude_in_list, self.list_display))


class FileAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("description_html",)
    exclude_in_list = ("description_html", "__str__")
    readonly_fields = ("preview",)

    def preview(self, obj):
        html = f'<img style="width:400px;" src={obj.url} />'
        return mark_safe(html)

    preview.short_description = "Preview"


class LinkAdmin(admin.ModelAdmin):
    pass


class SnippetAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("html",)
    exclude_in_list = ("html", "__str__")


class HomeContentAdmin(ImplicitModelAdmin):
    exclude_in_list = ("__str__", "id", "html", "position")
    list_display = ("digest",)


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
