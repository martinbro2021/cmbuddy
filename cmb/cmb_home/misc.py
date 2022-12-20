from cmb_home.models import File, Link, Snippet


def get_context(content_model, **kwargs) -> dict:
    context = \
        (content_model.get_context(**kwargs)) | \
        Link.get_context() | \
        Snippet.get_context() | \
        File.get_context()
    return context
