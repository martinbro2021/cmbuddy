from .models import Content, File, Link, Snippet


def get_context(reference="") -> dict:
    context = \
        (Content.get_context(reference)) | \
        Link.get_context() | \
        Snippet.get_context() | \
        File.get_context()
    return context
