import logging
import time

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader

import cmb_contact.captcha_wrapper
import cmb_home.misc
from cmb_captcha.cmb_captcha import ProofOfWorkException
from cmb_contact.captcha_wrapper import is_valid_captcha
from cmb_contact.mail_wrapper import send_mail_wrapper
from cmb_contact.models import ContactContent

logger = logging.getLogger(__name__)
REDIRECT_TIME_DELTA = 30


def contact(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('contact.html')
    context = cmb_home.misc.get_context(ContactContent)
    context |= cmb_contact.captcha_wrapper.get_context()

    if request.method == "GET":
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        try:
            captcha_validation = "valid" if is_valid_captcha(request.POST.dict()) else "invalid"
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
            send_mail_wrapper(request.POST)
            return redirect("send-success", timestamp_str=hex(int(time.time()))[2:])
    else:
        return HttpResponseBadRequest()


def success(request: HttpRequest, timestamp_str: str) -> HttpResponse:
    try:
        timestamp = int(timestamp_str, base=16)
        if time.time() - timestamp > REDIRECT_TIME_DELTA:
            return redirect("home")
    except Exception as ex:
        logger.warning(ex)
        return redirect("home")
    template = loader.get_template('success.html')
    context = cmb_home.misc.get_context(ContactContent, reference='/contact/success')
    return HttpResponse(template.render(context, request))
