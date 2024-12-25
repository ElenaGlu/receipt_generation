from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

CREATE_RECEIPT = (
    swagger_auto_schema(
        operation_summary='create data for receipt',
        operation_description='',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=''
                ),
                'restaurant': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=''
                ),
            },
        ),
        responses={
            201: openapi.Response(
                'the request for creating a receipt has been created'
            ),
            409: openapi.Response(
                'This restaurant does not have a printer',
            ),
            400: openapi.Response(
                'Order with this header has already been created',
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
