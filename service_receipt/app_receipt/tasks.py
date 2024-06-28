from typing import Dict

from celery import shared_task
from django.template.loader import get_template
import pdfkit

from app_receipt.models import Order
from exceptions import AppError, ErrorType


@shared_task()
def generate_PDF_task(request: Dict[str, str]) -> Dict[str, bool]:
    """
    Generate a PDF file from an HTML template.
    :param request: dict containing keys - title, restaurant
    :return: {"status": True}
    :raises AppError: if there is a PDF creation error
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
    title = request['title']
    try:
        template = get_template("pdf_template.html")
        html = template.render(request)
        pdfkit.from_string(
            html,
            f'/home/elena/lena/receipt_generation/service_receipt/app_receipt/media/PDF/{title}.pdf',
            options=options
            )
        Order.objects.filter(title=title).update(status='READY')
        return {"status": True}
    except Exception:
        raise AppError(
            {
                'error_type': ErrorType.PDF_ERROR,
                'description': 'PDF creation error'
            }
        )
