from django.contrib.admin import AdminSite

class EmployeeAdminSite(AdminSite):
    site_header = "Employee Admin"
    site_title = "Employee Admin"
    index_title = "Employee Dashboard"

employee_admin_site = EmployeeAdminSite(name="employee_admin")