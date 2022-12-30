from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template import loader

from cmb_calendar.models import CalendarEntry
from cmb_home.misc import get_context


def calendar(request: HttpRequest, year) -> HttpResponse:
    template = loader.get_template('calendar.html')
    context = get_context(CalendarEntry, year=year)
    context["links"] |= {
        "curr_year": {
            "value": year,
            "url": f"/calendar/{year}"},
        "next_year": {
            "value": year+1,
            "url": f"/calendar/{year+1}",
        },
        "prev_year": {
            "value": year-1,
            "url": f"/calendar/{year-1}",
        }
    }
    return HttpResponse(template.render(context, request))


def calendar_redirect(_) -> HttpResponse:
    return redirect('calendar', year=date.today().year)
