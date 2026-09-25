from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.student_list,
        name="student_list"
    ),

    path(
        "create/",
        views.student_create,
        name="student_create"
    ),

    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail"
    ),

    path(
        "<int:pk>/update/",
        views.student_update,
        name="student_update"
    ),

    path(
        "<int:pk>/delete/",
        views.student_delete,
        name="student_delete"
    ),

    path(
        "documents/",
        views.student_documents,
        name="student_documents"
    ),

    path(
        "documents/<int:pk>/",
        views.upload_document,
        name="upload_document"
    ),

    
    path(
        "management/",
        views.student_management,
        name="student_management"
    ),

    path(
        "dashboard/",
        views.company_dashboard,
        name="company_dashboard",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
    path(
    "staff/",
    views.staff_list,
    name="staff_list"
    ),
    path(
    "staff/add/",
    views.add_staff,
    name="add_staff"
),
   path(
    "courses/",
    views.course_list,
    name="course_list"
),
path(
    "courses/add/",
    views.add_course,
    name="add_course"
),

path(
    "staff/<int:pk>/edit/",
    views.edit_staff,
    name="edit_staff",
),

path(
    "staff/<int:pk>/delete/",
    views.delete_staff,
    name="delete_staff",
),

path(
    "courses/<int:pk>/edit/",
    views.edit_course,
    name="edit_course"
),

path(
    "courses/<int:pk>/delete/",
    views.delete_course,
    name="delete_course"
),
path(
        "student-report/",
        views.student_report,
        name="student_report"
    ),


    path(
        "settings/",
        views.company_settings,
        name="company_settings"
    ),

   

    path(
        "settings/company-profile/",
        views.company_profile,
        name="company_profile"
    ),

    path(
        "account/settings/",
        views.account_settings,
        name="account_settings"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

    path(
        "logout-all-devices/",
        views.logout_all_devices,
        name="logout_all_devices"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "account/profile/",
        views.account_profile,
        name="account_profile"
    ),
    path(
        "settings/employees/",
        views.student_employee_settings,
        name="student_employee_settings"
    ),


    path(
        "settings/students/",
        views.student_settings,
        name="student_settings"
    ),

  

    path(
        "settings/notifications/",
        views.notification_settings,
        name="notification_settings"
    ),


    path(
        "settings/appearance/",
        views.appearance_settings,
        name="appearance_settings"
    ),

  

    path(
        "settings/reports/",
        views.report_settings,
        name="report_settings"
    ),

    
]