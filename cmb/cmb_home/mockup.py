import importlib
import logging
import tempfile
from pathlib import Path

from django.core.files import File as DjangoFile

from cmb_utils.misc import to_snake_case_upper

BASE_DIR = Path(__file__).resolve().parent.parent
AUTO_IMPORT_FROM = ["cmb_contact", "cmb_home"]

logger = logging.getLogger(__name__)


class NoMockupException(Exception):
    pass


def auto_import(cls) -> dict:
    """Imports mockup data from the given paths automatically."""
    imports = {}
    for name in AUTO_IMPORT_FROM:
        try:
            module = importlib.import_module(f"{name}.mockups", package=None)
            imports |= getattr(module, to_snake_case_upper(cls.__name__) + "_MOCKUP")
        except (ModuleNotFoundError, AttributeError) as ex:
            logger.info(str(ex))
    return imports


def mockup_snippets(cls) -> bool:
    """Adds mockup data for snippet model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            s = cls(key=k, value=v)
            s.save()
        return True
    return False


def mockup_settings(cls) -> bool:
    """Adds mockup data for setting model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            s = cls(key=k, value=v)
            s.save()
        return True
    return False


def mockup_links(cls) -> bool:
    """Adds mockup data for link model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for k, v in mocks.items():
            link = cls(target=k, url=v)
            link.save()
        return True
    return False


def mockup_menu_entries(cls) -> bool:
    """Adds mockup data for the menu entry model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException

    if cls.objects.count() == 0:
        for _, entry in mocks.items():
            menu_entry = cls()
            for key, value in entry.items():
                if not hasattr(menu_entry, key):
                    logger.warning(f"Unknown key: {cls.__name__}.{key}")
                setattr(menu_entry, key, value)
            menu_entry.save()
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


def mockup_files(cls) -> bool:
    """Adds mockup data for file model."""
    mocks = auto_import(cls)
    if not mocks:
        raise NoMockupException
    FILE_PATH = BASE_DIR / "mockup_files/"

    if cls.objects.count() == 0:
        for identifier, entry in mocks.items():
            file_name = entry["file_name"]
            temp = tempfile.NamedTemporaryFile(dir=FILE_PATH)
            with open(FILE_PATH / file_name, "rb") as file:
                temp.write(file.read())
                file_instance = cls()
                file_instance.identifier = identifier
                file_instance.description = entry["description"]
                file_instance.file = DjangoFile(temp, name=file_name)
                file_instance.save()
            temp.close()
        return True
    return False
