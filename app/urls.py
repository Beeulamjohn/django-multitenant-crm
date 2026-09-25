from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),
    path( "forgot-password/", views.forgot_password, name="forgot_password" ), 
    path( "reset-password/<int:user_id>/<str:token>/", views.reset_password, name="reset_password" ),
    path(
        "get/",
        views.get,
        name="get"
    ),
    path("start-trial/", views.start_trial, name="start_trial"),
    path(
    "professional-checkout/",
    views.professional_checkout,
    name="professional_checkout",
),
    path(
        "contact-sales/",
        views.contact_sales,
        name="contact_sales",
    ),
    path("admin-login/", views.admin_login, name="admin_login"),
path("staff-login/", views.staff_login, name="staff_login"),
path(
    "student-portal/",
    views.student_portal,
    name="student_portal"
    
),


path("features/", views.features, name="features"),

]