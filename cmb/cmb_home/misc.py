from cmb_home.models import File, Link, Snippet, MenuEntry


def get_context(content_model, **kwargs) -> dict:
    context = \
        (content_model.get_context(**kwargs)) | \
        Link.get_context() | \
        Snippet.get_context() | \
        File.get_context() | \
        MenuEntry.get_context()
    return context
