from django.contrib.admin import AdminSite


class CustomerAdminSite(AdminSite):
    site_header = "Customer Management Administration"
    site_title = "Customer Admin"
    index_title = "Customer Management Dashboard"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff


customer_admin_site = CustomerAdminSite(name="customer_admin")