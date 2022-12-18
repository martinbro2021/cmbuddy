import logging
import time

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import redirect

import cmb_home.views
import cmb_contact.captcha_wrapper
from cmb_captcha.cmb_captcha import ProofOfWorkException
from cmb_contact.captcha_wrapper import is_valid_captcha

logger = logging.getLogger(__name__)
REDIRECT_TIME_DELTA = 10


def contact(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('contact.html')
    context = cmb_home.views.get_context('contact')
    context |= cmb_contact.captcha_wrapper.get_context()

    if request.method == "GET":
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        try:
            captcha_validation = "valid" if is_valid_captcha(request.POST) else "invalid"
        except ProofOfWorkException:
            return HttpResponseBadRequest()

        try:
            email_validation = ""
            validate_email(request.POST["email"])
        except ValidationError:
            email_validation = "invalid"

        if email_validation == "invalid" or captcha_validation == "invalid":
            context |= {
                "validation": {
                    "captcha": captcha_validation,
                    "email": email_validation,
                }
            }
            context |= {"user": request.POST}
            return HttpResponse(template.render(context, request))
        else:
            return redirect("send-success", timestamp=hex(int(time.time()))[2:])
    else:
        return HttpResponseBadRequest()


def success(request: HttpRequest, timestamp: str) -> HttpResponse:
    try:
        timestamp = int(timestamp, base=16)
        if time.time() - timestamp > REDIRECT_TIME_DELTA:
            return redirect("home")
    except Exception as ex:
        logger.warning(ex)
        return redirect("home")
    template = loader.get_template('success.html')
    context = cmb_home.views.get_context('contact/success')
    return HttpResponse(template.render(context, request))
