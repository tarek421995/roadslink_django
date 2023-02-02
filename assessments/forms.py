from django import forms
import random
from django.forms import ValidationError


class EnglishQuestionForm(forms.Form):
    def __init__(self, test, *args, **kwargs):
        super(EnglishQuestionForm, self).__init__(*args, **kwargs)
        self.test = test
        self.fields["test_id"] = forms.IntegerField(
            widget=forms.HiddenInput(), initial=test.id)
        
        for question in test.question_set.all():
            choices = [(choice.id, choice.text)
                       for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(
                label=question.text, choices=choices, widget=forms.RadioSelect(attrs={'class': 'RadioSelect'}))



def select_random_questions(test, num_questions, question_type):
    questions = test.question_set.filter(type=question_type, active=True)
    if questions.count() < num_questions:
        raise ValidationError("Not enough questions of type {} available.".format(question_type))
    selected_questions = random.sample(list(questions), num_questions)
    return selected_questions


class SingleChoiceQuestionForm(forms.Form):
    def __init__(self, question_number,test, *args, **kwargs):
        super(SingleChoiceQuestionForm, self).__init__(*args, **kwargs)
        self.test = test
        self.question_number = question_number
        
        for question in test.random_questions_mixed(question_number):
            choices = [(choice.id, choice.text)
                       for choice in question.choice_set.all()]
            self.fields[str(question.id)] = forms.ChoiceField(
                label=question.text, widget=forms.CheckboxSelectMultiple, choices=choices
            )


class PsycoMetricQuestionForm(forms.Form):
    def __init__(self,test, *args, **kwargs):
        super(PsycoMetricQuestionForm, self).__init__(*args, **kwargs)
        self.test = test
        if test.psycometric_must:
            for question in test.question_set.filter(active=True):
                choices = [(choice.id, choice.text)
                            for choice in question.choice_set.all()]
                self.fields[str(question.id)] = forms.ChoiceField(
                    label=question.text, widget=forms.CheckboxSelectMultiple, choices=choices
                )
        else:
            for question in test.question_set.filter(active=True, must=True):
                choices = [(choice.id, choice.text)
                            for choice in question.choice_set.all()]
                self.fields[str(question.id)] = forms.ChoiceField(
                    label=question.text, widget=forms.CheckboxSelectMultiple, choices=choices
                )
