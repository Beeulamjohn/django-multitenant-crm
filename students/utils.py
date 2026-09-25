from app.models import Company
from .models import AppearanceSettings


def get_user_company(user):

    if not user.is_authenticated:
        return None

    return Company.objects.filter(
        user=user
    ).first()


def appearance_settings_context(request):

    appearance = None
    company = None

    if request.user.is_authenticated:

        company = get_user_company(
            request.user
        )

        if company:

            appearance, created = (
                AppearanceSettings.objects.get_or_create(
                    company=company
                )
            )

    return {
        "appearance": appearance,
        "company": company,
    }