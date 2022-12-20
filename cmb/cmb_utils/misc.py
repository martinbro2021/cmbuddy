from html.parser import HTMLParser


class HTMLFilterInnerText(HTMLParser):
    inner_text = ""

    def handle_data(self, data) -> None:
        self.inner_text += data
