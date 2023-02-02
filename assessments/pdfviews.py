from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from weasyprint import HTML,  CSS

from django.contrib.auth import get_user_model
User = get_user_model()

  
def generate_pdf(request, user_id):
    # Render the HTML template
    user = User.objects.filter(id=user_id).first()
    print(user.print_certificate)
    # certifiicate = user.cretificate
    mycss = CSS(string=(
        "@page longpage {\n"
        "    size: 400mm 400mm;\n"
        "}"
        "body {\n"
        "   page: longpage;\n"
        "}\n"
    ))
    
    html_template = render(request, 'assessments/certificate/pdf.html', {'data': user})

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