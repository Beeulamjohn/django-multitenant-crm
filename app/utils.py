from .models import Company
from django.shortcuts import get_object_or_404


def get_company(request):

    if not request.user.is_authenticated:
        return None

    if request.user.is_superuser:
        return None

    return Company.objects.filter(
        user=request.user
    ).first()