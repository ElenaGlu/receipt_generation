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
                    description='the unique name of the receipt'
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
        tags=['base']),
    'create_receipt',
)
GET_RECEIPT = (
    swagger_auto_schema(
        operation_summary='get a receipt',
        operation_description='',
        manual_parameters=[
            openapi.Parameter(
                name='printer_id', in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='the unique identifier of the printer',
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                'successful operation'
            ),
            400: openapi.Response(
                'invalid input',
            ),
        },
        tags=['base']),
    'get_receipt'
)
