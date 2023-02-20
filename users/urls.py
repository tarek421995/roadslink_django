from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.view import about_page, contact_page
from .views import (
    certificate_print,
    downalod_invoice,
    edit_driver_username,
    edit_profile,
    generate_company_invoice,
    generate_user_invoice,
    get_agents,
    get_companies,
    home_view,
    login_view,
    logout_view,
    forgot_password_view,
    register,
    registeration_view,
    check_otp_view,
    check_reset_otp_view,
    reset_new_password_view,
    user_search,

)

app_name = 'users'

urlpatterns = [
    path('', home_view, name='home'),
    path('contact/',contact_page, name='contact'),
    path('about/',about_page, name='about'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registeration_view, name='register'),
    path('list-users/', certificate_print, name='certificate_print'),
    path('user_search/', user_search, name='user_search'),
    path('get-companies/', get_companies, name='get-companies'),
    path('get-agent/', get_agents, name='get-agents'),
    path('invoices/<int:user_id>/<int:company_id>/generate/', generate_user_invoice, name='generate_invoice'),
    path('generate-invoices/', generate_company_invoice, name='generate_company_invoice'),
    path('invoices/<int:id>/downloads/', downalod_invoice, name='download_invoice'),
    # path('driver_edit/<str:username>/', edit_driver,
    #      name='driver_edit'),
    path('driver/', register,
         name='driver_registeration_view'),
    path('edit_driver_username/<int:id>/', edit_driver_username,
         name='edit_driver_username'),
    
    path('edit/', edit_profile, name='edit_profile'),

    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('activate-email/', check_otp_view, name='activate_email'),
    path('reset-code/', check_reset_otp_view, name='reset_code'),
    path('new-password/', reset_new_password_view, name='reset_new_password'),
        # path('ledger/', include('django_ledger.urls', namespace='django_ledger')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
