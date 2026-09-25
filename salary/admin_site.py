from django.contrib.admin import AdminSite


class SalaryAdminSite(AdminSite):
    site_header = "Salary Management Administration"
    site_title = "Salary Admin"
    index_title = "Salary Management Dashboard"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


salary_admin_site = SalaryAdminSite(name="salary_admin")