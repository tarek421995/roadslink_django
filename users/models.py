from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os import path
from assessments.models import Test, TestAttempt, DriverCategory, Psycometric
from django.db.models.signals import pre_save, post_save

from core.models import HashableModel


def get_profile_picture_filepath(instance, filename):
    filename = filename.split('.')[-1]
    return path.join('profile_images', '{}profile_image.{}'.format(instance.pk, filename))


class CompanyCategory(HashableModel):
    name = models.CharField(max_length=20, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    full_name = models.CharField(_('full_name'), max_length=50, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'), upload_to=get_profile_picture_filepath, null=True, blank=True)
    driver_category = models.OneToOneField(
        DriverCategory, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    source = models.CharField(_('source'), max_length=50, blank=True)
    contact = models.IntegerField(_('contact'), blank=True, null=True)
    current_attempts = models.PositiveIntegerField(default=0)
    test_active = models.BooleanField(default=False)
    final_score = models.PositiveIntegerField(default=0)
    company = models.OneToOneField(
        CompanyCategory, on_delete=models.CASCADE, blank=True, null=True)
    nationality = models.CharField(_('nationality'), max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['full_name', 'current_attempts', 'driver_category', 'source',
                         'contact', 'final_score', 'test_active', 'company', 'nationality']),
        ]

    def __str__(self):
        return self.username

    @property
    def print_certificate(self):
        active_tests = Test.objects.filter(active=True,type='en')
        passed_tests = TestAttempt.objects.filter(user=self, final_mark='passed' , type='en')
        passed_tests = passed_tests.prefetch_related('test').filter(test__in=active_tests)
        print(active_tests.count(),passed_tests.count())
        active_psycometric_tests = Psycometric.objects.filter(active=True)
        print('active_psycometric_tests',active_psycometric_tests.count())
        passed_psycometric_tests = TestAttempt.objects.filter(user=self, final_mark='passed', type='psyc')
        passed_psycometric_tests = passed_psycometric_tests.prefetch_related('test').filter(psycometric__in=active_psycometric_tests)
        print(passed_psycometric_tests.count())
        
        return len(passed_tests) >= len(active_tests) and len(passed_psycometric_tests) >= len(active_psycometric_tests)


# @receiver(post_save, sender=CustomUser)
# def create_certificate(sender,created, instance, **kwargs):
    

class OtpCode(HashableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.code
