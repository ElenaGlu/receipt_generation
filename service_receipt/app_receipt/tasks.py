from celery import shared_task
from django.template.loader import get_template
import pdfkit

from django.http import HttpResponse


@shared_task()
def generate_PDF_task(data):
    """
    Generate a PDF file from an HTML template
    :return:
    """
    options = {
        'page-size': 'Letter',
        'orientation': 'Landscape',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [('Accept-Encoding', 'gzip')],
        'no-outline': None
    }

    template = get_template("pdf_template.html")
    template.render(context=data)
    pdfkit.from_file('/home/elena/lena/receipt_generation/service_receipt/app_receipt/templates/pdf_template.html', '/home/elena/lena/receipt_generation/service_receipt/app_receipt/templates/out.pdf', options=options)

    pdf = open("/home/elena/lena/receipt_generation/service_receipt/app_receipt/templates/out.pdf", encoding="utf8", errors='ignore')

    response = HttpResponse(pdf.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=output.pdf'
    # pdf.close()
    return response
