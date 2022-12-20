import importlib
import logging

from django.core.files import File as DjangoFile

from cmb_sample.settings import BASE_DIR

logger = logging.getLogger(__name__)
AUTO_IMPORT = ["cmb_contact", "cmb_home"]


class NoMockupException(Exception):
    pass


def auto_import(cls) -> dict:
    """Imports mockup data from the given paths automatically."""
    imports = {}
    for name in AUTO_IMPORT:
        try:
            module = importlib.import_module(f"{name}.mockups", package=None)
            imports |= getattr(module, cls.__name__.upper() + "_MOCKUP")
        except (ModuleNotFoundError, AttributeError) as ex:
            logger.info(str(ex))
    return imports


def mockup_snippets(cls):
    """Adds mockup data for snippet model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            s = cls()
            s.key, s.value = k, v
            s.save()
        return True
    return False


def mockup_settings(cls):
    """Adds mockup data for setting model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            s = cls()
            s.key, s.value = k, v
            s.save()
        return True
    return False


def mockup_links(cls):
    """Adds mockup data for link model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            link = cls()
            link.target, link.url = k, v
            link.save()
        return True
    return False


def mockup_content(cls) -> bool:
    """Adds mockup data for the content model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for _, entry in mocks.items():
            content = cls()
            for key, value in entry.items():
                if not hasattr(content, key):
                    logger.warning(f"Unknown key: {cls.__name__}.{key}")
                setattr(content, key, value)
            content.save()
        return True
    return False


def mockup_files(cls):
    """Adds mockup data for file model."""
    # todo add auto import mockups
    if cls.objects.count() == 0:
        file_object = cls()
        with open(BASE_DIR / "media/sample_portrait.jpg", "rb") as file:
            file_object.file = DjangoFile(file)
            file_object.identifier = "portrait_01"
            file_object.save()
        return True
    return False
