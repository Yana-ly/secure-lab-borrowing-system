from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="equipment:dashboard", permanent=False)),
    path("SSDProject/", include("equipment.urls")),
    path("SSDProject/accounts/", include("accounts.urls")),
    path("SSDProject/audit/", include("audit.urls")),
]

handler403 = "accounts.views.permission_denied_view"
handler404 = "accounts.views.not_found_view"
handler500 = "accounts.views.server_error_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
