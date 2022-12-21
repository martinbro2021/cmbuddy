from html.parser import HTMLParser

MAX_DIGEST_LEN = 100


def trim(_str: str, trim_len: int = MAX_DIGEST_LEN) -> str:
    return _str[:trim_len] + (" [...]" if len(_str) > trim_len else "")


class HTMLFilterInnerText(HTMLParser):
    inner_text = ""

    def handle_data(self, data) -> None:
        self.inner_text += data


class DigestMixin:

    @property
    # noinspection PyTypeChecker
    def digest(self, trim_len: int = MAX_DIGEST_LEN) -> str:
        inner_text = ""
        if self.html:
            text_filter = HTMLFilterInnerText()
            text_filter.feed(self.html)
            inner_text = text_filter.inner_text
        return "[NO TEXT]" if not self.html else trim(inner_text, trim_len)


class ContentContextMixin:
    @classmethod
    # noinspection PyUnresolvedReferences
    def _get_context(cls, objects) -> dict:
        all_obj = sorted(objects, key=lambda obj: obj.position)
        sec_1 = filter(lambda obj: -1 < obj.position <= 10, all_obj)
        sec_2 = filter(lambda obj: 10 < obj.position <= 20, all_obj)
        sec_3 = filter(lambda obj: 20 < obj.position <= 99, all_obj)
        return {"content": {
            "all": all_obj,
            "section_1": sec_1,
            "section_2": sec_2,
            "section_3": sec_3
        }}
