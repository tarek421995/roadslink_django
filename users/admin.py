import json
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
from .models import AgentCategory, CompanyCategory, Contact, Cretificate, DriverAge, DriverCategory, DriverNationality, Invocies, InvociesFile, OtpCode
from django.contrib import admin

# Register your models here.
from .models import (
    CustomUser,
)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords are not match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.source = 'adminsite'
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput)

    class Meta:
        model = CustomUser
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# admin.py
def my_convert_function(value):
    if (value == 'convert'):
        return True, 'converted'
    elif (type(value) == list):
        return json.dumps(value)
    return False, None

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        'id',
        'username',
        'email',
        'last_login',
        'date_joined',
        'source',
    )
    fieldsets = (
        (None, {'fields': ('username','full_name','company','agents','driver_category','nationality', 'email', 'password')}),
        (_('Personal info'), {
         'fields': ('bio', 'current_attempts', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('is_active', 'test_active','is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display_links = ('id', 'username')
    ordering = ('-id',)



admin.site.register(CompanyCategory)
admin.site.register(DriverCategory)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OtpCode)
admin.site.register(Contact)
admin.site.register(DriverAge)
admin.site.register(DriverNationality)

admin.site.register(InvociesFile)

admin.site.register(AgentCategory)

admin.site.register(Invocies)
admin.site.register(Cretificate)




