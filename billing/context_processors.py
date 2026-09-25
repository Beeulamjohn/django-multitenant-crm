from .models import BillingAppearanceSettings
from .utils import get_user_company




def billing_appearance_settings_context(request):

    billing_appearance = None

    if request.user.is_authenticated:

        company = get_user_company(
            request.user
        )

        if (
            company is not None
            and company.company_type == "billing"
        ):

            billing_appearance, created = (
                BillingAppearanceSettings.objects
                .get_or_create(
                    company=company
                )
            )

    return {
        "billing_appearance": billing_appearance
    }


