from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

from users.forms import ContactForm
from users.models import Contact
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def home_page(request):
    print('homepage')
    return render(request, 'shared_layout/home.html')

@login_required()
def staff_dashboard(request):
    if not request.user.is_superuser:
        messages.success(request,'you have no active psycometric test')
        return redirect('users:edit_profile')
    return render(request, 'shared_layout/staff_dashboard.html')

def about_page(request):
    
    return render(request, "shared_layout/contact/aboutus.html")

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    nextPage = '/courses/'
    context = {
        "pagetilte":"Contact Us",
        "nextPage":nextPage,
        "nextPagetext":'View Our Product',
        "form": contact_form,
    }
    if contact_form.is_valid():
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        contact = Contact(full_name=full_name,email=email,subject=subject,content=content)
        contact.save()
        messages.success(
                    request, (f'Mr {full_name}, We have reviced your query ,We will review in touch very soon '))
    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, "shared_layout/contact/contact.html", context)

