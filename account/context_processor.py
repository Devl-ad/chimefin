from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .models import Kyc


def kyc_status(request):
    if not request.user.is_authenticated:
        return {}

    try:
        kyc = Kyc.objects.get(user=request.user)
        return {
            "kyc_exists": True,
            "kyc_status": kyc.status,
            "kyc_approved": kyc.is_approved,
        }
    except Kyc.DoesNotExist:
        return {
            "kyc_exists": False,
            "kyc_status": None,
            "kyc_approved": False,
        }
