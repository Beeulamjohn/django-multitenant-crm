from django.contrib.admin import AdminSite


class StudentAdminSite(AdminSite):
    site_header = "Student Administration"
    site_title = "Student Admin"
    index_title = "Student Dashboard"


student_admin_site = StudentAdminSite(name="student_admin")