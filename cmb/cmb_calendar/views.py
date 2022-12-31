from datetime import date

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.template import loader

from cmb_calendar.models import CalendarEntry
from cmb_home.misc import get_context

MAX_YEAR = date.today().year + 10
MIN_YEAR = date.today().year - 10


def calendar(request: HttpRequest, year) -> HttpResponse:
    if not MIN_YEAR <= year <= MAX_YEAR:
        return HttpResponseNotFound()

    template = loader.get_template('calendar.html')
    context = get_context(CalendarEntry, year=year)
    context["links"] |= {
        "curr_year": {
            "value": year,
            "url": f"/calendar/{year}"},
        "next_year": {
            "value": min(year + 1, MAX_YEAR),
            "url": f"/calendar/{min(year + 1, MAX_YEAR)}",
        },
        "prev_year": {
            "value": max(year - 1, MIN_YEAR),
            "url": f"/calendar/{max(year - 1, MIN_YEAR)}",
        }
    }
    return HttpResponse(template.render(context, request))


def calendar_redirect(_) -> HttpResponse:
    return redirect('calendar', year=date.today().year)
