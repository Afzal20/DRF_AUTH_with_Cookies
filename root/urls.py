from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# setuping schema
schema_view = get_schema_view (
    openapi.Info (
        title="Django Authentications", 
        default_version="V1", 
        description="This API is for authenticate users",
    ),
    public=True, 
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path('auth/', include('Accounts.urls'))
]
