from django.contrib import admin
from .models import Test, QuestionCategory, DriverCategory, Question, Psycometric, Choice, Answer, TestAttempt

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class PsycometricInline(admin.TabularInline):
    model = Psycometric
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'timestamp', 'active')
    list_filter = ('type', 'active')
    search_fields = ('name', 'type')
    ordering = ('-timestamp',)
    inlines = [PsycometricInline]
    list_editable = ('active',)

class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class DriverCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'en_passing_rate', 'pscy_passing_rate')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'type', 'active')
    list_filter = ('type', 'active')
    search_fields = ('text', 'test__name')
    ordering = ('text',)
    inlines = [ChoiceInline]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__name')
    ordering = ('is_correct','text',)

class PsycometricAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'must', 'active')
    list_filter = ('must', 'active')
    search_fields = ('text', 'test__name')
    ordering = ('text',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'choice', 'created_at')
    search_fields = ('question__text', 'user__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_filter = ('created_at',)

class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'final_mark', 'timestamp')
    list_filter = ('final_mark',)
    search_fields = ('user__username', 'test__name')
    ordering = ('-timestamp',)
    actions = ['make_passed', 'make_failed']
    def make_passed(self, request, queryset):
        queryset.update(final_mark='PASSED')
    make_passed.short_description = "Mark selected attempts as PASSED"

    def make_failed(self, request, queryset):
        queryset.update(final_mark='FAILED')
    make_failed.short_description = "Mark selected attempts as FAILED"


admin.site.register(Test, TestAdmin)
admin.site.register(QuestionCategory, QuestionCategoryAdmin)
# admin.site.register(DriverCategory, DriverCategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Psycometric, PsycometricAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TestAttempt, TestAttemptAdmin)
