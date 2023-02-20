from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from users.models import CustomUser, OtpCode
User = get_user_model()


class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        if "@" in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        else:
            data = {'username': username_or_email}
        try:
            get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                _('This {} does not exist'.format(list(data.keys())[0])))
        else:
            return username_or_email


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "repeat password", "class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email address is already exists.")
        return email

    class Meta:
        model = get_user_model()
        fields = ("username", "email")


# class DriversRegisterForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(DriversRegisterForm, self).__init__(*args, **kwargs)

#         self.fields['username'].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields['company'].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields['email'].widget = widgets.EmailInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields['first_name'].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields['last_name'].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields[].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})
#         self.fields['nationality'].widget = widgets.TextInput(attrs={'autocomplete': 'off', 'autocorrect': 'off', 'autocapitalize': 'off', 'spellcheck': 'false'})

#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if get_user_model().objects.filter(email=email).exists():
#             raise ValidationError("This email address is already exists.")
#         return email


# class DriversRegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'driver_category', 'contact',
#                   'final_score', 'company', 'nationality']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['class'] = 'form-control'
#         self.fields['username'].widget.attrs['placeholder'] = 'Username'
#         self.fields['driver_category'].widget.attrs['class'] = 'form-control'
#         self.fields['driver_category'].widget.attrs['placeholder'] = 'Driver Category'
#         self.fields['contact'].widget.attrs['class'] = 'form-control'
#         self.fields['contact'].widget.attrs['placeholder'] = 'Contact Information'
#         self.fields['company'].widget.attrs['class'] = 'form-control'
#         self.fields['company'].widget.attrs['placeholder'] = 'Company'
#         self.fields['nationality'].widget.attrs['class'] = 'form-control'
#         self.fields['nationality'].widget.attrs['placeholder'] = 'Nationality'

# class DriverEditForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username',
#             'full_name',
#             'driver_category',
#             'contact',
#             'company',
#             'nationality',
#             'test_active'
#         ]
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Username'}),
#             'full_name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Full Name'}),
#             'driver_category': forms.Select(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Driver Category'}),
#             'contact': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Contact'}),
#             'company': forms.Select(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Company'}),
#             'nationality': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Nationality'}),
#             'test_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
#         }


class DriversRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'source',
            'contact',
            'company',
            'nationality',
            'offical_ID_number',
            'age',
            'test_active'
        ]

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'bio'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Full Name'}),
            'offical_ID_number': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'offical ID number'}),
            'driver_category': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Driver Category'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control',  'placeholder': 'Contact'}),
            'company': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Company'}),
            'nationality': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Nationality'}),
            'age': forms.Select(attrs={'class': 'form-control',  'placeholder': 'age'}),
            'source': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'source'}),
        }

        def clean_username(self):
            username = self.cleaned_data['username']
            if get_user_model().objects.filter(username=username).exists():
                raise ValidationError("This username is already taken.")
            return username

        def clean_full_name(self):
            full_name = self.cleaned_data['full_name']
            if get_user_model().objects.filter(full_name=full_name).exists():
                raise ValidationError("This full_name is already taken.")
            return full_name

        def clean_contact(self):
            contact = self.cleaned_data['contact']
            if get_user_model().objects.filter(contact=contact).exists():
                raise ValidationError("This contact number is already taken.")
            return contact


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name',
            'profile_picture',
            'bio',
            'source',
            'contact',
            'company',
            'nationality',
            'offical_ID_number',
            'age',
        ]

        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'bio'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Full Name'}),
            'offical_ID_number': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'offical ID number'}),
            'driver_category': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Driver Category'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control',  'placeholder': 'Contact'}),
            'company': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Company'}),
            'nationality': forms.Select(attrs={'class': 'form-control',  'placeholder': 'Nationality'}),
            'age': forms.Select(attrs={'class': 'form-control',  'placeholder': 'age'}),
            'source': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'source'}),
        }


class ForgetPasswordEmailCodeForm(forms.Form):
    username_or_email = forms.CharField(max_length=256,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Type your username or email'}
                                        )
                                        )

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        data = {'username': username_or_email}

        if '@' in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        try:
            get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                'There is no account with this {}'.format(list(data.keys())[0]))

        if not get_user_model().objects.get(**data).is_active:
            raise ValidationError(_('This account is not active.'))

        return data


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password'
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords are not match'))
        password_validation.validate_password(password2)
        return password2


class OtpForm(forms.Form):
    otp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter code',
            }
        )
    )

    def clean_otp(self):
        otp_code = self.cleaned_data['otp']
        try:
            OtpCode.objects.get(code=otp_code)
        except OtpCode.DoesNotExist:
            raise ValidationError(
                _('You have entered incorrect code!')
            )
        else:
            return otp_code


User = get_user_model()


class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control border-0 bg-light px-4",
                "placeholder": "Your full name"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control border-0 bg-light px-4",
                "placeholder": "Your email"
            }
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={

                "class": "form-control border-0 bg-light px-4",
                "placeholder": "Subject"
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control border-0 bg-light px-4 py-3',
                "placeholder": "Your message"
            }
        )
    )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be gmail.com")
    #     return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong.")
