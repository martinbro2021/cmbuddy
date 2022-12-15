import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import Content, Link, File, Snippet

logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
def get_context(reference="") -> dict:
    context = \
        (Content.get_context(reference)) | \
        Link.get_context() | \
        Snippet.get_context() | \
        File.get_context()
    return context


def home(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('home.html')
    return HttpResponse(template.render(get_context("home"), request))


def home_redirect(_) -> HttpResponse:
    return redirect('home', permanent=True)
