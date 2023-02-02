from django.conf import settings
from django.db import models
import random
import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

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


class DriverCategory(HashableModel):
    name = models.CharField(max_length=20,null=True)
    en_passing_rate = models.PositiveIntegerField(default=0)
    pscy_passing_rate = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['name','en_passing_rate','pscy_passing_rate']), 
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
    file = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    number_question = models.PositiveIntegerField(default=1)
    maximum_attempts = models.PositiveIntegerField(default=5)
    psycometric_must = models.BooleanField(default=True)
    time_limit = models.PositiveIntegerField(default=7)
    second_chance = models.PositiveIntegerField(default=48)
    do_all_must = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name','file', 'type','number_question','maximum_attempts','psycometric_must','do_all_must']), 
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
        if number_of_audio_questions > audio_questions.count() or number_of_questions :
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


QUESTION_TYPE = (
    ('text', 'text'),
    ('audio', 'audio'),
)


class Question(HashableModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    text = models.TextField()
    category = models.ManyToManyField(DriverCategory)
    type = models.CharField(max_length=10, choices=QUESTION_TYPE, default='')
    file = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['text','test', 'type','file','active']), 
        ] 

    def __str__(self):
        return self.text


class Psycometric(HashableModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    text = models.CharField(max_length=30)
    category = models.ManyToManyField(DriverCategory)
    file = models.FileField(
        upload_to=upload_file_path, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    time_limit = models.PositiveIntegerField(default=7)
    must = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['active','test','must', 'text','file','description','time_limit']), 
        ] 


    def __str__(self):
        return self.text
    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user','choice','created_at','question']), 
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    psycometric = models.ForeignKey(Psycometric, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TEST_TYPE, default='')
    final_score = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    current_attempts = models.PositiveIntegerField(default=0)
    final_mark = models.CharField(max_length=10, choices=FINAL_MARK, default='not_taken')
    created_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user','test', 'type','final_score','timestamp','final_mark','created_at','psycometric']), 
        ] 
    
    def __str__(self):
        return f'{self.final_mark} {self.test} {self.psycometric}'        



class Cretificate(HashableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    test_attemp = models.ManyToManyField(TestAttempt)
    final_en_score = models.FloatField(default=0)
    final_psyco_score = models.FloatField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    created_at= models.DateTimeField(auto_now=True,blank=True,null=True)
    images =  models.ImageField(
        upload_to=upload_file_path, null=True, blank=True)
    

    class Meta:
        indexes = [
            models.Index(fields=['user', 'final_en_score','final_psyco_score','timestamp','created_at']), 
        ] 
    
    def __str__(self):
        return f'{self.user} => Psych: {self.final_psyco_score}, English: {self.final_en_score}'


    def check_certificate(self):
        if self.final_en_score >= self.user.driver_category.en_passing_rate and self.final_psyco_score >= self.user.driver_category.pscy_passing_rate:
            return True
        else:
            i = 0
            for marks in self.test_attemp:
                if marks.final_mark == 'passed':
                    i=+1
            if i == self.test_attemp.count():
                return True
            return False
        
        
        
        
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
        user.test_active = False
    user.save()
    instance.current_attempt = current_attempts_count + 1
    


pre_save.connect(increment_attempt, sender=TestAttempt)
