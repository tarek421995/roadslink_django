from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import (
    logout,
)
from django.db.models.functions import Now

from assessments.forms import SingleChoiceQuestionForm
from users.views import logout_view
from .models import Answer, Cretificate, Test, Question, TestAttempt, Psycometric
# Create your views here.
from django.contrib import messages
import csv
from .models import Test, Question, Choice
from django.core.cache import cache

def test_list(request):
    user = request.user
    # certifiicate = user.cretificate
    if not user.test_active:
        messages.error(
            request, 'Your account have no test active. Please pay the fees to reactivate your account.')
    tests = list(Test.objects.filter(active=True).all())
    context = {'tests': tests, "user": user}
    return render(request, 'assessments/tests.html', context)
    
        
def calculate_score(answers):
    total_score = 0
    if answers:
        for answer in answers:
            if answer.is_correct:
                total_score += 1
        final_score = total_score / len(answers)
        return final_score

def question_list(request, test_id):
    user = request.user
    test = cache.get(f'test:{test_id}')
    if not test:
        test = get_object_or_404(Test, id=test_id)
        cache.set(f'test:{test_id}', test, 3600)
    question_number = test.number_question
    form = SingleChoiceQuestionForm(test=test, question_number=question_number)
    total_score = 0
    if request.method == "POST":
        answers = []
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                question_id = key
                choice_id = request.POST[key]
                question = Question.objects.get(id=question_id)
                choice = Choice.objects.get(id=choice_id)
                if choice.is_correct:
                    total_score += 1
                answers.append(Answer(question=question, choice=choice, user=user))
        Answer.objects.bulk_create(answers)
        try:
            en_passing_rate = user.driver_category.en_passing_rate
        except:
            en_passing_rate = 60
            
        if round(float(total_score), 2) >= en_passing_rate:
            mark = "passed"
        else:
            mark = "failed"
        test_attempts = TestAttempt.objects.create(
            user= user, test=test,final_mark=mark,type='en', final_score=total_score)
        test_attempts.save()
        if not test.do_all_must:
            return redirect('assessments:test_list')
        return redirect('assessments:psycometric_test')
    questions = test.random_questions(question_number)
    context = {'questions': questions, 'test': test, 'form': form}
    return render(request, 'assessments/questions.html', context)


def psycometric_tests(request):
    user = request.user
    test = Test.objects.filter(
        type='psyc', psycometric_must=True, active=True)
    if test.count() == 0:
        messages.warning(request, "you have no pycometric tests avalible")
        return redirect('assessments:test_list')

    test = test.first()
    last_psyco_attemp = TestAttempt.objects.filter(user=user, test=test, type='psyc').all()
    last_psyco_attemp.filter(created_at__lt=Now()-timedelta(hours=test.second_chance)).order_by('-created_at')
    psyco_ids = []
    for attemp in last_psyco_attemp:
        psyco_ids.append(attemp.psycometric.id)
    print('psyco_ids',psyco_ids)
    active_notpassed_psyco = test.psycometric_set.filter(active=True, must=True).exclude(id__in=psyco_ids)

    if active_notpassed_psyco.count() == 0:
        messages.warning(request, "you have no pycometric tests avalible")
        return redirect('assessments:results')
    context = {'question': active_notpassed_psyco.first(), 'test': test, 'active_notpassed_psyco': active_notpassed_psyco}
    return render(request, 'assessments/psycometric_test.html', context)




def evaluate_psycometric_test(request):
    user = request.user
    test_id = request.POST.get('test_id')
    question_id = request.POST.get('question_id')
    psycometric = Psycometric.objects.get(id=question_id)
    final_score = request.POST.get('final_score')
    test = Test.objects.get(id=test_id)
    try:
        pscy_passing_rate = user.driver_category.pscy_passing_rate
    except:
        pscy_passing_rate = 50
    if round(float(final_score), 2) >= pscy_passing_rate:
        mark = "passed"
    else:
        mark = "falied"
    # print('mark', mark)
    last_passed_psyco_attemp = TestAttempt.objects.filter(user=user, test=test, type='psyc').all()
    last_passed_psyco_attemp.filter(created_at__lt=Now()-timedelta(hours=test.second_chance)).order_by('-created_at')
    test_attemp = TestAttempt.objects.create(
        user=user, test=test, psycometric=psycometric, final_score=final_score, final_mark=mark, type="psyc")
    test_attemp.save()
    # print(last_passed_psyco_attemp)
    if not test.do_all_must:
        return JsonResponse({'url': '/assessments'}, status=202)
    if last_passed_psyco_attemp.count() == 0:
        print('you have to try after two days')
        return JsonResponse({'url': '/assessments/results'}, status=202)
    

    return JsonResponse({'url': '/assessments/psycometric_test'}, status=202)

    # if test_attemp:

def psycometric_tests_detail(request,psyco_id):
    user = request.user
    test = Test.objects.filter(
        type='psyc', psycometric_must=True, active=True)
    if test.count() == 0:
        messages.warning(request, "you have no pycometric tests avalible")
        # print('you have no pycometric tests avalible')
        return redirect('assessments:test_list')
    test = test.first()
    psyco = Psycometric.objects.get_object_or_404(id=psyco_id)
    context = {'question': psyco, 'test': test}
    return render(request, 'assessments/psycometric_test.html', context)
 
 
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    choices = list(Choice.objects.filter(question=question))
    context = {'question': question, 'choices': choices}
    return render(request, 'assessments/question_detail.html', context)


def validate_and_save_answers(request):
    answers = request.POST
    print(answers)
    for question_id, choice_id in answers.items():
        print(question_id, choice_id)
        question = Question.objects.get(id=question_id)
        choice = question.choice_set.get(id=choice_id)
        if choice.is_correct:
            # Save the answer to the database
            answer = Answer(question=question,
                            choice=choice, user=request.user)
            answer.save()
    # return redirect('results')


def english_questions(request):
    if request.method == 'POST':
        print("POST")
        validate_and_save_answers(request)
        return redirect('assessments/results')
    else:
        questions = list(Question.objects.all())
        context = {'questions': questions}
        return render(request, 'all_questions.html', context)



def results(request):
    user_answers = Answer.objects.filter(user=request.user)
    correct_answers = user_answers.filter(choice__is_correct=True)
    user = request.user
    current_attempts = TestAttempt.objects.filter(user=user)
    print(current_attempts.count())
    can_print= user.print_certificate
    print(can_print)
    if can_print:
        all_passed = current_attempts.filter(final_mark='passed')
        en = all_passed.filter(type='en')
        all_psyco = TestAttempt.objects.filter(user=user,type='psyc',final_mark='passed')
        
        print('all_psycp',all_psyco.count())
        try:
            certificate = Cretificate.objects.create(user=user)
        except:
            certificate = Cretificate.objects.get(user=user)

        psyco_sum = 0
        i=0
        certificate.test_attemp.set('')
        certificate.test_attemp.add(en.last())
        psyco_list = []
        for psyco in all_psyco:
            psyco_list.append(psyco)
            i=+1
            psyco_sum =+ psyco.final_score
        psyco_avg = psyco_sum / i
        certificate.test_attemp.add(*psyco_list)
        certificate.final_en_score = en.last().final_score
        certificate.final_psyco_score = psyco_avg
        certificate.save()
        print(certificate.test_attemp.count())
    
    context = {
        'total_en_questions': list(Question.objects.all()),
        'total_en_answers': user_answers.count(),
        'correct_en_answers': correct_answers.count(),
        'current_attempts':current_attempts.order_by('-type')
        
        
    }
    return render(request, 'assessments/results.html', context)


# messages.debug(request, '%s SQL statements were executed.' % count)
# messages.info(request, 'Three credits remain in your account.')
# messages.success(request, 'Profile details updated.')
# messages.warning(request, 'Your account expires in three days.')
# messages.error(request, 'Document deleted.')
