from django.template import loader
from django.utils.safestring import mark_safe

from cmb_utils.misc import HTMLFilterInnerText

MAX_DIGEST_LEN = 100


def trim(_str: str, trim_len: int = MAX_DIGEST_LEN) -> str:
    return _str[:trim_len] + (" [...]" if len(_str) > trim_len else "")


class PreviewMixin:
    """Provides a preview of an html field embedded in an <iframe> in the django admin"""

    def preview(self, obj) -> str:
        template = loader.get_template("previews/description.html")
        temp = template.render({"preview": obj.html}).replace("\"", "'")
        html = f'<iframe style="width:100%; height: 400px" srcdoc="{temp}"></iframe>'
        return mark_safe(html)
    preview.short_description = "Current content"


class DigestMixin:

    @property
    def digest(self, trim_len: int = MAX_DIGEST_LEN) -> str:
        inner_text = ""
        if self.html:  # type: ignore
            self.html: str
            text_filter = HTMLFilterInnerText()
            text_filter.feed(self.html)
            inner_text = text_filter.inner_text
        return "[NO TEXT]" if not self.html else trim(inner_text, trim_len)


class ContentContextMixin:

    @classmethod
    def _get_context(cls, query_set) -> dict:
        all_ordered = query_set.order_by("position")
        sec_1 = all_ordered.filter(position__gt=-1).filter(position__lte=10)
        sec_2 = all_ordered.filter(position__gt=10).filter(position__lte=20)
        sec_3 = all_ordered.filter(position__gt=20).filter(position__lte=30)
        return {"content": {
            "all": all_ordered,
            "section_1": sec_1,
            "section_2": sec_2,
            "section_3": sec_3
        }}
