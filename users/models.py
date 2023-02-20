from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from os import path
from django.template.loader import render_to_string
from assessments.models import Test, TestAttempt, DriverCategory, Psycometric
from django.db.models.signals import pre_save, post_save

from core.models import HashableModel

from django.conf import settings

User = settings.AUTH_USER_MODEL

def get_profile_picture_filepath(instance, filename):
    filename = filename.split('.')[-1]
    return path.join('profile_images', '{}profile_image.{}'.format(instance.pk, filename))

def get_invoice_filepath(instance,filename):
    filename = filename.split('.')[-1]
    return path.join('invoice', '{}'.format(instance.pk))






class AgentCategory(HashableModel):
    name = models.CharField(max_length=20, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class CompanyCategory(HashableModel):
    name = models.CharField(max_length=20, null=True)
    agents = models.ManyToManyField(AgentCategory)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
    
    
class DriverAge(HashableModel):
    number = models.CharField(_('Range'),unique=True, max_length=50, null=True, blank=True)
    def __str__(self):
        return self.number
    class Meta:
        indexes = [
            models.Index(fields=['number']),
        ]
        
    
class DriverNationality(HashableModel):
    name = models.CharField(_('name'),unique=True ,max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

GENDER=(
    ('male','male'),
    ('female','female'),
)

class CustomUser(AbstractUser):
    full_name = models.CharField(_('full_name'), max_length=50, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'), upload_to=get_profile_picture_filepath, null=True, blank=True)
    driver_category = models.ForeignKey(
        DriverCategory, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(_('Bio'), max_length=500, blank=True)
    source = models.CharField(_('source'), max_length=50, blank=True)
    contact = models.IntegerField(_('contact'), blank=True, null=True)
    current_attempts = models.PositiveIntegerField(default=0)
    test_active = models.BooleanField(default=False)
    final_score = models.PositiveIntegerField(default=0)
    company = models.ForeignKey(
        CompanyCategory, on_delete=models.CASCADE, blank=True, null=True)
    agents = models.ForeignKey(AgentCategory, on_delete=models.CASCADE, blank=True, null=True)
    age = models.ForeignKey(DriverAge ,on_delete=models.CASCADE, blank=True, null=True)
    nationality = models.ForeignKey(DriverNationality ,on_delete=models.CASCADE, blank=True, null=True)
    offical_ID_number = models.CharField(_('Offical ID'),max_length=50,null=True, blank=True)
    gender = models.CharField(_('Gender'),max_length=10,choices=GENDER ,default='male')


    class Meta:
        indexes = [
            models.Index(fields=['full_name','agents', 'gender','current_attempts', 'driver_category', 'source',
                         'contact', 'final_score', 'test_active','offical_ID_number', 'company', 'nationality']),
        ]
        unique_together = ("full_name", "offical_ID_number")
       

    def __str__(self):
        return self.username

    @property
    def print_certificate(self):
        active_tests = Test.objects.filter(active=True,type='en')
        passed_tests = TestAttempt.objects.filter(user=self, final_mark='passed' , type='en')
        passed_tests = passed_tests.prefetch_related('test').filter(test__in=active_tests)
        active_psycometric_tests = Psycometric.objects.filter(active=True)
        passed_psycometric_tests = TestAttempt.objects.filter(user=self, final_mark='passed', type='psyc')
        passed_psycometric_tests = passed_psycometric_tests.prefetch_related('test').filter(psycometric__in=active_psycometric_tests)
        return len(passed_tests) >= len(active_tests) and len(passed_psycometric_tests) >= len(active_psycometric_tests)

class OtpCode(HashableModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.code


class Contact(HashableModel):
    full_name = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=120, blank=True, null=True)
    content = models.TextField()  

    class Meta:
        indexes = [
            models.Index(fields=['full_name', 'email','subject', 'content']),
        ]
    def __str__(self):
        return 'Subject {} by {}'.format(self.subject, self.email)

INVOICE_TYPE= (
    ('indvidual', 'indvidual'),
    ('group', 'group'),
    ('company', 'company'),
)

class InvociesFile(HashableModel):
    file = models.FileField(
        _('Invoice File'), upload_to=get_invoice_filepath, null=True, blank=True)
    type = models.CharField(max_length=50,choices=INVOICE_TYPE, default='')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False)
    fees = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=50,default='Dubai UAE')

    
    class Meta:
                indexes = [
                    models.Index(fields=['file','active','location','fees','type','timestamp']),
                ]

    def __str__(self):
        return '{}'.format(self.type)

class Invocies(HashableModel):
    users = models.ManyToManyField(User,related_name='users', blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True,related_name='user')
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    create_by = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)
    company = models.ForeignKey(
        CompanyCategory, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=50,choices=INVOICE_TYPE, default='')
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
            indexes = [
                models.Index(fields=['active','start_date', 'end_date','company','user','type','create_by','timestamp']),
            ]

    def __str__(self):
        return 'issued by {} for company {}'.format(self.create_by,self.company)


class Cretificate(HashableModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='certificate')
    test_attemps = models.ManyToManyField(TestAttempt)
    company = models.ForeignKey(CompanyCategory, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='compnay' )
    final_en_score = models.FloatField(default=0)
    final_psyco_score = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    code = models.CharField(max_length=10, default='72109C87')
    active = models.BooleanField(default=True)
    
    
    # objects = CertificateManager()

    class Meta:
        indexes = [
            models.Index(fields=['user', 'final_en_score','company','active',
                         'final_psyco_score', 'timestamp', 'created_at']),
        ]

    def __str__(self):
        return f'{self.user} => Psych: {self.final_psyco_score}, English: {self.final_en_score}'

    def check_certificate(self):
        if self.final_en_score >= self.user.driver_category.en_passing_rate and self.final_psyco_score >= self.user.driver_category.pscy_passing_rate:
            return True
        else:
            i = 0
            for marks in self.test_attemps:
                if marks.final_mark == 'passed':
                    i = +1
            if i == self.test_attemps.count():
                return True
            return False
