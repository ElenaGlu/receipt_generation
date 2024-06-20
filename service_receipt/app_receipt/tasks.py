from celery import shared_task


@shared_task()
def generate_PDF_task():
    """
    Generate a PDF file from an HTML template
    :return:
    """