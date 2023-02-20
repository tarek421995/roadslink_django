from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from weasyprint import HTML,  CSS
from .models import Test
from users.models import Cretificate,CompanyCategory
from django.contrib.auth import get_user_model
User = get_user_model()

  
def generate_pdf(request, user_id,company_id):
    # Render the HTML template
    user = User.objects.get(id=user_id)
    print(user)
    
    company= CompanyCategory.objects.get(id=company_id)
    certificate = Cretificate.objects.filter(user=user,company=company).first()
    print(certificate)
    test = Test.objects.filter(type='en').first()
    # test_attemp = certificate.test_attemps.all().first().test
    # 210 x 297
    mycss = CSS(string=(
        "@page longpage {\n"
            "margin: 0;\n"
        "    size: 350mm 400mm ;\n"
        "}"
        "body {\n"
        "   page: longpage;\n"
        "}\n"
    ))
    
    html_template = render(request, 'assessments/certificate/pdf.html', {'data': certificate ,'test':test})

    # Convert the HTML to a PDF
    pdf_file = HTML(string=html_template.content.decode('utf-8')).write_pdf(stylesheets=[mycss])
    if pdf_file:
            response = HttpResponse(pdf_file, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341232")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        
    return HttpResponse("Not found")
    # # Return the PDF file as a response
    # response = FileResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # return response