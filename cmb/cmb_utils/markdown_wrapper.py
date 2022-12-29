from markdown import Markdown


class MarkdownWrapper(Markdown):
    """Wraps the Markdown class in a way that a single line will not be surrounded by a <p> tag."""

    def convert(self, source: str) -> str:
        temp = super().convert(source)
        if temp.count("<p>") <= 1:
            temp = temp.removeprefix("<p>").removesuffix("</p>")
        return temp


md = MarkdownWrapper()
