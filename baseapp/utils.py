import random
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.utils.http import urlsafe_base64_decode
from django.core.cache import cache
from django.utils.encoding import force_str
from datetime import timedelta

from uuid import uuid4
import qrcode
from django.core.mail import EmailMessage
from django.template.loader import get_template
from io import BytesIO


import pyotp

from base64 import b64encode


def generate_totp_secret():
    return pyotp.random_base32()


def generate_qr_code(secret, user):
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        user.username, issuer_name="Bank"
    )

    img = qrcode.make(totp_uri)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    encoded_img = b64encode(buffer.read()).decode()
    qr_code = f"data:image/png;base64,{encoded_img}"
    return qr_code


EMAIL_ADMIN = settings.DEFAULT_FROM_EMAIL
D = "deposit"
W = "withdraw"


def gen_random_number():
    return str(random.randint(1000000000, 9999999999))


def gen_random_code(len):
    code = str(uuid4()).replace(" ", "-").upper()[:len]
    return code


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[-1].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_next_destination(request):
    next = None
    if request.GET.get("next"):
        next = str(request.GET.get("next"))
    return next


def trans_code():
    code = str(uuid4()).replace(" ", "-").upper()[:8]
    return code


def send_mail(subject, context, to_email, template):
    message = get_template(template).render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_ADMIN,
        to=to_email,
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)


def checkToken(token, k):

    try:
        email = force_str(urlsafe_base64_decode(token))
        ke_y = f"{k}-{email}"
    except:
        ke_y = None
    if ke_y is not None:
        data = cache.get(ke_y)
        if data:
            return True
    return False


def getToken(verifyToken, k):
    """
    This fuction must be called only when the token has been verified
    """

    email = force_str(urlsafe_base64_decode(verifyToken))
    ke_y = f"{k}-{email}"

    data = cache.get(ke_y)

    return [data, ke_y]


STATUS = {
    "PENDING": "PENDING",
    "SUCCESS": "SUCCESS",
    "DECLINED": "DECLINED",
}

TX_TYPE = {"LO": "Local transfer", "DO": "Domestic transfer", "IN": "International"}


def alertTx(transaction, current_site, subject, status, to_email, name):
    context = {
        "name": name,
        "domain": current_site.domain,
        "tx": transaction,
        "ty_pe": status,
    }
    message = get_template("superuser/txprocess.email.html").render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_ADMIN,
        to=[to_email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)


def ref_code():
    code = str(uuid4()).replace(" ", "-").upper()[:8]
    return code
