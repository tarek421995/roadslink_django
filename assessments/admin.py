from django.contrib import admin
from .models import Answer, Cretificate, Psycometric, Test,Question,Choice, TestAttempt

# Register your models here.
admin.site.register(TestAttempt)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Psycometric)
admin.site.register(Answer)
admin.site.register(Choice)
admin.site.register(Cretificate)
