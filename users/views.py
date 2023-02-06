from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.shortcuts import (
    redirect,
    render,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from assessments.models import Cretificate
from django.db.models import Prefetch
from .forms import (
    CustomLoginForm,
    DriversRegisterForm,
    RegisterForm,
    ForgetPasswordEmailCodeForm,
    ChangePasswordForm,
    OtpForm,
)
from .models import OtpCode, CustomUser
from .utils import (
    send_activation_code,
    send_reset_password_code,
)
from .decorators import only_authenticated_user, redirect_authenticated_user



User = get_user_model()

@only_authenticated_user
def home_view(request):
    return render(request, 'users/home.html')


@redirect_authenticated_user
def login_view(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username_or_email'], password=form.cleaned_data['password'])
            if user:
                if not user.is_active:
                    messages.warning(request, _(
                        f"It's look like you haven't still verify your email - {user.email}"))
                    return redirect('users:activate_email')
                else:
                    login(request, user)
                    return redirect('users:home')
            else:
                error = 'Invalid Credentials'
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form, 'error': error})


@only_authenticated_user
@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@redirect_authenticated_user
def registeration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.source = 'Register'
            user.save(True)

            code = get_random_string(20)
            otp = OtpCode(code=code, user=user)
            otp.save(True)
            try:
                send_activation_code(user.email, code)
            except:
                otp.delete()
                user.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(
                    request, _(f'We have sent a verification code to your email - {user.email}'))
                return redirect('users:activate_email')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def driver_registeration_view(request):
    if request.method == 'POST':
        form = DriversRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password('123456')
            user.test_active = True
            user.email = user.username
            user.full_name = user.username
            user.is_active = True
            user.source = 'Driver_Registeration'
            user.save()
            return redirect('users:driver_registeration_view')
    else:
        form = DriversRegisterForm()
    return render(request, 'users/driver_registr.html', {'form': form, 'custom': True})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        driver_category = request.POST.get('driver_category')
        contact = request.POST.get('contact')
        company = request.POST.get('company')
        nationality = request.POST.get('nationality')
        user = User.objects.create(username=username,driver_category=driver_category,contact=contact,company=company,nationality=nationality)
        user.set_password('123456')
        user.test_active = True
        user.email = username
        user.full_name = username
        user.is_active = True
        user.source = 'Driver_Registeration'
        user.save()
        # process the data and save to database
        print(username)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

@redirect_authenticated_user
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgetPasswordEmailCodeForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user = get_user_model().objects.get(**username_or_email)
            code = get_random_string(20)

            otp = OtpCode(code=code, user=user, email=user.email)
            otp.save()

            try:
                send_reset_password_code(user.email, code)
            except:
                otp.delete()
                messages.error(request, _('Failed while sending code!'))
            else:
                messages.success(request, _(
                    f"We've sent a passwrod reset otp to your email - {user.email}"))
                return redirect('users:reset_code')
    else:
        form = ForgetPasswordEmailCodeForm()
    return render(request, 'users/forgot_password.html', context={'form': form})

@redirect_authenticated_user
def check_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            user = otp.user
            otp.delete()
            user.is_active = True
            user.save()
            return redirect('users:login')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})

@redirect_authenticated_user
def check_reset_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            otp = OtpCode.objects.get(code=form.cleaned_data['otp'])
            request.session['email'] = otp.user.email
            messages.success(request, _(
                "Please create a new password that you don't use on any other site."))
            return redirect('users:reset_new_password')
    else:
        form = OtpForm()
    return render(request, 'users/user_otp.html', {'form': form})


@redirect_authenticated_user
def reset_new_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            email = request.session['email']
            del request.session['email']
            user = CustomUser.objects.get(email=email)
            user.password = make_password(form.cleaned_data["new_password2"])
            user.save()
            messages.success(request, _(
                "Your password changed. Now you can login with your new password."))
            return redirect('users:login')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/new_password.html', {'form': form})




def certificate_print(request):
    users = User.objects.all().order_by('-last_login').prefetch_related(
        Prefetch('certificate', queryset=Cretificate.objects.only('final_en_score', 'final_psyco_score')))
    if request.user.is_staff:
        return render(request, 'users/printing.html', {'users': users})
    return render(request, 'users/printing.html')

# def check_user_certificate(user):
#     if hasattr(user, 'certificate'):
#         return True
#     else:
#         return False
    
def user_search(request):
    search_value = request.GET.get('search', '')
    user_data = User.objects.filter(username__contains=search_value) \
                        .values('id', 'username', 'company__name', 'test_active', 'last_login', 'current_attempts', 'is_active') \
                        .prefetch_related('company')
    user_ids = [user['id'] for user in user_data]
    certificate_data = Cretificate.objects.filter(user_id__in=user_ids) \
                        .values('user_id', 'final_en_score', 'final_psyco_score')

    certificate_data_dict = {cert['user_id']: cert for cert in certificate_data}

    data = [{
        'username': user['username'],
        'company': user['company__name'],
        'status': user['test_active'],
        'last_login': user['last_login'],
        'final_en_score': certificate_data_dict.get(user['id'], {}).get('final_en_score', ''),
        'final_psyco_score': certificate_data_dict.get(user['id'], {}).get('final_psyco_score', ''),
        'current_attempts': user['current_attempts'],
        'is_active': user['is_active'],
    } for user in user_data]

    return JsonResponse(data, safe=False)
