"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static

from core.view import TotalProductSales
# from .admin_site import admin_site
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
    re_path(r'^report_builder/', include('report_builder.urls')),
    path('', include('users.urls', namespace="users")),
    path('assessments/', include('assessments.urls', namespace="assessments")),
    path("data-browser/", include("data_browser.urls")),
    path('report/', TotalProductSales.as_view()),
    path('ledger/', include('django_ledger.urls', namespace='django_ledger')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
