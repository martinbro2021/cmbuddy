from markdown import Markdown


class MyMarkdown(Markdown):
    # todo doc
    def convert(self, source: str) -> str:
        temp = super().convert(source)
        if temp.count("<p>") <= 1:
            temp = temp.removeprefix("<p>").removesuffix("</p>")
            return temp
        return temp


md = MyMarkdown()
