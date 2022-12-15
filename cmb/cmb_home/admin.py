from django.apps import apps as applications
from django.template import loader
from django.contrib import admin
from django.template import loader
from django.utils.safestring import mark_safe
from .models import Content, Link, File, Snippet
import logging

logger = logging.getLogger(__name__)


class ImplicitModelAdmin(admin.ModelAdmin):
    """Implicitly registers all fields except for the id field for displaying and editing."""
    exclude_in_list = ("id",)
    exclude_in_editor = ("id",)

    # noinspection PyProtectedMember
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.exclude = self.exclude_in_editor
        self.list_display = self.list_display + tuple(field.name for field in model._meta.fields)
        self.list_display = tuple(filter(lambda name: name not in self.exclude_in_list, self.list_display))


class ContentAdmin(ImplicitModelAdmin):
    list_display = ("digest",)
    exclude_in_list = ("id", "html", "reference", "text")
    exclude_in_editor = ("id", "html", "reference")
    readonly_fields = ("preview",)
    filter_queryset_prefix = "home"

    def preview(self, obj):
        template = loader.get_template("preview.html")
        temp = template.render({"preview": obj.html}).replace("\"", "'")
        html = f'<iframe style="width:75%; hight: 350px;" srcdoc="{temp}"></iframe>'
        return mark_safe(html)
    preview.short_description = "Preview"

    def get_queryset(self, _):
        return self.model.objects.filter(reference__startswith=self.filter_queryset_prefix)


class FileAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("description_html",)
    exclude_in_list = ("description_html",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        html = f'<img style="width:250px; height:250px" src={obj.url} />'
        return mark_safe(html)

    preview.short_description = "Preview"


class LinkAdmin(admin.ModelAdmin):
    pass


class SnippetAdmin(ImplicitModelAdmin):
    exclude_in_editor = ("html",)
    exclude_in_list = ("html", "__str__")


def register_automatically(standard_model_admin):
    """Registers all yet unregistered models to the admin site."""
    models = applications.get_models()
    for model in models:
        try:
            admin.site.register(model, standard_model_admin)
        except admin.sites.AlreadyRegistered:
            pass


admin.site.register(Content, ContentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Snippet, SnippetAdmin)
register_automatically(ImplicitModelAdmin)