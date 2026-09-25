from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from employees.models import Employee
from .models import Company
from .models import SubscriptionPlan, CompanySubscription, Company
from django.utils import timezone
from datetime import timedelta
from .models import ContactSales
from django.db import transaction
from django.contrib.auth.tokens import default_token_generator




def home(request):
    return render(request, "home.html")



DASHBOARD_MAP = {
    "education": "company_dashboard",
    "billing": "billing_dashboard",
    "customer": "product_dashboard",
    "employee": "employee_dashboard",
    "salary": "salary_dashboard",
}



def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )


        if not username or not password:

            return render(
                request,
                "login.html",
                {
                    "error": "Please enter username and password."
                }
            )


        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid username or password."
                }
            )

        try:

            company = Company.objects.get(
                user=user
            )

        except Company.DoesNotExist:

            messages.error(
                request,
                "No company is linked to this account."
            )

            return redirect("login")

        if not company.is_active:

            messages.error(
                request,
                "Your company account is inactive."
            )

            return redirect("login")


        dashboard = DASHBOARD_MAP.get(
            company.company_type
        )

        if not dashboard:

            messages.error(
                request,
                "Invalid company type."
            )

            return redirect("login")


        login(
            request,
            user
        )

        return redirect(
            dashboard
        )

    return render(
        request,
        "login.html"
    )

def register(request):

    if request.method == "POST":

        company_name = request.POST.get("company_name", "").strip()
        company_type = request.POST.get("company_type", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        plan = request.POST.get("plan", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # -----------------------------
        # REQUIRED FIELD VALIDATION
        # -----------------------------

        if not company_name:
            messages.error(request, "Company name is required.")
            return redirect("register")

        if not full_name:
            messages.error(request, "Company admin name is required.")
            return redirect("register")

        if not company_type:
            messages.error(request, "Please select a business module.")
            return redirect("register")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if not email:
            messages.error(request, "Business email is required.")
            return redirect("register")

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("register")

        if not plan:
            messages.error(request, "Please select a subscription plan.")
            return redirect("register")

        if not password:
            messages.error(request, "Password is required.")
            return redirect("register")

        if not confirm_password:
            messages.error(request, "Please confirm your password.")
            return redirect("register")

        # -----------------------------
        # VALIDATE COMPANY TYPE
        # -----------------------------

        valid_company_types = dict(Company.COMPANY_TYPES)

        if company_type not in valid_company_types:
            messages.error(request, "Invalid business module.")
            return redirect("register")

        # -----------------------------
        # VALIDATE PLAN
        # -----------------------------

        valid_plans = [
            "Starter",
            "Professional",
            "Enterprise",
        ]

        if plan not in valid_plans:
            messages.error(request, "Invalid subscription plan.")
            return redirect("register")

        # -----------------------------
        # PASSWORD CHECK
        # -----------------------------

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return redirect("register")

        # -----------------------------
        # USERNAME CHECK
        # -----------------------------

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists. Please choose another username."
            )

            return redirect("register")

        # -----------------------------
        # EMAIL CHECK
        # -----------------------------

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "Email already exists. Please use another email."
            )

            return redirect("register")

        # -----------------------------
        # COMPANY CHECK
        # -----------------------------

        if Company.objects.filter(
            company_name__iexact=company_name
        ).exists():

            messages.error(
                request,
                "Company name already exists. Please use another company name."
            )

            return redirect("register")

        # -----------------------------
        # CREATE ACCOUNT
        # -----------------------------

        try:

            with transaction.atomic():

                # Create Django User
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=full_name,
                )

                # Create Company
                company = Company.objects.create(
                    user=user,
                    company_name=company_name,
                    full_name=full_name,
                    phone=phone,
                    company_type=company_type,
                    role="company_admin",
                    is_active=True,
                )

                # Find selected subscription plan
                subscription_plan = SubscriptionPlan.objects.filter(
                    name=plan
                ).first()

                # If plan does not exist, create it
                if subscription_plan is None:

                    subscription_plan = SubscriptionPlan.objects.create(
                        name=plan
                    )

                # Create company subscription
                CompanySubscription.objects.create(
                    company=company,
                    plan=subscription_plan,
                    is_trial=True,
                    is_active=True,
                )

            messages.success(
                request,
                "Registration successful. Please log in."
            )

            return redirect("login")

        except Exception as e:

            print("REGISTRATION ERROR:", e)

            messages.error(
                request,
                f"Registration failed: {e}"
            )

            return redirect("register")

    return render(
        request,
        "register.html"
    )



def forgot_password(request):

    reset_link = None

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            # Generate Django's built-in reset token
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                f"/reset-password/{user.pk}/{token}/"
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "No account was found with this email address."
            )

    return render(
        request,
        "forgot.html",
        {
            "reset_link": reset_link
        }
    )


def reset_password(request, user_id, token):

    user = get_object_or_404(User, pk=user_id)

    # Check whether token is valid
    if not default_token_generator.check_token(user, token):

        messages.error(
            request,
            "This password reset link is invalid or has expired."
        )

        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password:

            messages.error(
                request,
                "Please enter a new password."
            )

        elif password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

        elif len(password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

        else:

            user.set_password(password)
            user.save()

            messages.success(
                request,
                "Your password has been changed successfully."
            )

            return redirect("login")

    return render(
        request,
        "reset_password.html"
    )

def get(request):
    return render(request, "get.html")


@login_required
def start_trial(request):

    company = request.user.company

    plan = get_object_or_404(
        SubscriptionPlan,
        name="Starter"
    )

    CompanySubscription.objects.update_or_create(
        company=company,
        defaults={
            "plan": plan,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=plan.trial_days),
            "is_trial": True,
            "is_active": True,
        }
    )

    messages.success(
        request,
        "Your 14-day free trial has started."
    )

    return redirect("register")

@login_required
def professional_checkout(request):

    company = request.user.company

    plan = get_object_or_404(
        SubscriptionPlan,
        name="Professional"
    )

    CompanySubscription.objects.update_or_create(
        company=company,
        defaults={
            "plan": plan,
            "start_date": timezone.now().date(),
            "end_date": timezone.now().date() + timedelta(days=365),
            "is_trial": False,
            "is_active": True,
        }
    )

    messages.success(
        request,
        "Professional plan activated successfully."
    )

    return redirect("register")

def contact_sales(request):

    if request.method == "POST":

        ContactSales.objects.create(
            name=request.POST.get("name"),
            company=request.POST.get("company"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            employees=request.POST.get("employees"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "Thank you! Our sales team will contact you within 24 hours."
        )

        return redirect("contact_sales")

    return render(request, "contact_sales.html")



def admin_login(request):
    if request.method == "POST":
        print("POST received")

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("Authenticated user:", user)

        if user is not None:
            print("is_staff:", user.is_staff)
            print("is_superuser:", user.is_superuser)

        if user is not None and user.is_staff:
            login(request, user)
            print("Login successful")
            return redirect("/admin/")

        print("Login failed")

        return render(
            request,
            "admin_login.html",
            {
                "error": "Invalid username/password or not a staff user."
            }
        )

    return render(request, "admin_login.html")


def staff_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("company_dashboard")

        return render(request, "staff_login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "staff_login.html")


def student_portal(request):
    return render(request, "student_portal.html")

def features(request):
    return render(request, "features.html")