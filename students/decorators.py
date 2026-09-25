from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Company


DASHBOARD_MAP = {
    "education": "company_dashboard",
    "billing": "billing_dashboard",
    "customer": "product_dashboard",
    "employee": "employee_dashboard",
    "salary": "salary_dashboard",
}


def company_type_required(required_type):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            try:
                company = Company.objects.get(
                    user=request.user
                )

            except Company.DoesNotExist:

                messages.error(
                    request,
                    "Company not found."
                )

                return redirect("login")

            if company.company_type != required_type:

                messages.error(
                    request,
                    "You cannot access another company module."
                )

                dashboard = DASHBOARD_MAP.get(
                    company.company_type
                )

                if dashboard:
                    return redirect(dashboard)

                return redirect("login")

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator