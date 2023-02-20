from django.conf import settings
from django.db import models
import random
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import pandas as pd
from django_quill.fields import QuillField
from django.template.loader import render_to_string
from core.models import HashableModel

User = settings.AUTH_USER_MODEL
# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "test/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def cretificate_upload_file_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "cretificate/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class QuestionCategory(HashableModel):
    name = models.CharField(max_length=20, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class DriverCategory(HashableModel):
    name = models.CharField(max_length=20, null=True)
    fees = models.IntegerField(blank=True, null=True)
    en_passing_rate = models.PositiveIntegerField(default=0)
    pscy_passing_rate = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(
                fields=['name','fees', 'en_passing_rate', 'pscy_passing_rate']),
        ]

    def __str__(self):
        return self.name


TEST_TYPE = (
    ('en', 'en'),
    ('psyc', 'psyc'),
)


class Test(HashableModel):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    type = models.CharField(max_length=10, choices=TEST_TYPE, default='')
    active = models.BooleanField(default=True)
    english_Questions = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    audio_Questions = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    tutorial_path = models.URLField(max_length=200,null=True, blank=True)
    number_question = models.PositiveIntegerField(default=1)
    maximum_attempts = models.PositiveIntegerField(default=5)
    psycometric_must = models.BooleanField(default=True)
    time_limit = models.PositiveIntegerField(default=7)
    second_chance = models.PositiveIntegerField(default=48)
    do_all_must = models.BooleanField(default=True)
    certificate_image = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    certificate_html = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    descriptions = QuillField(blank=True,null=True)
    report_page = models.TextField(blank=True, null=True)  # modified
    
    class Meta:
        indexes = [
            models.Index(fields=['name','certificate_image','tutorial_path','certificate_html', 'type', 'number_question',
                         'maximum_attempts','report_page', 'psycometric_must', 'do_all_must','descriptions']),
        ]

    def __str__(self):
        return f'{self.name} {self.type}'

    def random_questions_mixed(self, number_of_questions, category=None):
        text_questions = self.question_set.filter(active=True, type='text')
        audio_questions = self.question_set.filter(active=True, type='audio')
        if category:
            text_questions = text_questions.filter(category=category)
            audio_questions = audio_questions.filter(category=category)

        number_of_text_questions = int(number_of_questions/2)
        number_of_audio_questions = number_of_questions - number_of_text_questions

        if number_of_text_questions > text_questions.count() or number_of_questions:
            number_of_text_questions = text_questions.count()
            # raise ValueError("Number of questions is greater than the number of questions available")
        if number_of_audio_questions > audio_questions.count() or number_of_questions:
            number_of_audio_questions = audio_questions.count()
        text_sample = random.sample(
            list(text_questions), number_of_text_questions)
        audio_sample = random.sample(
            list(audio_questions), number_of_audio_questions)
        return text_sample + audio_sample

    def random_questions(self, number_of_questions, question_type=None, category=None):
        questions = self.question_set.filter(active=True)
        if question_type:
            print(question_type)
            questions = questions.filter(type=question_type)
            print(questions)
        if category:
            questions = questions.filter(category=category)
            print(questions)
        # Check if number_of_questions is greater than the number of questions available
        if number_of_questions > questions.count() or number_of_questions < 0:
            number_of_questions = questions.count()
            # raise ValueError("Number of questions is greater than the number of questions available")
        return random.sample(list(questions), number_of_questions)

    def get_report_template(self):
        """
        Returns the report page template for the test
        """
        return self.report_page

    def set_report_template(self, template):
        """
        Sets the report page template for the test
        """
        self.report_page = template
        
        


@receiver(post_save, sender=Test)
def handle_uploaded_excel_file(sender, created, instance, **kwargs):
    if not instance.type == "en":
        instance.question_set.filter(type='text').delete()       
        return
    if not instance.english_Questions:
        return
    df = pd.read_excel(instance.english_Questions.path, sheet_name=None)

    # loop through each sheet
    for sheet_name, data in df.items():
        # process the data for the current sheet
        # extract the columns "Question Text", "Option A", "Option B", "Option C", "Option D", "Correct Answer"
        question_text = data["Question Text"]
        option_a = data["Option A"]
        option_b = data["Option B"]
        option_c = data["Option C"]
        option_d = data["Option D"]
        correct_answer = data["Correct Answer"]
        print(len(correct_answer))
        # create the Question and Choice objects and save them to the database
        for i in range(len(question_text)):
            category, created = QuestionCategory.objects.get_or_create(
                name=sheet_name)
            # create the Question object
            question = Question.objects.create(
                test=instance,
                active=True,
                text=question_text[i],
                type="text",
                file=None
            )
            question.category.add(category)
            question.save()

            # create the Choice objects
            choice_a = Choice.objects.create(
                question=question,
                text=option_a[i],
                is_correct=True if correct_answer[i] == "a" or correct_answer[i] == "A" else False
            )
            choice_b = Choice.objects.create(
                question=question,
                text=option_b[i],
                is_correct=True if correct_answer[i] == "b" or correct_answer[i] == "B" else False
            )
            choice_c = Choice.objects.create(
                question=question,
                text=option_c[i],
                is_correct=True if correct_answer[i] == "c" or correct_answer[i] == "C" else False
            )
            choice_d = Choice.objects.create(
                question=question,
                text=option_d[i],
                is_correct=True if correct_answer[i] == "d" or correct_answer[i] == "D" else False
            )
post_save.connect(handle_uploaded_excel_file, sender=Test)

QUESTION_TYPE = (
    ('text', 'text'),
    ('audio', 'audio'),
)

class Question(HashableModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(QuestionCategory)
    type = models.CharField(max_length=10, choices=QUESTION_TYPE, default='')
    file = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['text', 'test', 'type', 'file', 'active']),
        ]

    def __str__(self):
        return self.text

@receiver(post_save, sender=Question)
def handle_delete(sender, created, instance, **kwargs):
    questions = Question.objects.filter(type='audio')
    for question in questions:
        if not question.file:
            question.delete() 
    
    post_save.connect(handle_uploaded_excel_file, sender=Test)


class Psycometric(HashableModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    text = models.CharField(max_length=30)
    category = models.ManyToManyField(QuestionCategory)
    file = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    tutorial_path = models.URLField(max_length=200,null=True, blank=True)
    description = QuillField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    time_limit = models.PositiveIntegerField(default=7)
    must = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['active', 'test', 'must','tutorial_path',
                         'text', 'file', 'description', 'time_limit']),
        ]

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=255, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'choice', 'created_at', 'question']),
        ]

    def __str__(self):
        return self.question.text

    def is_correct(self):
        return self.choice.is_correct


FINAL_MARK = (
    ('passed', 'passed'),
    ('falied', 'falied'),
    ('not_taken', 'not_taken'),
)


class TestAttempt(HashableModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, null=True, blank=True)
    psycometric = models.ForeignKey(
        Psycometric, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TEST_TYPE, default='')
    final_score = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    current_attempts = models.PositiveIntegerField(default=0)
    final_mark = models.CharField(
        max_length=10, choices=FINAL_MARK, default='not_taken')
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    company = models.ForeignKey('users.CompanyCategory',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'test', 'type', 'final_score',
                         'timestamp', 'final_mark', 'created_at', 'psycometric']),
        ]

    def __str__(self):
        return f'{self.final_mark} {self.test} {self.psycometric}'



@receiver(pre_save, sender=TestAttempt)
def increment_attempt(sender, instance, **kwargs):
    if instance.pk:
        return
    test = instance.test
    user = instance.user
    current_attempts = TestAttempt.objects.filter(user=user)
    current_attempts_count = current_attempts.count()
    user.current_attempts = current_attempts_count + 1
    if not user.is_superuser:
        user.test_active = True
    user.save()
    instance.current_attempt = current_attempts_count + 1


pre_save.connect(increment_attempt, sender=TestAttempt)

class TestReport(HashableModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    test_attemp = models.OneToOneField(TestAttempt, on_delete=models.CASCADE,)
    type = models.CharField(max_length=10,)
    description = models.CharField(max_length=1000)
    report_template = models.TextField(null=True)  # added


    def get_report(self):
        """
        Returns the rendered report page for the test attempt
        """
        user = self.user
        timestamp = self.timestamp
        test_attemp = self.test_attemp
        description = self.description
        context = {'user':user,'timestamp':timestamp, 'test_attemp':test_attemp,'description':description}  # context dictionary to pass data to the report template
        # Populate the context dictionary with data from the test attempt
        # ...
        # Render the report template with the populated context dictionary
        report = render_to_string(self.report_template, context)
        return report

    def set_report_template(self, template):
        """
        Sets the report page template for the test report
        """
        self.report_template = template
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'test_attemp',
                         'type', 'timestamp','report_template', 'description']),
        ]

    def __str__(self):
        return f'{self.user}'

   
    
