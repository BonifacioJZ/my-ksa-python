from django.template.loader import render_to_string

from django.http import HttpResponse
from weasyprint import HTML

def generators_pdf(template:str,context):
    """
    Generate a PDF file from a template and context.
    """
    html = render_to_string(template,context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"
    HTML(string=html).write_pdf(response)
    return response