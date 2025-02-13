class AppExceptions(Exception):
    pass


class AppError(AppExceptions):
    pass


class ErrorType:

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
