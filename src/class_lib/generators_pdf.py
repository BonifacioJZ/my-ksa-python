from django.template.loader import render_to_string

from django.http import HttpResponse,HttpRequest
from weasyprint import HTML

def generators_pdf(request:HttpRequest,template:str,context):
    """
    Generate a PDF file from a template and context.
    """
    # Render the template with the context
    html = render_to_string(template,context) 
    pdf = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf,content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    return response

def ticket_generator(request:HttpRequest,template:str,context):
    """
    Generate a ticket PDF file from a template and context.
    """
    # Render the template with the context
    html = render_to_string(template,context)
    pdf = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ticket.pdf"'
    return response