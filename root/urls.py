from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


# setuping schema
schema_view = get_schema_view (
    openapi.Info (
        title="Django Rest Framework", 
        default_version="0.0.1", 
        description="This API is for authenticate users",
    ),
    public=True, 
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path('accounts/', include('Accounts.urls'), name='account_uers')
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    