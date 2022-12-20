from django.core.mail import send_mail

from cmb_home.models import Setting


def send_mail_wrapper(post):
    # noinspection PyUnresolvedReferences
    recipients = [address.strip() for address in Setting.objects.get(key="contact_email_recipients").value.split(",")]
    print("will send", post)
    print("to", recipients)
    send_mail(
        post["subject"],
        post["message"],
        None,
        recipients,
        fail_silently=False)
