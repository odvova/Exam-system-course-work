from django.contrib import admin
from django.http import Http404

class HodOrSuperuserAdminSite(admin.AdminSite):
    site_header = "Admin"
    site_title  = "Admin"
    index_title = "Administration"

    def has_permission(self, request):
        u = request.user
        return u.is_authenticated and u.is_active and (
            u.is_superuser or u.groups.filter(name="hod").exists()
        )

    def login(self, request, extra_context=None):
        if not self.has_permission(request):
            raise Http404("Page not found")
        return super().login(request, extra_context=extra_context)