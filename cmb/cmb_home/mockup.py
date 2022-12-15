import importlib
import logging

from django.core.files import File as DjangoFile

from cmb_sample.settings import BASE_DIR

logger = logging.getLogger(__name__)
AUTO_IMPORT = ["cmb_contact", "cmb_home"]


def auto_import(cls) -> dict:
    """Imports mockup data from the given paths automatically."""
    imports = {}
    for name in AUTO_IMPORT:
        try:
            module = importlib.import_module(f"{name}.mockups", package=None)
            imports |= getattr(module, cls.__name__.upper() + "_MOCKUP")
        except ModuleNotFoundError | AttributeError as ex:
            logger.warning(ex.__class__.__name__ + str(ex))
    return imports


def mockup_snippets(cls):
    """Adds mockup data for snippet model."""
    if cls.objects.count() == 0:
        mocks = auto_import(cls)
        for k, v in mocks.items():
            s = cls()
            s.key, s.value = k, v
            s.save()
        return True
    return False


def mockup_links(cls):
    """Adds mockup data for link model."""
    if cls.objects.count() == 0:
        mocks = auto_import(cls)
        for k, v in mocks.items():
            link = cls()
            link.target, link.url = k, v
            link.save()
        return True
    return False


def mockup_files(cls):
    """Adds mockup data for file model."""
    if cls.objects.count() == 0:
        file_object = cls()
        with open(BASE_DIR / "media/sample_portrait.jpg", "rb") as file:
            file_object.file = DjangoFile(file)
            file_object.identifier = "portrait_01"
            file_object.save()
        return True
    return False


def mockup_content(cls) -> bool:
    """Adds mockup data for the content model."""
    if cls.objects.count() == 0:
        mocks = auto_import(cls)
        for _, entry in mocks.items():
            content = cls()
            content.header = entry["header"]
            content.text = entry["text"]
            content.reference = entry["reference"]
            content.save()
        return True
    return False


def mockup_reference(cls) -> bool:
    """Adds mockup data for reference model."""
    if cls.objects.count() == 0:
        mocks = auto_import(cls)
        for _, ref in mocks.items():
            reference = cls()
            reference.name = ref
            reference.save()
        return True
    return False
