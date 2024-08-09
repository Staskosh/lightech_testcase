from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from payments_api import views


schema_view = get_schema_view(
    openapi.Info(
        title="Payments API",
        default_version='v1',
        description="API документация для Payments API",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page, name='start_page'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('api/', include('payments_api.urls', namespace='payments_api')),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
