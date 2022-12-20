import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template import loader

from cmb_home.misc import get_context

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('home.html')
    return HttpResponse(template.render(get_context("home"), request))


def home_redirect(_) -> HttpResponse:
    return redirect('home')
