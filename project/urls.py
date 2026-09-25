from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from billing.admin_site import billing_admin_site
from customers.admin_site import customer_admin_site
from employees.admin_site import employee_admin_site
from salary.admin_site import salary_admin_site


urlpatterns = [

    # Django Default Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Custom Admin Sites
    path(
        "customer-admin/",
        customer_admin_site.urls
    ),

    path(
        "billing-admin/",
        billing_admin_site.urls
    ),

    path(
        "employee-admin/",
        employee_admin_site.urls
    ),

    path(
        "salary-admin/",
        salary_admin_site.urls
    ),

    # Main application
    path(
        "",
        include("app.urls")
    ),

    # Applications
    path(
        "students/",
        include("students.urls")
    ),

    path(
        "billing/",
        include("billing.urls")
    ),

    path(
        "customers/",
        include("customers.urls")
    ),

    path(
        "employees/",
        include("employees.urls")
    ),

    path(
        "salary/",
        include("salary.urls")
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )