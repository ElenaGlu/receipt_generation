from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

CREATE_RECEIPT = (
    swagger_auto_schema(
        operation_summary='create a receipt',
        operation_description='',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='the unique identification of the receipt'
                ),
                'restaurant': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='restaurant name'
                ),
            },
        ),
        responses={
            201: openapi.Response(
                'successful operation'
            ),
            400: openapi.Response(
                'invalid input',
            ),
        },
    ),
    'create_receipt',
)
GET_RECEIPT = (
    swagger_auto_schema(
        operation_summary='get receipt',
        operation_description='',
        manual_parameters=[
                openapi.Parameter(
                    name='printer_id', in_=openapi.IN_QUERY,
                    type=openapi.TYPE_INTEGER,
                    description='printer_id',
                    required=True,
                ),
            ],
        responses={
            200: openapi.Response(
                'Return a list of receipts ready to be printed on a specific printer'
            ),
            404: openapi.Response(
                'there are no receipts for printing or the printer does not exist',
            ),
            400: openapi.Response(
                'archive creation error',
            ),
        },
    ),
    'get_receipt'
)
