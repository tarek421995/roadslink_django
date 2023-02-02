from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    certificate_print,
    home_view,
    login_view,
    logout_view,
    forgot_password_view,
    registeration_view,
    check_otp_view,
    check_reset_otp_view,
    reset_new_password_view,
    driver_registeration_view,
    user_search,
)

app_name = 'users'

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registeration_view, name='register'),
    path('list-users/', certificate_print, name='certificate_print'),
    path('user_search/', user_search, name='user_search'),
    path('driver-register/', driver_registeration_view,
         name='driver_registeration_view'),

    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('activate-email/', check_otp_view, name='activate_email'),
    path('reset-code/', check_reset_otp_view, name='reset_code'),
    path('new-password/', reset_new_password_view, name='reset_new_password'),
        path('ledger/', include('django_ledger.urls', namespace='django_ledger')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
