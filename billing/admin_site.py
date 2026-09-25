from django.contrib.admin import AdminSite


class BillingAdminSite(AdminSite):

    site_header = "Billing Management Administration"
    site_title = "Billing Admin"
    index_title = "Billing Dashboard"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff



billing_admin_site = BillingAdminSite(name="billing_admin")