class AppExceptions(Exception):
    pass


class AppError(AppExceptions):
    pass


class ErrorType:
    PRINTER_ERROR = {
        'status_code': 409,
        'summary': 'Conflict',
    }

    ORDER_ERROR = {
        'status_code': 400,
        'summary': 'Bad Request',
    }

    RECEIPT_ERROR = {
        'status_code': 404,
        'summary': 'Not found',
    }

    PDF_ERROR = {
        'status_code': 400,
        'summary': 'Bad Request',
    }

    ARCHIVE_ERROR = {
        'status_code': 400,
        'summary': 'Bad Request',
    }
